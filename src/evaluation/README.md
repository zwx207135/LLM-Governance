# 幻觉评估器（规则基线）

## 用法

```python
from src.evaluation import HallucinationEvaluator

evaluator = HallucinationEvaluator()
result = evaluator.evaluate(
    question="爱因斯坦获得过几次诺贝尔物理学奖？",
    answer="爱因斯坦获得过一次诺贝尔物理学奖。",
    reference="爱因斯坦获得过一次诺贝尔物理学奖。",
)
print(result)