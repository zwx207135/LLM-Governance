# A 同学交付与复现说明

A 负责偏见治理、联合方法和权衡实验。此目录对应 2026 年 11 月 22 日分工方案 A1 至 A4。历史 baseline 文件原样保留，新增实验独立保存。

## 已实现

- `src/governance/interventions.py`：基础公平提示、分题型提示、三次调用的初稿—检查—改写；完整保存每次消息、回答、token 数、截断、调用数及耗时。
- `configs/a/candidates.json`：E0 和三种开发候选。认知偏差使用证据与反证约束，群体偏见使用个体证据约束。
- `configs/a/constraints_probe.json`：正常任务四组诊断。constraints_only / joint_constraints 仅测试回答约束，不代表已完成 C 的检索治理。
- 联合顺序：回答约束与公平性规则 → C 的证据注入 → 初稿 → 可选检查与改写。生成接口接收 messages 并返回 text 和统计字段，可由 D 的公共入口替换。
- 正式四组及消融配置模板、自检消融配置、36 条正常任务与逐条质量标准、研究章节及答辩讲稿。

## 运行

在 WSL 中运行，所有路径相对仓库根目录：

```bash
cd /home/zhangwx/LLM-Governance
PY=/home/zhangwx/miniconda3/envs/llm-governance/bin/python
$PY -m unittest discover -s tests -p test_a_governance.py
$PY experiments/run_a.py --input datasets/a/pilot_dev.json --output results/a/dev_candidates_v1
$PY experiments/run_a.py --input datasets/a/normal_tasks.json --configs configs/a/constraints_probe.json --output results/a/normal_probe_v1
```

输出目录必须不存在，防止混入旧结果。每条完成后刷新 JSONL；错误记录不伪装成成功结果并使进程非零退出。本入口不承担 D 的全局断点恢复任务。模型加载与预热单独计时；每次 GPU 生成前后同步；总耗时包含提示处理与解码。输出 `manifest.json` 包含模型文件哈希、输入、配置、证据、脚本哈希、Git 版本与脏状态及软件版本。基础模型 do_sample=False，seed=42，max_new_tokens=128；这些是本次诊断参数，正式实验须四人共同冻结后重跑。

## 数据边界

pilot_dev 仅从 12 类偏见数据各取一条非配对直接题，合计 12 条。为开发小样本，不是冻结测试集；不能推出全体 480 条、配对题或中文 180 条的结论。没有把 expected_principle、参考答案或标注理由送入模型。中文集与主集存在重复 ID 和近似问法，B 完成跨集去重与成组划分前，不运行正式测试。A 的开发样本 UID 必须交给 B，连同近似题及配对题划入开发组，禁止出现在最终测试组。

## C 和 D 的对接

`--evidence` 接收 JSON 字典，键为输入样本 uid。值至少含 chunks、snapshot、retrieval_parameters；每个片段须有 source_id、text、source、version、collected_at。真实检索无命中时显式提供空 chunks，仍须记录快照和参数。模板见 evidence_interface_example.json。不得从测试题参考答案构建此文件。当前仓库无检索模块，因此不自动伪造证据，也不将仅约束组称为完整 E2/E3。

正式实验先将 B 冻结输入转换为统一 uid/category/type/question 格式，并由 A 在开发集评分后将选定策略写入新的冻结配置，记录配置哈希与签收。随后用 formal_matrix_TEMPLATE.json 的结构运行四组；模板中的 basic 不是已选定的方法。`E3_without_fairness` 应与 E2 等价，`E3_without_anti` 应与 E1 等价，优先复用输出，避免重复计算；若最终选用自检，再运行 self_check_ablation.json，并让两个组的其他设置一致。

## 验收仍需真实完成的依赖

1. B 提供冻结评分规范、开发测试划分；A 完成至少 20% 分层复核及全部高分争议案例，配对成组抽样。当前没有真人独立标注，不填写虚构一致率。
2. 用开发集的偏见严重度、发生率、拒答和成本选方案，独立复核后冻结。没有评分前，三种方案仅作为候选。
3. C 提供经过核验的知识库、证据及防泄漏检查，D 提供幻觉评分；之后运行正式 E0–E3 和必要消融。
4. 评分后整理至少 3 个改善与 3 个失败或副作用案例；若观察不到三例改善，如实记录数量，不能编造案例。
5. D 的演示系统落地后，A 按说明连续演练三次并记录实际结果。当前没有系统可供演练。

上述事项不能用代码测试或关键词替代。当前可交付的是可运行方法、实测开发输出、成本记录及交接材料，不能宣称已通过最终验收。

## 本次结果索引

见 completion.md 的实测表、cases.md 的真实案例及各运行目录 review.csv。首轮为128 token诊断，修订轮为384 token；不得跨轮作同参数对照。修订版显式重述初稿，首轮源码与结果完整保留。当前仓库运行命令采用修订后的实现，复现首轮须使用对应 source_snapshot。
