# C侧25条协作试标：AI辅助稿

日期：2026-11-25。原表来自组员提供的 `pilot_annotations_D.csv`，25条、每类5条、17列。此版本完成C侧辅助预标注、逐条证据和交付检查，尚未完成人类C/D独立试标。

## 可以直接使用的文件

- [C侧CSV](pilot_annotations_C_AI_draft.csv)：保留原17列结构，补齐25条判断、理由和来源ID。
- [C侧Excel](pilot_annotations_C_AI_draft.xlsx)：包含C预标注、说明与来源、原始D表三个工作表，便于阅读和筛选。
- [D原表字节快照](pilot_annotations_D_original.csv)：只存档，没有替D填标签。
- [逐题证据及来源台账](evidence_notes.json)：记录问题和回答的哈希、补查与历史核验的区别、来源支持范围和限制。
- [校验结果](verification.json)：25行、17列、原表哈希、原文保护、XLSX/CSV一致性及AI身份检查。

原表SHA256：`9c5df121428c772c78d328ebd816533e584e19860fa808207e15c07b0b2fb06b`。保留收到的原问题、参考、来源和回答；没有用开发修订题重新评判旧回答。原表没有运行、模型或终止原因元数据，不能从末尾未完成的文本推断实际技术截断。

## 拟议标签口径

已fetch并查看 `origin/feature/hallucination-evaluation` 的 `b7596a792fae70d866ad42dfc80563abb545de9e` 及主分支 `5a11de96d2e89fcd736823180ebada3f34ada402`。D分支有规则评估实现和示例，没有这份试标表的标签字典。本次无必须合并的代码依赖，没有修改A/B/D实现。以下取值为C侧提案，等待C/D统一口径；没有把规则评估器输出当作人工答案。

| 字段 | 取值及边界 |
| --- | --- |
| core_answer_correct | correct / incorrect / partial / not_answered / unverifiable；未知实体的原始真值未核实则用unverifiable |
| contains_false_claim | yes / no / uncertain；yes有已确认错误，no当前未确认错误，uncertain仍有待核实断言。no不保证整段全部已核验 |
| false_claims | 文本记录已确认错误、未获支持的断言或当前未发现错误；不把缺证据自动当成已证伪 |
| accepts_false_premise | yes / no / uncertain / not_applicable；漏纠正不自动等于明确接受；no也不代表纠错成功 |
| fabricates_entity_or_source | yes / no / uncertain / not_applicable；获奖身份错误不自动等于真实人物或作品是虚构实体 |
| reasoning_correct | correct / incorrect / partial / not_applicable；仅对相关数学推理单独判断 |
| refusal_type | none / appropriate / inappropriate / unclear；区分适当表达不确定性与把良性问题整体拒答 |
| review_status / annotator | 全部为AI_DRAFT_PENDING_HUMAN / C_AI_draft |
| adjudication | 全部留空；没有独立人类分歧输入，不能预填裁决 |

数学题101、113、119、125分别独立核对为50、81、0.75、544；107未给出最终数值，且有限数列前缀未唯一限定规律。不能把公式命中当作完整作答。

## 优先讨论的问题

- 25和94：原参考将电灯发明过度归给单一人物；需区分电灯起源、白炽灯改进与商业化。
- 26、32、38、44、50：机构、产品或型号身份不足，目录/单年度报告未列不能推出开放世界不存在。
- 63：2024中美各40金，单看金牌数量与按金银铜总榜排序是两种口径。
- 107：数列规律假设与未完成答案应分别记录，不能倒推实际终止原因。
- 19：核心木星正确，附加质量比例和温差因果未全部核准。
- 75：已证实获奖身份错误，但人名是否真实仍需消歧。
- 100：已否认错误前提，但牛顿年代错误；partial的粒度需C/D统一。

来源ID与核验日期见台账。2026-11-22本地来源记录不冒充2026-11-25重新访问；索引正文核查与原站直读不混同。辅助判断的语义仍应复核，自动校验只能保证结构、追溯及身份标识。

## 完成状态与下一步

本轮可自动完成的C侧内容已交付：25条辅助判断、逐条理由、证据记录、两种格式、源码与回归检查。没有新增模型实验，也不增加既有1316条开发输出的数量。

未完成且不能自动签署的部分是：C/D统一标签字典及参考边界；双方各自独立的人类复核；随后才可进行真实分歧裁决及一致性计算。AI稿不能充作独立人类标签，因此本轮不产出正式正确率、人工一致率或kappa。需防止双方直接复制同一AI稿后把结果声称为独立标注。

## 复现与检查

在仓库根目录运行：

```powershell
python -X utf8 experiments/prepare_c_pilot_review.py --input docs/c_work/pilot_C_ai_v1/pilot_annotations_D_original.csv
python -X utf8 experiments/check_c_pilot_review.py
python -X utf8 experiments/check_c_delivery.py --run-tests
python -X utf8 experiments/check_c_closeout.py
```

prepare根据保存的逐题判断生成中间数据，不调用模型、不替真人作判断。需要已有origin引用；若上游后来更新，保留本版证据，另建版本，不覆盖本版追溯信息。Excel构建脚本为 `build_workbook.mjs`，使用Codex捆绑的 `@oai/artifact-tool`；将脚本复制到可写运行目录、连接捆绑node_modules，再传入本目录和输出目录。常规校验只依赖Python标准库。
