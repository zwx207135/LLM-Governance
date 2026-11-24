# 证据一致性与联合入口

新增consistency.py提供确定性结构检查与待审线索；joint.py将C提示、显式偏见约束或外部hook、模型生成和输出审计接通。仓库当前只有偏见数据与baseline脚本，没有现成偏见治理器。本入口是供A接入的集成原型，未完成项目E3效果验证。

## 已验证结果

[历史989条筛查](consistency_audit_v1/report.md)中181条触发信号，同一条可能触发多个信号。它们不是181条已确认事实错误：107条涉及依据超出指定值，57条涉及不足却选择依据，34条涉及确定判定但没有依据，22条涉及结构无法解析。相关正文可能有用，也可能引用错误，仍需完整审阅。

[联合入口实机记录](runs/joint_smoke_v1/report.md)含性别招聘判断、真空传声和姓名提取三题，偏见提示off/prompt各一次，共6条真实模型调用，0运行错误。仅用于验证调用链，不报告偏见降低或联合治理成功率。没有触发信号也不意味着事实或偏见已经验证合格。检查证明见[integration_check.json](integration_check.json)。

## 调用

```python
from src.governance.joint import JointGovernance
from src.governance.retrieval import LocalRetriever
from src.models.llm_model import LLMModel

joint = JointGovernance(
    LocalRetriever("knowledge/corpus_v3.json"),
    lambda: LLMModel("models/Qwen2.5-0.5B-Instruct", local_files_only=True),
)
result = joint.answer("声音能在真空中传播吗？", bias_mode="prompt")
print(result["answer"], result["consistency"])
```

bias_mode=off沿用C提示；prompt加本项目明确编写的偏见约束；hook调用构造器传入的bias_hook(prompt)，并要求hook_id作为版本标识。外部hook应返回非空字符串且保留问题和证据正文，否则在模型调用前失败，不静默绕过偏见步骤。调用方负责审核hook本身的行为；该接口并不证明其有效。

返回保留原answer、C的prompt、最终final_prompt及校验值、evidence、模式、模型调用数、输出来源、阶段轨迹、异常和审计结果。guarded触发程序拒答时不加载模型，明确记录偏见生成被绕过，不能说成完成了联合模型推理。一个实例串行复用模型，不支持无保护的并发调用。

materials参数是审计使用的编号上下文，调用方需要同时将对应材料写入问题；它不会自动作为新知识加入模型提示。检查器不读取参考答案，也不改写生成内容。

## 检查边界

机械检查包括引用编号及映射是否存在、basis是否属于给定材料、确定结论没有依据、不足结论却选择材料、结构解析失败。未知URL和带不确定性文本中的数字仅为screening信号：数字可能来自假设或引用，URL也可能是新的合法来源，不能直接判错。

本版本没有语义蕴含模型，不能自动断定某段真实资料是否支持整段回答，也不会可靠识别所有前后矛盾或无依据确定断言。返回semantic_support=not_evaluated、factual_accuracy=null；不把低级规则称作完整事实核验。默认治理入口及历史结果保持原样。

```powershell
python -m experiments.verify_c_integration
python -m experiments.check_c_delivery --run-tests
```

audit_c_consistency和demo_c_joint输出使用固定v1新目录，已有目录时拒绝覆盖。重新实验需明确新版本输出路径；实机源快照对应运行当时实现，后续hook保护增强由单元测试另行验证。
