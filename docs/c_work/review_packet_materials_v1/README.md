# 本轮材料复核填写说明

本包为C、D各96项空白表，抽取完整2/8主题组，保留三种结论、两种材料位置、四种生成条件及中英文标签。当前人工复核完成数为0；模板不是评分成果。

先阅读上级REVIEW_PROTOCOL.md及C_REVIEW_WORKFLOW.md，再各自阅读items.md、填写CSV。不要先看balanced_checks或对比报告中的自动标签。对任务完成度、格式、实际证据支持和附加解释分开判断；没有填对字段不代表所有事实错误，填对结论也不代表依据正确。source_ids可使用题目材料对应的已登记来源ID；原始来源汇总在datasets/controls/c_balanced_material_specs.json及source_followup_v1/report.md。

另存completed_materials_C.csv、completed_materials_D.csv后，在仓库根目录执行：

```powershell
python -m experiments.import_c_annotations completed_materials_C.csv --mapping docs/c_work/review_packet_materials_v1_mapping.json --reviewer-id actual_C --reviewer-type human --output docs/c_work/reviews/materials_C_v1.json
python -m experiments.import_c_annotations completed_materials_D.csv --mapping docs/c_work/review_packet_materials_v1_mapping.json --reviewer-id actual_D --reviewer-type human --output docs/c_work/reviews/materials_D_v1.json
python -m experiments.reconcile_c_reviews docs/c_work/reviews/materials_C_v1.json docs/c_work/reviews/materials_D_v1.json --output docs/c_work/reconciliation_materials_round1
```

身份使用真实负责者的稳定ID，不用同一人充当两人。不把裁决后意见算作第三份独立意见。措辞与输出语言可能暴露条件，不能宣称完全盲化；分组抽样仅供开发质量复核。

对本题给定M1/M2及任务规则，可直接用task:materials_v1:复核编号引用，例如task:materials_v1:RB0001。它指向该复核项问题中的材料和要求，已登记为可用来源，不需要打开隐藏映射。给定材料不足的问题不能用材料外知识补为supported；另查网页只用于确认整理资料本身，不改变本任务的材料范围。
