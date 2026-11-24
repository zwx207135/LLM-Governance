"""Organize C's existing artifacts; read logs without launching inference."""
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "docs/c_work"
GROUPS = [
    ("基础四组与正常对照", ["expanded_v3", "controls_v3"], "runs/expanded_v3/report.md"),
    ("三种提示/门控策略", ["policy_comparison_v1"], "runs/policy_comparison_v1/report.md"),
    ("给定材料及结构约束", ["source_bound_v1", "structured_v1"], "C_STRUCTURED_OUTPUT.md"),
    ("材料位置与中英文措辞", ["balanced_materials_v1", "balanced_labels_cn_v1"], "C_MATERIAL_DIAGNOSTICS.md"),
    ("正常任务路由检查", ["normal_route_v1"], "runs/normal_route_v1/report.md"),
    ("错误证据链与锚点修复", ["anchor_diagnostics_v1", "evidence_first_v1"], "C_FAILURE_EVIDENCE.md"),
    ("奖项补库与范围检索", ["nobel_scope_v1", "nobel_scope_followup_v1", "nobel_scope_followup_v2"], "C_NOBEL_SUPPLEMENT.md"),
    ("资料对照卡与年份别名", ["evidence_binding_v1", "year_alias_v1"], "C_EVIDENCE_USE.md"),
    ("主体错配单轮对照", ["subject_focus_v1"], "C_SUBJECT_FOCUS.md"),
]


def read(relative):
    return json.loads((FOLDER / relative).read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def collect():
    groups = []
    for title, names, report in GROUPS:
        group = {"title": title, "report": report, "runs": [], "outputs": 0, "model_calls": 0, "program_outputs": 0}
        if not (FOLDER / report).is_file():
            raise ValueError("Missing report: " + report)
        for name in names:
            folder = FOLDER / "runs" / name
            rows = [json.loads(line) for line in (folder / "records.jsonl").read_text(encoding="utf-8").splitlines()]
            manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
            if manifest["status"] != "completed" or any(r["status"] != "ok" or not isinstance(r.get("answer"), str) for r in rows):
                raise ValueError("Selected run is not completed real output: " + name)
            origins = Counter(r.get("answer_origin", "model") for r in rows)
            if set(origins) - {"model", "policy_abstention"}:
                raise ValueError("Unexpected output origin: " + name)
            model_calls = sum(r.get("model_calls", 1 if r.get("answer_origin", "model") == "model" else 0) for r in rows)
            if model_calls != origins["model"]:
                raise ValueError("Inconsistent model-call count: " + name)
            item = {"name": name, "outputs": len(rows), "model_calls": model_calls, "program_outputs": origins["policy_abstention"],
                    "records_sha256": digest(folder / "records.jsonl"), "manifest_sha256": digest(folder / "manifest.json")}
            group["runs"].append(item)
            for key in ("outputs", "model_calls", "program_outputs"):
                group[key] += item[key]
        groups.append(group)
    return {"as_of": "2026-11-24", "scope": "selected_C_development_runs_not_independent_samples",
            "groups": groups, "totals": {key: sum(g[key] for g in groups) for key in ("outputs", "model_calls", "program_outputs")},
            "run_directories": sum(len(g["runs"]) for g in groups),
            "excluded": ["all_prepared_and_dry_runs", "early_smoke_runs", "standalone_demo", "joint_integration_runs", "historical_read_only_audit"],
            "independent_human_reviews": 0, "formal_accuracy": None}


def main():
    inventory = collect()
    audit = read("data_audit.json")["summary"]
    followup = read("source_followup_v1/manifest.json")
    tests = read("test_results.json")
    v4 = json.loads((ROOT / "knowledge/build_manifest_v4.json").read_text(encoding="utf-8"))
    totals = inventory["totals"]
    lines = ["# C分工已完成内容总览", "", "整理日期：2026-11-25。只汇总C自己的数据、知识库、抗幻组件、消融和故障分析。旧记录与不成功候选保留；开发成果不代表正式验收通过。", "",
             "## 一眼看当前状态", "",
             "- 开发交付收尾说明与待核验事项：[C_CLOSEOUT](C_CLOSEOUT.md)。",
             "- 新增组员25条试标的[C侧AI辅助稿](pilot_C_ai_v1/README.md)：CSV/Excel、逐条证据及原表快照已交付；等待C/D标签统一和独立真人复核，不计为新模型实验或正式评分。",
             f"- 原题{audit['items']}条已完成结构与来源初审；22条不确定性探针不再把未证实的不存在断言当事实真值。",
             f"- 当前v4开发知识库：{v4['sources']}个来源、{v4['chunks']}个片段；旧v3的16源25段及实验快照保留。",
             f"- 下列{inventory['run_directories']}个C开发运行目录，共{totals['outputs']}条输出：{totals['model_calls']}次模型调用、{totals['program_outputs']}条程序拒答。跨轮包含重复题目和重复答案，不是独立样本数。",
             f"- 最近记录的自动测试为{tests['tests_run']}项，{'全部通过' if tests['passed'] else '尚未全部通过'}；[详细检查](delivery_check.json)。",
             "- 真实独立人工评分仍为0；正式正确率、幻觉降低幅度和评分一致性留空。", "",
             "## 按我们的分工归类", "",
             "| 分工 | 已经做过的工作 | 主要材料 |", "| --- | --- | --- |",
             "| C1 数据核验 | 初审与多轮提案已统一：30条字段提案涉及28题，另有5道限定材料新题；原题不覆盖、候选不自动批准 | [统一索引](revision_index_v1/report.md)、[初审](source_audit_report.md)、[五题候选](pending_repairs_v2/report.md) |",
             "| C2 知识库与检索 | 来源转述与定位、可重建语料、中文BM25、主题锚点、年份/类别/主体范围筛选、年份别名回退 | [构建方法](C_METHODS.md)、[v4补库](C_NOBEL_SUPPLEMENT.md)、[最新修复](C_EVIDENCE_USE.md) |",
             "| C3 抗幻组件 | baseline/constraint/retrieval/combined四组；数学绕过；短提示、门控、JSON约束和资料对照卡候选；证据与输出来源分开记录 | [方法协议](C_METHODS.md)、[结构约束](C_STRUCTURED_OUTPUT.md)、[组件边界](C_EVIDENCE_USE.md) |",
             "| C4 消融与故障 | 四组对照、正常任务副作用、材料位置/标签措辞、检索与生成故障区分；11个历史案例链、30条支持分析和检索图 | [案例链](failure_evidence_ledger_v1.json)、[30条分析](retrieval_support_30_v1.json)、[检索图](figures/c_retrieval_support_30.png) |",
             "| C交接与答辩 | 可复现输入、源码/模型文件哈希、prepare接口、显式组件配置与六类零模型调用接口检查、C方法和讲述要点 | [组件交接](C_COMPONENT_HANDOFF.md)、[C讲述材料](C_DEFENSE_NOTES.md)、[进度](../../C_PROGRESS.md) |", "",
             "## 实验已经做到哪些", "",
             "以下从原始records.jsonl读取数量，逐轮来源与哈希见[实验清单](c_work_inventory.json)。只列选定的C开发运行，不把演示、联合入口、早期smoke或仅准备记录加进来。", "",
             "| 实验组 | 输出条数 | 模型调用 | 程序拒答 | 内容入口 |", "| --- | ---: | ---: | ---: | --- |"]
    for group in inventory["groups"]:
        lines.append(f"| {group['title']} | {group['outputs']} | {group['model_calls']} | {group['program_outputs']} | [报告]({group['report']}) |")
    lines.extend([f"| 合计 | {totals['outputs']} | {totals['model_calls']} | {totals['program_outputs']} | 开发记录，非独立样本 |", "",
                  "阶段不同、题目重复、部分提示和回答逐字一致，不能把这些数量当作效果样本量相加统计。后续策略是在观察已有失败后提出，不能当成独立盲测。", "",
                  "## 已经得到的具体改进", "",
                  "1. 消除‘诺贝尔’中的‘贝尔’误匹配电话史。125题检索回归中15题去掉同类误召回，其余110题结果不变；不是15题全部答对。",
                  "2. 补充5个官方来源、6个片段并独立生成v4。第7题获奖次数、第64/66题年度获奖者等出现具体纠错，但未证明总体正确率提高。",
                  "3. 年份、奖项类别筛选减少跨年证据混入；年份别名回退修复‘1921年度……’有资料却漏检的问题，实际回答由编造转为1922年。原125题对该别名修复的检索回归全部保持相同。",
                  "4. 将‘没有资料’‘主题相关但主体不足’‘资料支持但生成错用’分开。30条V2支持分析为16条核心支持、1条需组合及范围、2条仅前提纠正、2条主题相关不足、8条无资料、1条库中有资料但漏检。全部是AI开发诊断。", "",
                  "## 哪些尝试没有成为默认方案", "",
                  "- 更短的提示可能减少输出和耗时，也可能损失正常任务、引起矛盾；不把更短更快视为正确率提高。",
                  "- 保守门控能阻止部分无依据生成，也会拒答北京等库外常识；程序拒答不算模型能力。",
                  "- 有限JSON约束能保证结构，仍会填错判断和依据；格式正确不等于内容正确。",
                  "- 资料对照卡在个别题改善判断，但也导致只给链接、输出片段ID、丢失比较内容；仍保留为实验候选。",
                  "- 同名人物贡献移植、牛顿相对论、太阳恒星矛盾、无资料时编造、奖项年度与颁发年混淆，均仍有失败实例。", "",
                  "## 尚未完成与协作边界", "",
                  f"C1的首轮统计与补查不合并冒充全部核实：首轮有17题待充分核验；补查17题后另记4条参考问题、8条有限背景及{followup['counts']['pending_source_review']}条仍待具体来源，新增4条提案与原19题提案分开保留，均未自动批准。",
                  "随后针对33、34、37、41、42题又形成5条参考表述提案和5条限定材料新题候选，见pending_repairs_v2。新题明确改变了问题，五个原题目标身份/产品仍未建立完整真值；不是5题已核实，不增加模型调用量，不自动入库或替换原题。",
                  "C仍需核实剩余资料缺口、改善主体绑定/前提纠正、继续检查来源和日期边界。现有语料与开发题主题重叠，尚未完成正式冻结后的独立验证。",
                  "与B交叉检查泄漏、向A交付抗幻接口、配合D复核证据是协作事项；A的联合方法、B的偏见任务、D的正式评分/综合图表/公共演示不由我们代做。已有相关历史工程单独保留，不算这些工作已经验收完成。", "",
                  "## 文件从哪里找", "",
                  "- `datasets/hallucination/test_set.json`：保留的原125题。",
                  "- `knowledge/`：来源输入、v3/v4语料、构建清单；`src/governance/`：C抗幻与检索组件。",
                  "- `docs/c_work/runs/`：逐轮原始记录、配置、证据及源码快照；具体目录见实验清单。",
                  "- `docs/c_work/figures/`：自己的检索图PNG/SVG；运行目录中的材料诊断图是各轮诊断附件。",
                  "- [旧交接页快照](C_HANDOFF_history_20261124.md)：保留早期阶段叙述与历史协作工具入口；旧数字按当时版本解释。", "",
                  "本次只是整理已有内容，没有新增模型实验，也没有改变原题、语料或历史回答。"])
    (FOLDER / "c_work_inventory.json").write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding="utf-8")
    (FOLDER / "C_HANDOFF.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"runs": inventory["run_directories"], **totals, "tests": tests["tests_run"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
