# LLM Governance

2026-11-25补齐：[C分工缺口补充材料](docs/c_work/closeout_supplement_20261125_v1/README.md)，含日期、时间故障、引文/使用说明、复现问答、5页可编辑研究页及A真实证据导出；正式冻结与独立复核仍待完成。

2026-11-25新增：[25条C侧辅助试标与证据](docs/c_work/pilot_C_ai_v1/README.md)，含CSV/Excel、原表快照和校验；为AI预标注，待C/D统一口径并独立人工复核。

C开发交付收尾与核验入口：[C_CLOSEOUT](docs/c_work/C_CLOSEOUT.md)。

继续工作先读：[C进度文件](C_PROGRESS.md)，包含任务范围、当前进度、未完成项和下一步顺序。

当前只推进C分工。先看[已完成内容总览](docs/c_work/C_HANDOFF.md)：按C1—C4整理成果、实验数量、有效改进、失败和待办；职责边界见[C自己的交付状态](docs/c_work/C_ONLY_STATUS.md)。下文联合入口等属于保留的历史开发材料。

针对上一轮正常任务退化，已完成[24题、48条路由对照](docs/c_work/runs/normal_route_v1/report.md)：差异题为JSON代码围栏，非拒答；扩大到10项封闭检查后两条路由均为5/10，未自动改默认方案。

最新一批：[可配置联合批量工具与一致性v2](docs/c_work/C_INTEGRATION_BATCH.md)，24案例四条件96条实机输出，支持快照、恢复和显式重试；材料同步进入实际提示与审计。结果包含82条模型生成、14条程序拒答，不作为偏见成效或E3验收证明。

新增[证据一致性与联合入口](docs/c_work/C_JOINT_INTEGRATION.md)：989条历史输出只读筛查、6条实机调用，支持偏见提示开关及外部hook，保留原回答和审计日志。当前是集成原型，未验证偏见治理或语义支持效果。

本项目研究大语言模型偏见与幻觉的评估及治理。现有仓库包含偏见数据、中文测试集、幻觉题集、原始模型调用，以及C方向的资料检索与抗幻开发实验。

查看C方向成果从[交接说明](docs/c_work/C_HANDOFF.md)开始；方法与边界见[实验协议](docs/c_work/C_METHODS.md)。旧阶段材料和历史回答保持原样。

## C 方向运行

在仓库根目录使用已配置的llm-governance环境，并将Qwen2.5-0.5B-Instruct权重放在models/Qwen2.5-0.5B-Instruct。交接包不包含模型权重。

```powershell
conda activate llm-governance
python -m unittest discover -s tests -v
python -m experiments.audit_hallucination
python -m experiments.build_c_knowledge
python -m experiments.prepare_c_development
python -m experiments.check_c_retrieval
python -m experiments.run_c_suite --config configs/c_expanded.json --output docs/c_work/runs/my_expanded_run
python -m experiments.report_c_suite docs/c_work/runs/my_expanded_run
python -m experiments.run_c_suite --config configs/c_controls.json --output docs/c_work/runs/my_control_run
python -m experiments.report_c_suite docs/c_work/runs/my_control_run
```

运行输出目录必须使用新名称。中断后保持配置、输入、代码和模型文件不变，可恢复：

```powershell
python -m experiments.run_c_suite --output docs/c_work/runs/my_expanded_run --resume
```

若要重试已记录失败的条目，另加--retry-errors。若原运行使用--dry-run，恢复时也必须加该选项。具体环境版本和模型校验值保存在交接资料及各运行目录中。

## 候选策略与评分

新增三策略开发比较包含120条输出（115条模型生成、5条程序拒答），见[比较报告](docs/c_work/runs/policy_comparison_v1/report.md)。结果有改善也有退化，默认治理实现保持原方案。

```powershell
python -m experiments.run_c_policy_comparison --config configs/c_policy_comparison.json --output docs/c_work/runs/my_policy_run
python -m experiments.report_c_policy_comparison docs/c_work/runs/my_policy_run
python -m experiments.verify_c_policy_comparison
```

verify_c_policy_comparison校验已保存的policy_comparison_v1。report_c_policy_comparison支持指定运行目录；新运行仅生成其运行统计，不沿用历史AI案例判断。六题封闭输出检查要求题号及冻结问题正文与原任务一致。

[评分协议](docs/c_work/REVIEW_PROTOCOL.md)区分事实错误、无依据断言、拒答和任务完成度；[独立复核材料](docs/c_work/review_packet_v1/README.md)为每人192条空白项。目前84条评分记录均为AI开发复核，独立人工评分为0，正式正确率与一致性不作填充。

两人填写后可按[复核与裁决流程](docs/c_work/C_REVIEW_WORKFLOW.md)合并一致项、处理分歧并形成最终标签。七维一致性保留裁决前结果，单人记录和未裁决项不会混入最终评分。

```powershell
python -m experiments.check_c_delivery --run-tests
```

此命令统一检查已交付的开发实验、独立演示与评分边界，不生成新模型回答；结果见[交付检查](docs/c_work/delivery_check.json)。

## 问答演示与接入

```powershell
python -m experiments.demo_c_governance --question "声音能在真空中传播吗？请说明原因。" --category factual --output docs/c_work/runs/my_single_demo
python -m experiments.demo_c_governance --input configs/c_demo_questions.json --strategies combined compact guarded --output docs/c_work/runs/my_demo
```

加--prepare-only可仅检查提示和检索，不加载模型。每次使用新目录，恢复时重复原命令加--resume。详见[演示与接入说明](docs/c_work/C_DEMO.md)、[实机问答](docs/c_work/runs/demo_v1/transcript.md)和[答辩讲述稿](docs/c_work/C_DEFENSE_NOTES.md)。演示结果单列，不作为独立测试成绩。

## 来源补查与材料任务

[17题补查](docs/c_work/source_followup_v1/report.md)提供4条新增参考修订、8条有限背景及5条仍缺具体来源的记录，保留首轮输入及历史结果。[五道给定材料诊断](docs/c_work/C_SOURCE_BOUND.md)已生成三策略15条模型回答，单列格式与字段检查，未给原实体题补真值。

```powershell
python -m experiments.run_c_policy_comparison --config configs/c_source_bound.json --output docs/c_work/runs/my_source_bound
python -m experiments.check_c_source_bound docs/c_work/runs/my_source_bound
```

[有限JSON输出约束](docs/c_work/C_STRUCTURED_OUTPUT.md)已完成30条普通/约束生成对照。受约束15条全部满足字段结构，但完整任务仍有内容错误；格式与材料判断分别报告，默认方案保留。

```powershell
python -m experiments.run_c_structured_comparison --output docs/c_work/runs/my_structured
python -m experiments.report_c_structured docs/c_work/runs/my_structured
```

新增[均衡材料判断与标签措辞诊断](docs/c_work/C_MATERIAL_DIAGNOSTICS.md)：8个相关主题、24条陈述、48个位置变体，两轮共384条模型生成。结论、实际依据、格式、位置交换和标签语言分别分析；[混淆矩阵与中英文比较](docs/c_work/material_label_comparison.md)保留全部负面结果，未作为独立测试。另有[每人96项空白复核表](docs/c_work/review_packet_materials_v1/README.md)。
