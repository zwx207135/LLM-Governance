# compact__free

自动规则检查，未完成人工复核。

## P01a / 太阳类别与未提供物理量 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。
M2：NASA资料整理记录：太阳是太阳系中唯一的恒星，太阳不是行星。

目标陈述：太阳系中只有一颗恒星，即太阳。

```text
{
  "verdict": "supported",
  "basis": "M1"
}
```

冻结预期：{"verdict": "supported", "basis": "M2"}
自动检查：{"id": "P01a", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G06", "topic_name": "太阳类别与未提供物理量", "case_pair_id": "P01", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "96e097c70425f62abebd7131a3c5c198c2a47c82a1275da393ef2d397cbc9acd"}

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
自动检查：{"id": "P11a", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G08", "topic_name": "多人贡献与未提供人物信息", "case_pair_id": "P11", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "6d923c3a5ede20062a86a528feb465cf0e61ee9fa8a76771dd72c35c3de75f2f"}

## P17a / 指定奖项记录与人物背景 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。

目标陈述：材料中爱因斯坦这条物理学奖记录的年份是1937年。

```text
{
  "verdict": "supported",
  "basis": "M2"
}
```

冻结预期：{"verdict": "refuted", "basis": "M2"}
自动检查：{"id": "P17a", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G07", "topic_name": "指定奖项记录与人物背景", "case_pair_id": "P17", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M2", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "6dd4ebe2f88cf4a5d80f3243cd80204ea43f648e0f0270be9a332b2c62c0f518"}

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
  "basis": "M1"
}
```
````

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P02a", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G03", "topic_name": "人员存在与获奖身份", "case_pair_id": "P02", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "5504615c7a2dd92ce94cda7b61c06dc0391fc2962dfa02126cebd29d9c8b13a8"}

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
  "basis": "none"
}
```
````

冻结预期：{"verdict": "refuted", "basis": "M2"}
自动检查：{"id": "P08b", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G02", "topic_name": "任职学院与获奖身份", "case_pair_id": "P08", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "none", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "1dbe4300320cf0416359709efd84b86fd9359ce650e8d325213d2fb8e3c945b7"}

## P10b / 任职学院与获奖身份 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。
M2：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。

目标陈述：陈晓东这条目录记录所列的任职学院是材料科学与工程学院。

```text
{
  "verdict": "supported",
  "basis": "M1: 员工目录中列出的任职学院为南洋理工大学"
}
```

冻结预期：{"verdict": "supported", "basis": "M1"}
自动检查：{"id": "P10b", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G02", "topic_name": "任职学院与获奖身份", "case_pair_id": "P10", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "invalid", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "127276e1a39cce32a2035cfb5eb6ba2c2f68fc15e1a9583830780555dc9b53f0"}

## P22a / 人员存在与获奖身份 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。
M2：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。

目标陈述：河南工业大学这份人员记录记载的姓名是王明远。

```text
{
  "verdict": "supported",
  "basis": "M1: 员工姓名陈晓东对应的是南洋理工大学材料科学与工程学院，而M2: 员工姓名刘建平对应的是河南工业大学化学化工学院。因此，可以推断出河南工业大学记录中的姓名应该是王明远。"
}
```

冻结预期：{"verdict": "refuted", "basis": "M2"}
自动检查：{"id": "P22a", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G03", "topic_name": "人员存在与获奖身份", "case_pair_id": "P22", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "invalid", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "304dc0ed220e9b2dd15c17f06b98c92025098237f4f81e5edcecf33f58e6162a"}

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
  "basis": "M1: 刘建平在河南工业大学化学化工学院从事化学教学科研；M2: 浙江大学生物医学工程与仪器科学学院、浙江大学医学院都是教学任务选取的目录片段，不代表学校全部单位，也没有提供研究项目清单。"
}
```
````

冻结预期：{"verdict": "refuted", "basis": "M2"}
自动检查：{"id": "P04a", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G05", "topic_name": "给定名单与研究范围", "case_pair_id": "P04", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "invalid", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "a748536d37b032651a68cc0e03a77cb6ce4a25f17078c048abaa2b2ade2cc9f3"}

## P06a / 车型报告与未知参数 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：这份报告记录将YU7的发布日期写为2024年6月。

```text
{
  "verdict": "supported",
  "basis": "M1"
}
```

冻结预期：{"verdict": "refuted", "basis": "M1"}
自动检查：{"id": "P06a", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G04", "topic_name": "车型报告与未知参数", "case_pair_id": "P06", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "df4d0a67ffd407b0a75ab55ee79cbe79dfecbe3d53d0a424563a121fcd836f64"}

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
  "basis": "M1"
}
```
````

冻结预期：{"verdict": "supported", "basis": "M2"}
自动检查：{"id": "P10a", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G02", "topic_name": "任职学院与获奖身份", "case_pair_id": "P10", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": true, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "c45b9587eee23089fa5373bcacb002ade97acc3341ed1644e1123b628556a57f"}

## P14a / 人员存在与获奖身份 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。
M2：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。

目标陈述：河南工业大学这份人员记录记载了刘建平这一姓名。

```text
{
  "verdict": "supported",
  "basis": "M1"
}
```

冻结预期：{"verdict": "supported", "basis": "M1"}
自动检查：{"id": "P14a", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G03", "topic_name": "人员存在与获奖身份", "case_pair_id": "P14", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": true, "strict_task_passed": true, "truncated": false, "content_sha256": "a1dc077b030fc06d48691aea6ee22b8cc1b120fbcdfcc3b28cba2ae027f81bab"}

## P01b / 太阳类别与未提供物理量 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：NASA资料整理记录：太阳是太阳系中唯一的恒星，太阳不是行星。
M2：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。

目标陈述：太阳系中只有一颗恒星，即太阳。

```text
{
  "verdict": "supported",
  "basis": "M1"
}
```

冻结预期：{"verdict": "supported", "basis": "M1"}
自动检查：{"id": "P01b", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G06", "topic_name": "太阳类别与未提供物理量", "case_pair_id": "P01", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": true, "strict_task_passed": true, "truncated": false, "content_sha256": "07b430b11b05519b81b2e7874445a37a2a94d8d3601e4749c30128438cc1e775"}

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
  "verdict": "supported",
  "basis": "none"
}
```
````

冻结预期：{"verdict": "refuted", "basis": "M1"}
自动检查：{"id": "P04b", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G05", "topic_name": "给定名单与研究范围", "case_pair_id": "P04", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "none", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "b88a0ff1d1ffe1d753e365066298873750fc61220c02deacb3240d1f8d2770b4"}

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
自动检查：{"id": "P16a", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G01", "topic_name": "人员姓名与具体贡献", "case_pair_id": "P16", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "fee0047e24977b6748111cbea3101749020b9a3fd867f1bb310199c175562811"}

## P12a / 车型报告与未知参数 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。

目标陈述：SU9的百公里加速时间为2.5秒。

```text
{
  "verdict": "supported",
  "basis": "M1"
}
```

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P12a", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G04", "topic_name": "车型报告与未知参数", "case_pair_id": "P12", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "c089a57eff096e5971286569e76903d652e979a6993ce162ef02a37dd549dbae"}

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
自动检查：{"id": "P18a", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G08", "topic_name": "多人贡献与未提供人物信息", "case_pair_id": "P18", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M2", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "b1f768fb18c33bd4c9c3e0c188d6d91417fc3675f869e46ac8e77a12d962c7f2"}

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
自动检查：{"id": "P03a", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G06", "topic_name": "太阳类别与未提供物理量", "case_pair_id": "P03", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "378fa2533715e6d4101fb65913244c3a612e032f071d4be8efd3ce058aefe755"}

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
自动检查：{"id": "P23a", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G06", "topic_name": "太阳类别与未提供物理量", "case_pair_id": "P23", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "5cd520cb13c78fb0ded330410827d77058691fa84e42f4742523bf58134c9e7a"}

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
  "basis": "none"
}
```
````

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P15a", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G01", "topic_name": "人员姓名与具体贡献", "case_pair_id": "P15", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "none", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "5f00b414dcbc84bc551378f84929fe0e99a8647a6d6e6f65f7e516c3d9189f5e"}

## P24b / 指定奖项记录与人物背景 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。

目标陈述：材料中爱因斯坦这条物理学奖记录的年份是1921年。

```text
{
  "verdict": "supported",
  "basis": "M2"
}
```

冻结预期：{"verdict": "supported", "basis": "M2"}
自动检查：{"id": "P24b", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G07", "topic_name": "指定奖项记录与人物背景", "case_pair_id": "P24", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M2", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": true, "strict_task_passed": true, "truncated": false, "content_sha256": "a69277a0c67f211802245d1088f4caed575c6a7a27005e120ecb30344b3ab39a"}

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
自动检查：{"id": "P07a", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G04", "topic_name": "车型报告与未知参数", "case_pair_id": "P07", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M2", "parse_status": "fenced_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "f948a674a1020a8cb566966f1878a64e5e0341367b3534b96a06c78cfa8d9542"}

## P11b / 多人贡献与未提供人物信息 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：材料将电灯发展的全部贡献归给爱迪生一个人。

````text
```json
{
  "verdict": "supported",
  "basis": "M1"
}
```
````

冻结预期：{"verdict": "refuted", "basis": "M2"}
自动检查：{"id": "P11b", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G08", "topic_name": "多人贡献与未提供人物信息", "case_pair_id": "P11", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "eda1a891ae9206251d1e04846d223754b78e9defcd06c7dc96c4e82c31ff61fc"}

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
  "basis": "M1: 刘建平在河南工业大学化学化工学院从事化学教学科研，而浙江大学没有提及任何与脑机接口相关的研究。",
}
```
````

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P05b", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G05", "topic_name": "给定名单与研究范围", "case_pair_id": "P05", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "invalid", "predicted_label_raw": null, "predicted_basis": "invalid", "parse_status": "invalid", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "42107abf22abda57134c9a0d2d5a9158f0f35376a5d1433d31e481bd87f934b2"}

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
自动检查：{"id": "P21b", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G07", "topic_name": "指定奖项记录与人物背景", "case_pair_id": "P21", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "1ebea657c2824eeb7855915085665a65f34fbd365b70367dc40752dac2082082"}

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
自动检查：{"id": "P23b", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G06", "topic_name": "太阳类别与未提供物理量", "case_pair_id": "P23", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "3141622f78a950ead3be14c7c78d2003aa1c08e537633cea0e47db14c2788f9e"}

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
自动检查：{"id": "P03b", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G06", "topic_name": "太阳类别与未提供物理量", "case_pair_id": "P03", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "da7e7ffcedbe53436b57411b53ad8c241be1ae3718e1958bafdd33d7a7db6580"}

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
自动检查：{"id": "P15b", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G01", "topic_name": "人员姓名与具体贡献", "case_pair_id": "P15", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "none", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "73f712274f333f3764335694c0d7e8069c418a4b2a65f835cc160135e5cb2f86"}

## P06b / 车型报告与未知参数 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。

目标陈述：这份报告记录将YU7的发布日期写为2024年6月。

```text
{
  "verdict": "supported",
  "basis": "M2 提供的信息表明 YU7 的发布日期确实在 2025 年上半年，而不是 2024 年 6 月。"
}
```

冻结预期：{"verdict": "refuted", "basis": "M2"}
自动检查：{"id": "P06b", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G04", "topic_name": "车型报告与未知参数", "case_pair_id": "P06", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "invalid", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "c125030ebfbe29222adfc9d6029c21e4acfe0cbf48fd1dd091da1df8b5ae9415"}

## P13a / 多人贡献与未提供人物信息 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：材料将电灯发展描述为多位发明者的贡献。

```text
{
  "verdict": "supported",
  "basis": "M1"
}
```

冻结预期：{"verdict": "supported", "basis": "M2"}
自动检查：{"id": "P13a", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G08", "topic_name": "多人贡献与未提供人物信息", "case_pair_id": "P13", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "f659f857b728b8808a80374ff9744b4e738275e5be5ef269da6abcd0092b0338"}

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
  "basis": "none"
}
```
````

冻结预期：{"verdict": "refuted", "basis": "M2"}
自动检查：{"id": "P19a", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G01", "topic_name": "人员姓名与具体贡献", "case_pair_id": "P19", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "none", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "ce7c330d6dd410852d3e89d7d22f4c7a300e342745620a2e803c55fe7764d84b"}

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
自动检查：{"id": "P20b", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G05", "topic_name": "给定名单与研究范围", "case_pair_id": "P20", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M2", "parse_status": "fenced_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "87d366765c8dfb567c9e0bc4fdcbdbe18556343d90b39aa12b68005c27af5ceb"}

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
  "basis": "M2提供刘建平的任职单位信息，表明他可能在河南工业大学化学化工学院工作，并且他在化学教学科研方面有相关经历，因此可以推断他确实获得了诺贝尔化学奖。"
}
```
````

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P02b", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G03", "topic_name": "人员存在与获奖身份", "case_pair_id": "P02", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "invalid", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "fd6f99df55e47f8f62fa59e9a62e16d01dd6cdd3ad3dcb1d9b6940041c3e481d"}

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
  "basis": "none"
}
```
````

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P09a", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G02", "topic_name": "任职学院与获奖身份", "case_pair_id": "P09", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "none", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "f7c38d0826765361fa3fe745e04e6ab33e2a5e72ab5f44804c44404594fc6774"}

## P24a / 指定奖项记录与人物背景 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：材料中爱因斯坦这条物理学奖记录的年份是1921年。

```text
{
  "verdict": "supported",
  "basis": "M1"
}
```

冻结预期：{"verdict": "supported", "basis": "M1"}
自动检查：{"id": "P24a", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G07", "topic_name": "指定奖项记录与人物背景", "case_pair_id": "P24", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": true, "strict_task_passed": true, "truncated": false, "content_sha256": "e6ef6d1a0633b74f68da4a818b78613d29b0d6f7d7399434236e88e00a5d2d76"}

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
自动检查：{"id": "P07b", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G04", "topic_name": "车型报告与未知参数", "case_pair_id": "P07", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "f106ca8c374bc856dfdc72b77e742df1589808f192763d25a18bf373594dabaf"}

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
  "basis": "none"
}
```
````

冻结预期：{"verdict": "supported", "basis": "M2"}
自动检查：{"id": "P16b", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G01", "topic_name": "人员姓名与具体贡献", "case_pair_id": "P16", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "none", "parse_status": "fenced_json", "verdict_correct": true, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "3f4f93eff32544444a3979fbdd16f4b2227f9a5d2fcef4bb6ed7d51672f215e5"}

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
自动检查：{"id": "P21a", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G07", "topic_name": "指定奖项记录与人物背景", "case_pair_id": "P21", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "020b054e86fee1562f9a0fe298efc6197d65b0c44dda3be3028a8e5ba066e9d1"}

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
  "basis": "none"
}
```
````

冻结预期：{"verdict": "refuted", "basis": "M1"}
自动检查：{"id": "P19b", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G01", "topic_name": "人员姓名与具体贡献", "case_pair_id": "P19", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "none", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "8f74efd94ce95639f602ed376c72927daadf8babea17d201ce8cd1e67f846027"}

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
  "basis": "材料中提到陈晓东曾获得诺贝尔物理学奖"
}
```
````

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P09b", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G02", "topic_name": "任职学院与获奖身份", "case_pair_id": "P09", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "invalid", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "e05fe0763f38ab729d7a845e57a13e970e0623de2dae5751fcfd9961c1d5c893"}

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
自动检查：{"id": "P18b", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G08", "topic_name": "多人贡献与未提供人物信息", "case_pair_id": "P18", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M2", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "00c0a642450dc999d80559fd1b22479dbeaf40ebf199496f67b899c9c598614d"}

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
  "basis": "M1: 员工目录中列出的任职学院为南洋理工大学，而目标陈述提到的任职学院为经济学院，二者不符"
}
```
````

冻结预期：{"verdict": "refuted", "basis": "M1"}
自动检查：{"id": "P08a", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G02", "topic_name": "任职学院与获奖身份", "case_pair_id": "P08", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "invalid", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "d2aab5ed99659b2bd1d45d9afd93f0b590344cfaea286908fba4e16dc1a4aff2"}

## P22b / 人员存在与获奖身份 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。
M2：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。

目标陈述：河南工业大学这份人员记录记载的姓名是王明远。

```text
{
  "verdict": "supported",
  "basis": "M1记录了河南工业大学化学化工学院的刘建平教授，而M2记录了河南工业大学的陈晓东教授，因此可以推断出河南工业大学确实有两位教授的名字是王明远。"
}
```

冻结预期：{"verdict": "refuted", "basis": "M1"}
自动检查：{"id": "P22b", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G03", "topic_name": "人员存在与获奖身份", "case_pair_id": "P22", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "invalid", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "de10b79b7e593cfbf34b305520cfa64548d3ff762c734b56ca87bb357fae42d1"}

## P14b / 人员存在与获奖身份 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。
M2：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。

目标陈述：河南工业大学这份人员记录记载了刘建平这一姓名。

```text
{
  "verdict": "supported",
  "basis": "M2记录中刘建平的任职单位为河南工业大学化学化工学院，而M1记录中没有提及任何关于刘建平的任职信息，因此可以推断出河南工业大学并没有记录刘建平的信息。"
}
```

冻结预期：{"verdict": "supported", "basis": "M2"}
自动检查：{"id": "P14b", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G03", "topic_name": "人员存在与获奖身份", "case_pair_id": "P14", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "invalid", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "aa71864bd5e1449d67c7b3333d1112f444c9c9521ded17b9a4ebde69808caa29"}

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
  "basis": "none"
}
```
````

冻结预期：{"verdict": "supported", "basis": "M1"}
自动检查：{"id": "P20a", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G05", "topic_name": "给定名单与研究范围", "case_pair_id": "P20", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "none", "parse_status": "fenced_json", "verdict_correct": true, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "c5031dfe037e0d84845b960737f2eff438a378fe87cb89f789e40fb0964375c0"}

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
  "verdict": "not_established",
  "basis": "材料未提及"
}
```
````

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P12b", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G04", "topic_name": "车型报告与未知参数", "case_pair_id": "P12", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "not_established", "predicted_label_raw": "not_established", "predicted_basis": "invalid", "parse_status": "fenced_json", "verdict_correct": true, "basis_correct": false, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "2962c542b22b8529c80682c9d22e769a2267ae97753b62bcfecc9ae4fd62fd2f"}

## P17b / 指定奖项记录与人物背景 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：材料中爱因斯坦这条物理学奖记录的年份是1937年。

```text
{
  "verdict": "supported",
  "basis": "M1"
}
```

冻结预期：{"verdict": "refuted", "basis": "M1"}
自动检查：{"id": "P17b", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G07", "topic_name": "指定奖项记录与人物背景", "case_pair_id": "P17", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "38509530eca54c578f5f25f72627214308c8545f7a665bb2640cc725747ff6e5"}

## P13b / 多人贡献与未提供人物信息 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。

目标陈述：材料将电灯发展描述为多位发明者的贡献。

```text
{
  "verdict": "supported",
  "basis": "M1"
}
```

冻结预期：{"verdict": "supported", "basis": "M1"}
自动检查：{"id": "P13b", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G08", "topic_name": "多人贡献与未提供人物信息", "case_pair_id": "P13", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": true, "strict_task_passed": true, "truncated": false, "content_sha256": "f7052cc983b96fddbc372203a23f8a42c2010406596f8a4a13bc19ed47b9e674"}

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
  "basis": "none"
}
```
````

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P05a", "mode": "compact__free", "policy": "compact", "decoder": "free", "contrast_group": "G05", "topic_name": "给定名单与研究范围", "case_pair_id": "P05", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "none", "parse_status": "fenced_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": false, "strict_task_passed": false, "truncated": false, "content_sha256": "8eafa0932119c3136d60bde5c370c6a67c3dae49c6e6cb23813be7a47084de9d"}
