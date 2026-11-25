# 均衡材料诊断、位置交换与标签措辞对照

本批完成两轮共384条真实模型生成：英文标签192条；观察到英文输出偏向后，另做中文标签探索性对照192条。两轮使用相同8个主题、24条陈述，每条陈述交换两段材料的位置，形成48个问题变体。支持、反驳、证据不足各16题，依据M1、M2、none也各16题。不是384道独立事实题。

直接查看[中英文成对比较](material_label_comparison.md)、[英文混淆矩阵及明细](runs/balanced_materials_v1/report.md)、[中文混淆矩阵及明细](runs/balanced_labels_cn_v1/report.md)。本轮评分是冻结材料任务的自动规则检查，独立人工评分仍为0。

## 这次补齐了什么

原五题几乎都要求判断资料不足，不能检查模型是否只会选择单一标签。本轮将三类平衡，加入明确相反事实，并单独检查模型选择的证据编号。人员记录的陈述明确写出姓名或机构，避免这位人员、同名等指代不清。

给定名单题只对本题提供的名单作有限判断，目录未列某学院不推断学校没有相关研究。出生年份或物理量即便在现实中为已知事实，若M1/M2未提供证据，本任务仍为不足。所有材料均注明整理记录范围，原始来源ID保存在规格与数据元信息中。

运行时显式设置question_only，外部检索返回资料数为0。legacy保留原combined提示模板，compact保留短提示模板；同题普通和约束解码的提示相同。正常任务下guarded与compact提示相同，本轮没有重复运行。有限JSON约束保留全部9种结论与依据组合，评分答案不进入生成。

## 实际结果

下表内容判断允许读取完整JSON或完整代码围栏内对象，但只认字段的指定值；格式、额外键、依据附带正文等问题另列。无法解析的输出不靠关键词猜测标签。

| 条件 | 英文结论符合/48 | 中文结论符合/48 | 英文结论与依据均符合/48 | 中文结论与依据均符合/48 |
| --- | ---: | ---: | ---: | ---: |
| legacy 普通 | 14 | 25 | 11 | 1 |
| legacy JSON约束 | 16 | 16 | 14 | 14 |
| compact 普通 | 17 | 34 | 9 | 4 |
| compact JSON约束 | 16 | 20 | 10 | 13 |

英文条件均没有输出合法的refuted标签；legacy JSON条件48题全选supported。三类均衡时总选一个类别也只有16/48，不能把这种偏向误当作判断可靠。中文compact普通生成的结论符合数较高，但有10/16条应反驳的陈述被判为不足，依据字段也频繁写成自由文字，所以联合符合数只有4/48。

两轮受约束条件的结构均为48/48合格，内容仍有错误。把结构强制合格直接等同于事实能力提高不成立。中文标签对普通生成有明显影响，但该追加是探索性的，改变了token和语言先验，不能据此确认模型内部机制；当前仍保留默认治理方案。

## 材料位置不是字符串不变测试

24条陈述各有两个材料位置版本：结论应保持一致，正确依据M1/M2应相应交换。不足项仍应给none。报告同时保留有效判定覆盖率、编号跟随和两个位置都同时正确，不能只以输出稳定来选方案。

| 条件 | 英文两位置都同时符合/24 | 中文两位置都同时符合/24 | 中文有证据时编号跟随/16 |
| --- | ---: | ---: | ---: |
| legacy 普通 | 4 | 0 | 0 |
| legacy JSON约束 | 6 | 6 | 9 |
| compact 普通 | 2 | 0 | 0 |
| compact JSON约束 | 2 | 5 | 10 |

一直输出supported可以在位置交换下100%稳定，却不能正确区分反驳与不足。依据写成M1加正文可能涉及字段规范问题，不能将所有编号未通过项直接判为事实编造。[案例说明](C_MATERIAL_CASES.md)区分了这两种失败。

## 预先计划与探索性追加

[英文评分计划](balanced_protocol_v1.json)及输入哈希在英文生成前保存；[中文追加计划](balanced_label_followup_v1.json)明确记录触发原因，并在中文生成前冻结。两轮材料、陈述、顺序、模型文件、运行源码、种子和生成预算均经成对核验，仅翻译指令和枚举标签。没有把后追加分析冒充原预先计划。

相关单位是8个主题组，不按48题独立假设计算显著性。材料与判定规则由开发流程整理，尚未完成独立真值与题意复核；这些记录不改变原22条实体探针的真值，不替换正式测试，不改变RAG知识库。

## 复现与真人复核

```powershell
python -m experiments.run_c_structured_comparison --config configs/c_balanced_materials.json --output docs/c_work/runs/my_balanced_en
python -m experiments.report_c_balanced_materials docs/c_work/runs/my_balanced_en
python -m experiments.run_c_structured_comparison --config configs/c_balanced_materials_cn.json --output docs/c_work/runs/my_balanced_zh
python -m experiments.report_c_balanced_materials docs/c_work/runs/my_balanced_zh
python -m experiments.check_c_delivery --run-tests
```

每次使用新目录，输入或代码变化后不恢复旧合同；历史运行保留了源码快照。比较固定两轮的compare_c_material_labels核对原始输出哈希与生成配置，不用于把旧评分套给新问题。模型权重仍由已有本地环境提供，交接包不分发。

本轮另备[每人96项独立复核材料](review_packet_materials_v1/README.md)，按完整2/8主题组抽取，保留全部类别、位置、条件和语言。两份表保持空白，映射绑定原问题与回答哈希，可用既有导入与裁决流程处理。原192项复核包保留，未被本轮材料覆盖或填充。
