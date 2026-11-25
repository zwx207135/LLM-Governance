# C组件交接说明

2026-11-25新增[C到A的真实证据导出](closeout_supplement_20261125_v1/A_HANDOFF.md)：覆盖A当前12条开发题和36条正常任务，固定输入副本、UID映射、语料和参数。48条均无命中，明确记录为空，不补造片段；另有1条有命中探针的接口夹具检查。实际模型调用0，不能替代A的真实联合生成与正式冻结。

本说明只交付C的检索与抗幻组件，不修改调用方的联合方法、界面或正式评分。当前为开发配置，不是正式验收批准。

## 明确采用的组合

`configs/c_component_profile.json`显式选择v4知识库、`AwardYearAliasRetriever`、top_k=2、min_score=1.5和原combined提示。配置绑定语料SHA256；不同语料需另存新配置，不能静默替换。原`GovernanceService`的全局默认没有被修改。

```python
from pathlib import Path
from src.governance.c_component import build_c_service

root = Path.cwd()  # 仓库根目录

def model_factory():
    from src.models.llm_model import LLMModel
    return LLMModel(str(root / "models/Qwen2.5-0.5B-Instruct"), local_files_only=True)

service, retriever, config = build_c_service(root, model_factory)
prepared = service.answer(
    "1921年度诺贝尔物理学奖实际在哪一年颁发？",
    strategy=config["strategy"], category="factual", prepare_only=True,
)
assert prepared["answer"] is None
assert prepared["model_calls"] == 0
diagnostics = retriever.search_with_diagnostics(prepared["question"])
```

真正需要生成时，将`prepare_only`置为False并使用`max_new_tokens`参数。生成来自模型，记录`answer_origin=model`、`model_calls=1`；已有guarded候选的程序拒答则标为`policy_abstention`，不能当模型回答。调用失败应保留异常，不能自行填入参考答案。

## 输入和输出

- 请求输入只有问题、策略、任务类别和生成长度等运行参数。配置拒绝未知字段，包括reference/gold，也不按配置动态导入任意Python模块。
- 返回原问题、实际prompt、evidence、检索状态、证据标签和输出来源；生成时另有token数、截断和耗时。`prepare_only`只准备提示，不加载模型、不输出答案。
- 数学逻辑使用`math_logic`类别，在combined中绕过检索；`normal_control`表示正常任务，但原combined并不因此强制关闭所有检索，不要误读为专用正常任务路由。
- 对命中的每条资料保留source_id、URL、定位、查阅时间和语料版本。年份别名回退的有效检索查询及新增别名在`search_with_diagnostics`返回值中；数学绕过时不要另行检索后冒称该证据被模型使用。

## 已检查的六种情况

[接口检查原件](c_component_contract.json)覆盖：年度资料命中、无命中、数学绕过、年份别名、错误主体但有年度公告、正常JSON任务。检查全部是prepare-only，模型工厂一旦被调用即报错。错误主体案例保留真实年度资料，不代表组件已判定人物存在/不存在或自动纠正回答。

```powershell
python -X utf8 experiments/check_c_component_contract.py
python -X utf8 experiments/build_c_revision_index.py --verify docs/c_work/revision_index_v1
python -X utf8 experiments/check_c_delivery.py --run-tests
```

## 可选候选与边界

| 组件 | 已具备的能力 | 不应宣称的能力 |
| --- | --- | --- |
| combined | 原回答约束＋检索证据；数学绕过 | 不保证事实正确、主体一致或没有矛盾 |
| SafeAnchorRetriever | 修复特定词项碰撞，保留BM25 | 不是通用实体消歧器 |
| AwardYearAliasRetriever | 显式年份/类别过滤及无命中别名回退 | 不补造库外年份记录，不验证现实中的全部事实 |
| compact/guarded | 短提示或按证据门控 | 可能漏信息或错拒常识，不作为默认替换 |
| 有限JSON约束 | 限制格式、键、类型和值域 | 不能证明字段内容和证据蕴含正确 |
| 对照卡/subject_focus | 可复现的证据呈现与问题分解候选 | 正反结果并存，均未替换默认 |

C只提供上述组件及证据说明；调用方需自行决定正式集成配置。任何独立评分、数据泄漏交叉检查或正式批准，不由此接口文档代签。
