"""Build C's missing documentation and a real A-interface export without generating answers."""
import csv
import hashlib
import json
import subprocess
import sys
import types
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.governance.c_component import build_c_service
from src.utils.experiment_io import stable_hash

FOLDER=ROOT/'docs/c_work/closeout_supplement_20261125_v1'
GIT=['git','-c',f'safe.directory={ROOT.as_posix()}']


def load(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8'))


def write(name, value):
    path=FOLDER/name
    path.parent.mkdir(parents=True,exist_ok=True)
    if not isinstance(value,str):
        value=json.dumps(value,ensure_ascii=False,indent=2)
    path.write_text(value,encoding='utf-8')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build():
    research=json.loads((FOLDER/'research_inputs.json').read_text(encoding='utf-8'))
    if (FOLDER/'frozen_inputs.json').exists():
        raise FileExistsError('Keep this completed version; create a new supplement version')
    tracked=subprocess.check_output(GIT+['ls-files'],cwd=ROOT,text=True,encoding='utf-8').splitlines()
    frozen=[p for p in tracked if p.startswith('knowledge/') or p=='datasets/hallucination/test_set.json' or
            p in ('results/hallucination/results.json','docs/c_work/data_audit.json','docs/c_work/data_usage.json','docs/c_work/source_registry.json',
                  'docs/c_work/source_followup_v1.json','docs/c_work/source_followup_pending_v2.json','docs/c_work/retrieval_support_30_v1.json',
                  'docs/c_work/failure_evidence_ledger_v1.json','configs/c_component_profile.json') or
            p.startswith('docs/c_work/runs/') and Path(p).name in ('records.jsonl','manifest.json')]
    original_audit=ROOT/'docs/c_work/assignment_check_20261125_v1'
    frozen += [p.relative_to(ROOT).as_posix() for p in original_audit.iterdir() if p.is_file()]
    write('frozen_inputs.json',{'stage':'preserve_old_artifacts','sha256':{p:sha(ROOT/p) for p in sorted(set(frozen))}})
    corpus=load('knowledge/corpus_v4.json')
    assert set(research['date_observations'])=={s['id'] for s in corpus['sources']}
    date_rows=[]
    for source in corpus['sources']:
        obs=research['date_observations'][source['id']]
        known=obs.get('published_at_verified',source.get('published_at'))
        assert known or obs['unknown_reason']
        date_rows.append({'source_id':source['id'],'title':source['title'],'url':source['url'],
                          'historical_published_at':source.get('published_at'),'published_at':known,
                          'publication_year':obs.get('publication_year'),'last_modified_at':obs.get('last_modified_at'),
                          'data_version':obs.get('data_version'),'historical_collected_at':source['accessed_at'],
                          'metadata_reviewed_at':research['date'],'access_result_this_review':obs['access_result'],
                          'date_evidence_locator':obs['locator'],'unknown_publication_reason':obs['unknown_reason'],
                          'use_limit':'只支持保存的来源与范围，不表示页面全部附加断言、日期或当前状态都已核验；正式引用需保留版本和截至日期。'})
    write('source_dates.json',{'date':research['date'],'applies_to_corpus_sha256':sha(ROOT/'knowledge/corpus_v4.json'),
                              'policy':research['date_policy'],'items':date_rows})
    lines=['# C知识来源日期补充台账','',research['date_policy'],'',
           '本表覆盖当前v4的21个来源；保留5条已有发表日期，16条无法确认精确首次发表日的来源均写明原因。部分来源新增页面更新日，电磁波资料只确认2010年精度。旧知识库及其哈希不改。','',
           '| 来源 | 首次发表 | 更新日或版本 | 本次核对与未知边界 |','| --- | --- | --- | --- |']
    for row in date_rows:
        date=row['published_at'] or (str(row['publication_year'])+'年，月日未知' if row['publication_year'] else '未知')
        update=row['last_modified_at'] or row['data_version'] or '未确认'
        lines.append(f"| [{row['source_id']}]({row['url']}) | {date} | {update} | {row['date_evidence_locator']}；{row['unknown_publication_reason'] or '保留已记录发表日期，访问状态见JSON。'} |")
    lines += ['','## 日期解释','',
              '页面关联新闻、任务发生时间、藏品年代、数据版本和记录创建时间不互相替代。发表日未知不自动使基础事实失效，但不能用该来源证明“最新”“首次”或当前身份。403、404或验证页仅说明本次访问状态，不证明来源事实错误；正式材料应保留旧快照，另寻可读依据后再创建新版本。',
              '', '每条历史采集日期、本轮核对日期和访问状态见[source_dates.json](source_dates.json)。本轮没有把失败访问标成已读正文。']
    write('SOURCE_DATES.md','\n'.join(lines)+'\n')

    registry=load('docs/c_work/source_registry.json')
    source_maps=[]
    for role, entries, origin in [('rag',corpus['sources'],'knowledge/corpus_v4.json'),('audit',registry['sources'],'docs/c_work/source_registry.json'),
                                  ('followup',load('docs/c_work/source_followup_v1.json')['sources'],'docs/c_work/source_followup_v1.json'),
                                  ('pending',load('docs/c_work/source_followup_pending_v2.json')['sources'],'docs/c_work/source_followup_pending_v2.json')]:
        for number, s in enumerate(entries,1):
            source_maps.append({'citation_id':f"{role}:{s.get('id',number)}",'role':role,'source_id':s.get('id'),
                                'title':s.get('title'),'url':s.get('url'),'locator':s.get('locator'),
                                'collected_or_checked_at':s.get('accessed_at',s.get('checked_at',registry.get('checked_at'))),
                                'original_access_method':s.get('access_method','see_original_record'),
                                'origin':origin,'fresh_content_recheck_claimed':False})
    methods=[{**m,'metadata_checked_at':research['date'],'review_origin':'AI_assisted_primary_source_check'} for m in research['methods']]
    write('reference_map.json',{'date':research['date'],'methods':methods,'factual_sources':source_maps,
                               'rule':'方法论文说明方法来源，来源网页说明对应事实；论文成效不迁移成本项目成效；历史事实来源未全部重新访问。'})
    refs=['# C方法来源与报告引文核对','',
          '本记录核对C使用的方法文献及事实来源入口，供C报告和研究页引用；不代替整组报告最终格式校对。方法原论文、来源网页和本项目实测结果分别使用，避免把相关工作中的改善幅度写成本项目结果。','',
          '| 引文 | 原始来源与核对位置 | 本项目对应及差异 |','| --- | --- | --- |']
    for method in methods:
        refs.append(f"| {method['id']} | {method['authors']}，{method['year'] or '网页日期未单列'}，[{method['title']}]({method['url']})。{method['locator']} | {method['supports']} {method['implementation_difference']} |")
    refs += ['','## 报告可以使用的表述','',
             '本文实现基于词面检索与证据提示的抗幻组件。BM25参考Robertson与Zaragoza的概率相关性研究[M1]；外部资料辅助生成的研究背景参考Lewis等[M2]。本实现不训练稠密检索器或生成器，也不复现RAG-Sequence/RAG-Token。主题锚点、特定词项消歧和年份别名回退为本项目的工程规则，效果只按对应开发对照解释。基础模型为本地Qwen2.5-0.5B-Instruct[M3]，身份以官方模型卡和本地权重哈希共同记录。','',
             '实际排序使用k1=1.5、b=0.75和非负平滑IDF；top_k=2、min_score=1.5属于当前显式配置。上述阈值与中文二元片段处理不是论文推荐的通用最佳参数。','',
             '事实来源映射覆盖v4检索资料、125题来源台账、17题补查及五题后续补查。完整标题、URL、定位、历史访问方式和日期见[reference_map.json](reference_map.json)。审计来源没有因为被列入参考文献就自动进入RAG。','',
             'M1的原论文正文在[大学保存的原论文副本](https://www.ccs.neu.edu/home/vip/teach/IRcourse/IR_surveys/robertson_foundations.pdf)核对；DOI当前落地页元数据版式可能不同，引用采用原PDF封面的2009年3卷4期333—389页。']
    write('METHOD_REFERENCES.md','\n'.join(refs)+'\n')
    write('references.bib','''@article{robertson2009bm25,
  author = {Robertson, Stephen and Zaragoza, Hugo},
  title = {The Probabilistic Relevance Framework: BM25 and Beyond},
  journal = {Foundations and Trends in Information Retrieval},
  volume = {3}, number = {4}, pages = {333--389}, year = {2009},
  doi = {10.1561/1500000019}
}
@inproceedings{lewis2020rag,
  author = {Lewis, Patrick and Perez, Ethan and Piktus, Aleksandra and others},
  title = {Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks},
  booktitle = {Advances in Neural Information Processing Systems}, year = {2020},
  url = {https://arxiv.org/abs/2005.11401}
}
@misc{qwen05modelcard,
  author = {{Qwen Team}}, title = {Qwen2.5-0.5B-Instruct model card},
  url = {https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct},
  note = {Accessed 2026-11-25; use local model hashes for reproduction}
}
''')

    policies=research['usage_policies']
    usage=[]
    for source in corpus['sources']:
        host=source['url'].split('/')[2]
        policy='P_NASA' if 'nasa.gov' in host else 'P_NOAA' if 'noaa.gov' in host else 'P_SI' if 'si.edu' in host else None
        usage.append({'source_id':source['id'],'url':source['url'],'policy_id':policy,
                      'material_used':'事实的中文人工转述、来源标识和少量短引文；不含整页/整本或官方装饰图片',
                      'asset_level_license':'not_individually_verified',
                      'attribution':'保留机构/页面标题、URL、定位、采集日期和日期边界',
                      'redistribution_statement':'本项目不为原网页、PDF、藏品图片或第三方材料重新授权；资料公开可访问不等于逐资产CC0。'})
    write('usage_registry.json',{'date':research['date'],'policies':policies,'source_items':usage,
                               'dataset':{'origin':'原仓库125题及其历史输出；本次只补说明，不主张新增数据权利',
                                          'root_license_present':any((ROOT/name).exists() for name in ('LICENSE','LICENSE.md','LICENSE.txt')),
                                          'permission_state':'未发现足以统一重新授权所有题目与外部材料的声明，外部分发许可不由C代签'},
                               'model':'官方卡标注apache-2.0；权重不随交接包分发，仍按实际官方许可使用。'})
    write('USAGE.md','''# C数据与知识资料使用说明

本项目以研究复现为目的保留原仓库125题、版本差异、历史模型回答和来源标识。C不改变题目原有权利归属，不为组员数据或外部资料添加统一开源许可证。根目录是否存在许可文件及来源逐项记录见[usage_registry.json](usage_registry.json)。这是一份实际使用边界登记，不是逐资产授权证书。

知识库以自行整理的中文事实转述为主，保留机构、页面标题、URL、定位、采集日期及少量必要短引文。来源核验台账与RAG入库材料分开；参考答案、人工评分理由不直接入库。没有随交接复制整页网页、整本外部PDF、官方图片或标志。对外发布应保留原署名和条件，不将中文转述称为来源机构发布的官方中文文本。

| 来源类型 | 使用条件入口 | 本项目记录的边界 |
| --- | --- | --- |
| NOAA | [National Ocean Service FAQ](https://oceanservice.noaa.gov/about/faq.html) | 保留署名，不暗示机构背书；第三方内容例外仍适用 |
| NASA | [官方媒体使用说明](https://www.nasa.gov/nasa-brand-center/images-and-media/) | 记录官方说明入口，不推定每一资产都无条件再利用；本次不使用机构标识和装饰图片 |
| Smithsonian | [Terms of Use](https://www.si.edu/termsofuse)、[Open Access FAQ](https://www.si.edu/openaccess/faq) | 未逐项确认当前四个资产CC0，不把整站内容统称开放许可；本轮部分页面读取失败如实保留 |
| Nobel、NIH、NIST等 | 各原始来源页面及其条件 | 事实转述保留引用；未核准逐资产许可，不进行整页或数据库资产再分发 |
| 模型 | [Qwen官方模型卡](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct) | 官方卡标注apache-2.0；权重不打包，模型许可与本仓库数据许可分别处理 |

日期说明、参考文献和使用边界均作为本次旁注保存，旧语料快照不重写。来源失效、访问限制和未知授权不会被自动改写为“已获许可”。C研究页中的统计图表来自本项目原始记录，图注应保留AI开发诊断及正式人工评分未完成的限定。
''')

    baseline=load('results/hallucination/results.json')
    audit={r['id']:r for r in load('docs/c_work/data_audit.json')['items']}
    temporal=[]
    for judgment in research['temporal_cases']:
        index=next(i for i,r in enumerate(baseline) if r['id']==judgment['id'])
        raw=baseline[index]
        temporal.append({**judgment,'source_file':'results/hallucination/results.json','source_file_sha256':sha(ROOT/'results/hallucination/results.json'),
                         'array_index_zero_based':index,'record_sha256':stable_hash(raw),'raw_record':raw,
                         'frozen_audit_evidence':audit[raw['id']]['review_evidence'],'review_origin':'AI_developer_not_independent_human',
                         'generation_time_or_training_cutoff_inferred':False})
    write('temporal_cases.json',{'date':research['date'],'purpose':'时间敏感故障专项，不是总体正确率或纯知识过时发生率',
                                 'selection':'有意选择73、51、59、64四条边界案例，非随机分层样本',
                                 'cases':temporal,'independent_human_reviews':0,'formal_accuracy':None,
                                 'version_risks':[{'source_id':'nobel-physics-repeat-snapshot','stored_scope':'1901—2025','rule':'超出冻结范围的最新/全部问题不能仅凭旧快照作肯定结论'},
                                                  {'source_id':'smithsonian-steam','fresh_access':'404','rule':'来源不可达与事实过时是不同问题，保留旧证据并寻找替代来源后另建版本'}]})
    text=['# 知识过时与时间范围故障分析','',
          '时间相关错误至少分为当前身份已变化、固定事件答错、事件日期错误、资料覆盖上限不足和来源失效。它们需要不同证据，不能一律归因为“知识过时”。本次有意选取4条原始回答作AI开发分析，不计算总体发生率或独立人工一致率。','',
          '原始运行日期和训练截止元数据不全，判断仅针对写明的评估截至日期或事件年度；不能倒推模型生成当日必然错误，也不能由一条旧回答推算模型知识截止时间。','',
          '| 原题ID | 观察 | 分类和边界 |','| --- | --- | --- |']
    for row in temporal:
        urls='、'.join(f'[来源{n+1}]({url})' for n,url in enumerate(row['evidence_urls']))
        text.append(f"| {row['id']} | {row['finding']} {urls} | {row['classification']}；{row['limits']} |")
    text += ['','## 定位与证据','',
             '每条原问题、完整回答、数组位置、原文件SHA256和记录内容哈希保存于[temporal_cases.json](temporal_cases.json)。第73题的身份对照使用本轮白宫页面及明确冻结的历史拜登档案；第51、64题沿用已保存的对应年度官方核验记录。第59题本轮官方URL访问403，额外时间断言仍列待核验。','',
             '这说明完整回答评分必须分开检查核心、附加事实和日期范围。识别旧任人物不能自动修正同段内的日期或编号；固定2022事件也不能拿另一个年份的事实直接替换。','',
             '## 检索与生成的区分','',
             'v4名录片段的覆盖范围1901—2025不等于持续联网更新。问题超出范围时，应记录范围不足，而不是让资料发布日期或采集日期替代问题截至日期。来源返回404是可追溯性风险，不等于其历史内容被证伪。资料已覆盖而模型仍移植主体或年份，则进入生成错用证据分析。','',
             '## 更新与复现','',
             '冻结旧题、旧语料、旧源码及旧回答；补来源只建旁注。新知识库使用新版本、原始来源日期和采集日期，重建索引并另存配置，随后重新执行相关组。若时间范围或参考答案变化，先建立新数据版本再运行，不能把新知识套到旧输出后冒称同一实验。具体交接口径见[复现问答](REPRODUCTION.md)。']
    write('TEMPORAL_ANALYSIS.md','\n'.join(text)+'\n')

    team=load('docs/c_work/team_review_20261125_v1.json')
    commit=team['branch_commits']['A_main']
    def git_blob(path):
        return subprocess.check_output(GIT+['show',commit+':'+path],cwd=ROOT)
    snapshots={}
    input_groups=[]
    for name,path in [('pilot_dev','datasets/a/pilot_dev.json'),('normal_tasks','datasets/a/normal_tasks.json')]:
        raw=git_blob(path)
        target=FOLDER/'source_snapshot'/f'A_{name}.json'; target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(raw)
        snapshots[path]={'snapshot':target.relative_to(FOLDER).as_posix(),'sha256':sha(target)}
        input_groups.extend((name,item) for item in json.loads(raw))
    def forbidden_model():
        raise AssertionError('Evidence export must never load a model')
    service,retriever,profile=build_c_service(ROOT,forbidden_model)
    def evidence(item):
        prepared=service.answer(item['question'],profile['strategy'],item.get('category'),prepare_only=True)
        chunks=[{'source_id':h['source_id'],'text':h['text'],'source':h['source']['url'],
                 'version':retriever.version,'collected_at':h['source']['accessed_at'],'chunk_id':h['id'],
                 'locator':h['source'].get('locator'),'score':h['score']} for h in prepared['evidence']]
        return {'chunks':chunks,'snapshot':retriever.version+'@sha256:'+retriever.sha256,
                'retrieval_parameters':{'retriever':profile['retriever'],'top_k':profile['top_k'],'min_score':profile['min_score']},
                'retrieval_status':prepared['retrieval_status'],'question_sha256':stable_hash(item['question']),
                'model_calls':0,'generation_done':False}
    exported={item['uid']:evidence(item) for _,item in input_groups}
    assert len(exported)==48 and service.model is None
    write('a_evidence_export.json',exported)
    source=git_blob('src/governance/interventions.py')
    (FOLDER/'source_snapshot/A_interventions.py').write_bytes(source)
    module=types.ModuleType('A_interface_snapshot'); exec(compile(source,'A_interventions.py','exec'),module.__dict__)
    config={'name':'E2_interface_fixture','anti_hallucination':True,'fairness':False,'strategy':'basic','self_check':False,'retrieval':True}
    fixture_calls=[]
    def stub(messages):
        fixture_calls.append(messages)
        return {'text':'C_INTERFACE_FIXTURE_NOT_MODEL_OUTPUT'}
    for _,item in input_groups:
        row=module.answer(item,config,stub,exported[item['uid']])
        assert row['evidence']==exported[item['uid']] and fixture_calls[-1][-1]['content']==item['question']
    probe={'question':'1921年度诺贝尔物理学奖实际在哪一年颁发？','category':'factual'}
    probe_evidence=evidence(probe); assert probe_evidence['chunks']
    probe_row=module.answer(probe,config,stub,probe_evidence)
    assert all(c['text'] in fixture_calls[-1][1]['content'] for c in probe_evidence['chunks'])
    write('a_handoff_manifest.json',{'date':research['date'],'A_commit':commit,'B_commit_observed':team['branch_commits']['B'],
                                    'input_snapshots':snapshots,'A_interventions_snapshot_sha256':hashlib.sha256(source).hexdigest(),
                                    'corpus_sha256':retriever.sha256,'profile_sha256':sha(ROOT/'configs/c_component_profile.json'),
                                    'export_sha256':sha(FOLDER/'a_evidence_export.json'),'items':len(exported),
                                    'items_with_hits':sum(bool(e['chunks']) for e in exported.values()),
                                    'uid_lineage':team['A_B_uid_lineage'],'formal_input_frozen':False,
                                    'positive_probe':{'request':probe,'prepared_evidence':probe_evidence,'passed_to_A_messages':True},
                                    'interface_checks':{'input_items_checked':48,'positive_probe_checked':1,'fixture_generate_calls':len(fixture_calls),
                                                        'model_calls':0,'fixture_text_not_experiment_output':True},
                                    'A_actual_model_joint_validation_completed':False})
    write('A_HANDOFF.md','''# C交给A的真实检索导出

导出文件[a_evidence_export.json](a_evidence_export.json)对应A当前提交中的12条开发题和36条正常任务，每个UID都有真实检索结果、知识库版本/哈希、参数、问题哈希及无命中状态。输入副本和来源提交见[a_handoff_manifest.json](a_handoff_manifest.json)。

当前固定配置下48条全部无命中，因此chunks均为空。空数组是真实覆盖结果，不代表已完成有效证据注入或证明RAG有收益；不以参考答案填补片段。正式联合实验应先共同确认输入和知识库范围。

A输入快照中的4条旧UID在B数据中已更名，显式映射为age的A-D01→AGE-D01、anchoring的A-D01→AN-D01、occupation的A-D01→OCC-D01、region_culture的A-D01→RC-D01。本导出保留A实际输入的旧UID，避免与现有历史输出错配；后续正式输入切换时另建版本，不能覆盖旧记录。

```powershell
# 在A负责的检出版本中使用；输出目录必须新建
python experiments/run_a.py --input datasets/a/pilot_dev.json --configs configs/a/formal_matrix_TEMPLATE.json --evidence path/to/a_evidence_export.json --output results/a/new_development_run
```

上例只是交接入口，formal_matrix_TEMPLATE仍是模板，不能当作已签收冻结协议；本轮没有执行该生成命令。先核对12条开发输入与导出中的问题哈希，正常任务应使用对应输入文件。

已通过A函数的48条无命中消息传递检查及1条有命中探针检查，生成函数为明确标识的测试夹具，实际模型调用为0。探针验证字段和片段能进入A消息，不属于正式数据、模型回答或联合效果验证。A的联合实现未改动。正式C3交接/联合复核仍等待双方冻结输入和实际生成检查。
''')

    write('REPRODUCTION.md','''# C知识更新复现与交接问答

## 检索为什么仍可能产生幻觉

召回表示片段与词面或主题相关，不等于支持目标主体和全部断言。原案例中一般相对论资料被移植到题设人物；已有前提纠正资料也可能被模型忽略。应先看实际片段及来源，再区分无命中、支持不足、主体错配和生成未遵循证据；不能只看是否有引用编号。

## 如何避免测试答案泄漏

事实核验台账与知识入库分开，知识构建拒绝question/reference/answer/score等字段。公开事实资料可以独立整理，但这个字段检查不能证明与测试语义独立。当前知识库与开发题有主题重叠；B/C仍需检查近重复、来源暴露和语义重叠，正式冻结前不使用测试集选择提示词或按测试答案补库。

## 知识更新后结果如何复现

旧结果绑定旧数据、知识库、源码、模型文件和生成配置的哈希。更新知识不能覆盖旧corpus或旧run：保留旧来源段落与日期，另建新语料版本和构建清单，重建索引，再新建显式配置、运行目录与相关对照。新页面更新日和本轮访问日不能改写旧来源的历史采集日。发现原题时间范围变化时，应另建数据版本，不能换参考后重评旧输出并称同一实验。

复现旧结果首先做无模型的证据重放；需要重新生成时使用保存的配置和模型文件，记录软件、硬件及生成参数。跨硬件/依赖版本不保证逐token相同。模型或网络不可用时展示明确标记的历史回放，不称为现场生成。

```powershell
python -X utf8 experiments/check_c_delivery.py --run-tests
python -X utf8 experiments/check_c_closeout.py
python -X utf8 experiments/check_c_supplement.py
```

命令在仓库根目录执行，不加载模型。完整生成命令应使用对应运行目录内保存的配置和来源，而不是用当前默认值覆盖旧配置。

## 环境记录

现有runtime_versions.json是实际开发版本记录，不是已验证的通用安装方案。本补充提供同一版本的requirements观察清单供D核对；含CUDA的torch版本应使用相应官方安装源并匹配目标机器。本轮未重装环境，未声称已在另一台机器完成模型批量独立复现。新环境验证记录仍待实际执行。
''')
    runtime=load('docs/c_work/runtime_versions.json')
    write('requirements-c-observed.txt','# Observed development versions, not a tested portable lockfile.\n# Python '+runtime['python']+'; CUDA/torch installation needs matching hardware and package index.\n'+'\n'.join(f'{k}=={v}' for k,v in runtime['packages'].items())+'\n')
    support=load('docs/c_work/retrieval_support_30_v1.json')
    write('slide_data.json',{'date':research['date'],'dataset_items':125,'uncertainty_probes':22,'unresolved_ids':[33,34,37,41,42],
                            'knowledge_sources':len(corpus['sources']),'knowledge_chunks':len(corpus['chunks']),
                            'retrieval_support_counts':support['counts'],'inventory':load('docs/c_work/c_work_inventory.json')['totals'],
                            'anchor_regression':{'questions':125,'removed_false_retrievals':15,'remaining_unchanged':110},
                            'A_input_items':48,'A_items_with_hits':0,'independent_human_reviews':0,'formal_accuracy':None})
    write('README.md','''# C分工缺口补充交付

本轮补齐原分工清单中C能独立准备的材料，旧题集、知识库、原始回答、历史审计和运行不改。

- [来源日期台账](SOURCE_DATES.md)：21源逐项记录，16条未知精确首次发表时间的来源均保留原因，不将更新日当发表日。
- [知识过时分析](TEMPORAL_ANALYSIS.md)：4条完整回答边界案例、日期口径、原文和哈希。
- [方法引文映射](METHOD_REFERENCES.md)及[使用说明](USAGE.md)：方法原文、实现差异、来源引用及未知权利边界。
- [知识更新复现问答](REPRODUCTION.md)：三类答辩问答、版本更新顺序及实际环境边界。
- [C到A证据交接](A_HANDOFF.md)：48条真实无命中导出，4条UID映射及明确标识的接口夹具检查；模型调用0。
- [C研究页](C_research_v1.pptx)：仅C部分的可编辑开发结果研究页；不替代整组正式结论或D的组装。

校验入口为check_c_supplement.py。正式冻结、独立真人复核、共同环境复现、学校要求确认和共同彩排仍以实际完成记录为准。
''')
    print(json.dumps({'sources':len(date_rows),'temporal_cases':len(temporal),'reference_entries':len(source_maps),'A_exports':len(exported),'model_calls':0},ensure_ascii=False))


if __name__=='__main__':
    build()
