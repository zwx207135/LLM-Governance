# 普通生成与有限JSON约束解码

五道既有给定材料诊断、三种提示策略、两种解码方式，共30条真实模型回答。问题、资料与提示保持一致，只改变下一token可选集合。全部6种语义组合保留，正确字段不参与生成；源码、模式及输入均冻结。

## 格式与内容分开报告

| 策略 | 解码 | 数量 | JSON格式 | 字段结构与类型 | 必需值均符合 | 严格任务符合 | 单字段通过/检查 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| compact | free | 5 | 0 | 0 | 1 | 0 | 3/10 |
| compact | json | 5 | 5 | 5 | 1 | 1 | 6/10 |
| guarded | free | 5 | 0 | 0 | 1 | 0 | 3/10 |
| guarded | json | 5 | 5 | 5 | 1 | 1 | 6/10 |
| legacy | free | 5 | 1 | 0 | 0 | 0 | 3/10 |
| legacy | json | 5 | 5 | 5 | 2 | 2 | 7/10 |

json解码固定键集合、字段顺序和序列化，禁止代码围栏及额外字段，保留每个布尔值与每个状态值。格式通过是程序约束的结果，不证明模型理解资料或事实更可靠。即使所有结构合格，模型仍可能选错布尔值或证据状态。

必需字段检查允许完整代码围栏内对象另查内容；严格任务要求整个回答本身满足JSON与预期值。无效JSON不靠零散词语强行恢复，因此从普通输出到可解析输出的字段通过变化也包含可检查性的变化，不能一概解释为事实纠错。

人员题同名措辞仍需第二人审核清晰度。本轮保留原题便于隔离解码作用，不将该诊断或其重复提示当作独立测试，不更换默认治理方案。

## 旧输出重放

{"matched": 15, "unmatched": 0, "same_prompt": 15, "same_answer": 15, "same_model_files": true}

## 耗时与配对

准备、约束编译、生成及输出token分别保存；约束改变输出长度且有回调开销，不据此泛化模型效率提升。

```json
{
  "paired": [
    {
      "policy": "legacy",
      "paired_questions": 5,
      "identical_prompts": 5,
      "both_parseable_objects": 4,
      "strict_task_gains": 2,
      "strict_task_losses": 0
    },
    {
      "policy": "compact",
      "paired_questions": 5,
      "identical_prompts": 5,
      "both_parseable_objects": 2,
      "strict_task_gains": 1,
      "strict_task_losses": 0
    },
    {
      "policy": "guarded",
      "paired_questions": 5,
      "identical_prompts": 5,
      "both_parseable_objects": 2,
      "strict_task_gains": 1,
      "strict_task_losses": 0
    }
  ],
  "costs": [
    {
      "policy": "compact",
      "decoder": "free",
      "mean_generation_seconds": 0.9924,
      "mean_constraint_compile_seconds": 0.0,
      "mean_total_seconds": 0.9925,
      "mean_output_tokens": 53
    },
    {
      "policy": "compact",
      "decoder": "json",
      "mean_generation_seconds": 0.3356,
      "mean_constraint_compile_seconds": 0.0008,
      "mean_total_seconds": 0.3364,
      "mean_output_tokens": 17.8
    },
    {
      "policy": "guarded",
      "decoder": "free",
      "mean_generation_seconds": 0.9964,
      "mean_constraint_compile_seconds": 0.0,
      "mean_total_seconds": 0.9965,
      "mean_output_tokens": 53
    },
    {
      "policy": "guarded",
      "decoder": "json",
      "mean_generation_seconds": 0.3378,
      "mean_constraint_compile_seconds": 0.0007,
      "mean_total_seconds": 0.3385,
      "mean_output_tokens": 17.8
    },
    {
      "policy": "legacy",
      "decoder": "free",
      "mean_generation_seconds": 0.7626,
      "mean_constraint_compile_seconds": 0.0,
      "mean_total_seconds": 0.763,
      "mean_output_tokens": 41
    },
    {
      "policy": "legacy",
      "decoder": "json",
      "mean_generation_seconds": 0.3505,
      "mean_constraint_compile_seconds": 0.0009,
      "mean_total_seconds": 0.3515,
      "mean_output_tokens": 17.8
    }
  ]
}
```

## 所有原始回答

### B01 / legacy__free

只根据以下材料判断，不调用材料外知识。材料：中国科学院大学人员页列有名为王明远的天文科研人员，方向包括天体测量、天体力学和行星无线电科学。该材料没有说明此人在相对论方面的具体贡献。只输出一个JSON对象，不要解释或Markdown。namesake_documented用布尔值表示材料是否记载了同名科研人员；specific_contribution取supported、refuted或not_established，表示材料对其相对论贡献是否建立了证据。

````text
```json
{
  "nameake_documented": false,
  "specific_contribution": not_established
}
```
````

### B01 / legacy__json

只根据以下材料判断，不调用材料外知识。材料：中国科学院大学人员页列有名为王明远的天文科研人员，方向包括天体测量、天体力学和行星无线电科学。该材料没有说明此人在相对论方面的具体贡献。只输出一个JSON对象，不要解释或Markdown。namesake_documented用布尔值表示材料是否记载了同名科研人员；specific_contribution取supported、refuted或not_established，表示材料对其相对论贡献是否建立了证据。

```text
{"namesake_documented":false,"specific_contribution":"not_established"}
```

### B01 / compact__free

只根据以下材料判断，不调用材料外知识。材料：中国科学院大学人员页列有名为王明远的天文科研人员，方向包括天体测量、天体力学和行星无线电科学。该材料没有说明此人在相对论方面的具体贡献。只输出一个JSON对象，不要解释或Markdown。namesake_documented用布尔值表示材料是否记载了同名科研人员；specific_contribution取supported、refuted或not_established，表示材料对其相对论贡献是否建立了证据。

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

### B01 / compact__json

只根据以下材料判断，不调用材料外知识。材料：中国科学院大学人员页列有名为王明远的天文科研人员，方向包括天体测量、天体力学和行星无线电科学。该材料没有说明此人在相对论方面的具体贡献。只输出一个JSON对象，不要解释或Markdown。namesake_documented用布尔值表示材料是否记载了同名科研人员；specific_contribution取supported、refuted或not_established，表示材料对其相对论贡献是否建立了证据。

```text
{"namesake_documented":false,"specific_contribution":"not_established"}
```

### B01 / guarded__free

只根据以下材料判断，不调用材料外知识。材料：中国科学院大学人员页列有名为王明远的天文科研人员，方向包括天体测量、天体力学和行星无线电科学。该材料没有说明此人在相对论方面的具体贡献。只输出一个JSON对象，不要解释或Markdown。namesake_documented用布尔值表示材料是否记载了同名科研人员；specific_contribution取supported、refuted或not_established，表示材料对其相对论贡献是否建立了证据。

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

### B01 / guarded__json

只根据以下材料判断，不调用材料外知识。材料：中国科学院大学人员页列有名为王明远的天文科研人员，方向包括天体测量、天体力学和行星无线电科学。该材料没有说明此人在相对论方面的具体贡献。只输出一个JSON对象，不要解释或Markdown。namesake_documented用布尔值表示材料是否记载了同名科研人员；specific_contribution取supported、refuted或not_established，表示材料对其相对论贡献是否建立了证据。

```text
{"namesake_documented":false,"specific_contribution":"not_established"}
```

### B02 / legacy__json

只根据以下材料判断，不调用材料外知识。材料：南洋理工大学官方Faculty页面列有Professor Chen Xiaodong，中文姓名陈晓东，任职于材料科学与工程学院。本材料没有给出任何诺贝尔物理学奖获奖年份或官方获奖记录。只输出一个JSON对象，不要解释或Markdown。namesake_documented用布尔值表示材料是否记载同名科研人员；nobel_identity取supported、refuted或not_established，表示本材料对题设诺贝尔物理学奖身份的证据状态。

```text
{"namesake_documented":false,"nobel_identity":"not_established"}
```

### B02 / compact__free

只根据以下材料判断，不调用材料外知识。材料：南洋理工大学官方Faculty页面列有Professor Chen Xiaodong，中文姓名陈晓东，任职于材料科学与工程学院。本材料没有给出任何诺贝尔物理学奖获奖年份或官方获奖记录。只输出一个JSON对象，不要解释或Markdown。namesake_documented用布尔值表示材料是否记载同名科研人员；nobel_identity取supported、refuted或not_established，表示本材料对题设诺贝尔物理学奖身份的证据状态。

````text
```json
{
  "namesake_documented": false,
  "nobel_identity": not_established,
  "reason": "缺少关于诺贝尔物理学奖获奖年份的信息"
}
```
````

### B02 / compact__json

只根据以下材料判断，不调用材料外知识。材料：南洋理工大学官方Faculty页面列有Professor Chen Xiaodong，中文姓名陈晓东，任职于材料科学与工程学院。本材料没有给出任何诺贝尔物理学奖获奖年份或官方获奖记录。只输出一个JSON对象，不要解释或Markdown。namesake_documented用布尔值表示材料是否记载同名科研人员；nobel_identity取supported、refuted或not_established，表示本材料对题设诺贝尔物理学奖身份的证据状态。

```text
{"namesake_documented":false,"nobel_identity":"not_established"}
```

### B02 / guarded__free

只根据以下材料判断，不调用材料外知识。材料：南洋理工大学官方Faculty页面列有Professor Chen Xiaodong，中文姓名陈晓东，任职于材料科学与工程学院。本材料没有给出任何诺贝尔物理学奖获奖年份或官方获奖记录。只输出一个JSON对象，不要解释或Markdown。namesake_documented用布尔值表示材料是否记载同名科研人员；nobel_identity取supported、refuted或not_established，表示本材料对题设诺贝尔物理学奖身份的证据状态。

````text
```json
{
  "namesake_documented": false,
  "nobel_identity": not_established,
  "reason": "缺少关于诺贝尔物理学奖获奖年份的信息"
}
```
````

### B02 / guarded__json

只根据以下材料判断，不调用材料外知识。材料：南洋理工大学官方Faculty页面列有Professor Chen Xiaodong，中文姓名陈晓东，任职于材料科学与工程学院。本材料没有给出任何诺贝尔物理学奖获奖年份或官方获奖记录。只输出一个JSON对象，不要解释或Markdown。namesake_documented用布尔值表示材料是否记载同名科研人员；nobel_identity取supported、refuted或not_established，表示本材料对题设诺贝尔物理学奖身份的证据状态。

```text
{"namesake_documented":false,"nobel_identity":"not_established"}
```

### B02 / legacy__free

只根据以下材料判断，不调用材料外知识。材料：南洋理工大学官方Faculty页面列有Professor Chen Xiaodong，中文姓名陈晓东，任职于材料科学与工程学院。本材料没有给出任何诺贝尔物理学奖获奖年份或官方获奖记录。只输出一个JSON对象，不要解释或Markdown。namesake_documented用布尔值表示材料是否记载同名科研人员；nobel_identity取supported、refuted或not_established，表示本材料对题设诺贝尔物理学奖身份的证据状态。

```text
{
  "namesake_documented": false,
  "nobel_identity": "not_established",
  "reason": "材料中没有提供任何诺贝尔物理学奖获奖年份或官方获奖记录"
}
```

### B03 / compact__free

只根据以下材料判断，不调用材料外知识。材料：小米官方展示了YU7车型，2025年中期报告也记录了YU7系列的发布。所给材料未记载SU9的加速和价格。只输出一个JSON对象，不要解释或Markdown。only_su7用布尔值判断只有SU7及其衍生款这一说法是否与材料一致；su9_parameters取supported、refuted或not_established，表示SU9参数在材料中的证据状态。不能把不同型号的参数混用。

````text
```json
{
  "only_su7": true,
  "su9_parameters": "not_established"
}
```
````

### B03 / compact__json

只根据以下材料判断，不调用材料外知识。材料：小米官方展示了YU7车型，2025年中期报告也记录了YU7系列的发布。所给材料未记载SU9的加速和价格。只输出一个JSON对象，不要解释或Markdown。only_su7用布尔值判断只有SU7及其衍生款这一说法是否与材料一致；su9_parameters取supported、refuted或not_established，表示SU9参数在材料中的证据状态。不能把不同型号的参数混用。

```text
{"only_su7":true,"su9_parameters":"not_established"}
```

### B03 / guarded__free

只根据以下材料判断，不调用材料外知识。材料：小米官方展示了YU7车型，2025年中期报告也记录了YU7系列的发布。所给材料未记载SU9的加速和价格。只输出一个JSON对象，不要解释或Markdown。only_su7用布尔值判断只有SU7及其衍生款这一说法是否与材料一致；su9_parameters取supported、refuted或not_established，表示SU9参数在材料中的证据状态。不能把不同型号的参数混用。

````text
```json
{
  "only_su7": true,
  "su9_parameters": "not_established"
}
```
````

### B03 / guarded__json

只根据以下材料判断，不调用材料外知识。材料：小米官方展示了YU7车型，2025年中期报告也记录了YU7系列的发布。所给材料未记载SU9的加速和价格。只输出一个JSON对象，不要解释或Markdown。only_su7用布尔值判断只有SU7及其衍生款这一说法是否与材料一致；su9_parameters取supported、refuted或not_established，表示SU9参数在材料中的证据状态。不能把不同型号的参数混用。

```text
{"only_su7":true,"su9_parameters":"not_established"}
```

### B03 / legacy__free

只根据以下材料判断，不调用材料外知识。材料：小米官方展示了YU7车型，2025年中期报告也记录了YU7系列的发布。所给材料未记载SU9的加速和价格。只输出一个JSON对象，不要解释或Markdown。only_su7用布尔值判断只有SU7及其衍生款这一说法是否与材料一致；su9_parameters取supported、refuted或not_established，表示SU9参数在材料中的证据状态。不能把不同型号的参数混用。

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

### B03 / legacy__json

只根据以下材料判断，不调用材料外知识。材料：小米官方展示了YU7车型，2025年中期报告也记录了YU7系列的发布。所给材料未记载SU9的加速和价格。只输出一个JSON对象，不要解释或Markdown。only_su7用布尔值判断只有SU7及其衍生款这一说法是否与材料一致；su9_parameters取supported、refuted或not_established，表示SU9参数在材料中的证据状态。不能把不同型号的参数混用。

```text
{"only_su7":false,"su9_parameters":"not_established"}
```

### B04 / compact__json

只根据以下提供的目录片段判断，不调用材料外知识。目录片段：浙江大学的生物医学工程与仪器科学学院、医学院。该片段没有列脑机接口学院，也没有任何研究项目清单。只输出一个JSON对象，不要解释或Markdown。listed_in_excerpt用布尔值表示脑机接口学院是否列在这段材料里；no_related_research取supported、refuted或not_established，表示学校完全没有脑机接口研究的断言在本材料中的证据状态。

```text
{"listed_in_excerpt":false,"no_related_research":"not_established"}
```

### B04 / guarded__free

只根据以下提供的目录片段判断，不调用材料外知识。目录片段：浙江大学的生物医学工程与仪器科学学院、医学院。该片段没有列脑机接口学院，也没有任何研究项目清单。只输出一个JSON对象，不要解释或Markdown。listed_in_excerpt用布尔值表示脑机接口学院是否列在这段材料里；no_related_research取supported、refuted或not_established，表示学校完全没有脑机接口研究的断言在本材料中的证据状态。

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

### B04 / guarded__json

只根据以下提供的目录片段判断，不调用材料外知识。目录片段：浙江大学的生物医学工程与仪器科学学院、医学院。该片段没有列脑机接口学院，也没有任何研究项目清单。只输出一个JSON对象，不要解释或Markdown。listed_in_excerpt用布尔值表示脑机接口学院是否列在这段材料里；no_related_research取supported、refuted或not_established，表示学校完全没有脑机接口研究的断言在本材料中的证据状态。

```text
{"listed_in_excerpt":false,"no_related_research":"not_established"}
```

### B04 / legacy__free

只根据以下提供的目录片段判断，不调用材料外知识。目录片段：浙江大学的生物医学工程与仪器科学学院、医学院。该片段没有列脑机接口学院，也没有任何研究项目清单。只输出一个JSON对象，不要解释或Markdown。listed_in_excerpt用布尔值表示脑机接口学院是否列在这段材料里；no_related_research取supported、refuted或not_established，表示学校完全没有脑机接口研究的断言在本材料中的证据状态。

````text
```json
{
  "supported": false,
  "refuted": true,
  "not_established": true
}
```
````

### B04 / legacy__json

只根据以下提供的目录片段判断，不调用材料外知识。目录片段：浙江大学的生物医学工程与仪器科学学院、医学院。该片段没有列脑机接口学院，也没有任何研究项目清单。只输出一个JSON对象，不要解释或Markdown。listed_in_excerpt用布尔值表示脑机接口学院是否列在这段材料里；no_related_research取supported、refuted或not_established，表示学校完全没有脑机接口研究的断言在本材料中的证据状态。

```text
{"listed_in_excerpt":false,"no_related_research":"not_established"}
```

### B04 / compact__free

只根据以下提供的目录片段判断，不调用材料外知识。目录片段：浙江大学的生物医学工程与仪器科学学院、医学院。该片段没有列脑机接口学院，也没有任何研究项目清单。只输出一个JSON对象，不要解释或Markdown。listed_in_excerpt用布尔值表示脑机接口学院是否列在这段材料里；no_related_research取supported、refuted或not_established，表示学校完全没有脑机接口研究的断言在本材料中的证据状态。

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

### B05 / guarded__free

只根据以下材料判断，不调用材料外知识。材料：河南工业大学化学化工学院官方人员页列有刘建平，介绍其化学教学科研背景。本材料没有提供诺贝尔化学奖获奖年份或官方获奖记录。只输出一个JSON对象，不要解释或Markdown。namesake_documented用布尔值表示同名人员是否有材料记录；nobel_identity取supported、refuted或not_established，表示题设诺贝尔化学奖身份在材料中的证据状态。

````text
```json
{
  "namesake_documented": false,
  "nobel_identity": not_established,
  "reason": "材料中未提供诺贝尔化学奖获奖年份或官方获奖记录，因此无法确定是否支持或拒绝了诺贝尔化学奖的身份。"
}
```
````

### B05 / guarded__json

只根据以下材料判断，不调用材料外知识。材料：河南工业大学化学化工学院官方人员页列有刘建平，介绍其化学教学科研背景。本材料没有提供诺贝尔化学奖获奖年份或官方获奖记录。只输出一个JSON对象，不要解释或Markdown。namesake_documented用布尔值表示同名人员是否有材料记录；nobel_identity取supported、refuted或not_established，表示题设诺贝尔化学奖身份在材料中的证据状态。

```text
{"namesake_documented":false,"nobel_identity":"not_established"}
```

### B05 / legacy__free

只根据以下材料判断，不调用材料外知识。材料：河南工业大学化学化工学院官方人员页列有刘建平，介绍其化学教学科研背景。本材料没有提供诺贝尔化学奖获奖年份或官方获奖记录。只输出一个JSON对象，不要解释或Markdown。namesake_documented用布尔值表示同名人员是否有材料记录；nobel_identity取supported、refuted或not_established，表示题设诺贝尔化学奖身份在材料中的证据状态。

````text
```json
{
  "namesake_documented": false,
  "nobel_identity": "not_established",
  "reason": "材料中没有提供诺贝尔化学奖获奖年份或官方获奖记录，因此无法确定是否获得过诺贝尔化学奖。"
}
```
````

### B05 / legacy__json

只根据以下材料判断，不调用材料外知识。材料：河南工业大学化学化工学院官方人员页列有刘建平，介绍其化学教学科研背景。本材料没有提供诺贝尔化学奖获奖年份或官方获奖记录。只输出一个JSON对象，不要解释或Markdown。namesake_documented用布尔值表示同名人员是否有材料记录；nobel_identity取supported、refuted或not_established，表示题设诺贝尔化学奖身份在材料中的证据状态。

```text
{"namesake_documented":false,"nobel_identity":"not_established"}
```

### B05 / compact__free

只根据以下材料判断，不调用材料外知识。材料：河南工业大学化学化工学院官方人员页列有刘建平，介绍其化学教学科研背景。本材料没有提供诺贝尔化学奖获奖年份或官方获奖记录。只输出一个JSON对象，不要解释或Markdown。namesake_documented用布尔值表示同名人员是否有材料记录；nobel_identity取supported、refuted或not_established，表示题设诺贝尔化学奖身份在材料中的证据状态。

````text
```json
{
  "namesake_documented": false,
  "nobel_identity": not_established,
  "reason": "材料中未提供诺贝尔化学奖获奖年份或官方获奖记录，因此无法确定是否支持或拒绝了诺贝尔化学奖的身份。"
}
```
````

### B05 / compact__json

只根据以下材料判断，不调用材料外知识。材料：河南工业大学化学化工学院官方人员页列有刘建平，介绍其化学教学科研背景。本材料没有提供诺贝尔化学奖获奖年份或官方获奖记录。只输出一个JSON对象，不要解释或Markdown。namesake_documented用布尔值表示同名人员是否有材料记录；nobel_identity取supported、refuted或not_established，表示题设诺贝尔化学奖身份在材料中的证据状态。

```text
{"namesake_documented":false,"nobel_identity":"not_established"}
```
