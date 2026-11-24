# compact__json

自动规则检查，未完成人工复核。

## P01a / 太阳类别与未提供物理量 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。
M2：NASA资料整理记录：太阳是太阳系中唯一的恒星，太阳不是行星。

目标陈述：太阳系中只有一颗恒星，即太阳。

```text
{"verdict":"supported","basis":"M1"}
```

冻结预期：{"verdict": "supported", "basis": "M2"}
自动检查：{"id": "P01a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G06", "topic_name": "太阳类别与未提供物理量", "case_pair_id": "P01", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "3f515a0ca5f7b966b42c7b94dcc631b398827a545b68024b634a882a25e846cf"}

## P11a / 多人贡献与未提供人物信息 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。

目标陈述：材料将电灯发展的全部贡献归给爱迪生一个人。

```text
{"verdict":"supported","basis":"none"}
```

冻结预期：{"verdict": "refuted", "basis": "M1"}
自动检查：{"id": "P11a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G08", "topic_name": "多人贡献与未提供人物信息", "case_pair_id": "P11", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "none", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "a3d163730f1b22b0c969865066a2d643347ade0378f66e982fb59b1f9a4fe2ff"}

## P17a / 指定奖项记录与人物背景 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。

目标陈述：材料中爱因斯坦这条物理学奖记录的年份是1937年。

```text
{"verdict":"supported","basis":"M2"}
```

冻结预期：{"verdict": "refuted", "basis": "M2"}
自动检查：{"id": "P17a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G07", "topic_name": "指定奖项记录与人物背景", "case_pair_id": "P17", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M2", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "e3ee372da4671ecce64374afdb9a55ba3b5b8abde9c6c24032189a59cba7894d"}

## P02a / 人员存在与获奖身份 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。
M2：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。

目标陈述：刘建平曾获得诺贝尔化学奖。

```text
{"verdict":"supported","basis":"M1"}
```

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P02a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G03", "topic_name": "人员存在与获奖身份", "case_pair_id": "P02", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "4e5eaed2665d31530276a30b05f330786f1a75bf6584d1a9e16de60934f6bb83"}

## P08b / 任职学院与获奖身份 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。
M2：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。

目标陈述：陈晓东这条目录记录所列的任职学院是经济学院。

```text
{"verdict":"supported","basis":"none"}
```

冻结预期：{"verdict": "refuted", "basis": "M2"}
自动检查：{"id": "P08b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G02", "topic_name": "任职学院与获奖身份", "case_pair_id": "P08", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "none", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "ffe6b20835667ec51bb93973c74c21afa16a147351b2c79d765576239830a0db"}

## P10b / 任职学院与获奖身份 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。
M2：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。

目标陈述：陈晓东这条目录记录所列的任职学院是材料科学与工程学院。

```text
{"verdict":"supported","basis":"M1"}
```

冻结预期：{"verdict": "supported", "basis": "M1"}
自动检查：{"id": "P10b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G02", "topic_name": "任职学院与获奖身份", "case_pair_id": "P10", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": true, "strict_task_passed": true, "truncated": false, "content_sha256": "52ca59b9b71bdbecf7b3cb1a02159673a319b502f6a0c3bd9fbb51bfe9e5e389"}

## P22a / 人员存在与获奖身份 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。
M2：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。

目标陈述：河南工业大学这份人员记录记载的姓名是王明远。

```text
{"verdict":"supported","basis":"none"}
```

冻结预期：{"verdict": "refuted", "basis": "M2"}
自动检查：{"id": "P22a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G03", "topic_name": "人员存在与获奖身份", "case_pair_id": "P22", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "none", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "add982a96131e63e46ab7e720433f045d72502ec2dd95cb634589ed8695fc947"}

## P04a / 给定名单与研究范围 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。
M2：本题给定的完整名单只有两个条目：浙江大学生物医学工程与仪器科学学院、浙江大学医学院。名单为教学任务选取的目录片段，不代表学校全部单位，也没有提供研究项目清单。

目标陈述：本题给定的名单列有脑机接口学院这一条目。

```text
{"verdict":"not_established","basis":"none"}
```

冻结预期：{"verdict": "refuted", "basis": "M2"}
自动检查：{"id": "P04a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G05", "topic_name": "给定名单与研究范围", "case_pair_id": "P04", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M2", "predicted_verdict": "not_established", "predicted_label_raw": "not_established", "predicted_basis": "none", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "bb7c88b022de65f1eee6a1213d0110e8053d6f311d57eecd98da0ed38faabeb9"}

## P06a / 车型报告与未知参数 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：这份报告记录将YU7的发布日期写为2024年6月。

```text
{"verdict":"supported","basis":"M1"}
```

冻结预期：{"verdict": "refuted", "basis": "M1"}
自动检查：{"id": "P06a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G04", "topic_name": "车型报告与未知参数", "case_pair_id": "P06", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "b40802c4496e44080127083f315a5a932f10f6dfa92e0c2d990a962feb3f223f"}

## P10a / 任职学院与获奖身份 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。
M2：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。

目标陈述：陈晓东这条目录记录所列的任职学院是材料科学与工程学院。

```text
{"verdict":"supported","basis":"none"}
```

冻结预期：{"verdict": "supported", "basis": "M2"}
自动检查：{"id": "P10a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G02", "topic_name": "任职学院与获奖身份", "case_pair_id": "P10", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "none", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "568bc7925a7032a904d34a62d113fd31f97e3d40d6e785486c38f4c1f7b7efa9"}

## P14a / 人员存在与获奖身份 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。
M2：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。

目标陈述：河南工业大学这份人员记录记载了刘建平这一姓名。

```text
{"verdict":"supported","basis":"M1"}
```

冻结预期：{"verdict": "supported", "basis": "M1"}
自动检查：{"id": "P14a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G03", "topic_name": "人员存在与获奖身份", "case_pair_id": "P14", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": true, "strict_task_passed": true, "truncated": false, "content_sha256": "8562f0878a9d11152a1da4f5566c89f7236be73edc1be6c1ff780f0402ac558a"}

## P01b / 太阳类别与未提供物理量 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：NASA资料整理记录：太阳是太阳系中唯一的恒星，太阳不是行星。
M2：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。

目标陈述：太阳系中只有一颗恒星，即太阳。

```text
{"verdict":"supported","basis":"M1"}
```

冻结预期：{"verdict": "supported", "basis": "M1"}
自动检查：{"id": "P01b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G06", "topic_name": "太阳类别与未提供物理量", "case_pair_id": "P01", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": true, "strict_task_passed": true, "truncated": false, "content_sha256": "cc1dcb8f92a7ee1e041edd0e7f18ea3c9515dea9d620be35ef5ca274136e0eba"}

## P04b / 给定名单与研究范围 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：本题给定的完整名单只有两个条目：浙江大学生物医学工程与仪器科学学院、浙江大学医学院。名单为教学任务选取的目录片段，不代表学校全部单位，也没有提供研究项目清单。
M2：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。

目标陈述：本题给定的名单列有脑机接口学院这一条目。

```text
{"verdict":"not_established","basis":"none"}
```

冻结预期：{"verdict": "refuted", "basis": "M1"}
自动检查：{"id": "P04b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G05", "topic_name": "给定名单与研究范围", "case_pair_id": "P04", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M1", "predicted_verdict": "not_established", "predicted_label_raw": "not_established", "predicted_basis": "none", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "7496b5ab9c0cc45c4c9b56ad7ccbc2e3039b04fc473d175af74fe0546d617439"}

## P16a / 人员姓名与具体贡献 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。
M2：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。

目标陈述：中国科学院国家天文台这份人员记录记载的姓名为王明远。

```text
{"verdict":"supported","basis":"M1"}
```

冻结预期：{"verdict": "supported", "basis": "M1"}
自动检查：{"id": "P16a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G01", "topic_name": "人员姓名与具体贡献", "case_pair_id": "P16", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": true, "strict_task_passed": true, "truncated": false, "content_sha256": "aa70e77ddb662661fee4634181d0795419670081ef9d699c3dfbf02a1c8adb52"}

## P12a / 车型报告与未知参数 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。

目标陈述：SU9的百公里加速时间为2.5秒。

```text
{"verdict":"supported","basis":"M1"}
```

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P12a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G04", "topic_name": "车型报告与未知参数", "case_pair_id": "P12", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "646002825894d67e3ada42e653ecd16db1ab3b3162816fc3c4a437d84ed7d64d"}

## P18a / 多人贡献与未提供人物信息 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：斯旺出生于1828年。

```text
{"verdict":"supported","basis":"none"}
```

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P18a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G08", "topic_name": "多人贡献与未提供人物信息", "case_pair_id": "P18", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "none", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "3b7c0e4db865d9e6748001600bb635a492407f967806f0264ba8bd142f5735c3"}

## P03a / 太阳类别与未提供物理量 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。
M2：NASA资料整理记录：太阳是太阳系中唯一的恒星，太阳不是行星。

目标陈述：太阳的有效温度为5772K。

```text
{"verdict":"supported","basis":"M1"}
```

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P03a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G06", "topic_name": "太阳类别与未提供物理量", "case_pair_id": "P03", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "1c64e8e7a4f11070814e9ae09b669b8fb6851878614315f577f0d72ab8d76dfb"}

## P23a / 太阳类别与未提供物理量 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：NASA资料整理记录：太阳是太阳系中唯一的恒星，太阳不是行星。
M2：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。

目标陈述：太阳属于行星而不属于恒星。

```text
{"verdict":"supported","basis":"M1"}
```

冻结预期：{"verdict": "refuted", "basis": "M1"}
自动检查：{"id": "P23a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G06", "topic_name": "太阳类别与未提供物理量", "case_pair_id": "P23", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "15bfecee5239c842d884a5515ba091e7f901e2921d5789cc17cd45ee2b5acbe2"}

## P15a / 人员姓名与具体贡献 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。
M2：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。

目标陈述：王明远提出过一项新的相对论理论。

```text
{"verdict":"supported","basis":"M1"}
```

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P15a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G01", "topic_name": "人员姓名与具体贡献", "case_pair_id": "P15", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "6a0f182692bb470f6ce9354c3261162fab4303cbcafe9d41f347680366e34782"}

## P24b / 指定奖项记录与人物背景 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。

目标陈述：材料中爱因斯坦这条物理学奖记录的年份是1921年。

```text
{"verdict":"supported","basis":"M2"}
```

冻结预期：{"verdict": "supported", "basis": "M2"}
自动检查：{"id": "P24b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G07", "topic_name": "指定奖项记录与人物背景", "case_pair_id": "P24", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M2", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": true, "strict_task_passed": true, "truncated": false, "content_sha256": "654f827d138046001bc94ddbf52dffb256da9d3d2efb804cdff0595401e25392"}

## P07a / 车型报告与未知参数 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。

目标陈述：这份报告记录将YU7定位为SUV。

```text
{"verdict":"supported","basis":"M2"}
```

冻结预期：{"verdict": "supported", "basis": "M2"}
自动检查：{"id": "P07a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G04", "topic_name": "车型报告与未知参数", "case_pair_id": "P07", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M2", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": true, "strict_task_passed": true, "truncated": false, "content_sha256": "b56f691feca7bd8b8274b51323c45a09c70941e03db67ebe33176880e3932f2e"}

## P11b / 多人贡献与未提供人物信息 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：材料将电灯发展的全部贡献归给爱迪生一个人。

```text
{"verdict":"supported","basis":"M1"}
```

冻结预期：{"verdict": "refuted", "basis": "M2"}
自动检查：{"id": "P11b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G08", "topic_name": "多人贡献与未提供人物信息", "case_pair_id": "P11", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "e36d8bc7129e35b1946d98dbe3362a0353515a920a11db7a966f80b39e45544d"}

## P05b / 给定名单与研究范围 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。
M2：本题给定的完整名单只有两个条目：浙江大学生物医学工程与仪器科学学院、浙江大学医学院。名单为教学任务选取的目录片段，不代表学校全部单位，也没有提供研究项目清单。

目标陈述：浙江大学完全没有脑机接口相关研究。

```text
{"verdict":"supported","basis":"M1"}
```

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P05b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G05", "topic_name": "给定名单与研究范围", "case_pair_id": "P05", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "49d4afcfa523e8d3a3105b42bb6156b964fa305353bfc5a13ebf6a6ed8350a4f"}

## P21b / 指定奖项记录与人物背景 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。

目标陈述：爱因斯坦的出生年份是1879年。

```text
{"verdict":"supported","basis":"M1"}
```

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P21b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G07", "topic_name": "指定奖项记录与人物背景", "case_pair_id": "P21", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "6d02ea705942c54829c16cdb15f45f0b1faebce78e0144dbf95d936b654a2962"}

## P23b / 太阳类别与未提供物理量 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。
M2：NASA资料整理记录：太阳是太阳系中唯一的恒星，太阳不是行星。

目标陈述：太阳属于行星而不属于恒星。

```text
{"verdict":"supported","basis":"M1"}
```

冻结预期：{"verdict": "refuted", "basis": "M2"}
自动检查：{"id": "P23b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G06", "topic_name": "太阳类别与未提供物理量", "case_pair_id": "P23", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "4a06a60e84739c2cae12fc53f9fa2f45f145857fd614d86061bcf9d5ce9a0b3a"}

## P03b / 太阳类别与未提供物理量 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：NASA资料整理记录：太阳是太阳系中唯一的恒星，太阳不是行星。
M2：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。

目标陈述：太阳的有效温度为5772K。

```text
{"verdict":"supported","basis":"M1"}
```

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P03b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G06", "topic_name": "太阳类别与未提供物理量", "case_pair_id": "P03", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "c5f88b591f67668f831fe780e10d513dce1d9b90bd41db3781bd0e1e638536aa"}

## P15b / 人员姓名与具体贡献 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。
M2：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。

目标陈述：王明远提出过一项新的相对论理论。

```text
{"verdict":"supported","basis":"none"}
```

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P15b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G01", "topic_name": "人员姓名与具体贡献", "case_pair_id": "P15", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "none", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "4d59735428569077d05e3b344207f2437a06b2bec37ad9d6b7d2b2ab5bf68bf4"}

## P06b / 车型报告与未知参数 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。

目标陈述：这份报告记录将YU7的发布日期写为2024年6月。

```text
{"verdict":"supported","basis":"M2"}
```

冻结预期：{"verdict": "refuted", "basis": "M2"}
自动检查：{"id": "P06b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G04", "topic_name": "车型报告与未知参数", "case_pair_id": "P06", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M2", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "ed14a036ea52336223a22b5679c1f0109c8b7a5f67361e10d70e7639c5f811e6"}

## P13a / 多人贡献与未提供人物信息 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：材料将电灯发展描述为多位发明者的贡献。

```text
{"verdict":"supported","basis":"M1"}
```

冻结预期：{"verdict": "supported", "basis": "M2"}
自动检查：{"id": "P13a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G08", "topic_name": "多人贡献与未提供人物信息", "case_pair_id": "P13", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "af6d2921fa7a6aa66bb134e2d3d136422792e27f5259e9ad6b0cb0fe49cba02b"}

## P19a / 人员姓名与具体贡献 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。
M2：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。

目标陈述：中国科学院国家天文台这份人员记录记载的姓名为李华。

```text
{"verdict":"supported","basis":"none"}
```

冻结预期：{"verdict": "refuted", "basis": "M2"}
自动检查：{"id": "P19a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G01", "topic_name": "人员姓名与具体贡献", "case_pair_id": "P19", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "none", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "c9e5b6b24601d72e1a42ff39e903207d9abe198886dd7e47a6ac56c78e5dbbe0"}

## P20b / 给定名单与研究范围 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。
M2：本题给定的完整名单只有两个条目：浙江大学生物医学工程与仪器科学学院、浙江大学医学院。名单为教学任务选取的目录片段，不代表学校全部单位，也没有提供研究项目清单。

目标陈述：本题给定的名单列有浙江大学医学院。

```text
{"verdict":"supported","basis":"M2"}
```

冻结预期：{"verdict": "supported", "basis": "M2"}
自动检查：{"id": "P20b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G05", "topic_name": "给定名单与研究范围", "case_pair_id": "P20", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M2", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": true, "strict_task_passed": true, "truncated": false, "content_sha256": "1744194c09cdec55784a3997f75eb5fadf16a445f558b37ac3ce60bc91cdd2b4"}

## P02b / 人员存在与获奖身份 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。
M2：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。

目标陈述：刘建平曾获得诺贝尔化学奖。

```text
{"verdict":"supported","basis":"M2"}
```

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P02b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G03", "topic_name": "人员存在与获奖身份", "case_pair_id": "P02", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M2", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "f7573e5e5a1193d535f4b4fee1e96fb82fb464f69fd12679b7bec79458ade4bb"}

## P09a / 任职学院与获奖身份 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。
M2：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。

目标陈述：陈晓东曾获得诺贝尔物理学奖。

```text
{"verdict":"supported","basis":"none"}
```

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P09a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G02", "topic_name": "任职学院与获奖身份", "case_pair_id": "P09", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "none", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "32d26c3c81a77dca47c96db99efc297f1b9c00ab34230891126b9053c3b413e3"}

## P24a / 指定奖项记录与人物背景 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：材料中爱因斯坦这条物理学奖记录的年份是1921年。

```text
{"verdict":"supported","basis":"M1"}
```

冻结预期：{"verdict": "supported", "basis": "M1"}
自动检查：{"id": "P24a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G07", "topic_name": "指定奖项记录与人物背景", "case_pair_id": "P24", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": true, "strict_task_passed": true, "truncated": false, "content_sha256": "6643f86563fc714d7cc5a688995106c5804bd203ba48ade4bd575b3061ef4714"}

## P07b / 车型报告与未知参数 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：这份报告记录将YU7定位为SUV。

```text
{"verdict":"supported","basis":"M1"}
```

冻结预期：{"verdict": "supported", "basis": "M1"}
自动检查：{"id": "P07b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G04", "topic_name": "车型报告与未知参数", "case_pair_id": "P07", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": true, "strict_task_passed": true, "truncated": false, "content_sha256": "64c51ca65faba928192053a1f08e53f1964438f2cce3654bdc11b4186f505cfb"}

## P16b / 人员姓名与具体贡献 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。
M2：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。

目标陈述：中国科学院国家天文台这份人员记录记载的姓名为王明远。

```text
{"verdict":"supported","basis":"none"}
```

冻结预期：{"verdict": "supported", "basis": "M2"}
自动检查：{"id": "P16b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G01", "topic_name": "人员姓名与具体贡献", "case_pair_id": "P16", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "none", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "f5a365d1ec6c570b11998738913c10cc574c3aa525767e959e9df1dba19192d9"}

## P21a / 指定奖项记录与人物背景 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：爱因斯坦的出生年份是1879年。

```text
{"verdict":"supported","basis":"M1"}
```

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P21a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G07", "topic_name": "指定奖项记录与人物背景", "case_pair_id": "P21", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "c0bb2d97dc8820a52914c0ea0549947c56a9e0d04d58da7177e520b7e8378cec"}

## P19b / 人员姓名与具体贡献 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。
M2：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。

目标陈述：中国科学院国家天文台这份人员记录记载的姓名为李华。

```text
{"verdict":"supported","basis":"none"}
```

冻结预期：{"verdict": "refuted", "basis": "M1"}
自动检查：{"id": "P19b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G01", "topic_name": "人员姓名与具体贡献", "case_pair_id": "P19", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "none", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "6d283958138d48a50021037909db6da77585292e39e9eaed1fe4025bb294a174"}

## P09b / 任职学院与获奖身份 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。
M2：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。

目标陈述：陈晓东曾获得诺贝尔物理学奖。

```text
{"verdict":"supported","basis":"M1"}
```

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P09b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G02", "topic_name": "任职学院与获奖身份", "case_pair_id": "P09", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "09a5ee11af5d673219ad09817f23a43ffae15f4d4ada7498bbfd59bf6ed64817"}

## P18b / 多人贡献与未提供人物信息 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。

目标陈述：斯旺出生于1828年。

```text
{"verdict":"supported","basis":"none"}
```

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P18b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G08", "topic_name": "多人贡献与未提供人物信息", "case_pair_id": "P18", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "none", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "cfccee83f4982b932731ed6020ea117c036b0a8cde40fb48fb7b22b4824ae187"}

## P08a / 任职学院与获奖身份 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。
M2：人员页整理记录：姓名为王明远；科研单位为中国科学院国家天文台；研究方向包括天体测量、天体力学、行星无线电科学。

目标陈述：陈晓东这条目录记录所列的任职学院是经济学院。

```text
{"verdict":"supported","basis":"M1"}
```

冻结预期：{"verdict": "refuted", "basis": "M1"}
自动检查：{"id": "P08a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G02", "topic_name": "任职学院与获奖身份", "case_pair_id": "P08", "position_variant": "base", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "3f3f45f201fc32d5786b544a35a3f35ec390c85166da5197cb4e26fa05fc263b"}

## P22b / 人员存在与获奖身份 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。
M2：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。

目标陈述：河南工业大学这份人员记录记载的姓名是王明远。

```text
{"verdict":"supported","basis":"none"}
```

冻结预期：{"verdict": "refuted", "basis": "M1"}
自动检查：{"id": "P22b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G03", "topic_name": "人员存在与获奖身份", "case_pair_id": "P22", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "none", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "c85dd1f47d23948c3c56395af1900fa530ede890f0b1e0f38dab23e7b4ebdf86"}

## P14b / 人员存在与获奖身份 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：人员目录整理记录：姓名陈晓东，对应Chen Xiaodong；所列任职学院为南洋理工大学材料科学与工程学院。
M2：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。

目标陈述：河南工业大学这份人员记录记载了刘建平这一姓名。

```text
{"verdict":"supported","basis":"none"}
```

冻结预期：{"verdict": "supported", "basis": "M2"}
自动检查：{"id": "P14b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G03", "topic_name": "人员存在与获奖身份", "case_pair_id": "P14", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M2", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "none", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "e00ddb6bd8f5f05a20e6149ee49b6b8f6498f4d20b2cdaa209056355ad5f6364"}

## P20a / 给定名单与研究范围 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：本题给定的完整名单只有两个条目：浙江大学生物医学工程与仪器科学学院、浙江大学医学院。名单为教学任务选取的目录片段，不代表学校全部单位，也没有提供研究项目清单。
M2：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。

目标陈述：本题给定的名单列有浙江大学医学院。

```text
{"verdict":"supported","basis":"none"}
```

冻结预期：{"verdict": "supported", "basis": "M1"}
自动检查：{"id": "P20a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G05", "topic_name": "给定名单与研究范围", "case_pair_id": "P20", "position_variant": "base", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "none", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": false, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "824fb586bbb52f4c7711fe86229148af42a848094e2205506c065d1d6180b270"}

## P12b / 车型报告与未知参数 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：小米2025年中期报告整理记录：2025年6月发布YU7系列；YU7的车型定位为SUV。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：SU9的百公里加速时间为2.5秒。

```text
{"verdict":"supported","basis":"none"}
```

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P12b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G04", "topic_name": "车型报告与未知参数", "case_pair_id": "P12", "position_variant": "swapped", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "none", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "82b3a7285f33957d9008f9e6ff95a1f9419d0b1d89759aa1057e959ed47e7f18"}

## P17b / 指定奖项记录与人物背景 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。
M2：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。

目标陈述：材料中爱因斯坦这条物理学奖记录的年份是1937年。

```text
{"verdict":"supported","basis":"M1"}
```

冻结预期：{"verdict": "refuted", "basis": "M1"}
自动检查：{"id": "P17b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G07", "topic_name": "指定奖项记录与人物背景", "case_pair_id": "P17", "position_variant": "swapped", "expected_verdict": "refuted", "expected_label_raw": "refuted", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "61f84331a7b4b9dd4a35f7c4473b90b93f903b1b7be9185177bc19d05ef343ea"}

## P13b / 多人贡献与未提供人物信息 / swapped

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：美国能源部资料整理记录：电灯的发展由多位发明者持续改进；爱迪生团队推动了实用化与商业化；斯旺也有贡献，不能把全部发明贡献归给单独一人。
M2：诺贝尔物理学奖档案整理记录：Albert Einstein，1921年；获奖理由涉及光电效应定律。此处仅提供这条奖项记录。

目标陈述：材料将电灯发展描述为多位发明者的贡献。

```text
{"verdict":"supported","basis":"M1"}
```

冻结预期：{"verdict": "supported", "basis": "M1"}
自动检查：{"id": "P13b", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G08", "topic_name": "多人贡献与未提供人物信息", "case_pair_id": "P13", "position_variant": "swapped", "expected_verdict": "supported", "expected_label_raw": "supported", "expected_basis": "M1", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "M1", "parse_status": "bare_json", "verdict_correct": true, "basis_correct": true, "joint_correct": true, "schema_conformant": true, "strict_task_passed": true, "truncated": false, "content_sha256": "19dc702b603342b17a898d2774c695c9ba64e9898d690be060272ea7af8a6d99"}

## P05a / 给定名单与研究范围 / base

只根据本题M1和M2两段材料判断目标陈述，不使用材料外知识。材料是整理记录，不代表完整现实资料。
verdict只能取supported、refuted、not_established：材料足以推出目标陈述时取supported；材料存在明确相反事实或与本题完整名单冲突时取refuted；两者都不能推出时取not_established。材料没说不等于事实已被反驳。
basis只能取M1、M2、none：填写足以支持该判定的材料编号；证据不足时填none。只输出包含verdict和basis两个字符串字段的JSON对象，不要额外字段、解释或Markdown。

M1：本题给定的完整名单只有两个条目：浙江大学生物医学工程与仪器科学学院、浙江大学医学院。名单为教学任务选取的目录片段，不代表学校全部单位，也没有提供研究项目清单。
M2：人员页整理记录：姓名刘建平；任职单位河南工业大学化学化工学院；从事化学教学科研。

目标陈述：浙江大学完全没有脑机接口相关研究。

```text
{"verdict":"supported","basis":"none"}
```

冻结预期：{"verdict": "not_established", "basis": "none"}
自动检查：{"id": "P05a", "mode": "compact__json", "policy": "compact", "decoder": "json", "contrast_group": "G05", "topic_name": "给定名单与研究范围", "case_pair_id": "P05", "position_variant": "base", "expected_verdict": "not_established", "expected_label_raw": "not_established", "expected_basis": "none", "predicted_verdict": "supported", "predicted_label_raw": "supported", "predicted_basis": "none", "parse_status": "bare_json", "verdict_correct": false, "basis_correct": true, "joint_correct": false, "schema_conformant": true, "strict_task_passed": false, "truncated": false, "content_sha256": "d0392ee0825783190018624d3a3dba5db6d82ace4c5ddfbec62e691e4842b436"}
