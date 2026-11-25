# C 分工实施与交接说明

当前交付包含125条幻觉数据的核查台账、带来源的小型中文知识库、中文BM25检索、抗幻回答约束，以及四种配置的开发实验入口。原始题集与历史模型回答保留。当前是开发阶段，正式测试需要先完成来源复核和数据划分。

当前完整入口为[C分工成果与交接](C_HANDOFF.md)，方法与复现协议见[C_METHODS.md](C_METHODS.md)。本批87题四组对照加20条正常任务共428条真实回答全部完成。

## 文件与成果

| 文件 | 用途 |
| --- | --- |
| `data_audit.json` | 125条原始记录、核验状态、证据、修订建议和统计 |
| `data_review.csv` | 可用Excel打开的逐题核验表，保留二次复核栏 |
| `source_registry.json` | 67个具体来源及77条新增来源核验记录 |
| `source_audit_report.md` | 核验状态统计与剩余问题清单 |
| `reviewed_candidate.json` | 待C与D复核的题集候选副本，尚未冻结 |
| `data_change_proposals.json` | 逐字段原值、建议值及修改理由 |
| `../../knowledge/corpus.json` | 5个官方来源、7个中文转述片段和短原文摘录 |
| `../../knowledge/corpus_v3.json` | 当前v3.1语料，16个来源、25个主题片段 |
| `../../knowledge/source_documents.json` | 可重建的中文主题资料与来源定位 |
| `../../src/governance/retrieval.py` | 无额外依赖的中文二元字符BM25检索 |
| `../../src/governance/anti_hallucination.py` | 独立的抗幻提示与证据注入接口 |
| `../../configs/c_hallucination.json` | 开发题ID、检索参数、生成设置及四组配置 |
| `runs/smoke_v2/report.md` | 当前版本真实模型的40条开发回答与证据 |
| `runs/smoke_v2/review.csv` | 交给D独立评分的空白记录表 |
| `development_findings.md` | 改善、无证据生成、未遵循证据及无效回答案例 |
| `runs/expanded_v3/report.md` | 87题、348条真实模型回答与分题型复核表 |
| `runs/controls_v3/report.md` | 20条正常任务、80条真实模型回答 |
| `expanded_case_studies.md` | 扩大实验中的改善与失败案例 |
| `DATA_DECISIONS.md` | 22条不确定性探针逐条使用边界 |

当前检查结果见test_results.json，涵盖来源有效性、状态分离、日期冻结、人工备注保留、原始数据不变、断点恢复、配对统计与交接包验证。smoke_v2的40条回答是早期开发记录；expanded_v3及controls_v3为扩大实验，全部仍待独立评分。

## 数据核查结果

结构检查覆盖125条，五类各25条，未发现重复ID或完全重复问题。100条非数学题的原始来源字段均没有直接URL；具体链接、定位、访问方式和证据集中补充在来源登记表及核查台账，原字段保留。来源名称本身不能视为核验通过。

当前72条核心答案有来源支持，22条数学逻辑已记录独立推导，10条发现参考或题意问题，4条证据范围有限，17条仍待来源核验。修订提案另外统计，共19条，包括日期冻结、判定边界及答案修正；有提案不代表来源已核验。全部记录仍需第二人复核，不能把这一轮整理等同于完整参考答案认证。

第25和94题不宜将电灯归为单一发明者；[美国能源部电灯史](https://www.energy.gov/articles/history-light-bulb)介绍了多人持续改进及爱迪生的实用化、商业化贡献。第111题的“144的平方根”应为12与-12；若保留答案12，应改问算术平方根。第107和117题应明确数列延续规则。第63题需要区分中美金牌数同为40枚与金银铜排序的美国榜首；第32题的公司不存在断言与北交所星辰科技证券名录冲突。所有建议独立保存，未改写原始题集。

25条虚构实体题需要核对具体主张，24条原参考含“不存在”的宽泛断言。查不到某个人的奖项或某个产品，不能推出同名人物、公司或作品本身不存在。现任职务、院系和产品等应补截至日期；历史赛事、奖项应记录事件年份与核验日期。

具体来源中direct_body表示读取原站正文，indexed_body表示查阅搜索服务返回的官方来源索引正文。原站403或超时不直接记为核验通过；索引资料也可能较旧，需要记录内容适用日期。所查特斯拉清单来自2025年度报告，不能拿它证明2026年或未来不会发布新车型。

重跑audit命令会保留data_review.csv中的reviewer、second_reviewer、human_decision、human_notes四个手工栏。其余栏由程序生成，修改事实应更新source_registry.json或提案。候选副本和人工裁决均不会自动写入正式测试集。

## 知识库来源和边界

知识库从NASA月球、行星、太阳、地球、波与相对论科普，NOAA海洋资料，Smithsonian科技史及公开科学数据中整理。每个来源保留URL、采集日期与原文定位，中文片段为查阅页面后的人工转述，不是完整网页归档。无法确认的发布日期为null，不能以采集日期代替。

知识库构建流程为选源、核验、中文转述、按主题分段、写入唯一片段ID，再由LocalRetriever建立内存词频及文档频率索引。每次运行固定复制所用语料，保存SHA256。当前25段由人工分段，后续扩库需保留相同来源字段，并增加第二人对照原文的记录。

知识入库不读取题集、参考答案或人工评分理由。当前资料选题已参考现有任务范围，与测试题主题重叠，因此本次只标为开发验证；不能据此声称完成无泄漏的独立测试。由B按近似题和主题分组划分，冻结独立测试与知识库后，再进行正式实验。

检索先要求命中资料片段的人工主题词，再用BM25排序，防止只因“贡献”“最大”等通用词召回无关资料。主题词由资料内容提取，扩库时需同步维护。检索分数只表示词面相关性，不表示证据支持结论；相关片段可能遗漏关键事实。检索器不作蕴含判定、不自动判定题设正确、不按未命中断言不存在。中文二元字符检索无法处理所有同义词，主题过滤也会漏掉同义表达，首版重在可检查与可离线运行。

## 运行方法

在仓库根目录运行，使用已有的llm-governance环境。无需安装新包或访问网络。

```powershell
conda activate llm-governance
python -m unittest discover -s tests -v
python -m experiments.audit_hallucination
python -m experiments.build_c_knowledge
python -m experiments.prepare_c_development
python -m experiments.check_c_retrieval
python -m experiments.run_c_suite --config configs/c_expanded.json --output docs/c_work/runs/new_model_run
python -m experiments.report_c_suite docs/c_work/runs/new_model_run
python -m experiments.run_c_suite --config configs/c_controls.json --output docs/c_work/runs/new_controls
python -m experiments.report_c_suite docs/c_work/runs/new_controls
python -m experiments.check_c_controls docs/c_work/runs/new_controls
```

每个新实验使用新目录。run_c_suite支持按行落盘、错误记录、断点恢复及显式重试；恢复时验证数据、语料、代码及模型校验值。输入变化需要新建目录。早期run_c_governance仍保留作历史入口，不支持恢复。权重不随发布包分发，复现需要相同模型。

四组为baseline、constraint、retrieval、combined，使用同一模型、关闭采样、固定种子。早期smoke最多160个新token，本次扩大实验最多192个，baseline重新生成，不能与旧采样结果混用。GPU计时同步，加载与预热分开；相同种子仍不保证跨硬件、跨软件版本逐token相同。

## 接口交接

```python
from src.governance.retrieval import LocalRetriever
from src.governance.anti_hallucination import AntiHallucination

governance = AntiHallucination(LocalRetriever("knowledge/corpus_v3.json"))
prepared = governance.prepare("太阳是什么？", mode="combined", category="factual")
answer = model.generate(prepared["prompt"], max_new_tokens=160, do_sample=False)
```

A可复用prepare返回的prompt、evidence、retrieval_status接入联合治理；D可调用独立入口并读取records.jsonl。接口只接收问题、模式和任务类别，不接收reference。数学类别跳过检索，保留回答约束。自由输入未提供类别时会正常检索，调用者需要明确任务类型。

四组对照是C的开发消融，不是整个项目的E0到E3：项目E1偏见治理与E3联合治理仍由A完成。

## 下一阶段

C与D逐条确认19条修订提案，并决定22条不确定性探针后续是否改为有明确材料的题型。B负责正式划分和近似题检查，D冻结完整回答评分规范。已有30条开发检索诊断仍需第二人复核相关性和支持程度，再开展冻结测试。新增答案核验资料不自动导入RAG。

当前review.csv的正确性、错误事实、错误前提、引用、拒答、证据相关性和支持程度均留空，交D独立判断。应复核完整回答，包含正确词语不能视为没有幻觉。拒答应区分合理、不合理与未拒答；截断回答单独报告。尚无人工评分，不报告正确率或幻觉降低幅度。

新增阶段已提供[评分规范](REVIEW_PROTOCOL.md)、84条明确标为AI开发复核的记录，以及[每人192项的独立复核材料](review_packet_v1/README.md)。AI复核未填入旧review.csv的人工栏。三策略120条比较见[报告](runs/policy_comparison_v1/report.md)，其中5条为程序模板；尚无统一胜出的策略，默认方案保留。当前总览以[C_HANDOFF.md](C_HANDOFF.md)为准。
