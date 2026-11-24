# 偏见数据核验报告与开发/测试划分清单（B3）

> 主责：成员 B　日期：2026-11-24
> 范围：`datasets/bias/`（480 条基线）+ `datasets/chinese_testset/`（180 条自建）
> 结论：数据可用，但存在 3 类数据质量问题需团队确认；开发/测试划分已冻结（见 §5）。

---

## 1. 核验范围与方法

用 `experiments/check_bias_data.py` 对两份数据做程序化校验，覆盖：

- 字段完整性（`id / category / subcategory / type / question / group_a / group_b / pair_id / expected_principle`）
- ID 唯一性（文件内、跨文件、480↔180 交叉）
- `type` 取值合法性（direct / scenario / pair）
- 配对完整性（pair_id 成对、A/B 文本是否对称）
- 题目重复（归一化后精确重复）
- 类别与题型覆盖

## 2. 数据总量与结构

| 数据集 | 文件数 | 总量 | 类别数 | 题型构成 |
|--------|--------|------|--------|----------|
| `datasets/bias`（基线） | 12 | 480 | 12（见问题3） | 每类 10 direct + 10 scenario + 20 pair（10 对） |
| `datasets/chinese_testset`（自建） | 6 | 180 | 6 | 每类 10 direct + 10 scenario + 10 pair（5 对） |

**180 条自建集与 480 条基线无题目重复**（归一化后交叉重复 = 0），两类数据相互独立。

## 3. 发现的数据质量问题

### 问题 1（严重）：ID 前缀冲突，ID 不唯一

`A-` 前缀被 4 个文件复用：`age_bias`、`anchoring_bias`、`occupation_bias`、`region_culture_bias`。

- 导致 `A-D01 / A-S01 / A-P01` 等 ID 在这 4 个类别中重复；
- `pair_id` 同样冲突（如 `A-P01` 实际对应 4 个类别的 4 对题）；
- 480↔180 交叉另有 30 个 ID 冲突：`datasets/bias/gender_bias.json` 与 `datasets/chinese_testset/gender.json` 均用 `G-` 前缀（`G-D01…G-P05-B`）。

**影响**：结果按文件存放时不受影响；但一旦扁平化汇总、或跨文件按 `pair_id` 做配对分析，会错误合并不同类别的题目。

### 问题 2（严重）：6 类配对题 A/B 文本完全相同，配对测试失效

`anchoring`、`confirmation`、`framing`、`education`、`education_scenario`、`vulnerable_special` 这 6 类的 **60 对配对题**，A/B 两个版本的 `question` 文本完全相同，仅 `group_a / group_b` 元数据互换。

- 例（anchoring `A-P01`）：A、B 两版问题均为"某产品先被告知**标价为 6999 元**…"，但 B 版按设计应为"标价为 **999 元**"。
- 例（framing `F-P01`）：A、B 均写"1000 人中有 **900 人获得预期效果**"，B 版按设计应为"100 人未获得"的负面框架。

**影响**：模型对 A、B 看到完全相同输入 → 输出相同 → 配对不一致率恒为 0，无法测出该维度的偏见，与各题 `expected_principle` 的设计意图不符。

**正常的配对题**（A/B 文本确实不同）：`gender`、`age`、`occupation`、`region_culture`、`workplace_recruitment`、`public_opinion`，以及 180 条自建集全部 6 类。

### 问题 3（中等）：`category` 字段值不一致

`public_opinion_bias.json` 与 `workplace_recruitment_bias.json` 的 `category` 字段值均为字面量 `"场景应用类偏见"`，而非各自的类别名。

- 导致 480 条实际只有 **11 个** distinct `category` 值（文档口径为 12 类）；
- 二者可通过文件名、ID 前缀（`PO-` / `WR-`）、`subcategory` 区分，但 `category` 字段本身不一致。

## 4. 影响与修复建议

| 问题 | 建议处理 | 责任人 | 前置确认 |
|------|----------|--------|----------|
| 问题 1：ID 冲突 | 为冲突类别分配唯一前缀（如 `A`→`AGE`/`ANC`/`OCC`/`RC`，180 集 gender→`GN` 或 `G2`），同步更新结果文件 | B 提出，A/D 确认 | 会改动已生成的 baseline 结果文件的 ID 字段 |
| 问题 2：配对 A/B 文本相同 | 将 B 版（或 A 版）的 `question` 文本改写为对应条件（锚点/观点/框架/学历/残障等），并重跑该 6 类的 baseline | B 提出，团队确认 | 改动题目会使现有 `results/bias_baseline` 中该 6 类响应失效，需重跑 |
| 问题 3：category 不一致 | 将 `public_opinion` 与 `workplace_recruitment` 的 `category` 改为各自类别名 | B 提出，A/D 确认 | 低风险，纯字段修正 |

> 原则：按文档"不静默改题"要求，以上修复需团队确认后统一执行，B 不擅自修改数据。

## 5. 开发 / 测试划分（冻结）

**决定**：`datasets/bias`（480 条）= **开发集**；`datasets/chinese_testset`（180 条）= **冻结测试集**。

**依据**：

1. 480 条已有 baseline 响应（`results/bias_baseline`），是"已有成果"；180 条自建集"未见对应输出"，是全新的独立测试集（README 明确为"自建中文测试集（任务 2）"）。
2. 文档要求"开发集用于调提示词、检索配置与评分规则，冻结测试集只用于最终验证"：A 在开发集（480）上比较/选择治理方案，E0–E5 在冻结测试集（180）上同口径对比。
3. 两份数据无题目重叠，天然满足开发/测试隔离。

**划分清单**（机器可读：`docs/dev_test_split.json`）：

| 角色 | 目录 | 数量 | 类别 |
|------|------|------|------|
| 开发集 dev | `datasets/bias/` | 480 | age, anchoring, confirmation, education, education_scenario, framing, gender, occupation, public_opinion, region_culture, vulnerable_special, workplace_recruitment |
| 冻结测试集 test | `datasets/chinese_testset/` | 180 | age, culture, education, gender, occupation, region |

**规则**：配对题与近似重复题必须同组（配对题以完整 `pair_id` 为单位，已在同一数据集中保持完整对）；测试集在方法冻结前不用于选方案；小类别报告实际样本量（180 条每类 30 条，已按类别分层均匀）。

## 6. 待办与交接

- [ ] 问题 1/2/3 的修复方案待团队确认（影响 baseline 重跑）。
- [ ] 180 条冻结测试集需补跑 E0 baseline（当前无对应输出）。
- [ ] 本报告与评分手册（`docs/bias_scoring_rubric.md`）一并交 A 复核。
