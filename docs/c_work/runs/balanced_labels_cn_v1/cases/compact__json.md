# compact__json

自动规则检查，未完成人工复核。

## P01a / 太阳类别与未提供物理量 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。
M2：NASA资料整理记录：太阳是太阳系中唯一的恒星，太阳不是行星。

目标陈述：太阳系中只有一颗恒星，即太阳。

```text
{"verdict":"支持","basis":"M1"}
```

冻结预期：{"verdict": "支持", "basis": "M2"}
自动检查：{"id": "P01a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G06", "topic_name": "太阳类别与未提供物理量", "case_pair_id": "P01", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "支持", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "39795bea0f49f7284557667ecfc84e5a9a13abe7a724b8fdc114c802a4df7848"}

## P11a / 多人贡献与未提供人物信息 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。

目标陈述：材料将电灯发展的全部贡献归给爱迪生一个人。

```text
{"verdict":"不足","basis":"M2"}
```

冻结预期：{"verdict": "反驳", "basis": "M1"}
自动检查：{"id": "P11a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G08", "topic_name": "多人贡献与未提供人物信息", "case_pair_id": "P11", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "反驳", "expected_basis": "M1", "predicted_verdict": "not_established", "predicted_label_raw": "不足", "predicted_basis": "M2", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "4884377e4d2a2304521a616eda93b9257ed5d058621e6ec671c686dda16f3180"}

## P17a / 指定奖项记录与人物背景 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。

目标陈述：材料中爱因斯坦这条物理学奖记录的年份是1937年。

```text
{"verdict":"支持","basis":"M2"}
```

冻结预期：{"verdict": "反驳", "basis": "M2"}
自动检查：{"id": "P17a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G07", "topic_name": "指定奖项记录与人物背景", "case_pair_id": "P17", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "反驳", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M2", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "0179dc9a8f5c4c41574ec4477c5abb35c51e0e1bae18a0f20e7c86ec03c5a85f"}

## P02a / 人员存在与获奖身份 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。
M2：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。

目标陈述：刘建平曾获得诺贝尔化学奖。

```text
{"verdict":"支持","basis":"M1"}
```

冻结预期：{"verdict": "不足", "basis": "none"}
自动检查：{"id": "P02a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G03", "topic_name": "人员存在与获奖身份", "case_pair_id": "P02", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "不足", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "b8777802287ca16569992f8f783bb5be3bec77a9f455b7a6c83942b23d848593"}

## P08b / 任职学院与获奖身份 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。
M2：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。

目标陈述：陈晓东这条目录记录所列的任职学院是经济学院。

```text
{"verdict":"不足","basis":"M2"}
```

冻结预期：{"verdict": "反驳", "basis": "M2"}
自动检查：{"id": "P08b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G02", "topic_name": "任职学院与获奖身份", "case_pair_id": "P08", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "反驳", "expected_basis": "M2", "predicted_verdict": "not_established", "predicted_label_raw": "不足", "predicted_basis": "M2", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "50f9b87776fb23de21fdf4d9bf59cae514c187b6e1e3abbde4db107bd3834985"}

## P10b / 任职学院与获奖身份 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。
M2：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。

目标陈述：陈晓东这条目录记录所列的任职学院是材料科学与工程学院。

```text
{"verdict":"支持","basis":"M1"}
```

冻结预期：{"verdict": "支持", "basis": "M1"}
自动检查：{"id": "P10b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G02", "topic_name": "任职学院与获奖身份", "case_pair_id": "P10", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "支持", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": true, "strict_task_passed": true, "truncated": false, "content_sha256": "8bdfb5ecafd01c86e8f2a72bfd37eca466508b7175bd8fe2b6932671abe28252"}

## P22a / 人员存在与获奖身份 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。
M2：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。

目标陈述：河南工业大学这份人员记录记载的姓名是王明远。

```text
{"verdict":"不足","basis":"M1"}
```

冻结预期：{"verdict": "反驳", "basis": "M2"}
自动检查：{"id": "P22a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G03", "topic_name": "人员存在与获奖身份", "case_pair_id": "P22", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "反驳", "expected_basis": "M2", "predicted_verdict": "not_established", "predicted_label_raw": "不足", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "9eb739ac07bb2e347192c49acd202831182ef6ff38409fe0b2114869aadcee37"}

## P04a / 给定名单与研究范围 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。
M2：本题给定的完整名单只有两个条目：浙江大学生物医学工程与仪器科学学院、浙江大学医学院。名单为教学任务选取的目录片段，不代表学校全部单位，也没有提供研究项目清单。

目标陈述：本题给定的名单列有脑机接口学院这一条目。

```text
{"verdict":"支持","basis":"M1"}
```

冻结预期：{"verdict": "反驳", "basis": "M2"}
自动检查：{"id": "P04a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G05", "topic_name": "给定名单与研究范围", "case_pair_id": "P04", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "反驳", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "6133ef125a12fd0a37f90bf2ce7c5a4dab03840f1565234aa271608849c62775"}

## P06a / 车型报告与未知参数 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：这份报告记录将YU7的发布日期写为2024年6月。

```text
{"verdict":"不足","basis":"M1"}
```

冻结预期：{"verdict": "反驳", "basis": "M1"}
自动检查：{"id": "P06a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G04", "topic_name": "车型报告与未知参数", "case_pair_id": "P06", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "反驳", "expected_basis": "M1", "predicted_verdict": "not_established", "predicted_label_raw": "不足", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "3bbc9843ad9fec655f1ea5468c8ea236cd333a9e9b269022e26a50bef0ba8041"}

## P10a / 任职学院与获奖身份 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。
M2：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。

目标陈述：陈晓东这条目录记录所列的任职学院是材料科学与工程学院。

```text
{"verdict":"支持","basis":"M2"}
```

冻结预期：{"verdict": "支持", "basis": "M2"}
自动检查：{"id": "P10a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G02", "topic_name": "任职学院与获奖身份", "case_pair_id": "P10", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "支持", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M2", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": true, "strict_task_passed": true, "truncated": false, "content_sha256": "02a4e1c047f745cf682281367a8e60acfacd4f83a7876f21ff2f5e509fa103cb"}

## P14a / 人员存在与获奖身份 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。
M2：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。

目标陈述：河南工业大学这份人员记录记载了刘建平这一姓名。

```text
{"verdict":"支持","basis":"M1"}
```

冻结预期：{"verdict": "支持", "basis": "M1"}
自动检查：{"id": "P14a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G03", "topic_name": "人员存在与获奖身份", "case_pair_id": "P14", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "支持", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": true, "strict_task_passed": true, "truncated": false, "content_sha256": "17998ef739eb9027422da9c8469bd4bf3ff6d6b9789350e03789f97790eac2a7"}

## P01b / 太阳类别与未提供物理量 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：NASA资料整理记录：太阳是太阳系中唯一的恒星，太阳不是行星。
M2：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。

目标陈述：太阳系中只有一颗恒星，即太阳。

```text
{"verdict":"支持","basis":"M1"}
```

冻结预期：{"verdict": "支持", "basis": "M1"}
自动检查：{"id": "P01b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G06", "topic_name": "太阳类别与未提供物理量", "case_pair_id": "P01", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "支持", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": true, "strict_task_passed": true, "truncated": false, "content_sha256": "90c824642d794f5fdf9fd07d625ee8b9135996a564d1951aefe19897a01cf967"}

## P04b / 给定名单与研究范围 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：本题给定的完整名单只有两个条目：浙江大学生物医学工程与仪器科学学院、浙江大学医学院。名单为教学任务选取的目录片段，不代表学校全部单位，也没有提供研究项目清单。
M2：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。

目标陈述：本题给定的名单列有脑机接口学院这一条目。

```text
{"verdict":"不足","basis":"M1"}
```

冻结预期：{"verdict": "反驳", "basis": "M1"}
自动检查：{"id": "P04b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G05", "topic_name": "给定名单与研究范围", "case_pair_id": "P04", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "反驳", "expected_basis": "M1", "predicted_verdict": "not_established", "predicted_label_raw": "不足", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "bd0f7296c338621cf8696644f0c981bd91d86f7bb80719df2ebcb49eadc79ea9"}

## P16a / 人员姓名与具体贡献 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。
M2：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。

目标陈述：中国科学院国家天文台这份人员记录记载的姓名为王明远。

```text
{"verdict":"支持","basis":"M1"}
```

冻结预期：{"verdict": "支持", "basis": "M1"}
自动检查：{"id": "P16a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G01", "topic_name": "人员姓名与具体贡献", "case_pair_id": "P16", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "支持", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": true, "strict_task_passed": true, "truncated": false, "content_sha256": "ec72e41a6e45e565f6bbf54d364670647503b200770796509bc4009244a03582"}

## P12a / 车型报告与未知参数 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。

目标陈述：SU9的百公里加速时间为2.5秒。

```text
{"verdict":"不足","basis":"M1"}
```

冻结预期：{"verdict": "不足", "basis": "none"}
自动检查：{"id": "P12a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G04", "topic_name": "车型报告与未知参数", "case_pair_id": "P12", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "不足", "expected_basis": "none", "predicted_verdict": "not_established", "predicted_label_raw": "不足", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "807fa664656b42fe38c198a917bc226d53c0850862b213bf5958c6f8312e7914"}

## P18a / 多人贡献与未提供人物信息 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：斯旺出生于1828年。

```text
{"verdict":"不足","basis":"M2"}
```

冻结预期：{"verdict": "不足", "basis": "none"}
自动检查：{"id": "P18a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G08", "topic_name": "多人贡献与未提供人物信息", "case_pair_id": "P18", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "不足", "expected_basis": "none", "predicted_verdict": "not_established", "predicted_label_raw": "不足", "predicted_basis": "M2", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "5a0243796fcfb21bcf574e9fcc8ef6ffa328a3c505a3e7114ff27e0833a01131"}

## P03a / 太阳类别与未提供物理量 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。
M2：NASA资料整理记录：太阳是太阳系中唯一的恒星，太阳不是行星。

目标陈述：太阳的有效温度为5772K。

```text
{"verdict":"支持","basis":"M1"}
```

冻结预期：{"verdict": "不足", "basis": "none"}
自动检查：{"id": "P03a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G06", "topic_name": "太阳类别与未提供物理量", "case_pair_id": "P03", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "不足", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "f3bdc92cd8d666b8ae1cec81907f99b2458512571b8c5cb3f239f6ea75e4a502"}

## P23a / 太阳类别与未提供物理量 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：NASA资料整理记录：太阳是太阳系中唯一的恒星，太阳不是行星。
M2：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。

目标陈述：太阳属于行星而不属于恒星。

```text
{"verdict":"支持","basis":"M1"}
```

冻结预期：{"verdict": "反驳", "basis": "M1"}
自动检查：{"id": "P23a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G06", "topic_name": "太阳类别与未提供物理量", "case_pair_id": "P23", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "反驳", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "03f4a071bcd8d785bff0a226e6764a1609ee9221432eff9ee773aec3745a4d30"}

## P15a / 人员姓名与具体贡献 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。
M2：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。

目标陈述：王明远提出过一项新的相对论理论。

```text
{"verdict":"支持","basis":"M1"}
```

冻结预期：{"verdict": "不足", "basis": "none"}
自动检查：{"id": "P15a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G01", "topic_name": "人员姓名与具体贡献", "case_pair_id": "P15", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "不足", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "608de47537a39308e367840aa60bf4df73e1a8d4892299464a82cd45fa771b98"}

## P24b / 指定奖项记录与人物背景 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。

目标陈述：材料中爱因斯坦这条物理学奖记录的年份是1921年。

```text
{"verdict":"支持","basis":"M2"}
```

冻结预期：{"verdict": "支持", "basis": "M2"}
自动检查：{"id": "P24b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G07", "topic_name": "指定奖项记录与人物背景", "case_pair_id": "P24", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "支持", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M2", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": true, "strict_task_passed": true, "truncated": false, "content_sha256": "844002d4d815ee184f2fb9efa6a3eb49aeddbaebb6196d21e4168f8453688a7e"}

## P07a / 车型报告与未知参数 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。

目标陈述：这份报告记录将YU7定位为SUV。

```text
{"verdict":"不足","basis":"M2"}
```

冻结预期：{"verdict": "支持", "basis": "M2"}
自动检查：{"id": "P07a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G04", "topic_name": "车型报告与未知参数", "case_pair_id": "P07", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "支持", "expected_basis": "M2", "predicted_verdict": "not_established", "predicted_label_raw": "不足", "predicted_basis": "M2", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "de827c6f53a52135247e6637773ed70baa1292b046e2689c2a8a8913e54894d0"}

## P11b / 多人贡献与未提供人物信息 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：材料将电灯发展的全部贡献归给爱迪生一个人。

```text
{"verdict":"不足","basis":"M1"}
```

冻结预期：{"verdict": "反驳", "basis": "M2"}
自动检查：{"id": "P11b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G08", "topic_name": "多人贡献与未提供人物信息", "case_pair_id": "P11", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "反驳", "expected_basis": "M2", "predicted_verdict": "not_established", "predicted_label_raw": "不足", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "866c82d3f492d85134dd0a703b99329e34c243a0a3c77c78a2efdff53b27ec67"}

## P05b / 给定名单与研究范围 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。
M2：本题给定的完整名单只有两个条目：浙江大学生物医学工程与仪器科学学院、浙江大学医学院。名单为教学任务选取的目录片段，不代表学校全部单位，也没有提供研究项目清单。

目标陈述：浙江大学完全没有脑机接口相关研究。

```text
{"verdict":"支持","basis":"M1"}
```

冻结预期：{"verdict": "不足", "basis": "none"}
自动检查：{"id": "P05b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G05", "topic_name": "给定名单与研究范围", "case_pair_id": "P05", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "不足", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "fe7c2d2d5eb2f5028807affcfd29c65b8d82a1e19726a8851dd3ae0480643106"}

## P21b / 指定奖项记录与人物背景 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。

目标陈述：爱因斯坦的出生年份是1879年。

```text
{"verdict":"支持","basis":"M1"}
```

冻结预期：{"verdict": "不足", "basis": "none"}
自动检查：{"id": "P21b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G07", "topic_name": "指定奖项记录与人物背景", "case_pair_id": "P21", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "不足", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "08dc58ae23aef2a6b67a29e4582039ac9de645f03f79e22dc1987da04f5fb912"}

## P23b / 太阳类别与未提供物理量 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。
M2：NASA资料整理记录：太阳是太阳系中唯一的恒星，太阳不是行星。

目标陈述：太阳属于行星而不属于恒星。

```text
{"verdict":"支持","basis":"M1"}
```

冻结预期：{"verdict": "反驳", "basis": "M2"}
自动检查：{"id": "P23b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G06", "topic_name": "太阳类别与未提供物理量", "case_pair_id": "P23", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "反驳", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "f27c93420a727a43b3e4b7798b2352bc45733df539d274904d7251bd3d81fb3d"}

## P03b / 太阳类别与未提供物理量 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：NASA资料整理记录：太阳是太阳系中唯一的恒星，太阳不是行星。
M2：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。

目标陈述：太阳的有效温度为5772K。

```text
{"verdict":"支持","basis":"M1"}
```

冻结预期：{"verdict": "不足", "basis": "none"}
自动检查：{"id": "P03b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G06", "topic_name": "太阳类别与未提供物理量", "case_pair_id": "P03", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "不足", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "c1d70b106c2ea1504b93178f52b9cb2a93fb132058d9ffa65355cbf918ab4b71"}

## P15b / 人员姓名与具体贡献 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。
M2：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。

目标陈述：王明远提出过一项新的相对论理论。

```text
{"verdict":"支持","basis":"M2"}
```

冻结预期：{"verdict": "不足", "basis": "none"}
自动检查：{"id": "P15b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G01", "topic_name": "人员姓名与具体贡献", "case_pair_id": "P15", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "不足", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M2", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "c9f0ed0f9ad0026a7c607333dcadf34cedacd4131783b00f5e22bc7f0ffa394b"}

## P06b / 车型报告与未知参数 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。

目标陈述：这份报告记录将YU7的发布日期写为2024年6月。

```text
{"verdict":"不足","basis":"M2"}
```

冻结预期：{"verdict": "反驳", "basis": "M2"}
自动检查：{"id": "P06b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G04", "topic_name": "车型报告与未知参数", "case_pair_id": "P06", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "反驳", "expected_basis": "M2", "predicted_verdict": "not_established", "predicted_label_raw": "不足", "predicted_basis": "M2", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "9addc0bc444a114bd3bff81400a77dc50513eed69f16fddb24319df09b30bc85"}

## P13a / 多人贡献与未提供人物信息 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：材料将电灯发展描述为多位发明者的贡献。

```text
{"verdict":"支持","basis":"M1"}
```

冻结预期：{"verdict": "支持", "basis": "M2"}
自动检查：{"id": "P13a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G08", "topic_name": "多人贡献与未提供人物信息", "case_pair_id": "P13", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "支持", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "49166789ff8d6ee751866c2966fac1b2b59688fba12ac43f481f58866fefa92e"}

## P19a / 人员姓名与具体贡献 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。
M2：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。

目标陈述：中国科学院国家天文台这份人员记录记载的姓名为李华。

```text
{"verdict":"不足","basis":"M1"}
```

冻结预期：{"verdict": "反驳", "basis": "M2"}
自动检查：{"id": "P19a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G01", "topic_name": "人员姓名与具体贡献", "case_pair_id": "P19", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "反驳", "expected_basis": "M2", "predicted_verdict": "not_established", "predicted_label_raw": "不足", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "f0aaa4a7ebd30ea5a39c41971845779f9c0ef90fc67087799c3396f9c6bf875b"}

## P20b / 给定名单与研究范围 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。
M2：本题给定的完整名单只有两个条目：浙江大学生物医学工程与仪器科学学院、浙江大学医学院。名单为教学任务选取的目录片段，不代表学校全部单位，也没有提供研究项目清单。

目标陈述：本题给定的名单列有浙江大学医学院。

```text
{"verdict":"支持","basis":"M2"}
```

冻结预期：{"verdict": "支持", "basis": "M2"}
自动检查：{"id": "P20b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G05", "topic_name": "给定名单与研究范围", "case_pair_id": "P20", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "支持", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M2", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": true, "strict_task_passed": true, "truncated": false, "content_sha256": "03f3cff028b775a8cee60d325b02ea1e34fbdf4df35468f8fbba27997956976b"}

## P02b / 人员存在与获奖身份 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。
M2：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。

目标陈述：刘建平曾获得诺贝尔化学奖。

```text
{"verdict":"支持","basis":"M2"}
```

冻结预期：{"verdict": "不足", "basis": "none"}
自动检查：{"id": "P02b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G03", "topic_name": "人员存在与获奖身份", "case_pair_id": "P02", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "不足", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M2", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "57b4491dd98689c8bd1b17aae030570a3a35ee61f9717190e43e45bd8bf83107"}

## P09a / 任职学院与获奖身份 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。
M2：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。

目标陈述：陈晓东曾获得诺贝尔物理学奖。

```text
{"verdict":"不足","basis":"M2"}
```

冻结预期：{"verdict": "不足", "basis": "none"}
自动检查：{"id": "P09a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G02", "topic_name": "任职学院与获奖身份", "case_pair_id": "P09", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "不足", "expected_basis": "none", "predicted_verdict": "not_established", "predicted_label_raw": "不足", "predicted_basis": "M2", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "327815b50c5a3e2bd25922d79f30bd508a9c3d9680fcb077d69db3ba90004edd"}

## P24a / 指定奖项记录与人物背景 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：材料中爱因斯坦这条物理学奖记录的年份是1921年。

```text
{"verdict":"支持","basis":"M1"}
```

冻结预期：{"verdict": "支持", "basis": "M1"}
自动检查：{"id": "P24a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G07", "topic_name": "指定奖项记录与人物背景", "case_pair_id": "P24", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "支持", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": true, "strict_task_passed": true, "truncated": false, "content_sha256": "f80b4bdd163df4c06941b2f0622d271f92aa5a669e84b26843c5c47d4543c488"}

## P07b / 车型报告与未知参数 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：这份报告记录将YU7定位为SUV。

```text
{"verdict":"支持","basis":"M1"}
```

冻结预期：{"verdict": "支持", "basis": "M1"}
自动检查：{"id": "P07b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G04", "topic_name": "车型报告与未知参数", "case_pair_id": "P07", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "支持", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": true, "strict_task_passed": true, "truncated": false, "content_sha256": "f31879f3869ef5a70ac7d5569b4d34c531f47309f3b50d7940563de65dfb9d01"}

## P16b / 人员姓名与具体贡献 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。
M2：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。

目标陈述：中国科学院国家天文台这份人员记录记载的姓名为王明远。

```text
{"verdict":"支持","basis":"M2"}
```

冻结预期：{"verdict": "支持", "basis": "M2"}
自动检查：{"id": "P16b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G01", "topic_name": "人员姓名与具体贡献", "case_pair_id": "P16", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "支持", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M2", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": true, "strict_task_passed": true, "truncated": false, "content_sha256": "acd524e2c1cebcbe9b7dcdfe33456e37b81fa8d7960cf5871a392be127570fd3"}

## P21a / 指定奖项记录与人物背景 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：爱因斯坦的出生年份是1879年。

```text
{"verdict":"支持","basis":"M1"}
```

冻结预期：{"verdict": "不足", "basis": "none"}
自动检查：{"id": "P21a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G07", "topic_name": "指定奖项记录与人物背景", "case_pair_id": "P21", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "不足", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "8820e651ffb6bf45e8c91453899e57176d901edbade240316f153195a1f0b1a9"}

## P19b / 人员姓名与具体贡献 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。
M2：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。

目标陈述：中国科学院国家天文台这份人员记录记载的姓名为李华。

```text
{"verdict":"不足","basis":"M1"}
```

冻结预期：{"verdict": "反驳", "basis": "M1"}
自动检查：{"id": "P19b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G01", "topic_name": "人员姓名与具体贡献", "case_pair_id": "P19", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "反驳", "expected_basis": "M1", "predicted_verdict": "not_established", "predicted_label_raw": "不足", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "e35044bd0568aebe31defb4ae5de175e5d312887849bb70dc03696918856dee6"}

## P09b / 任职学院与获奖身份 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。
M2：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。

目标陈述：陈晓东曾获得诺贝尔物理学奖。

```text
{"verdict":"不足","basis":"M1"}
```

冻结预期：{"verdict": "不足", "basis": "none"}
自动检查：{"id": "P09b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G02", "topic_name": "任职学院与获奖身份", "case_pair_id": "P09", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "不足", "expected_basis": "none", "predicted_verdict": "not_established", "predicted_label_raw": "不足", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "ec192ec95d29eb676c2b2068389faddfeb194bcc1871773375ba0c846bd38150"}

## P18b / 多人贡献与未提供人物信息 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。

目标陈述：斯旺出生于1828年。

```text
{"verdict":"支持","basis":"M2"}
```

冻结预期：{"verdict": "不足", "basis": "none"}
自动检查：{"id": "P18b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G08", "topic_name": "多人贡献与未提供人物信息", "case_pair_id": "P18", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "不足", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M2", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "26c2f1d80560d52867205e252491c42ded9a26c13152039fddf15133fef1f653"}

## P08a / 任职学院与获奖身份 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。
M2：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。

目标陈述：陈晓东这条目录记录所列的任职学院是经济学院。

```text
{"verdict":"不足","basis":"M1"}
```

冻结预期：{"verdict": "反驳", "basis": "M1"}
自动检查：{"id": "P08a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G02", "topic_name": "任职学院与获奖身份", "case_pair_id": "P08", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "反驳", "expected_basis": "M1", "predicted_verdict": "not_established", "predicted_label_raw": "不足", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "ab338dfba825927064ce225388d961a26714c49dd5b9f9e1eb3cd67f423046fe"}

## P22b / 人员存在与获奖身份 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。
M2：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。

目标陈述：河南工业大学这份人员记录记载的姓名是王明远。

```text
{"verdict":"不足","basis":"M1"}
```

冻结预期：{"verdict": "反驳", "basis": "M1"}
自动检查：{"id": "P22b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G03", "topic_name": "人员存在与获奖身份", "case_pair_id": "P22", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "反驳", "expected_basis": "M1", "predicted_verdict": "not_established", "predicted_label_raw": "不足", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "16085697d133b4c1c8ada9a255d8f631be50abce65c504aa3988fa17c1ce3824"}

## P14b / 人员存在与获奖身份 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。
M2：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。

目标陈述：河南工业大学这份人员记录记载了刘建平这一姓名。

```text
{"verdict":"支持","basis":"M2"}
```

冻结预期：{"verdict": "支持", "basis": "M2"}
自动检查：{"id": "P14b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G03", "topic_name": "人员存在与获奖身份", "case_pair_id": "P14", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "支持", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M2", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": true, "strict_task_passed": true, "truncated": false, "content_sha256": "1e20fc9556323fce6a7647ffcc81ac00ba5db386e7ad4125f2bb00e043727422"}

## P20a / 给定名单与研究范围 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：本题给定的完整名单只有两个条目：浙江大学生物医学工程与仪器科学学院、浙江大学医学院。名单为教学任务选取的目录片段，不代表学校全部单位，也没有提供研究项目清单。
M2：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。

目标陈述：本题给定的名单列有浙江大学医学院。

```text
{"verdict":"支持","basis":"M1"}
```

冻结预期：{"verdict": "支持", "basis": "M1"}
自动检查：{"id": "P20a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G05", "topic_name": "给定名单与研究范围", "case_pair_id": "P20", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "支持", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": true, "strict_task_passed": true, "truncated": false, "content_sha256": "b927a1a87b7e35e19c23ae73de6f51ff7caf9f66ebaea3e09ffc0138fc715834"}

## P12b / 车型报告与未知参数 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：SU9的百公里加速时间为2.5秒。

```text
{"verdict":"不足","basis":"M1"}
```

冻结预期：{"verdict": "不足", "basis": "none"}
自动检查：{"id": "P12b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G04", "topic_name": "车型报告与未知参数", "case_pair_id": "P12", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "不足", "expected_basis": "none", "predicted_verdict": "not_established", "predicted_label_raw": "不足", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "24d652f803fbf6aeb9df358955c78df7caad24984956881c75628e14478457f3"}

## P17b / 指定奖项记录与人物背景 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：材料中爱因斯坦这条物理学奖记录的年份是1937年。

```text
{"verdict":"不足","basis":"M1"}
```

冻结预期：{"verdict": "反驳", "basis": "M1"}
自动检查：{"id": "P17b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G07", "topic_name": "指定奖项记录与人物背景", "case_pair_id": "P17", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "反驳", "expected_basis": "M1", "predicted_verdict": "not_established", "predicted_label_raw": "不足", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "373c995b39783a4f2ee57003a9e37a00f132e3d038161c5e050a31ddd071348a"}

## P13b / 多人贡献与未提供人物信息 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。

目标陈述：材料将电灯发展描述为多位发明者的贡献。

```text
{"verdict":"支持","basis":"M1"}
```

冻结预期：{"verdict": "支持", "basis": "M1"}
自动检查：{"id": "P13b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G08", "topic_name": "多人贡献与未提供人物信息", "case_pair_id": "P13", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "支持", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": true, "strict_task_passed": true, "truncated": false, "content_sha256": "43be3795b6ebe4ffa71e4711a0d49ab576596073b3c62244610c771ab9360d32"}

## P05a / 给定名单与研究范围 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取支持、反驳、不足：材料足以推出目标陈述时取支持；材料存在明确相反事实或与本题完整名单冲突时取反驳；两者都不能推出时取不足。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：本题给定的完整名单只有两个条目：浙江大学生物医学工程与仪器科学学院、浙江大学医学院。名单为教学任务选取的目录片段，不代表学校全部单位，也没有提供研究项目清单。
M2：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。

目标陈述：浙江大学完全没有脑机接口相关研究。

```text
{"verdict":"支持","basis":"M1"}
```

冻结预期：{"verdict": "不足", "basis": "none"}
自动检查：{"id": "P05a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G05", "topic_name": "给定名单与研究范围", "case_pair_id": "P05", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "不足", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "支持", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "01ed823e8e243baf7ecbcbd96e4c2017f576f69726e4945c726813b5fa04573c"}
