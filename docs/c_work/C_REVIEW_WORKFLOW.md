# 独立复核、分歧裁决与最终标签

当前已准备[每人192项材料](review_packet_v1/README.md)，[评分协议](REVIEW_PROTOCOL.md)规定七个维度。真实人工复核仍为0。现有84条AI开发复核仅用于开发分析；[实际流程状态](reconciliation_status_v1/report.md)验证了这些AI记录不会生成双人一致性或最终人工评分。

## 两人独立填写与导入

C、D分别填写自己的CSV，先不查看另一位或AI的标签；保留空白原表，把完成文件另存为completed_C.csv和completed_D.csv。在仓库根目录执行：

```powershell
python -m experiments.import_c_annotations completed_C.csv --reviewer-id reviewer_C --reviewer-type human --output docs/c_work/reviews/human_C_v1.json
python -m experiments.import_c_annotations completed_D.csv --reviewer-id reviewer_D --reviewer-type human --output docs/c_work/reviews/human_D_v1.json
python -m experiments.reconcile_c_reviews docs/c_work/reviews/human_C_v1.json docs/c_work/reviews/human_D_v1.json --output docs/c_work/reconciliation_round1
```

请把reviewer_C、reviewer_D替换为稳定的真实标注身份。工具只核对身份声明与格式，不能认证真人身份或保证两人确实独立。不同人不能共用一个ID；同一人的重复记录不能当作第二人。

输出review_state.json保存全部原意见及状态，report.md提供问题、回答、意见和模型所见证据；adjudication_blank.csv只列尚未裁决的分歧。输入文件与运行代码均保留快照及哈希。

## 一致项与分歧项如何处理

同一运行、题号、模式、回答哈希下，必须有两位不同human标注者。七个标签全部相同，自动形成一条two_human_consensus；两份来源与理由均保留，模型回答分母只计一次。来源选择或理由措辞不同，不单独算标签分歧。

只要事实错误、证据使用等任一标签不同，即使核心正确标签相同，也进入裁决。一人已填另一人未填的项保持single_review，不用AI补齐。当前协议要求每项两位标注者，多于两位会提示使用明确的双人输入版本。

最终标签写在resolved_records中，采用resolution_origin、reviewer_ids及可选adjudicator_id记录来源，不伪装成某位新增独立标注者的原始判断。

## 人工裁决

另存adjudication_blank.csv为adjudication_completed.csv，依据原问题、完整回答和可靠来源，为每条分歧填写全部七个标签、source_ids和rationale。可由指定裁决者复核，也可在独立提交完成后共同讨论，由真实负责者签署；讨论后的裁决不能算作第三份独立意见。

保留resolution_id、review_group_sha256原样。原始意见、理由或证据记录有变化时，应重新生成裁决表，旧表不能继续套用。

```powershell
python -m experiments.reconcile_c_reviews docs/c_work/reviews/human_C_v1.json docs/c_work/reviews/human_D_v1.json --decisions adjudication_completed.csv --adjudicator-id actual_adjudicator --output docs/c_work/reconciliation_final1
```

每次使用新输出目录，旧原件与裁决保留。未知实体的真值仍受原始数据用途约束，不能通过裁决强行判成存在或不存在。程序模板拒答不能被改标为模型实质回答。裁决须记录证据；裁决者身份不能留空。

## 一致性与统计口径

一致性使用裁决前的两份原标签，分别计算核心正确、事实错误、无依据断言、前提处理、拒答、回答类型、证据使用。不同标注者配对分开报告，不混为同一个Cohen kappa。核心正确的一致性排除unverifiable和not_applicable；其他维度将其允许的标签作为分类水平，因此各维度分母可能不同。

若两人的标签都为同一类别，期望一致率为1，kappa不可定义，保持null，同时给出实际一致的条数与分母。无双人记录时保持unavailable；不能用AI或裁决后的结果填充高一致性。

tables仅描述已经由双人一致或人工裁决形成最终标签的回答。单人项、未裁决项另列，覆盖率为resolved_fraction_of_human_reviewed_answers；该覆盖率只相对已有人工意见的回答，不代表全部192项或整个实验已经完成。resolved_reviewed_subset表示已有复核子集处理完毕，不表示正式测试或验收完成。

原evaluate_c_reviews仍提供原意见的保守汇总；发现同题多份意见时留空评分表并要求裁决。完成裁决后的统计应读取本流程review_state.json中的report.tables，不把最终标签重新导入为第三人的独立意见。

## 一次检查当前交付

```powershell
python -m experiments.check_c_delivery --run-tests
```

该命令运行测试、核对三轮开发输出与单独演示、核对独立复核材料及AI排除状态，生成delivery_check.json；不运行新模型生成。当前检查针对已交付的固定开发工件，人工复核后的新目录需要单独运行上述裁决流程。
