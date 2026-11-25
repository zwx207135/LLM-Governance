# legacy__free

自动规则检查，未完成人工复核。

## P01a / 太阳类别与未提供物理量 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。
M2：NASA资料整理记录：太阳是太阳系中唯一的恒星，太阳不是行星。

目标陈述：太阳系中只有一颗恒星，即太阳。

````text
```json
{
  "verdict": "supported",
  "basis": "M1"
}
```
````

冻结预期：{"verdict": "supported", "basis": "M2"}
自动检查：{"id": "P01a", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G06", "topic_name": "太阳类别与未提供物理量", "case_pair_id": "P01", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": true, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "2a40a4c153d56c8898198225bf1e9fee59645a9a32c60eebe55e7cf4096c3ff5"}

## P11a / 多人贡献与未提供人物信息 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。

目标陈述：材料将电灯发展的全部贡献归给爱迪生一个人。

````text
```json
{
  "verdict": "supported",
  "basis": "M1"
}
```
````

冻结预期：{"verdict": "refuted", "basis": "M1"}
自动检查：{"id": "P11a", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G08", "topic_name": "多人贡献与未提供人物信息", "case_pair_id": "P11", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "6d923c3a5ede20062a86a528feb465cf0e61ee9fa8a76771dd72c35c3de75f2f"}

## P17a / 指定奖项记录与人物背景 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。

目标陈述：材料中爱因斯坦这条物理学奖记录的年份是1937年。

````text
```json
{
  "verdict": "supported",
  "basis": "M2"
}
```
````

冻结预期：{"verdict": "refuted", "basis": "M2"}
自动检查：{"id": "P17a", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G07", "topic_name": "指定奖项记录与人物背景", "case_pair_id": "P17", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M2", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "f95e7104c677c11d961f50f65487050c4dc19b83effa2b7f0b0419061960d464"}

## P02a / 人员存在与获奖身份 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。
M2：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。

目标陈述：刘建平曾获得诺贝尔化学奖。

````text
```json
{
  "verdict": "supported",
  "basis": "M1: 刘建平在河南工业大学化学化工学院工作，并且他在化学教学科研方面有经验，因此可以推断他可能获得了诺贝尔化学奖。"
}
```
````

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P02a", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G03", "topic_name": "人员存在与获奖身份", "case_pair_id": "P02", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "invalid", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "a9bcc551054f87f91758adab44753f86cee9536b8743527ef659acd295d22443"}

## P08b / 任职学院与获奖身份 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。
M2：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。

目标陈述：陈晓东这条目录记录所列的任职学院是经济学院。

````text
```json
{
  "verdict": "supported",
  "basis": "M2"
}
```
````

冻结预期：{"verdict": "refuted", "basis": "M2"}
自动检查：{"id": "P08b", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G02", "topic_name": "任职学院与获奖身份", "case_pair_id": "P08", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M2", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "db59a4a5d39ee906ee1024223733cd06b0b53bd1cef816703dd01b7a60360756"}

## P10b / 任职学院与获奖身份 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。
M2：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。

目标陈述：陈晓东这条目录记录所列的任职学院是材料科学与工程学院。

````text
```json
{
  "verdict": "supported",
  "basis": "M1: 姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院"
}
```
````

冻结预期：{"verdict": "supported", "basis": "M1"}
自动检查：{"id": "P10b", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G02", "topic_name": "任职学院与获奖身份", "case_pair_id": "P10", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "invalid", "parse_status": "fenced_json", "verdict_correct": true, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "e76058365fdb836bede399a2a32d8ff54d3df0620c6dd1af107fa0ce2ceef530"}

## P22a / 人员存在与获奖身份 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。
M2：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。

目标陈述：河南工业大学这份人员记录记载的姓名是王明远。

````text
```json
{
  "verdict": "supported",
  "basis": "M1: 姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。"
}
```
````

冻结预期：{"verdict": "refuted", "basis": "M2"}
自动检查：{"id": "P22a", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G03", "topic_name": "人员存在与获奖身份", "case_pair_id": "P22", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "invalid", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "d8200d9c8f33c1336ddc39408ce16761ef9fef88ef4aa351b325703d0865b214"}

## P04a / 给定名单与研究范围 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。
M2：本题给定的完整名单只有两个条目：浙江大学生物医学工程与仪器科学学院、浙江大学医学院。名单为教学任务选取的目录片段，不代表学校全部单位，也没有提供研究项目清单。

目标陈述：本题给定的名单列有脑机接口学院这一条目。

````text
```json
{
  "verdict": "supported",
  "basis": "M1: 刘建平在河南工业大学化学化工学院从事化学教学科研；M2: 浙江大学生物医学工程与仪器科学学院、浙江大学医学院不是本题给出的名单中的单位。"
}
```
````

冻结预期：{"verdict": "refuted", "basis": "M2"}
自动检查：{"id": "P04a", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G05", "topic_name": "给定名单与研究范围", "case_pair_id": "P04", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "invalid", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "bc8331ee10f9e6dc3754aebce1209f19707eb95011f4a2fbce0ddd07ad1c0bf1"}

## P06a / 车型报告与未知参数 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：这份报告记录将YU7的发布日期写为2024年6月。

````text
```json
{
  "verdict": "supported",
  "basis": "M1"
}
```
````

冻结预期：{"verdict": "refuted", "basis": "M1"}
自动检查：{"id": "P06a", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G04", "topic_name": "车型报告与未知参数", "case_pair_id": "P06", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "393464b393fd91536e65b780e669cd17d4d6f07f992768450084104f5c24fc61"}

## P10a / 任职学院与获奖身份 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。
M2：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。

目标陈述：陈晓东这条目录记录所列的任职学院是材料科学与工程学院。

````text
```json
{
  "verdict": "supported",
  "basis": "M2"
}
```
````

冻结预期：{"verdict": "supported", "basis": "M2"}
自动检查：{"id": "P10a", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G02", "topic_name": "任职学院与获奖身份", "case_pair_id": "P10", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M2", "parse_status": "fenced_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "2232e77c1368bb16b1223923a1519cbd5c256ec5cc92f0843d7db43ea899ec04"}

## P14a / 人员存在与获奖身份 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。
M2：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。

目标陈述：河南工业大学这份人员记录记载了刘建平这一姓名。

````text
```json
{
  "verdict": "supported",
  "basis": "M1"
}
```
````

冻结预期：{"verdict": "supported", "basis": "M1"}
自动检查：{"id": "P14a", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G03", "topic_name": "人员存在与获奖身份", "case_pair_id": "P14", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "e23c2e1053522973c68074c3681152c6cf64f9d5e328fc4875f138a6ff638072"}

## P01b / 太阳类别与未提供物理量 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：NASA资料整理记录：太阳是太阳系中唯一的恒星，太阳不是行星。
M2：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。

目标陈述：太阳系中只有一颗恒星，即太阳。

````text
```json
{
  "verdict": "supported",
  "basis": "M1"
}
```
````

冻结预期：{"verdict": "supported", "basis": "M1"}
自动检查：{"id": "P01b", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G06", "topic_name": "太阳类别与未提供物理量", "case_pair_id": "P01", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "dc3ba3dc6833b6610c3dbb0d8c15a149506dbb6252705863ce9e634339e54ba3"}

## P04b / 给定名单与研究范围 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：本题给定的完整名单只有两个条目：浙江大学生物医学工程与仪器科学学院、浙江大学医学院。名单为教学任务选取的目录片段，不代表学校全部单位，也没有提供研究项目清单。
M2：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。

目标陈述：本题给定的名单列有脑机接口学院这一条目。

````text
```json
{
  "verdict": "not_established",
  "basis": "none"
}
```
````

冻结预期：{"verdict": "refuted", "basis": "M1"}
自动检查：{"id": "P04b", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G05", "topic_name": "给定名单与研究范围", "case_pair_id": "P04", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M1", "predicted_verdict": "not_established", "predicted_label_raw": "not_established", "predicted_basis": "none", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "603d07aab873c08f75fec6bf757c89d6944630df3b3c3bfd58ff4f1664b2c28a"}

## P16a / 人员姓名与具体贡献 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。
M2：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。

目标陈述：中国科学院国家天文台这份人员记录记载的姓名为王明远。

````text
```json
{
  "verdict": "supported",
  "basis": "M1"
}
```
````

冻结预期：{"verdict": "supported", "basis": "M1"}
自动检查：{"id": "P16a", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G01", "topic_name": "人员姓名与具体贡献", "case_pair_id": "P16", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "fee0047e24977b6748111cbea3101749020b9a3fd867f1bb310199c175562811"}

## P12a / 车型报告与未知参数 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。

目标陈述：SU9的百公里加速时间为2.5秒。

````text
```json
{
  "verdict": "supported",
  "basis": "M1"
}
```
````

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P12a", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G04", "topic_name": "车型报告与未知参数", "case_pair_id": "P12", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "67f01b662c260e605ed0008d6a059cf0eeb8ab6edfb6abad035ff7403d4be2e1"}

## P18a / 多人贡献与未提供人物信息 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：斯旺出生于1828年。

````text
```json
{
  "verdict": "supported",
  "basis": "M2"
}
```
````

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P18a", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G08", "topic_name": "多人贡献与未提供人物信息", "case_pair_id": "P18", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M2", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "b1f768fb18c33bd4c9c3e0c188d6d91417fc3675f869e46ac8e77a12d962c7f2"}

## P03a / 太阳类别与未提供物理量 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。
M2：NASA资料整理记录：太阳是太阳系中唯一的恒星，太阳不是行星。

目标陈述：太阳的有效温度为5772K。

````text
```json
{
  "verdict": "supported",
  "basis": "M1"
}
```
````

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P03a", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G06", "topic_name": "太阳类别与未提供物理量", "case_pair_id": "P03", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "378fa2533715e6d4101fb65913244c3a612e032f071d4be8efd3ce058aefe755"}

## P23a / 太阳类别与未提供物理量 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：NASA资料整理记录：太阳是太阳系中唯一的恒星，太阳不是行星。
M2：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。

目标陈述：太阳属于行星而不属于恒星。

````text
```json
{
  "verdict": "supported",
  "basis": "M1"
}
```
````

冻结预期：{"verdict": "refuted", "basis": "M1"}
自动检查：{"id": "P23a", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G06", "topic_name": "太阳类别与未提供物理量", "case_pair_id": "P23", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "5cd520cb13c78fb0ded330410827d77058691fa84e42f4742523bf58134c9e7a"}

## P15a / 人员姓名与具体贡献 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。
M2：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。

目标陈述：王明远提出过一项新的相对论理论。

````text
```json
{
  "verdict": "supported",
  "basis": "M1: 姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。",
          "M2: 姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。"
}
```
````

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P15a", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G01", "topic_name": "人员姓名与具体贡献", "case_pair_id": "P15", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "invalid", "predicted_label_raw": null, "predicted_basis": "invalid", "parse_status": "invalid", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "aa1304cadb3c75d4675ed182ab469cbc0cea16e62af9016dde949609b3666528"}

## P24b / 指定奖项记录与人物背景 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。

目标陈述：材料中爱因斯坦这条物理学奖记录的年份是1921年。

```text
{"verdict": supported, "basis": "材料中提到诺贝尔物理学奖档案中的信息，但没有直接提及爱因斯坦获得该奖项的具体年份。"}
```

冻结预期：{"verdict": "supported", "basis": "M2"}
自动检查：{"id": "P24b", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G07", "topic_name": "指定奖项记录与人物背景", "case_pair_id": "P24", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M2", "predicted_verdict": "invalid", "predicted_label_raw": null, "predicted_basis": "invalid", "parse_status": "invalid", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "d52a0eb8af69ce594eef08584273842dba76a430fa5e9c21196a231aacb387c3"}

## P07a / 车型报告与未知参数 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。

目标陈述：这份报告记录将YU7定位为SUV。

````text
```json
{
  "verdict": "supported",
  "basis": "M2"
}
```
````

冻结预期：{"verdict": "supported", "basis": "M2"}
自动检查：{"id": "P07a", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G04", "topic_name": "车型报告与未知参数", "case_pair_id": "P07", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M2", "parse_status": "fenced_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "f948a674a1020a8cb566966f1878a64e5e0341367b3534b96a06c78cfa8d9542"}

## P11b / 多人贡献与未提供人物信息 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：材料将电灯发展的全部贡献归给爱迪生一个人。

```text
{"verdict": supported, "basis": "M1: 诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。"}
```

冻结预期：{"verdict": "refuted", "basis": "M2"}
自动检查：{"id": "P11b", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G08", "topic_name": "多人贡献与未提供人物信息", "case_pair_id": "P11", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M2", "predicted_verdict": "invalid", "predicted_label_raw": null, "predicted_basis": "invalid", "parse_status": "invalid", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "9844d328baae5448e58feb92efb95c673cd117ae883f377ca2d9bc842d7d7c75"}

## P05b / 给定名单与研究范围 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。
M2：本题给定的完整名单只有两个条目：浙江大学生物医学工程与仪器科学学院、浙江大学医学院。名单为教学任务选取的目录片段，不代表学校全部单位，也没有提供研究项目清单。

目标陈述：浙江大学完全没有脑机接口相关研究。

````text
```json
{
  "verdict": "supported",
  "basis": "M1: 刘建平在河南工业大学化学化工学院从事化学教学科研，而M2: 浙江大学生物医学工程与仪器科学学院和浙江大学医学院没有提及脑机接口相关研究。"
}
```
````

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P05b", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G05", "topic_name": "给定名单与研究范围", "case_pair_id": "P05", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "invalid", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "26130fe50db466e526135f273f25fd2019b67c10e0262df7cfb3e84766335423"}

## P21b / 指定奖项记录与人物背景 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。

目标陈述：爱因斯坦的出生年份是1879年。

````text
```json
{
  "verdict": "supported",
  "basis": "M1"
}
```
````

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P21b", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G07", "topic_name": "指定奖项记录与人物背景", "case_pair_id": "P21", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "1ebea657c2824eeb7855915085665a65f34fbd365b70367dc40752dac2082082"}

## P23b / 太阳类别与未提供物理量 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。
M2：NASA资料整理记录：太阳是太阳系中唯一的恒星，太阳不是行星。

目标陈述：太阳属于行星而不属于恒星。

````text
```json
{
  "verdict": "supported",
  "basis": "M1"
}
```
````

冻结预期：{"verdict": "refuted", "basis": "M2"}
自动检查：{"id": "P23b", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G06", "topic_name": "太阳类别与未提供物理量", "case_pair_id": "P23", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "3141622f78a950ead3be14c7c78d2003aa1c08e537633cea0e47db14c2788f9e"}

## P03b / 太阳类别与未提供物理量 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：NASA资料整理记录：太阳是太阳系中唯一的恒星，太阳不是行星。
M2：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。

目标陈述：太阳的有效温度为5772K。

````text
```json
{
  "verdict": "supported",
  "basis": "M1"
}
```
````

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P03b", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G06", "topic_name": "太阳类别与未提供物理量", "case_pair_id": "P03", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "da7e7ffcedbe53436b57411b53ad8c241be1ae3718e1958bafdd33d7a7db6580"}

## P15b / 人员姓名与具体贡献 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。
M2：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。

目标陈述：王明远提出过一项新的相对论理论。

````text
```json
{
  "verdict": "supported",
  "basis": "none"
}
```
````

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P15b", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G01", "topic_name": "人员姓名与具体贡献", "case_pair_id": "P15", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "none", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "73f712274f333f3764335694c0d7e8069c418a4b2a65f835cc160135e5cb2f86"}

## P06b / 车型报告与未知参数 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。

目标陈述：这份报告记录将YU7的发布日期写为2024年6月。

````text
```json
{
  "verdict": "supported",
  "basis": "M2"
}
```
````

冻结预期：{"verdict": "refuted", "basis": "M2"}
自动检查：{"id": "P06b", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G04", "topic_name": "车型报告与未知参数", "case_pair_id": "P06", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M2", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "054afff9d0fc94adcccda63ef11c04f9e04e6b4450c6de0c468588a27a513cd2"}

## P13a / 多人贡献与未提供人物信息 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：材料将电灯发展描述为多位发明者的贡献。

````text
```json
{
  "verdict": "supported",
  "basis": "M1"
}
```
````

冻结预期：{"verdict": "supported", "basis": "M2"}
自动检查：{"id": "P13a", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G08", "topic_name": "多人贡献与未提供人物信息", "case_pair_id": "P13", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": true, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "a7ce5df992d2a8c350ba31aed38ad5e75d2ca74b93d94e8aff40d87838ed89f5"}

## P19a / 人员姓名与具体贡献 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。
M2：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。

目标陈述：中国科学院国家天文台这份人员记录记载的姓名为李华。

````text
```json
{
  "verdict": "supported",
  "basis": "M1: 刘建平 是河南工业大学化学化工学院的教师，从事化学教学科研；M2: 王明远 是中国科学院国家天文台的研究员，研究方向包括天体测量、天体力学、行星无线电科学。"
}
```
````

冻结预期：{"verdict": "refuted", "basis": "M2"}
自动检查：{"id": "P19a", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G01", "topic_name": "人员姓名与具体贡献", "case_pair_id": "P19", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "invalid", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "d3d00ff63e5dee8cbc5acb8f1a3e60b2e4746b49197dd37eb4b312e1ae5a08d1"}

## P20b / 给定名单与研究范围 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。
M2：本题给定的完整名单只有两个条目：浙江大学生物医学工程与仪器科学学院、浙江大学医学院。名单为教学任务选取的目录片段，不代表学校全部单位，也没有提供研究项目清单。

目标陈述：本题给定的名单列有浙江大学医学院。

````text
```json
{
  "verdict": "supported",
  "basis": "M2"
}
```
````

冻结预期：{"verdict": "supported", "basis": "M2"}
自动检查：{"id": "P20b", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G05", "topic_name": "给定名单与研究范围", "case_pair_id": "P20", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M2", "parse_status": "fenced_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "87d366765c8dfb567c9e0bc4fdcbdbe18556343d90b39aa12b68005c27af5ceb"}

## P02b / 人员存在与获奖身份 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。
M2：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。

目标陈述：刘建平曾获得诺贝尔化学奖。

````text
```json
{
  "verdict": "supported",
  "basis": "M2"
}
```
````

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P02b", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G03", "topic_name": "人员存在与获奖身份", "case_pair_id": "P02", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M2", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "962c473aa3366e340ea4984ff8dcc003fb1f54d6f0741f7ebe70eabcc0c0cd4e"}

## P09a / 任职学院与获奖身份 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。
M2：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。

目标陈述：陈晓东曾获得诺贝尔物理学奖。

````text
```json
{
  "verdict": "supported",
  "basis": "M2"
}
```
````

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P09a", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G02", "topic_name": "任职学院与获奖身份", "case_pair_id": "P09", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M2", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "9be667e4aeae7c391118905633daa765b491dd48138a692f5ce56f98f3a5aad4"}

## P24a / 指定奖项记录与人物背景 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：材料中爱因斯坦这条物理学奖记录的年份是1921年。

```text
{"verdict": supported, "basis": "M1"}
```

冻结预期：{"verdict": "supported", "basis": "M1"}
自动检查：{"id": "P24a", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G07", "topic_name": "指定奖项记录与人物背景", "case_pair_id": "P24", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M1", "predicted_verdict": "invalid", "predicted_label_raw": null, "predicted_basis": "invalid", "parse_status": "invalid", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "baa7f179e1d25ee82a8df42476c29f8231c50ea427015dc890cf91ebace514e2"}

## P07b / 车型报告与未知参数 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：这份报告记录将YU7定位为SUV。

````text
```json
{
  "verdict": "supported",
  "basis": "M1"
}
```
````

冻结预期：{"verdict": "supported", "basis": "M1"}
自动检查：{"id": "P07b", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G04", "topic_name": "车型报告与未知参数", "case_pair_id": "P07", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "f106ca8c374bc856dfdc72b77e742df1589808f192763d25a18bf373594dabaf"}

## P16b / 人员姓名与具体贡献 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。
M2：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。

目标陈述：中国科学院国家天文台这份人员记录记载的姓名为王明远。

````text
```json
{
  "verdict": "supported",
  "basis": "M2"
}
```
````

冻结预期：{"verdict": "supported", "basis": "M2"}
自动检查：{"id": "P16b", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G01", "topic_name": "人员姓名与具体贡献", "case_pair_id": "P16", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M2", "parse_status": "fenced_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "e65ca618c5ae4b3439aeac038204fb0e71b397ece989642c66fa9f82949b51a4"}

## P21a / 指定奖项记录与人物背景 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：爱因斯坦的出生年份是1879年。

````text
```json
{
  "verdict": "supported",
  "basis": "M1"
}
```
````

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P21a", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G07", "topic_name": "指定奖项记录与人物背景", "case_pair_id": "P21", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "020b054e86fee1562f9a0fe298efc6197d65b0c44dda3be3028a8e5ba066e9d1"}

## P19b / 人员姓名与具体贡献 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。
M2：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。

目标陈述：中国科学院国家天文台这份人员记录记载的姓名为李华。

````text
```json
{
  "verdict": "supported",
  "basis": "M1: 姓名为王明远；M2: 姓名为刘建平。"
}
```
````

冻结预期：{"verdict": "refuted", "basis": "M1"}
自动检查：{"id": "P19b", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G01", "topic_name": "人员姓名与具体贡献", "case_pair_id": "P19", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "invalid", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "2b61b4c15a65f38c994dde6224def5382a8aaee748bfcc56899cb777e5bcc225"}

## P09b / 任职学院与获奖身份 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。
M2：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。

目标陈述：陈晓东曾获得诺贝尔物理学奖。

````text
```json
{
  "verdict": "supported",
  "basis": "M1: 姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。"
}
```
````

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P09b", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G02", "topic_name": "任职学院与获奖身份", "case_pair_id": "P09", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "invalid", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "02e7afe8578c092a2b76c22a7e235cf2b50c0e77c14c18aaff9bfdf0a1d7d6cd"}

## P18b / 多人贡献与未提供人物信息 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。

目标陈述：斯旺出生于1828年。

````text
```json
{
  "verdict": "supported",
  "basis": "M2"
}
```
````

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P18b", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G08", "topic_name": "多人贡献与未提供人物信息", "case_pair_id": "P18", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M2", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "00c0a642450dc999d80559fd1b22479dbeaf40ebf199496f67b899c9c598614d"}

## P08a / 任职学院与获奖身份 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。
M2：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。

目标陈述：陈晓东这条目录记录所列的任职学院是经济学院。

````text
```json
{
  "verdict": "supported",
  "basis": "M1: 姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院"
}
```
````

冻结预期：{"verdict": "refuted", "basis": "M1"}
自动检查：{"id": "P08a", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G02", "topic_name": "任职学院与获奖身份", "case_pair_id": "P08", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "invalid", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "6484a88c29c3dd8da2cf312c49434f410dfbcacf5fcc86748c21f01e9eceb625"}

## P22b / 人员存在与获奖身份 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。
M2：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。

目标陈述：河南工业大学这份人员记录记载的姓名是王明远。

````text
```json
{
  "verdict": "supported",
  "basis": "M1: 姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。",
              "M2: 姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院"
}
```
````

冻结预期：{"verdict": "refuted", "basis": "M1"}
自动检查：{"id": "P22b", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G03", "topic_name": "人员存在与获奖身份", "case_pair_id": "P22", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M1", "predicted_verdict": "invalid", "predicted_label_raw": null, "predicted_basis": "invalid", "parse_status": "invalid", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "29d45e03007a850aff354159d8abf69279389b9367371f8c37410299000b29c3"}

## P14b / 人员存在与获奖身份 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。
M2：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。

目标陈述：河南工业大学这份人员记录记载了刘建平这一姓名。

````text
```json
{
  "verdict": "supported",
  "basis": "M2"
}
```
````

冻结预期：{"verdict": "supported", "basis": "M2"}
自动检查：{"id": "P14b", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G03", "topic_name": "人员存在与获奖身份", "case_pair_id": "P14", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M2", "parse_status": "fenced_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "e91f8a674029183bfea8046f07bd583b515da8ea416fee8dcf4dfca488796e4c"}

## P20a / 给定名单与研究范围 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：本题给定的完整名单只有两个条目：浙江大学生物医学工程与仪器科学学院、浙江大学医学院。名单为教学任务选取的目录片段，不代表学校全部单位，也没有提供研究项目清单。
M2：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。

目标陈述：本题给定的名单列有浙江大学医学院。

````text
```json
{
  "verdict": "supported",
  "basis": "M1"
}
```
````

冻结预期：{"verdict": "supported", "basis": "M1"}
自动检查：{"id": "P20a", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G05", "topic_name": "给定名单与研究范围", "case_pair_id": "P20", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "ab6010e072e9734273d3d6a88294d8be374a2a64f7ecbb019cf6fb5b6fdfe9d2"}

## P12b / 车型报告与未知参数 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：SU9的百公里加速时间为2.5秒。

````text
```json
{
  "verdict": "supported",
  "basis": "M1"
}
```
````

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P12b", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G04", "topic_name": "车型报告与未知参数", "case_pair_id": "P12", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "3880886e87e9336c15165e9971d2f850638b22d97afa48fc2a52d741e0624f4f"}

## P17b / 指定奖项记录与人物背景 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：材料中爱因斯坦这条物理学奖记录的年份是1937年。

````text
```json
{
  "verdict": "supported",
  "basis": "M1"
}
```
````

冻结预期：{"verdict": "refuted", "basis": "M1"}
自动检查：{"id": "P17b", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G07", "topic_name": "指定奖项记录与人物背景", "case_pair_id": "P17", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "b1ecc5bdcfcc58308af4579bfced2f2dc2f6dc2bb2ce2cbf10eba9d4190f6ff7"}

## P13b / 多人贡献与未提供人物信息 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。

目标陈述：材料将电灯发展描述为多位发明者的贡献。

````text
```json
{
  "verdict": "supported",
  "basis": "M1"
}
```
````

冻结预期：{"verdict": "supported", "basis": "M1"}
自动检查：{"id": "P13b", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G08", "topic_name": "多人贡献与未提供人物信息", "case_pair_id": "P13", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "007238eea9fb973a06dbc3d26aa710f7ef92991ca2055a5fde13f95a21790583"}

## P05a / 给定名单与研究范围 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：本题给定的完整名单只有两个条目：浙江大学生物医学工程与仪器科学学院、浙江大学医学院。名单为教学任务选取的目录片段，不代表学校全部单位，也没有提供研究项目清单。
M2：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。

目标陈述：浙江大学完全没有脑机接口相关研究。

````text
```json
{
  "verdict": "supported",
  "basis": "M1: 浙江大学生物医学工程与仪器科学学院和浙江大学医学院都是教学任务选取的目录片段，不代表学校全部单位，也没有提供研究项目清单。",
          "M2: 刘建平在河南工业大学化学化工学院担任化学教学科研，但没有提到任何关于脑机接口的研究。"
}
```
````

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P05a", "mode": "legacy__free", "policy": "legacy", "decoder": "free", "contrast_group": "G05", "topic_name": "给定名单与研究范围", "case_pair_id": "P05", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "invalid", "predicted_label_raw": null, "predicted_basis": "invalid", "parse_status": "invalid", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "0009a4022d248464f8035b76399aca40e502b9bcf3d1a0841a98e6fd5dcfa56a"}
