"""Read-only checks for C's added provenance, evidence export and editable slides."""
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.governance.c_component import build_c_service
from src.utils.experiment_io import stable_hash
FOLDER=ROOT/'docs/c_work/closeout_supplement_20261125_v1'


def read(name):
    return json.loads((FOLDER/name).read_text(encoding='utf-8'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition,message):
    if not condition:
        raise ValueError(message)


def check():
    frozen=read('frozen_inputs.json')['sha256']
    for name,expected in frozen.items():
        require(digest(ROOT/name)==expected,'Historical artifact changed: '+name)
    corpus=json.loads((ROOT/'knowledge/corpus_v4.json').read_text(encoding='utf-8'))
    sources={s['id']:s for s in corpus['sources']}
    dates=read('source_dates.json')
    require(dates['applies_to_corpus_sha256']==digest(ROOT/'knowledge/corpus_v4.json'),'Wrong corpus binding')
    require({r['source_id'] for r in dates['items']}==set(sources),'Missing source date rows')
    for row in dates['items']:
        source=sources[row['source_id']]
        require(row['historical_published_at']==source.get('published_at') and row['historical_collected_at']==source['accessed_at'],'History dates rewritten')
        require(row['published_at'] or row['unknown_publication_reason'],'Unknown date lacks reason')
        require(row['date_evidence_locator'] and row['metadata_reviewed_at']=='2026-11-25','Missing review provenance')
        require(not row['published_at'] or row['published_at']==source.get('published_at'),'Update date promoted to publication date')
    refs=read('reference_map.json'); usage=read('usage_registry.json')
    require({m['id'] for m in refs['methods']}=={'M1','M2','M3'},'Missing method citation')
    require(len({r['citation_id'] for r in refs['factual_sources']})==len(refs['factual_sources']),'Duplicate citation IDs')
    require({r['source_id'] for r in refs['factual_sources'] if r['role']=='rag'}==set(sources),'Missing RAG citation')
    require({r['source_id'] for r in usage['source_items']}==set(sources),'Missing usage explanation')
    require(all(r['asset_level_license']=='not_individually_verified' for r in usage['source_items']),'Invented asset permission')
    temporal=read('temporal_cases.json')
    require(temporal['independent_human_reviews']==0 and temporal['formal_accuracy'] is None,'AI analysis promoted to human metrics')
    original=json.loads((ROOT/'results/hallucination/results.json').read_text(encoding='utf-8'))
    for case in temporal['cases']:
        raw=original[case['array_index_zero_based']]
        require(digest(ROOT/case['source_file'])==case['source_file_sha256'],'Temporal source changed')
        require(raw==case['raw_record'] and stable_hash(raw)==case['record_sha256'],'Temporal answer mismatch')
        require(not case['generation_time_or_training_cutoff_inferred'],'Unsupported cutoff inference')
    manifest=read('a_handoff_manifest.json'); exported=read('a_evidence_export.json')
    require(digest(FOLDER/'a_evidence_export.json')==manifest['export_sha256'],'Export hash differs')
    require(digest(ROOT/'knowledge/corpus_v4.json')==manifest['corpus_sha256'] and digest(ROOT/'configs/c_component_profile.json')==manifest['profile_sha256'],'Export profile differs')
    inputs=[]
    for value in manifest['input_snapshots'].values():
        path=FOLDER/value['snapshot']; require(digest(path)==value['sha256'],'A input snapshot changed')
        inputs.extend(json.loads(path.read_text(encoding='utf-8')))
    require(digest(FOLDER/'source_snapshot/A_interventions.py')==manifest['A_interventions_snapshot_sha256'],'A interface snapshot changed')
    require(len(exported)==len(inputs)==48 and set(exported)=={i['uid'] for i in inputs},'UID set mismatch')
    def forbidden_model():
        raise AssertionError('Verification must not load model')
    service,retriever,profile=build_c_service(ROOT,forbidden_model)
    for item in inputs:
        actual=service.answer(item['question'],profile['strategy'],item.get('category'),prepare_only=True)
        row=exported[item['uid']]
        require(row['question_sha256']==stable_hash(item['question']),'Wrong question binding')
        require(row['retrieval_status']==actual['retrieval_status'] and len(row['chunks'])==len(actual['evidence']),'Export no longer replays')
        require(row['retrieval_parameters']=={'retriever':profile['retriever'],'top_k':profile['top_k'],'min_score':profile['min_score']},'Wrong retrieval parameters')
        for chunk,hit in zip(row['chunks'],actual['evidence']):
            require(chunk['text']==hit['text'] and chunk['source_id']==hit['source_id'] and chunk['source']==hit['source']['url'],'Changed evidence')
            require(all(chunk.get(k) for k in ('source_id','text','source','version','collected_at')),'Missing A source fields')
        require(row['model_calls']==0 and not row['generation_done'],'Export claims generation')
    require(sum(bool(v['chunks']) for v in exported.values())==manifest['items_with_hits']==0,'A coverage changed')
    require(manifest['interface_checks']['fixture_text_not_experiment_output'] and manifest['interface_checks']['model_calls']==0 and not manifest['A_actual_model_joint_validation_completed'],'Fixture promoted to formal results')
    links=0
    for doc in FOLDER.glob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',doc.read_text(encoding='utf-8')):
            if target.startswith(('https://','http://','#')):
                continue
            require((doc.parent/target).resolve().exists(),'Broken supplement link: '+target); links+=1
    deck=FOLDER/'C_research_v1.pptx'
    with zipfile.ZipFile(deck) as archive:
        ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','c':'http://schemas.openxmlformats.org/drawingml/2006/chart'}
        names=archive.namelist(); slides=sorted(n for n in names if re.fullmatch(r'ppt/slides/slide\d+\.xml',n))
        notes=[n for n in names if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',n)]
        charts=[n for n in names if re.search(r'/charts/chart\d+\.xml$',n)]
        require(len(slides)==5 and len(notes)==5 and len(charts)==1,'Slide/notes/chart counts differ')
        tables=sum(len(ET.fromstring(archive.read(n)).findall('.//a:tbl',ns)) for n in slides)
        require(tables==3,'Tables must be editable')
        numeric=ET.fromstring(archive.read(charts[0])).findall('.//c:numCache/c:pt/c:v',ns)
        require([int(float(v.text)) for v in numeric]==[16,1,2,2,8,1],'Chart counts differ')
        require(any(n.startswith('ppt/embeddings/') and n.endswith('.xlsx') for n in names),'Chart workbook missing')
        text='\n'.join(''.join(t.text or '' for t in ET.fromstring(archive.read(n)).findall('.//a:t',ns)) for n in slides)
        require('正式正确率' in text and '尚未' in text and '48条均无命中' in text,'Research limits lost')
    return {'passed':True,'historical_files_unchanged':len(frozen),'source_dates':len(dates['items']),
            'publication_unknown_with_reason':sum(not r['published_at'] for r in dates['items']),
            'method_references':len(refs['methods']),'factual_reference_entries':len(refs['factual_sources']),
            'temporal_cases':len(temporal['cases']),'A_export_rows':len(exported),'A_rows_with_hits':0,
            'A_positive_interface_probe':manifest['positive_probe']['passed_to_A_messages'],
            'slides':5,'native_tables':tables,'native_charts':1,'slide_sha256':digest(deck),
            'local_links_checked':links,'model_calls':0,'independent_human_reviews':0,'formal_accuracy':None}


if __name__=='__main__':
    result=check(); (FOLDER/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
