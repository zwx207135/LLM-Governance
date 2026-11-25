# 本轮来源补查与给定材料诊断

本轮完成首轮17条待充分核验实体题的逐题补查，记录14个来源条目，形成4条新增参考修订、8条有限背景和5条仍缺具体来源的记录。详见[补查报告](source_followup_v1/report.md)、[4条逐字段提案](source_followup_v1/reference_proposals.json)与[后续动作表](source_followup_v1/actions.csv)。这是AI开发者查阅资料后的记录，独立人工复核仍为0。

## 证据带来的变化

第28、29、48题出现同名科研人员的官网记录，原参考直接否定人物存在会误伤真人；这些人员页并不建立题设的相对论贡献或诺贝尔获奖身份。第40题原参考仅有SU7及衍生款的背景与小米官方YU7资料不符，但YU7参数不能用于回答SU9。每条来源的页面定位、实际访问方式、支持内容与不支持范围均已登记。

原题集、首轮data_audit、source_registry、候选副本、开发副本、data_usage和RAG语料均保持原校验值。补查作为独立版本附加，不把原17条自动变为已核实，不给22条不确定性探针补上开放世界真值。新4条提案与原19题提案分开保存，待真实第二人确认。

8条有限背景包括目录、近似奖名、已知产品、真实机构或人员简历。目录未列某名称不等于相关研究不存在；環宇与寰宇以及带前缀名称不能自动合并；ACM Fellow不等于图灵奖。部分原站403或超时，实际使用索引正文的来源明确标为indexed_body。书名、片名、建筑地址和具体服务等缺乏唯一身份线索的项仍保持待核验。

## 五道新诊断

[数据文件](../../datasets/controls/c_source_bound_development.json)将补查材料放入问题，要求分别判断材料中人员或车型是否有记录，以及具体贡献、奖项或参数是否建立证据。题目要求输出两个字段的JSON，事后检查预期字段保存在expected_fields，未发送给模型。模型只收到question及策略提示，交付检查逐条重建prompt核对。

这是开发者编写的材料任务，和开放世界原题不同，不作为新增独立测试，也不能用来改写原题真值。三策略共15条实机回答，均来自模型；完整记录和逐字段检查见[诊断报告](runs/source_bound_v1/report.md)。compact和guarded在normal_control下使用相同提示，这两组不是独立重复证据。

| 策略 | 严格任务通过 | 两个必需字段均符合 | 单字段通过/检查 |
| --- | ---: | ---: | ---: |
| legacy | 0/5 | 0/5 | 3/10 |
| compact | 0/5 | 1/5 | 3/10 |
| guarded | 0/5 | 1/5 | 3/10 |

严格任务同时检查完整JSON语法、两个键及其值和类型，并拒绝额外键。完整代码围栏内的可解析对象另查字段，带解释的任意JSON片段不抽取。不能把格式失败直接说成事实全部错误：目录题的compact、guarded两个必需字段正确，却添加了其他键；legacy在产品题能否定仅有SU7，但SU9字段输出了嵌套对象，仍不符合约定。部分输出还把枚举字符串写成未加引号的文本，无法作为JSON解析。

人员题的namesake_documented设计意图是材料记载给定姓名的人员；中文同名措辞未完全显式说明参照对象，后续应由第二人审核题意，不能直接从这些字段错误推断模型认知机制或总体事实能力。下一版本如改写问题或字段，应另存数据、使用新运行目录，保留本轮结果。

## 复现与检查

```powershell
python -m experiments.run_c_policy_comparison --config configs/c_source_bound.json --output docs/c_work/runs/my_source_bound
python -m experiments.check_c_source_bound docs/c_work/runs/my_source_bound
python -m experiments.check_c_delivery --run-tests
```

运行目录必须是新目录。诊断检查使用该运行冻结的controls.json，拒绝问题改写、失败或仅准备记录；评分脚本按内容哈希保存到evaluation_snapshot。check_c_delivery针对已保存的source_bound_v1核对生成输入、评分结果及快照，不调用模型。

若要重建补查报告，可运行report_c_source_followup并提供一个新--output目录；原source_followup_v1保持不变。补查来源ID已登记到评分工具可接受的来源集合，不自动产生任何人工标签，也不进入RAG语料。
