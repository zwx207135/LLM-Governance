# 独立复核填写说明

先阅读上级目录的REVIEW_PROTOCOL.md，再分别打开items.md和自己的空白CSV。source_ids使用来源登记ID、math:样本ID或正常任务的task:Nxx，多个ID用分号隔开；每条填写理由。材料标明回答来自模型还是程序模板，该信息可能部分暴露策略。

不要复制另一人的标签或AI开发者判断。填完后用import_c_annotations导入，再用evaluate_c_reviews比较；分歧在裁决前保留。映射文件在本目录之外，不需要提前打开。模板数量不表示已完成标注。

每人192项：原开发实验116项、正常任务16项、新策略比较60项。原两轮均至少覆盖20%题组；争议题另行加入。这是质量复核材料，不能直接作为总体效果估计。当前独立人工复核完成数为0。

另存为自己的completed_C.csv、completed_D.csv，填完后在仓库根目录执行（将身份替换为真实标注者）：

```powershell
python -m experiments.import_c_annotations completed_C.csv --reviewer-id reviewer_C --reviewer-type human --output docs/c_work/reviews/human_C_v1.json
python -m experiments.import_c_annotations completed_D.csv --reviewer-id reviewer_D --reviewer-type human --output docs/c_work/reviews/human_D_v1.json
python -m experiments.evaluate_c_reviews docs/c_work/reviews/human_C_v1.json docs/c_work/reviews/human_D_v1.json --output docs/c_work/reviews/human_agreement_v1.json
```

导入拒绝全空表、未完成的单条记录和与原回答不符的哈希。身份由提交者声明，工具不认证其真实身份。两人意见会保留，一致性按同一对标注者计算；存在重复评分时先报告需要裁决，不合并为重复模型样本。

两份原意见导入后，使用[双人一致与分歧裁决流程](../C_REVIEW_WORKFLOW.md)形成最终标签。七个标签均一致的项可自动合并，其他项人工裁决；原意见和裁决前一致性全部保留。

原始材料与空白表未改写。实体题可结合[新增来源补查](../source_followup_v1/report.md)核验具体陈述，sf_来源ID可用于source_ids；这些证据不建立题设身份真值，unknown探针的标签边界仍按REVIEW_PROTOCOL执行。新增五道材料诊断没有混入本192项复核包。
