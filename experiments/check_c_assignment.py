"""Plan then audit C against the original assignment, without accepting old completion labels."""
import argparse
import csv
import hashlib
import json
import subprocess
import sys
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
FOLDER = ROOT / 'docs/c_work/assignment_check_20261125_v1'
SOURCE = Path('C:/Users/ASUS/xwechat_files/wxid_7400344003511_f082/msg/file/2026-11/LLM-Governance验收答辩四人详细分工方案.docx')
GIT = ['git', '-c', f'safe.directory={ROOT.as_posix()}']

# These criteria are written before --run, rather than inferred from existing artifacts.
ITEMS = [
 ('C1.1','C1','检查125条问题','原125题结构和版本','125个唯一ID、五类各25条，问题/参考/来源/注释可追溯，原文件不被覆盖'),
 ('C1.2','C1','事实题确认来源','事实来源与核验完成度','事实核验覆盖逐题证据；来源支持范围、未确认目标和待复核项明确，不能把提案当正式批准'),
 ('C1.3','C1','错误前提题写清','错误前提逐题记录','25道错误前提题均有纠正依据，参考自身有误时单列修订'),
 ('C1.4','C1','虚构实体题写清','未知实体证据边界','无法确认的目标写清原因；检索不到不推出不存在，开发副本移除未经确认的真值'),
 ('C1.5','C1','数学逻辑题补推导','数学推导与歧义','25道均有推导或明确歧义；平方根、数列规律等条件缺口单列'),
 ('C1.6','C1','时效题补截至日期','时效日期和可接受答案','事件年份或截至日期齐备；正式题面与可接受答案口径确认后冻结'),
 ('C1.7','C1','交付修订记录','修订可追溯','修订前后、理由、来源与批准状态明确，旧题及旧回答不静默改写'),
 ('C2.1','C2','选取项目任务范围内','来源身份与采集信息','每个来源有身份、标题、URL或文件、定位及采集日期'),
 ('C2.2','C2','发布日期和采集日期','来源发布日期','发布日期已记录；未知日期显式说明原因及使用限制，不以采集日期替代'),
 ('C2.3','C2','完成清洗','分段索引和来源关联','片段唯一、文本非空、主题明确、来源可解析，检索输出保留片段和来源'),
 ('C2.4','C2','知识库快照与构建说明','知识库可重建','从来源输入重建v3/v4，与保存语义及哈希一致，不修改历史语料'),
 ('C2.5','C2','不得直接导入题目','知识输入隔离','构建输入不包含问答/参考/评分字段；拒绝带此类字段的新增输入；不把该检查当成无泄漏证明'),
 ('C2.6','C2','与B交叉检查','B交叉泄漏复核','有B/C实际交叉复核记录，覆盖来源、近重复、语义重叠及测试暴露'),
 ('C2.7','C2','固定知识库快照','正式知识库冻结','正式运行前冻结知识库、题集和评分版本；开发哈希不能代替正式冻结批准'),
 ('C3.1','C3','实现“检索证据','回答约束与检索组件','仅约束、仅检索、组合均可调用，包含证据不足、前提和引用约束，不要求效果必然提升'),
 ('C3.2','C3','数学题按任务设计','数学绕过无关检索','数学任务保留推导路径并绕过无关检索，有prepare-only检查'),
 ('C3.3','C3','记录每条使用的证据','逐条检索日志','记录实际使用片段、来源、参数、查询诊断及无命中；模型回答与程序拒答分开'),
 ('C3.4','C3','向A提供抗幻接口','A接口和真实导出','C接口及真实证据导出可对接A冻结输入，包含UID、来源、版本和日期'),
 ('C3.5','C3','共同调试联合方案','与A联合接入复核','检查A实际调用与证据使用；主题不足和无命中如实记录，不能只凭C自己的原型宣布接入完成'),
 ('C4.1','C4','配合D比较','四组开发消融','相同开发输入和生成配置下baseline/constraint/retrieval/combined有原始输出与可复放日志'),
 ('C4.2','C4','抽查不少于30个','30条检索支持分析','至少30个不同问题，逐条保留证据、相关性/支持标签与理由，标清判断来源'),
 ('C4.3','C4','区分检索失败','检索与生成故障区分','案例能从原回答回到实际片段，区分无命中、支持不足和未遵循证据'),
 ('C4.4','C4','对错误引用','三类故障逐项分析','错误引用、过度拒答、知识过时分别有绑定原输出的案例分析；未观察到的类型也应明确处理'),
 ('C4.5','C4','C输出检索图','C检索图','提供与逐条支持标签和实际样本数一致的检索图，不冒充正式正确率'),
 ('C4.6','C4','消融结果及方法章节','C方法和研究章节','C数据、来源、方法、消融及限制有可追溯研究文本，负面结果保留'),
 ('X1','协作','先与C双人独立试标','C与D独立试标25条','两名真人分别保留25条独立意见；统一规则、分歧裁决和真实一致性记录齐备'),
 ('X2','协作','C复核不少于20%','D正式评分的C复核','按类别复核至少20%及所有争议，保留抽样分母、原标签和C意见'),
 ('X3','协作','E0至E3使用同一冻结','正式E2与必要消融','在共同冻结测试集、模型与生成配置下完成C所属正式运行，由D独立评价'),
 ('X4','共同交付','代码与环境','环境和独立复现','依赖与命令明确，发布版本固定，独立检出并复现一批样本；记录安装与硬件边界'),
 ('X5','共同交付','C核对方法来源','方法来源与参考文献','方法来源、公开事实来源和报告参考文献能一一对应，实际核对有记录'),
 ('X6','共同交付','授权或使用说明','数据来源与使用说明','幻觉数据及知识来源的来源、版本和授权或使用边界有明确说明'),
 ('X7','答辩','四人各制研究页','C正式研究幻灯片','有C研究页及对应图表，版本和数字与报告/原始结果一致'),
 ('X8','答辩','知识更新后结果如何复现','C讲述及三类问答','讲清数据/RAG/边界/失败，并明确准备检索仍幻觉、泄漏避免、知识更新复现三类回答'),
 ('X9','答辩','两次彩排记录','共同彩排与C部分','有两次共同彩排中C讲述、问答、计时及修正记录'),
 ('X10','共同交付','第一周先对照项目任务书','学校硬性要求核对','已取得任务书及验收模板并记录C相关硬性要求；不擅自追加LoRA或第二模型'),
 ('X11','共同交付','各人使用独立分支','贡献和版本追溯','C开发交付在独立分支中，有实际提交、命令、输入输出与已知问题；未提交增量单列'),
]


def load(relative):
    return json.loads((ROOT / relative).read_text(encoding='utf-8'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def plan():
    FOLDER.mkdir(parents=True, exist_ok=False)
    raw = SOURCE.read_bytes()
    with zipfile.ZipFile(SOURCE) as archive:
        tree = ET.fromstring(archive.read('word/document.xml'))
    ns = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    texts = [''.join(t.text or '' for t in p.findall('.//w:t', ns)) for p in tree.findall('.//w:p', ns)]
    paragraphs = [{'paragraph':i+1,'text':t} for i,t in enumerate(texts) if t.strip()]
    source = {'file_name':SOURCE.name,'source_sha256':hashlib.sha256(raw).hexdigest(),'paragraphs':paragraphs}
    (FOLDER/'assignment_source.json').write_text(json.dumps(source, ensure_ascii=False, indent=2), encoding='utf-8')
    items = []
    for ident, area, anchor, title, criterion in ITEMS:
        matches = [p for p in paragraphs if anchor in p['text']]
        if not matches:
            raise ValueError('Original assignment clause not found: '+anchor)
        items.append({'id':ident,'area':area,'title':title,'acceptance':criterion,
                      'assignment_clauses':matches,'initial_status':'not_checked'})
    payload = {'date':'2026-11-25','source_sha256':source['source_sha256'],'reviewer':'AI_assistant_fresh_assignment_based_audit_not_independent_human',
               'status_policy':'已满足 / 部分满足 / 待协作 / 未交付 / 核验失败；数量不是任务完成百分比',
               'excluded_as_optional':['第二模型','LoRA','必须提升某个分数'],'items':items}
    (FOLDER/'checklist_plan.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = ['# C分工检查清单','', '依据原始分工方案建立，逐项核验前全部标为待检查。','']
    for item in items:
        lines.append(f"- [ ] {item['id']} {item['title']}：{item['acceptance']}")
    (FOLDER/'CHECKLIST.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print(json.dumps({'phase':'plan_created_before_checks','items':len(items),'source_sha256':source['source_sha256']},ensure_ascii=False))


def command(label, args):
    proc = subprocess.run([sys.executable,'-X','utf8',*args], cwd=ROOT, encoding='utf-8', text=True, capture_output=True)
    log = FOLDER / f'{label}.log'
    log.write_text(proc.stdout+'\n'+proc.stderr,encoding='utf-8')
    return {'argv':[sys.executable,'-X','utf8',*args],'exit_code':proc.returncode,
            'log':log.relative_to(ROOT).as_posix(),'log_sha256':digest(log)}


def run():
    if (FOLDER/'results.json').exists():
        raise FileExistsError('Keep the completed audit; use a new version for another audit')
    p = json.loads((FOLDER/'checklist_plan.json').read_text(encoding='utf-8'))
    commands = [command('full_delivery',['experiments/check_c_delivery.py','--run-tests']),
                command('closeout',['experiments/check_c_closeout.py'])]
    from experiments.build_c_knowledge import build, validate_document
    from experiments.check_c_component_contract import check as component_check
    from experiments.check_c_pilot_review import check as pilot_check
    from experiments.check_c_closeout import check as closeout_check
    from src.utils.experiment_io import latest_records, read_records

    audit = load('docs/c_work/data_audit.json')
    rows = audit['items']
    usage = load('docs/c_work/data_usage.json')
    corpus = load('knowledge/corpus_v4.json')
    sources, chunks = corpus['sources'], corpus['chunks']
    v3 = build(load('knowledge/corpus.json'),load('knowledge/source_documents.json'))
    v4 = build(load('knowledge/corpus_v3.json'),load('knowledge/nobel_documents_v1.json'))
    v4.update(version='c-dev-2026-11-23-v4',selection_policy=load('knowledge/nobel_documents_v1.json')['scope'],
              base_corpus_sha256=digest(ROOT/'knowledge/corpus_v3.json'),supplement_version=load('knowledge/nobel_documents_v1.json')['version'])
    rebuilt = {'v3_equal':v3==load('knowledge/corpus_v3.json'),'v4_equal':v4==corpus,
               'v4_hash_matches_manifest':digest(ROOT/'knowledge/corpus_v4.json')==load('knowledge/build_manifest_v4.json')['corpus_sha256']}
    fields = {'question','reference','reference_source','answer','score','rationale'}
    def forbidden_keys(value):
        if isinstance(value,dict):
            return fields.intersection(value).union(*(forbidden_keys(v) for v in value.values()))
        if isinstance(value,list):
            return set().union(*(forbidden_keys(v) for v in value))
        return set()
    no_qa = not any(forbidden_keys(load(path)) for path in ('knowledge/corpus.json','knowledge/source_documents.json','knowledge/nobel_documents_v1.json'))
    bad = dict(load('knowledge/source_documents.json')['documents'][0],reference='must not ingest')
    rejected = False
    try:
        validate_document(bad)
    except ValueError:
        rejected=True
    component = component_check()
    pilot = pilot_check()
    support = load('docs/c_work/retrieval_support_30_v1.json')
    ledger = load('docs/c_work/failure_evidence_ledger_v1.json')
    expanded = list(latest_records(read_records(ROOT/'docs/c_work/runs/expanded_v3/records.jsonl')).values())
    category_counts = Counter(r['category'] for r in rows)
    math_rows = [r for r in rows if r['category']=='math_logic']
    timed = [r for r in rows if r['category']=='time_sensitive']
    source_missing_pub = [s['id'] for s in sources if not s.get('published_at')]
    evidence_files = [path for path in (ROOT/'docs/c_work').glob('C_*.md')]
    stale_mentions = [{'file':path.relative_to(ROOT).as_posix(),'line':n,'text':line.strip()} for path in evidence_files
                      for n,line in enumerate(path.read_text(encoding='utf-8').splitlines(),1) if any(w in line for w in ('知识过时','知识过期','旧知识'))]
    files = [str(path.relative_to(ROOT)).replace('\\','/') for top in ('docs','configs','datasets','src','tests','experiments')
             for path in (ROOT/top).rglob('*') if path.is_file() and '__pycache__' not in path.parts and 'runs' not in path.parts]
    presentation_files = [path for path in files if path.endswith(('.pptx','.ppt','.odp'))]
    dependency_files = [path for path in files if any(k in Path(path).name.lower() for k in ('requirements','environment.yml','pyproject.toml','poetry.lock','conda-lock'))]
    git_status = subprocess.check_output(GIT+['status','--porcelain','--untracked-files=normal'],cwd=ROOT,text=True,encoding='utf-8')
    observed = {'dataset_items':len(rows),'categories':dict(category_counts),'original_dataset_unchanged':digest(ROOT/'datasets/hallucination/test_set.json')==audit['summary']['original_sha256'],
                'math_derivations':sum(bool(r['review_evidence']) for r in math_rows),'math_ambiguity_ids':[r['id'] for r in math_rows if r['source_verification_status']=='reference_issue'],
                'time_items':len(timed),'time_items_with_event_or_asof':sum(bool(r['as_of'] or r['event_year']) for r in timed),
                'approved_final_items':sum(bool(r['approved_for_final_test']) for r in rows),
                'source_count':len(sources),'chunk_count':len(chunks),'source_ids_without_publication_date':source_missing_pub,
                'all_sources_have_identity_url_locator_access_date':all(all(s.get(k) for k in ('id','title','url','locator','accessed_at')) for s in sources),
                'all_chunks_resolve_source':all(c['source_id'] in {s['id'] for s in sources} and c.get('text') and c.get('topics') for c in chunks),
                'rebuild':rebuilt,'knowledge_no_forbidden_input_keys':no_qa,'answer_input_rejected':rejected,
                'component_cases':len(component['cases']),'pilot':pilot,'retrieval_support_queries':len({r['question'] for r in support['cases']}),
                'support_ai_judgments':sum(r['inspection_origin']=='AI_developer_not_independent_human' for r in support['cases']),
                'expanded_development_mode_counts':dict(Counter(r['mode'] for r in expanded)),
                'failure_chain_records':len(ledger['cases']),'stale_knowledge_text_mentions':stale_mentions,
                'presentation_files_found':presentation_files,'dependency_install_files_found':dependency_files,
                'git_head':subprocess.check_output(GIT+['rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                'git_status_at_check':git_status,'independent_human_reviews':0,'new_model_calls':0}
    P='已满足'; A='部分满足'; W='待协作'; M='未交付'
    assessments = {
      'C1.1':(P,'125个唯一ID，五类各25条，原数据SHA256保持不变。','docs/c_work/data_audit.json','保留原数据及新版本差异记录。'),
      'C1.2':(A,'有125题初审与来源补查；33/34/37/41/42目标身份仍未核实，候选均未获正式批准。','docs/c_work/pending_repairs_v2/report.md','补具体身份/产品版本证据并交D独立复核，不靠背景资料补真值。'),
      'C1.3':(P,'错误前提25条均有核验说明；牛顿、爱迪生等参考问题有显式修订提案。','docs/c_work/data_audit.json','待正式批准时使用修订版本，不覆盖历史题目。'),
      'C1.4':(P,'开发使用角色明确记录22条不确定性探针，未把检索不到统一判为不存在。','docs/c_work/data_usage.json','后续沿用未知与已证伪的区分。'),
      'C1.5':(P,'25条数学题均有推导/边界说明；107、111、117明确列参考或条件歧义。','docs/c_work/data_audit.json','正式题集批准时确认三条歧义修订。'),
      'C1.6':(A,'25条均有事件年份或截至日期；日期在核验台账中，原题修订和可接受答案仍未正式冻结。','docs/c_work/revision_index_v1/report.md','确认第63题榜单口径、动态事实的截至日期及接受范围。'),
      'C1.7':(P,'修订索引30条字段提案涉及28题，限定新题另列；输入和旧运行不变检查通过。','docs/c_work/revision_index_v1/report.md','保持提案、批准、正式采用三个状态分离。'),
      'C2.1':(P,'21个来源均有身份、标题、URL、定位和采集日期。','knowledge/corpus_v4.json','新来源保持相同元数据要求。'),
      'C2.2':(A,'21源中5条有发布日期，16条为null；未逐源说明未知原因与日期使用边界。','knowledge/corpus_v4.json','新建日期补充台账；能查到的记录来源，查不到的明确未知，不改旧快照。'),
      'C2.3':(P,'31个片段非空且关联有效来源，包含主题锚点，运行日志保留完整片段。','knowledge/corpus_v4.json','继续检查中文转述的支持范围。'),
      'C2.4':(P,'从原输入重建v3/v4语义一致，v4字节哈希与构建清单一致。','knowledge/build_manifest_v4.json','未来更新知识库另存版本并保留旧输入。'),
      'C2.5':(P,'递归检查三份知识输入未发现问答/参考/评分字段；带reference的输入被构建器拒绝。','experiments/build_c_knowledge.py','仍需来源和语义层面的泄漏交叉复核。'),
      'C2.6':(W,'已有C侧精确匹配筛查，尚无B/C共同确认的语义、近重复和来源暴露复核记录。','docs/c_work/team_review_20261125_v1.json','与B交叉确认并保存双方真实意见。'),
      'C2.7':(A,'开发语料有哈希及配置；build_manifest_v4明确independent_holdout=false。','knowledge/build_manifest_v4.json','正式冻结题集/知识库/评分协议并记录确认人和日期。'),
      'C3.1':(P,'四种模式及约束实现存在，固定输出和源码重放检查通过；失败与退化结果保留。','src/governance/anti_hallucination.py','不以单题改善宣称总体有效。'),
      'C3.2':(P,'六类prepare-only接口检查含数学绕过，模型工厂未被调用。','docs/c_work/c_component_contract.json','实际调用方保持math_logic类别映射。'),
      'C3.3':(P,'运行合同及逐条日志保留证据、参数、无命中和回答来源；冻结证据可复放。','docs/c_work/runs/expanded_v3/manifest.json','联合调用时同样记录真实使用片段。'),
      'C3.4':(A,'有C可调用接口；尚无A冻结UID到证据JSON的实际交付包，A/B另有4条UID更名。','docs/c_work/C_COMPONENT_HANDOFF.md','显式确认输入版本与映射，导出真实片段/日期/版本及无命中。'),
      'C3.5':(A,'有C自己的集成原型；A的12开发题和36正常题在当前配置下均无命中，尚无A实际使用C证据的联合验证。','docs/c_work/team_review_20261125_v1.json','与A对齐覆盖范围和正式输入；无命中如实保留，不按测试答案补库。'),
      'C4.1':(P,'87题四组348条开发输出存在，各组相同基础生成参数；原始记录及源码重放检查通过。','docs/c_work/runs/expanded_v3/manifest.json','正式测试与D独立评分另见X3。'),
      'C4.2':(P,'30个不同检索问题有支持标签、理由及可重放证据；全部明确为AI开发诊断。','docs/c_work/retrieval_support_30_v1.json','复核标签语义；不能把30条AI诊断算作独立真人评分。'),
      'C4.3':(P,'11个历史案例链逐条绑定原日志及哈希，区分无证据、主体错配、证据忽略和任务未完成。','docs/c_work/failure_evidence_ledger_v1.json','正式案例结论交D复核。'),
      'C4.4':(A,'有错误引用和过度拒答案例；知识过时尚未形成独立的带日期/版本对照及原输出定位的专项分析。','docs/c_work/C_FAILURE_EVIDENCE.md','补知识过时分析或明确当前语料/样本中未观察到并给出检查范围。'),
      'C4.5':(P,'PNG/SVG检索图与30条AI支持诊断对应，未标为正式准确率。','docs/c_work/figures/c_retrieval_support_30.png','独立复核后若标签变化，另存图表版本。'),
      'C4.6':(P,'C方法、故障、消融和答辩文字存在；负面结果与局限明确。','docs/c_work/C_METHODS.md','正式评分完成后补结果章节，保留开发阶段限定。'),
      'X1':(W,'25条辅助稿全部为C_AI_draft；独立真人C/D标签、规则冻结和裁决均未完成。','docs/c_work/pilot_C_ai_v1/README.md','C/D分别独立复核，先统一标签口径，保存分歧再裁决。'),
      'X2':(W,'未见D正式完整评分包，缺可用于20%分层抽样和全部争议复核的标签分母。','docs/c_work/C_REVIEW_WORKFLOW.md','收到D正式评分后按类别抽样并保留C意见及争议处理。'),
      'X3':(W,'现有结果均为开发运行；没有共同冻结正式测试和D独立评价的E2/E4结果。','docs/c_work/DATA_DECISIONS.md','与D固定入口、测试划分、生成参数和评分协议后执行C所属正式组。'),
      'X4':(A,'有实际依赖版本、命令与历史导出重放；仓库未见可安装环境文件，未完成新环境模型批量独立复现。','docs/c_work/runtime_versions.json','C核对D提供的依赖安装/启动流程，记录实际独立复现。'),
      'X5':(A,'公开事实来源登记充分；未见将BM25等方法原始文献与结题参考文献逐项对照的核对记录。','docs/c_work/C_METHODS.md','整理方法文献和事实来源的报告引文映射，记录核对日期与范围。'),
      'X6':(A,'有来源、版本和中文转述说明；数据及各类知识资料的授权或使用边界未集中明确登记。','docs/c_work/README.md','补来源使用说明，未知授权写未知，不假称开放许可。'),
      'X7':(M,'在本仓库业务目录未找到C正式幻灯片；讲述Markdown不能替代正式研究页。','docs/c_work/C_DEFENSE_NOTES.md','依据最终研究结果制作C页面，交D组装并核对数字。'),
      'X8':(A,'讲述和FAQ已覆盖检索仍幻觉、答案泄漏；知识更新复现有协议但未形成清晰的专项问答。','docs/c_work/C_DEFENSE_NOTES.md','将版本冻结、来源日期和旧快照重放整理为第三类明确回答。'),
      'X9':(W,'仓库中未见两次共同彩排及C计时/问答记录；不据此推断线下从未演练。','docs/c_work/C_DEFENSE_NOTES.md','共同彩排后记录实际日期、问题、计时和修正。'),
      'X10':(W,'当前仓库未见学校正式任务书/模板及硬性要求对照记录；原分工方案仅给建议。','C_PROGRESS.md','取得学校材料后确认C必做项，不把可选增强擅自设为必做。'),
      'X11':(P,'C已有独立分支、真实提交和命令/输入输出/局限记录；本次新增审计仍为本地增量，未冒充已推送。','docs/c_work/C_CLOSEOUT.md','按需要在C分支提交本次审计，发布时保留版本与贡献对应。'),
    }
    flags = {
        'C1.1': observed['dataset_items']==125 and set(category_counts.values())=={25} and observed['original_dataset_unchanged'] and len({r['id'] for r in rows})==125,
        'C1.3': all(r['review_evidence'] for r in rows if r['category']=='false_premise'),
        'C1.4': usage['summary']['roles']['uncertainty_probe']==22,
        'C1.5': observed['math_derivations']==25,
        'C2.1': observed['all_sources_have_identity_url_locator_access_date'],
        'C2.3': observed['all_chunks_resolve_source'] and len({c['id'] for c in chunks})==31,
        'C2.4':all(rebuilt.values()),'C2.5':no_qa and rejected,
        'C3.2':component['passed'] and len(component['cases'])==6,
        'C4.1':dict(Counter(r['mode'] for r in expanded))=={mode:87 for mode in ('baseline','constraint','retrieval','combined')},
        'C4.2':observed['retrieval_support_queries']>=30 and all(r['basis'] and r['support_judgment'] for r in support['cases']),
        'C4.3':len(ledger['cases'])==11,
    }
    supplement_path=ROOT/'docs/c_work/closeout_supplement_20261125_v1/verification.json'
    if supplement_path.exists():
        from experiments.check_c_supplement import check as check_supplement
        supplement=check_supplement()
        observed['closeout_supplement']=supplement
        prefix='docs/c_work/closeout_supplement_20261125_v1/'
        upgrades={
            'C2.2':('21源日期旁注已补；16条未知精确首次发表时间均说明原因，页面更新日、数据版本与采集日分开。','SOURCE_DATES.md','未来核实到精确发表日时另建来源版本，不修改旧语料。'),
            'C4.4':('原错误引用/过拒分析保留；另补4条时间故障案例，绑定完整原文、日期口径、数组位置和哈希。','TEMPORAL_ANALYSIS.md','时间分析为AI开发判断，正式标签仍交独立真人复核。'),
            'X5':('补3项方法/模型原始来源及实现差异，107条事实来源映射；事实网页和方法论文作用分开。','METHOD_REFERENCES.md','整组报告最终引文格式及新增论断仍按最终稿逐项核对。'),
            'X6':('数据与21源使用边界说明已交付；逐资产权限未知明确保留，不声称统一开放许可。','USAGE.md','外部分发前按具体材料核对条件，不把本说明当授权证书。'),
            'X7':('C的5页可编辑研究页已交付，含3张原生表、1张原生统计图及讲稿备注；已做导入、图表值与版式检查。','C_research_v1.pptx','交D组装；正式评分后另存研究页版本，不将开发结论写成正式验收。'),
            'X8':('新增三类明确问答，知识更新复现按旧快照、新版本、独立运行和哈希分别解释。','REPRODUCTION.md','按实际学校时长和现场问答演练，不虚构彩排完成。'),
        }
        for ident,(finding,evidence,action) in upgrades.items():
            assessments[ident]=(P,finding,prefix+evidence,action)
        flags.update({'C2.2':supplement['source_dates']==21,'C4.4':supplement['temporal_cases']==4,
                      'X5':supplement['method_references']==3,'X6':supplement['source_dates']==21,
                      'X7':supplement['slides']==5 and supplement['native_tables']==3 and supplement['native_charts']==1,
                      'X8':all(q in (ROOT/(prefix+'REPRODUCTION.md')).read_text(encoding='utf-8') for q in ('检索为什么仍可能产生幻觉','如何避免测试答案泄漏','知识更新后结果如何复现'))})
        assessments['C3.4']=(A,'已补A当前48条输入的真实证据导出和4条UID映射；全部无命中。正式输入冻结仍待双方确认。',prefix+'A_HANDOFF.md','共同冻结输入后另存正式导出版本，保留真实无命中。')
        assessments['C3.5']=(A,'已补48条无命中与1条有命中探针的A函数接口夹具检查；模型调用0，不是A实际联合生成验证。',prefix+'A_HANDOFF.md','A实际接入后复核每条证据使用及生成结果。')
        assessments['X4']=(A,'补实际依赖观察清单与复现问答；有历史导出重放，但未在新环境完成真实模型批量独立复现。',prefix+'REPRODUCTION.md','与D核对安装/启动流程，并记录实际独立复现。')
    results = []
    for item in p['items']:
        status, finding, evidence, action = assessments[item['id']]
        if flags.get(item['id']) is False:
            status='核验失败'; finding='实际数据未通过本项自动断言；'+finding
        if not (ROOT/evidence).exists():
            status='核验失败'; finding='引用的证据文件不存在；'+finding
        results.append({**item,'status':status,'finding':finding,'evidence':evidence,'next_action':action})
    check_failures = [r for r in commands if r['exit_code']]
    payload = {'date':'2026-11-25','assignment_source_sha256':p['source_sha256'],
               'plan_sha256':digest(FOLDER/'checklist_plan.json'),'reviewer':p['reviewer'],
               'scope':'Fresh AI audit against original C and shared clauses; not independent human signoff or formal acceptance',
               'counts':dict(Counter(r['status'] for r in results)), 'items':results,'observed':observed,
               'commands':commands,'automatic_checks_passed':not check_failures and not any(r['status']=='核验失败' for r in results),
               'overall_assignment_complete':False,'formal_accuracy':None,'independent_human_reviews':0}
    (FOLDER/'results.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    (FOLDER/'observed_facts.json').write_text(json.dumps(observed,ensure_ascii=False,indent=2),encoding='utf-8')
    lines=['# C分工逐项检查结果','',
           '按原始分工方案重新检查C职责及C承担的协作事项。开发组件和证据材料已有较多交付，但原分工整体尚未完成。这里的“已满足”仅表示该条检查范围已具备证据，不代表整体验收通过。','',
           '日期：2026-11-25。执行者：AI助手；不是另一位真人的独立评分。原始Word来源与SHA256见[条款快照](assignment_source.json)，先建立的[检查计划](checklist_plan.json)保留未检查状态。','',
           '状态数量：'+ '；'.join(f'{k}{v}项' for k,v in payload['counts'].items())+'。这是检查条目数量，不是项目完成百分比。','',
           '自动检查：'+('通过' if payload['automatic_checks_passed'] else '存在失败')+'；本轮新增模型调用0、真实人工标注0、正式正确率未计算。','',
           '| 编号 | 对照条款与检查项 | 状态 | 证据与发现 | 下一步 |','| --- | --- | --- | --- | --- |']
    for item in results:
        ev='../../..'+'/'+item['evidence']
        paragraph=item['assignment_clauses'][0]['paragraph']
        lines.append(f"| {item['id']} | 原方案第{paragraph}段：{item['title']} | {item['status']} | [证据]({ev})：{item['finding']} | {item['next_action']} |")
    lines.extend(['','## 优先处理顺序','',
                  ('1. 日期旁注、时间故障分析、方法引文/使用说明、复现问答及C研究页已补齐。仍保留33/34/37/41/42的身份/产品来源缺口，等待唯一身份或官方发布线索。' if 'closeout_supplement' in observed else '1. 先补C能独立准备的交接材料：来源日期缺口台账、知识过时专项分析、方法文献/事实来源映射、知识更新复现问答、C正式研究页。不得把日期未知补成估计值，也不改旧快照。'),
                  ('2. A当前48条输入的真实导出与4条UID映射已交付；下一步共同确认正式输入与知识库范围，再另存正式导出并开展真实联合生成，不按测试答案补库。' if 'closeout_supplement' in observed else '2. 与A确认输入版本及4条UID映射，交付真实检索导出；当前A的12条开发题与36条正常任务全部无命中，先确认覆盖范围，不能按测试答案补库。'),
                  '3. C/D统一25条试标规则并分别独立真人复核；与B完成来源、近重复和测试暴露的交叉检查。',
                  '4. 在共同入口、数据与评分冻结后执行C正式E2及必要消融，复核D至少20%的分层样本和全部争议。',
                  '5. 对照学校任务书和模板，完成环境复现及两次共同彩排。A/B/D负责的实现仍由对应成员维护。','',
                  '以上待办不因157项代码测试通过、开发运行数量增加或辅助预标注填满而自动完成。第二模型、LoRA和分数必然提升未被追加为C的必达条件。','',
                  '## 本轮核验边界','',
                  ('核验原始Word、现有证据与本轮补充材料。21源日期元数据已另核对访问情况，未重新核准每个来源的全部事实；403/404和日期未知保留。未找到协作记录的结论仅针对本仓库，不断言线下未开展。' if 'closeout_supplement' in observed else '核验原始Word条款、现有逐条台账、语料输入和片段、开发运行、证据重放、接口及本仓库材料。旧外部来源没有在本轮重新联网逐条核准；来源日期是已保存的历史记录。未找到材料的结论仅针对本仓库，不断言线下没有相关成果。'),'',
                  '完整机器结果见[results.json](results.json)，实际命令及退出状态见同文件commands；原始输出见[交付测试日志](full_delivery.log)与[收尾日志](closeout.log)。'])
    (FOLDER/'RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    checked = ['# C分工检查清单','',
               '已依据原始Word逐项核对。勾选表示本条检查范围已满足；未勾选项按实际状态保留。',
               '核验前的[原检查计划](checklist_plan.json)单独保存，逐项证据、发现与下一步见[检查结果](RESULTS.md)。','']
    area = None
    for item in results:
        if item['area'] != area:
            area = item['area']
            checked.extend(['## '+area,''])
        mark = 'x' if item['status'] == '已满足' else ' '
        checked.append(f"- [{mark}] {item['id']} {item['title']}　{item['status']}")
    (FOLDER/'CHECKLIST.md').write_text('\n'.join(checked)+'\n',encoding='utf-8')
    print(json.dumps({'items':len(results),'counts':payload['counts'],'automatic_checks_passed':payload['automatic_checks_passed'],'overall_assignment_complete':False,'rebuild':rebuilt},ensure_ascii=False,indent=2))
    if check_failures or not payload['automatic_checks_passed']:
        raise SystemExit(1)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan',action='store_true')
    parser.add_argument('--run',action='store_true')
    parser.add_argument('--folder',type=Path,help='New version directory; existing completed results are never overwritten')
    args=parser.parse_args()
    if args.folder:
        FOLDER=args.folder.resolve()
    if args.plan == args.run:
        parser.error('Choose exactly one of --plan or --run')
    plan() if args.plan else run()
