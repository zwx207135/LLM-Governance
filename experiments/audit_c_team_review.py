"""Read teammate refs and report C-owned review dependencies; never merge or score humans."""
import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.governance.c_component import build_c_service

GIT = ["git", "-c", f"safe.directory={ROOT.as_posix()}"]


def git(*args):
    return subprocess.check_output(GIT + list(args), cwd=ROOT)


def read(ref, path):
    return json.loads(git("show", f"{ref}:{path}").decode("utf-8-sig"))


def norm(text):
    return re.sub(r"[^\w\u4e00-\u9fff]", "", text.lower())


def run(output=None):
    refs = {name: git("rev-parse", ref).decode().strip() for name, ref in {
        "C": "HEAD", "A_main": "origin/main", "B": "origin/feature/b-bias-evaluation",
        "D": "origin/feature/hallucination-evaluation", "dataset": "origin/feature/hallucination-dataset"}.items()}
    a, b, d = refs["A_main"], refs["B"], refs["D"]
    bfiles = [p for p in git("ls-tree", "-r", "--name-only", b).decode().splitlines() if p.startswith("datasets/bias/") and p.endswith(".json")]
    by_uid = {}
    bdev = []
    for filename in bfiles:
        for item in read(b, filename):
            by_uid[f"bias/{Path(filename).stem}/{item['id']}"] = item
            bdev.append(item)
    testfiles = [p for p in git("ls-tree", "-r", "--name-only", b).decode().splitlines() if p.startswith("datasets/chinese_testset/") and p.endswith(".json")]
    btest = [r for f in testfiles for r in read(b, f)]
    inputs = read(a, "datasets/a/pilot_dev.json")
    normals = read(a, "datasets/a/normal_tasks.json")
    lineage = []
    for item in inputs:
        current = by_uid.get(item["uid"])
        candidates = [uid for uid, r in by_uid.items() if r["question"] == item["question"] and uid.split('/')[1] == item["uid"].split('/')[1]]
        lineage.append({"A_uid": item["uid"], "uid_exists_in_B": current is not None,
                        "same_question_at_uid": current is not None and current["question"] == item["question"],
                        "same_question_current_B_uids": candidates})
    def no_model():
        raise AssertionError("Read-only review must never load a model")
    service, retriever, profile = build_c_service(ROOT, no_model)
    coverage = {}
    for label, items in (("A_pilot_dev", inputs), ("A_normal_tasks", normals)):
        rows = []
        for item in items:
            prepared = service.answer(item["question"], profile["strategy"], item.get("category"), prepare_only=True)
            assert prepared["model_calls"] == 0 and prepared["answer"] is None
            rows.append({"uid": item["uid"], "retrieval_status": prepared["retrieval_status"],
                         "chunk_ids": [e["id"] for e in prepared["evidence"]]})
        coverage[label] = {"items": len(rows), "items_with_hits": sum(bool(r["chunk_ids"]) for r in rows), "rows": rows}
    # Execute only the inspected, dependency-free rule class, outside src package imports.
    source = git("show", f"{d}:src/evaluation/hallucination_evaluator.py")
    module = types.ModuleType("reviewed_D_rules")
    exec(compile(source, "D_snapshot/hallucination_evaluator.py", "exec"), module.__dict__)
    evaluator = module.HallucinationEvaluator()
    examples = read(d, "datasets/hallucination/evaluator_examples.json")
    rule_checks = [{"case": r["id"], "score": evaluator.evaluate(r["question"], r["answer"], r["reference"])} for r in examples]
    correct = "爱因斯坦获得过一次诺贝尔物理学奖。"
    clean = evaluator.evaluate("爱因斯坦获奖次数？", correct, correct)
    added_error = evaluator.evaluate("爱因斯坦获奖次数？", correct + "另外，1+1=3。", correct)
    dev_questions = {norm(r["question"]) for r in bdev}
    test_questions = {norm(r["question"]) for r in btest}
    corpus = json.loads((ROOT / profile["corpus"]).read_text(encoding="utf-8"))
    chunk_texts = [norm(r["text"]) for r in corpus["chunks"]]
    leakage = {"B_dev_items": len(bdev), "B_test_items": len(btest),
               "dev_test_exact_normalized_overlaps": len(dev_questions & test_questions),
               "A_pilot_vs_B_test_exact_overlaps": sum(norm(r["question"]) in test_questions for r in inputs),
               "test_question_contained_verbatim_in_C_chunks": sum(any(q and q in chunk for chunk in chunk_texts) for q in test_questions),
               "scope": "exact normalized strings only; not semantic independence or full leakage clearance; frozen test not used for tuning",
               "test_question_text_not_exported": True}
    pilot = ROOT / "docs/c_work/pilot_C_ai_v1"
    with (pilot / "pilot_annotations_C_AI_draft.csv").open(encoding="utf-8-sig", newline="") as stream:
        pilot_rows = list(csv.DictReader(stream))
    assert len(pilot_rows) == 25 and all(r["annotator"] == "C_AI_draft" for r in pilot_rows)
    team_paths = git("ls-tree", "-r", "--name-only", d).decode().splitlines()
    result = {
        "date": "2026-11-25", "scope": "C review of teammate branch contents; no merge, no model inference, no human signoff",
        "branch_commits": refs, "upstream_new_commits_since_previous_pilot_review": {
            "A_main": a != "5a11de96d2e89fcd736823180ebada3f34ada402",
            "B": b != "f579a5f8f2a6253a872260fdf2f33b492df85ec1",
            "D": d != "b7596a792fae70d866ad42dfc80563abb545de9e"},
        "A_B_uid_lineage": {"items": len(inputs), "missing_current_B_uids": sum(not r["uid_exists_in_B"] for r in lineage), "rows": lineage},
        "C_profile": profile, "C_profile_file_sha256": hashlib.sha256((ROOT / 'configs/c_component_profile.json').read_bytes()).hexdigest(),
        "A_input_prepare_only_coverage": coverage, "exact_overlap_screen": leakage,
        "D_rule_screen": {"source_sha256": hashlib.sha256(source).hexdigest(), "examples": rule_checks,
                          "control_clean": clean, "control_with_arithmetic_falsehood": added_error,
                          "same_risk_score_despite_extra_false_claim": clean["hallucination_score"] == added_error["hallucination_score"],
                          "formal_semantic_accuracy": None,
                          "pilot_or_annotation_named_paths_in_D_branch": [p for p in team_paths if re.search(r'pilot|annotation|rubric', p, re.I)]},
        "C_pilot_status": {"AI_draft_rows": len(pilot_rows), "independent_human_reviews": 0, "adjudications": 0},
        "C_owned_review_queue": [
            {"priority": "P0", "task": "与D统一25条试标的字段枚举及参考边界；再由C/D分别独立复核", "entry": "docs/c_work/pilot_C_ai_v1/README.md", "needs_independent_humans": True},
            {"priority": "P0", "task": "为A明确冻结输入版本、UID映射及C证据导出契约；真实无命中必须保留，不补造片段", "entry": "origin/main:docs/a/handoff.md", "owner_boundary": "C负责证据；A负责联合方法与正式运行"},
            {"priority": "P1", "task": "与B交叉复核C语料来源与开发/测试隔离；本报告精确匹配筛查不能替代近重复、语义和来源暴露检查", "entry": "origin/feature/b-bias-evaluation:docs/dev_test_split.json"},
            {"priority": "P1", "task": "向D说明关键词覆盖可能漏掉核心错误与附加错误；C仅提供完整答案证据意见，不代做D评分实现", "entry": "origin/feature/hallucination-evaluation:src/evaluation/hallucination_evaluator.py"},
            {"priority": "P1", "task": "继续保留33/34/37/41/42的目标真值缺口；B的C已完成表述仅能理解为开发交付，不是正式验收", "entry": "C_PROGRESS.md"}
        ],
        "model_calls": 0, "team_implementation_modified": False,
    }
    output = output or ROOT / "docs/c_work/team_review_20261125_v1.json"
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if output.exists() and output.read_text(encoding="utf-8") != text:
        raise FileExistsError("Review inputs changed; choose a new --output version")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    print(json.dumps({"output": str(output), "branch_commits": refs, "uid_gaps": result["A_B_uid_lineage"]["missing_current_B_uids"],
                      "coverage": {k: {f: v[f] for f in ('items', 'items_with_hits')} for k, v in coverage.items()},
                      "leakage": leakage, "D_added_error_same_score": result["D_rule_screen"]["same_risk_score_despite_extra_false_claim"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    run(parser.parse_args().output)
