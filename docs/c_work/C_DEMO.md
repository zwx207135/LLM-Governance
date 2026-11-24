# C 现场演示与接入

已有一轮RTX 4060实机记录：[完整问答与资料](runs/demo_v1/transcript.md)，[完整性检查](demo_verification.json)。四个问题分别演示有证据的常识问答、无法核实的产品、数学推导和材料提取，三策略共12条输出，其中11条模型回答、1条程序拒答。此轮是功能演示，不加入前三轮548条开发输出的效果统计。

## 单题运行

在仓库根目录激活llm-governance环境，使用本地Qwen2.5-0.5B-Instruct模型：

```powershell
python -m experiments.demo_c_governance --question "声音能在真空中传播吗？请说明原因。" --category factual --output docs/c_work/runs/my_single_demo
```

默认combined沿用原治理提示。策略还可选baseline、constraint、retrieval、legacy、compact、guarded；legacy与combined的提示相同。只有guarded可在资料不足时跳过模型并返回固定说明。

```powershell
python -m experiments.demo_c_governance --input configs/c_demo_questions.json --strategies combined compact guarded --output docs/c_work/runs/my_demo
```

输出目录必须是新目录。只检查提示、检索和路由时加--prepare-only，不加载模型，记录状态为prepared、答案为空。恢复时重复原命令并加--resume；已有错误需要重试时另加--retry-errors。输入、策略、代码、语料或模型发生变化后应使用新目录。

目录中保存manifest.json、records.jsonl、语料与源码快照，以及可直接阅读的transcript.md。日志含证据正文、来源URL、模型或程序输出来源、token数、模型加载和生成耗时。演示未做正式预热或轮换顺序，耗时不能与正式实验作效率比较。

## A 接入联合治理

```python
from src.governance.retrieval import LocalRetriever
from src.governance.service import GovernanceService
from src.models.llm_model import LLMModel

service = GovernanceService(
    LocalRetriever("knowledge/corpus_v3.json"),
    model_factory=lambda: LLMModel("models/Qwen2.5-0.5B-Instruct", local_files_only=True),
)
result = service.answer("声音能在真空中传播吗？", strategy="combined", category="factual")
print(result["answer"])
print(result["evidence"], result["answer_origin"])
```

模型在首次需要生成时才加载，一实例可连续处理问题；程序拒答与prepare_only均不加载模型。该同步实例供单线程或串行调用，共享model.last_generation，不应直接用于并发请求。接入方可先用prepare取得prompt和evidence交给自己的模型或偏见治理步骤。接口只接收问题、策略和任务类别，不接收参考答案、评分标签或来源登记中的答案核验资料。

category由调用方提供，未提供则正常检索，不自动识别题型。math_logic在既有策略中跳过检索；候选compact、guarded还对normal_control绕过证据门控。分类会改变路由，应按实际任务使用，不能把未知事实问题标为正常材料任务来绕过门控。

## 本轮实际发现

- 真空传声题：combined给出不能传播及介质原因；compact和guarded却先说能传播、后说不能传播，同段矛盾。guarded有命中时仍可能生成错误。
- 产品题：guarded给程序限定说明；combined虽未编造售价，却自行添加商业秘密与知识产权作为无法回答的理由，该理由没有资料支持。检索未命中不能证明企业或产品不存在。
- 数学题：三组均列出正负12。本题显式要求全部实数解，不能据此声称原第111题只给正12的问题已经全面修复。
- JSON提取题：三组内容均为林青、23，但仍加了Markdown代码围栏；若按只输出JSON的严格语法约束，围栏输出不符合要求。

以上为直接观察的开发说明，未增加独立人工评分或总体正确率。演示保留失败回答，现场应同时展示证据与完整回答。
