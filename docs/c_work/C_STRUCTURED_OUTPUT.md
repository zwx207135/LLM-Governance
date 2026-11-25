# 小规模枚举任务的JSON输出约束

本轮新增有限JSON解码模块，专门处理字段和值域已知、组合数较小的分类输出。使用原五道给定材料问题，在三种提示策略下分别运行普通生成和JSON约束生成，共30条真实模型回答。问题、提示、模型和生成预算保持一致，普通生成15条与上一轮逐字重放一致。完整输出见[对照报告](runs/structured_v1/report.md)，逐条核对见[检查记录](runs/structured_v1/structured_checks.json)。

## 结果与含义

| 策略 | 普通生成结构符合 | JSON约束结构符合 | 普通生成严格任务符合 | JSON约束严格任务符合 |
| --- | ---: | ---: | ---: | ---: |
| legacy | 0/5 | 5/5 | 0/5 | 2/5 |
| compact | 0/5 | 5/5 | 0/5 | 1/5 |
| guarded | 0/5 | 5/5 | 0/5 | 1/5 |

结构符合要求完整JSON对象、准确键集合和合法值类型及枚举；严格任务还要求字段值符合给定材料的冻结预期。全部15条约束输出结构合格是程序限制的直接作用。模型仍在选择值，例如compact、guarded在产品题选择only_su7=true，未能按材料中的YU7作出正确判断。

本轮把普通生成无法解析或多键的输出转成可检查对象，字段通过数的变化也包含可检查性变化，不能统一表述为事实纠错。人员题同名措辞仍需第二人确认清晰度。compact、guarded在这些正常任务上提示相同，重复结果不构成两份独立效果证据。当前保持默认方案不变，有限约束作为显式可选能力。

## 如何保证没有输入正确答案

[独立schema文件](../../configs/c_source_bound_schemas.json)只定义字段和完整可选值：一个布尔字段与一个三值状态字段，每题全部6种组合均保留。包括与冻结预期不一致的组合，模型通过逐token生成自行选择。字段顺序和序列化方式固定，JSON空白、键名、键次序、类型及额外内容都受到约束。

生成入口立即将任务裁剪为id、question、category，expected_fields只供事后检查。单元测试修改预期值、加入伪造参考，确认问题与允许输出均不变。运行后逐条重建提示、检查6种组合和输出所属关系，并核对源码快照。受约束回答仍由模型调用生成，model_calls=1，未以程序拒答或预选正确模板替代。

## 复现

```powershell
python -m experiments.run_c_structured_comparison --output docs/c_work/runs/my_structured
python -m experiments.report_c_structured docs/c_work/runs/my_structured
python -m experiments.check_c_delivery --run-tests
```

恢复时重复原参数并加--resume；错误记录需要显式加--retry-errors。每次改变输入、schema、模型、运行代码或配置必须使用新目录。--dry-run只准备提示及允许组合，不加载模型；已实际用--stop-after 2中断后恢复，得到30条唯一prepared记录，答案均为空，不计作模型回答。交接包包含这份恢复证明。

## A 接入现有模型

在已有model和prepared提示上，可以显式建立一个请求的约束：

```python
from src.governance.finite_json import FiniteJsonConstraint, allowed_outputs

schema = {"fields": [
    {"name": "recorded", "values": [True, False]},
    {"name": "identity", "values": ["supported", "refuted", "not_established"]},
]}
prompt = prepared["prompt"]
chat = model.tokenizer.apply_chat_template(
    [{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True,
)
eos = model.model.generation_config.eos_token_id
constraint = FiniteJsonConstraint(
    model.tokenizer, allowed_outputs(schema),
    prompt_length=len(model.tokenizer(chat)["input_ids"]),
    eos_token_ids=eos if isinstance(eos, list) else [eos], max_new_tokens=192,
)
answer = model.generate(
    prompt, max_new_tokens=192, do_sample=False,
    prefix_allowed_tokens_fn=constraint.allowed_tokens,
)
```

prompt必须要求相同字段和值域。每个串行请求使用独立constraint，prompt长度必须与实际聊天模板token化一致；当前实现用于单样本greedy解码。支持布尔值和字符串枚举，最多64种完整组合，预算须能容纳每一种完整对象及EOS。任一候选无法分词往返、预算不足或前缀越界时直接报错，避免静默退回自由生成。

该模块适用于小规模分类输出。开放自然语言答案、任意嵌套结构、连续数值或大量组合需要其他方案。程序限定格式也可能改变模型在不同标签上的选择及其偏好；当前没有概率校准或总体事实可靠性验证。耗时同时受输出长度和约束回调开销影响，不能仅凭本轮变快宣称通用效率提升。
