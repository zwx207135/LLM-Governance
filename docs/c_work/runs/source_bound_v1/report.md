# 给定材料证据边界开发诊断

五题由开发者按补查材料编写，检查同名人物与获奖身份、目录与研究活动、不同产品型号能否分开判断。没有使用此前38题作为独立测试，也没有为原22条不确定性探针建立真值。

材料与字段要求均在问题中提供；expected_fields只供事后检查，模型只收到question及治理提示。分类normal_control使compact、guarded绕过外部证据门控，legacy保留原combined行为。

## 自动检查

必需字段符合表示从可解析对象中读取的两个必需键、值和类型均符合，额外键另列；键集合符合进一步要求没有额外键。完整代码围栏可单列检查字段；严格任务符合还要求整个回答本身是JSON对象，不带围栏或解释。其他文字中的零散JSON不抽取评分。额外键、重复键、布尔值写成数字及非JSON常量均不能通过相应检查。

| 策略 | 检查数 | JSON对象格式 | 必需字段符合 | 键集合及字段符合 | 严格任务符合 | 单字段通过/检查 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| compact | 5 | 0 | 1 | 0 | 0 | 3/10 |
| guarded | 5 | 0 | 1 | 0 | 0 | 3/10 |
| legacy | 5 | 1 | 0 | 0 | 0 | 3/10 |

这是5道指定材料任务的自动检查，不是总体事实正确率或幻觉率。JSON无法解析时不抽取零散词语臆测标签，未通过也不等于每条事实都错误。namesake_documented设计意图为材料记载给定姓名的人员，中文同名措辞仍需独立复核清晰度，不能将该题型直接用于正式能力结论。compact与guarded在这些题上使用相同提示，不能当作两份独立改善证据。不据本轮更换默认方案。

## 完整材料与原始回答

### B01 / legacy

只根据以下材料判断，不调用材料外知识。材料：中国科学院大学人员页列有名为王明远的天文科研人员，方向包括天体测量、天体力学和行星无线电科学。该材料没有说明此人在相对论方面的具体贡献。只输出一个JSON对象，不要解释或Markdown。namesake_documented用布尔值表示材料是否记载了同名科研人员；specific_contribution取supported、refuted或not_established，表示材料对其相对论贡献是否建立了证据。

输出来源：model。

````text
```json
{
  "nameake_documented": false,
  "specific_contribution": not_established
}
```
````

冻结预期字段：{"namesake_documented": true, "specific_contribution": "not_established"}
检查：{"id": "B01", "mode": "legacy", "content_sha256": "5908d529466e7dd73864d4887d6ce6daa7c61e40f0676335f21b83c3da1a9530", "strict_json_object": false, "code_fence_wrapper": false, "content_fields_passed": false, "required_field_values_passed": false, "strict_task_passed": false, "field_checks": {"namesake_documented": false, "specific_contribution": false}, "unexpected_fields": []}
来源登记ID：sf_ucas_wang

### B01 / compact

只根据以下材料判断，不调用材料外知识。材料：中国科学院大学人员页列有名为王明远的天文科研人员，方向包括天体测量、天体力学和行星无线电科学。该材料没有说明此人在相对论方面的具体贡献。只输出一个JSON对象，不要解释或Markdown。namesake_documented用布尔值表示材料是否记载了同名科研人员；specific_contribution取supported、refuted或not_established，表示材料对其相对论贡献是否建立了证据。

输出来源：model。

````text
```json
{
  "nameake_documented": false,
  "specific_contribution": not_established,
  "result": {
    "王明远" : {
      "directions": ["天体测量", "天体力学", "行星无线电科学"],
      "relative_contribution": "未提供",
      "specific_contribution": "未建立证据"
    }
  }
}
```
````

冻结预期字段：{"namesake_documented": true, "specific_contribution": "not_established"}
检查：{"id": "B01", "mode": "compact", "content_sha256": "77af6b4b70e0790b5cc4c4d73e7c7f35f79e1cd9e5cde1efb0ce5906fed513a0", "strict_json_object": false, "code_fence_wrapper": false, "content_fields_passed": false, "required_field_values_passed": false, "strict_task_passed": false, "field_checks": {"namesake_documented": false, "specific_contribution": false}, "unexpected_fields": []}
来源登记ID：sf_ucas_wang

### B01 / guarded

只根据以下材料判断，不调用材料外知识。材料：中国科学院大学人员页列有名为王明远的天文科研人员，方向包括天体测量、天体力学和行星无线电科学。该材料没有说明此人在相对论方面的具体贡献。只输出一个JSON对象，不要解释或Markdown。namesake_documented用布尔值表示材料是否记载了同名科研人员；specific_contribution取supported、refuted或not_established，表示材料对其相对论贡献是否建立了证据。

输出来源：model。

````text
```json
{
  "nameake_documented": false,
  "specific_contribution": not_established,
  "result": {
    "王明远" : {
      "directions": ["天体测量", "天体力学", "行星无线电科学"],
      "relative_contribution": "未提供",
      "specific_contribution": "未建立证据"
    }
  }
}
```
````

冻结预期字段：{"namesake_documented": true, "specific_contribution": "not_established"}
检查：{"id": "B01", "mode": "guarded", "content_sha256": "77af6b4b70e0790b5cc4c4d73e7c7f35f79e1cd9e5cde1efb0ce5906fed513a0", "strict_json_object": false, "code_fence_wrapper": false, "content_fields_passed": false, "required_field_values_passed": false, "strict_task_passed": false, "field_checks": {"namesake_documented": false, "specific_contribution": false}, "unexpected_fields": []}
来源登记ID：sf_ucas_wang

### B02 / compact

只根据以下材料判断，不调用材料外知识。材料：南洋理工大学官方Faculty页面列有Professor Chen Xiaodong，中文姓名陈晓东，任职于材料科学与工程学院。本材料没有给出任何诺贝尔物理学奖获奖年份或官方获奖记录。只输出一个JSON对象，不要解释或Markdown。namesake_documented用布尔值表示材料是否记载同名科研人员；nobel_identity取supported、refuted或not_established，表示本材料对题设诺贝尔物理学奖身份的证据状态。

输出来源：model。

````text
```json
{
  "namesake_documented": false,
  "nobel_identity": not_established,
  "reason": "缺少关于诺贝尔物理学奖获奖年份的信息"
}
```
````

冻结预期字段：{"namesake_documented": true, "nobel_identity": "not_established"}
检查：{"id": "B02", "mode": "compact", "content_sha256": "91781d7df35bb9db71dc970eb494b4fa3cf152cbc01f7d46476124a86a48bdb7", "strict_json_object": false, "code_fence_wrapper": false, "content_fields_passed": false, "required_field_values_passed": false, "strict_task_passed": false, "field_checks": {"namesake_documented": false, "nobel_identity": false}, "unexpected_fields": []}
来源登记ID：sf_ntu_chen

### B02 / guarded

只根据以下材料判断，不调用材料外知识。材料：南洋理工大学官方Faculty页面列有Professor Chen Xiaodong，中文姓名陈晓东，任职于材料科学与工程学院。本材料没有给出任何诺贝尔物理学奖获奖年份或官方获奖记录。只输出一个JSON对象，不要解释或Markdown。namesake_documented用布尔值表示材料是否记载同名科研人员；nobel_identity取supported、refuted或not_established，表示本材料对题设诺贝尔物理学奖身份的证据状态。

输出来源：model。

````text
```json
{
  "namesake_documented": false,
  "nobel_identity": not_established,
  "reason": "缺少关于诺贝尔物理学奖获奖年份的信息"
}
```
````

冻结预期字段：{"namesake_documented": true, "nobel_identity": "not_established"}
检查：{"id": "B02", "mode": "guarded", "content_sha256": "91781d7df35bb9db71dc970eb494b4fa3cf152cbc01f7d46476124a86a48bdb7", "strict_json_object": false, "code_fence_wrapper": false, "content_fields_passed": false, "required_field_values_passed": false, "strict_task_passed": false, "field_checks": {"namesake_documented": false, "nobel_identity": false}, "unexpected_fields": []}
来源登记ID：sf_ntu_chen

### B02 / legacy

只根据以下材料判断，不调用材料外知识。材料：南洋理工大学官方Faculty页面列有Professor Chen Xiaodong，中文姓名陈晓东，任职于材料科学与工程学院。本材料没有给出任何诺贝尔物理学奖获奖年份或官方获奖记录。只输出一个JSON对象，不要解释或Markdown。namesake_documented用布尔值表示材料是否记载同名科研人员；nobel_identity取supported、refuted或not_established，表示本材料对题设诺贝尔物理学奖身份的证据状态。

输出来源：model。

```text
{
  "namesake_documented": false,
  "nobel_identity": "not_established",
  "reason": "材料中没有提供任何诺贝尔物理学奖获奖年份或官方获奖记录"
}
```

冻结预期字段：{"namesake_documented": true, "nobel_identity": "not_established"}
检查：{"id": "B02", "mode": "legacy", "content_sha256": "1ad07aab3ab8d8e44a8d92fe135276bbf01917f4421202c22e2e7df6deb20d26", "strict_json_object": true, "code_fence_wrapper": false, "content_fields_passed": false, "required_field_values_passed": false, "strict_task_passed": false, "field_checks": {"namesake_documented": false, "nobel_identity": true}, "unexpected_fields": ["reason"]}
来源登记ID：sf_ntu_chen

### B03 / guarded

只根据以下材料判断，不调用材料外知识。材料：小米官方展示了YU7车型，2025年中期报告也记录了YU7系列的发布。所给材料未记载SU9的加速和价格。只输出一个JSON对象，不要解释或Markdown。only_su7用布尔值判断只有SU7及其衍生款这一说法是否与材料一致；su9_parameters取supported、refuted或not_established，表示SU9参数在材料中的证据状态。不能把不同型号的参数混用。

输出来源：model。

````text
```json
{
  "only_su7": true,
  "su9_parameters": "not_established"
}
```
````

冻结预期字段：{"only_su7": false, "su9_parameters": "not_established"}
检查：{"id": "B03", "mode": "guarded", "content_sha256": "fc7f4014ad5e33f86bf4f0afc174c5e61e5767c31aa1eff26d8891ba10020168", "strict_json_object": false, "code_fence_wrapper": true, "content_fields_passed": false, "required_field_values_passed": false, "strict_task_passed": false, "field_checks": {"only_su7": false, "su9_parameters": true}, "unexpected_fields": []}
来源登记ID：sf_xiaomi_yu7; sf_xiaomi_h1

### B03 / legacy

只根据以下材料判断，不调用材料外知识。材料：小米官方展示了YU7车型，2025年中期报告也记录了YU7系列的发布。所给材料未记载SU9的加速和价格。只输出一个JSON对象，不要解释或Markdown。only_su7用布尔值判断只有SU7及其衍生款这一说法是否与材料一致；su9_parameters取supported、refuted或not_established，表示SU9参数在材料中的证据状态。不能把不同型号的参数混用。

输出来源：model。

````text
```json
{
  "only_su7": false,
  "su9_parameters": {
    "acceleration": "not_established",
    "price": "not_established"
  }
}
```
````

冻结预期字段：{"only_su7": false, "su9_parameters": "not_established"}
检查：{"id": "B03", "mode": "legacy", "content_sha256": "f2b0ddbf5960ef1206108693a3f4e9939b71dbef9cbef6cdc28cecdaa3585c86", "strict_json_object": false, "code_fence_wrapper": true, "content_fields_passed": false, "required_field_values_passed": false, "strict_task_passed": false, "field_checks": {"only_su7": true, "su9_parameters": false}, "unexpected_fields": []}
来源登记ID：sf_xiaomi_yu7; sf_xiaomi_h1

### B03 / compact

只根据以下材料判断，不调用材料外知识。材料：小米官方展示了YU7车型，2025年中期报告也记录了YU7系列的发布。所给材料未记载SU9的加速和价格。只输出一个JSON对象，不要解释或Markdown。only_su7用布尔值判断只有SU7及其衍生款这一说法是否与材料一致；su9_parameters取supported、refuted或not_established，表示SU9参数在材料中的证据状态。不能把不同型号的参数混用。

输出来源：model。

````text
```json
{
  "only_su7": true,
  "su9_parameters": "not_established"
}
```
````

冻结预期字段：{"only_su7": false, "su9_parameters": "not_established"}
检查：{"id": "B03", "mode": "compact", "content_sha256": "fc7f4014ad5e33f86bf4f0afc174c5e61e5767c31aa1eff26d8891ba10020168", "strict_json_object": false, "code_fence_wrapper": true, "content_fields_passed": false, "required_field_values_passed": false, "strict_task_passed": false, "field_checks": {"only_su7": false, "su9_parameters": true}, "unexpected_fields": []}
来源登记ID：sf_xiaomi_yu7; sf_xiaomi_h1

### B04 / legacy

只根据以下提供的目录片段判断，不调用材料外知识。目录片段：浙江大学的生物医学工程与仪器科学学院、医学院。该片段没有列脑机接口学院，也没有任何研究项目清单。只输出一个JSON对象，不要解释或Markdown。listed_in_excerpt用布尔值表示脑机接口学院是否列在这段材料里；no_related_research取supported、refuted或not_established，表示学校完全没有脑机接口研究的断言在本材料中的证据状态。

输出来源：model。

````text
```json
{
  "supported": false,
  "refuted": true,
  "not_established": true
}
```
````

冻结预期字段：{"listed_in_excerpt": false, "no_related_research": "not_established"}
检查：{"id": "B04", "mode": "legacy", "content_sha256": "c680e6a69e0a495293fa8f7aea36d3bfa19b6d421dec56ff5e8a025fdf852c9c", "strict_json_object": false, "code_fence_wrapper": true, "content_fields_passed": false, "required_field_values_passed": false, "strict_task_passed": false, "field_checks": {"listed_in_excerpt": false, "no_related_research": false}, "unexpected_fields": ["not_established", "refuted", "supported"]}
来源登记ID：sf_zju_directory

### B04 / compact

只根据以下提供的目录片段判断，不调用材料外知识。目录片段：浙江大学的生物医学工程与仪器科学学院、医学院。该片段没有列脑机接口学院，也没有任何研究项目清单。只输出一个JSON对象，不要解释或Markdown。listed_in_excerpt用布尔值表示脑机接口学院是否列在这段材料里；no_related_research取supported、refuted或not_established，表示学校完全没有脑机接口研究的断言在本材料中的证据状态。

输出来源：model。

````text
```json
{
  "listed_in_excerpt": false,
  "no_related_research": "not_established",
  "supported": true,
  "refuted": false,
  "not_established": false
}
```
````

冻结预期字段：{"listed_in_excerpt": false, "no_related_research": "not_established"}
检查：{"id": "B04", "mode": "compact", "content_sha256": "f82f88e6facdc4f64cd49fd0982f9dead2ae197717447eeea95f992a38a490f9", "strict_json_object": false, "code_fence_wrapper": true, "content_fields_passed": false, "required_field_values_passed": true, "strict_task_passed": false, "field_checks": {"listed_in_excerpt": true, "no_related_research": true}, "unexpected_fields": ["not_established", "refuted", "supported"]}
来源登记ID：sf_zju_directory

### B04 / guarded

只根据以下提供的目录片段判断，不调用材料外知识。目录片段：浙江大学的生物医学工程与仪器科学学院、医学院。该片段没有列脑机接口学院，也没有任何研究项目清单。只输出一个JSON对象，不要解释或Markdown。listed_in_excerpt用布尔值表示脑机接口学院是否列在这段材料里；no_related_research取supported、refuted或not_established，表示学校完全没有脑机接口研究的断言在本材料中的证据状态。

输出来源：model。

````text
```json
{
  "listed_in_excerpt": false,
  "no_related_research": "not_established",
  "supported": true,
  "refuted": false,
  "not_established": false
}
```
````

冻结预期字段：{"listed_in_excerpt": false, "no_related_research": "not_established"}
检查：{"id": "B04", "mode": "guarded", "content_sha256": "f82f88e6facdc4f64cd49fd0982f9dead2ae197717447eeea95f992a38a490f9", "strict_json_object": false, "code_fence_wrapper": true, "content_fields_passed": false, "required_field_values_passed": true, "strict_task_passed": false, "field_checks": {"listed_in_excerpt": true, "no_related_research": true}, "unexpected_fields": ["not_established", "refuted", "supported"]}
来源登记ID：sf_zju_directory

### B05 / compact

只根据以下材料判断，不调用材料外知识。材料：河南工业大学化学化工学院官方人员页列有刘建平，介绍其化学教学科研背景。本材料没有提供诺贝尔化学奖获奖年份或官方获奖记录。只输出一个JSON对象，不要解释或Markdown。namesake_documented用布尔值表示同名人员是否有材料记录；nobel_identity取supported、refuted或not_established，表示题设诺贝尔化学奖身份在材料中的证据状态。

输出来源：model。

````text
```json
{
  "namesake_documented": false,
  "nobel_identity": not_established,
  "reason": "材料中未提供诺贝尔化学奖获奖年份或官方获奖记录，因此无法确定是否支持或拒绝了诺贝尔化学奖的身份。"
}
```
````

冻结预期字段：{"namesake_documented": true, "nobel_identity": "not_established"}
检查：{"id": "B05", "mode": "compact", "content_sha256": "28ec18c41bd55d093f3fdd7b445f7554ac6593fabc4c744a062503331043b98f", "strict_json_object": false, "code_fence_wrapper": false, "content_fields_passed": false, "required_field_values_passed": false, "strict_task_passed": false, "field_checks": {"namesake_documented": false, "nobel_identity": false}, "unexpected_fields": []}
来源登记ID：sf_haut_liu

### B05 / guarded

只根据以下材料判断，不调用材料外知识。材料：河南工业大学化学化工学院官方人员页列有刘建平，介绍其化学教学科研背景。本材料没有提供诺贝尔化学奖获奖年份或官方获奖记录。只输出一个JSON对象，不要解释或Markdown。namesake_documented用布尔值表示同名人员是否有材料记录；nobel_identity取supported、refuted或not_established，表示题设诺贝尔化学奖身份在材料中的证据状态。

输出来源：model。

````text
```json
{
  "namesake_documented": false,
  "nobel_identity": not_established,
  "reason": "材料中未提供诺贝尔化学奖获奖年份或官方获奖记录，因此无法确定是否支持或拒绝了诺贝尔化学奖的身份。"
}
```
````

冻结预期字段：{"namesake_documented": true, "nobel_identity": "not_established"}
检查：{"id": "B05", "mode": "guarded", "content_sha256": "28ec18c41bd55d093f3fdd7b445f7554ac6593fabc4c744a062503331043b98f", "strict_json_object": false, "code_fence_wrapper": false, "content_fields_passed": false, "required_field_values_passed": false, "strict_task_passed": false, "field_checks": {"namesake_documented": false, "nobel_identity": false}, "unexpected_fields": []}
来源登记ID：sf_haut_liu

### B05 / legacy

只根据以下材料判断，不调用材料外知识。材料：河南工业大学化学化工学院官方人员页列有刘建平，介绍其化学教学科研背景。本材料没有提供诺贝尔化学奖获奖年份或官方获奖记录。只输出一个JSON对象，不要解释或Markdown。namesake_documented用布尔值表示同名人员是否有材料记录；nobel_identity取supported、refuted或not_established，表示题设诺贝尔化学奖身份在材料中的证据状态。

输出来源：model。

````text
```json
{
  "namesake_documented": false,
  "nobel_identity": "not_established",
  "reason": "材料中没有提供诺贝尔化学奖获奖年份或官方获奖记录，因此无法确定是否获得过诺贝尔化学奖。"
}
```
````

冻结预期字段：{"namesake_documented": true, "nobel_identity": "not_established"}
检查：{"id": "B05", "mode": "legacy", "content_sha256": "eb18f4e56b3035a825dc8e798cd47c5db04fa9bf9aaaed3fc82321fb991e51a7", "strict_json_object": false, "code_fence_wrapper": true, "content_fields_passed": false, "required_field_values_passed": false, "strict_task_passed": false, "field_checks": {"namesake_documented": false, "nobel_identity": true}, "unexpected_fields": ["reason"]}
来源登记ID：sf_haut_liu
