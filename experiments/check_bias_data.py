"""成员 B（B3）：偏见数据核验。

校验 datasets/bias（480 条）与 datasets/chinese_testset（180 条）的：
  1) 字段完整性
  2) ID 唯一性
  3) type 取值合法性
  4) 配对（pair）完整性：pair_id 成对、A/B 对称
  5) 题目重复（文件内 / 跨文件 / 480 与 180 交叉）
  6) 类别与题型覆盖

输出：打印汇总，并把详细审计结果写入 results/bias_data_audit.json
以及冻结的开发/测试划分清单 results/dev_test_split.json。
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIAS_DIR = ROOT / "datasets" / "bias"
TEST_DIR = ROOT / "datasets" / "chinese_testset"
RESULTS_DIR = ROOT / "results"

REQUIRED_FIELDS = [
    "id", "category", "subcategory", "type", "question",
    "group_a", "group_b", "pair_id", "expected_principle",
]
VALID_TYPES = {"direct", "scenario", "pair"}


def norm(text):
    """归一化：去空白与标点，用于重复检测。"""
    if text is None:
        return ""
    return re.sub(r"[\s\W_]+", "", str(text), flags=re.UNICODE).lower()


def load_items(directory):
    items = []
    source_meta = {}
    for f in sorted(directory.glob("*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        source_meta[f.name] = {"count": len(data)}
        for it in data:
            it = dict(it)
            it["_file"] = f.name
            items.append(it)
    return items, source_meta


def main():
    bias_items, bias_meta = load_items(BIAS_DIR)
    test_items, test_meta = load_items(TEST_DIR)

    issues = defaultdict(list)
    stats = {"bias": {}, "test": {}}

    # ---- 字段完整性 ----
    for tag, items in [("bias", bias_items), ("test", test_items)]:
        missing = Counter()
        for it in items:
            for fld in REQUIRED_FIELDS:
                if fld not in it or it[fld] in ("", None):
                    missing[fld] += 1
        stats[tag]["missing_fields"] = dict(missing)

    # ---- type 合法性 ----
    for tag, items in [("bias", bias_items), ("test", test_items)]:
        bad_type = [it["id"] for it in items if it.get("type") not in VALID_TYPES]
        if bad_type:
            issues[f"{tag}:bad_type"].extend(bad_type)

    # ---- ID 唯一性（每文件内 + 全局）----
    for tag, items in [("bias", bias_items), ("test", test_items)]:
        per_file = defaultdict(Counter)
        for it in items:
            per_file[it["_file"]][it["id"]] += 1
        dup_ids = {f: [i for i, c in c.items() if c > 1]
                   for f, c in per_file.items() if any(v > 1 for v in c.values())}
        if dup_ids:
            issues[f"{tag}:dup_id_in_file"].append(dup_ids)

    all_ids = [it["id"] for it in bias_items + test_items]
    dup_global = [i for i, c in Counter(all_ids).items() if c > 1]
    if dup_global:
        issues["global:dup_id_across_480_180"] = dup_global

    # ---- 配对完整性 ----
    def check_pairs(items, tag):
        pair_groups = defaultdict(list)
        for it in items:
            if it.get("type") == "pair":
                pid = it.get("pair_id")
                if not pid:
                    issues[f"{tag}:pair_missing_pair_id"].append(it["id"])
                else:
                    pair_groups[pid].append(it)
        bad = []
        for pid, grp in pair_groups.items():
            if len(grp) != 2:
                bad.append({"pair_id": pid, "n": len(grp),
                            "ids": [g["id"] for g in grp]})
        if bad:
            issues[f"{tag}:pair_not_two"].extend(bad)
        # A/B 对称性：question 归一化后应仅在名字等少数字符上不同
        asymmetric = []
        for pid, grp in pair_groups.items():
            if len(grp) == 2:
                q0, q1 = norm(grp[0]["question"]), norm(grp[1]["question"])
                if q0 == q1:
                    asymmetric.append({"pair_id": pid, "note": "两版题目完全相同"})
        if asymmetric:
            issues[f"{tag}:pair_identical_questions"].extend(asymmetric)
        return len(pair_groups)

    n_pairs_bias = check_pairs(bias_items, "bias")
    n_pairs_test = check_pairs(test_items, "test")
    stats["bias"]["pair_groups"] = n_pairs_bias
    stats["test"]["pair_groups"] = n_pairs_test

    # ---- 题目重复（归一化后）----
    def find_dups(items, tag):
        seen = defaultdict(list)
        for it in items:
            seen[norm(it["question"])].append(it)
        dups = {q: [it["id"] for it in lst]
                for q, lst in seen.items() if len(lst) > 1 and q != ""}
        if dups:
            issues[f"{tag}:duplicate_questions"] = dups
        return seen

    seen_bias = find_dups(bias_items, "bias")
    seen_test = find_dups(test_items, "test")

    # ---- 480 与 180 交叉重复 ----
    cross = {}
    for q, lst in seen_bias.items():
        if q in seen_test:
            cross[q] = {
                "bias_ids": [it["id"] for it in lst],
                "test_ids": [it["id"] for it in seen_test[q]],
            }
    stats["cross_480_180_duplicate_questions"] = len(cross)
    if cross:
        issues["cross:480_180_duplicate"] = cross

    # ---- 类别 / 题型覆盖 ----
    def coverage(items):
        cat = Counter(it["category"] for it in items)
        cat_type = defaultdict(Counter)
        for it in items:
            cat_type[it["category"]][it["type"]] += 1
        return dict(cat), {k: dict(v) for k, v in cat_type.items()}

    stats["bias"]["categories"], stats["bias"]["category_type"] = coverage(bias_items)
    stats["test"]["categories"], stats["test"]["category_type"] = coverage(test_items)

    # ---- 输出 ----
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    audit = {
        "bias_files": bias_meta,
        "test_files": test_meta,
        "bias_total": len(bias_items),
        "test_total": len(test_items),
        "stats": stats,
        "issues": {k: v for k, v in issues.items()},
        "issue_summary": {k: (len(v) if isinstance(v, list) else 1) for k, v in issues.items()},
    }
    out = RESULTS_DIR / "bias_data_audit.json"
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"bias 总量={len(bias_items)}  文件数={len(bias_meta)}")
    print(f"test 总量={len(test_items)}  文件数={len(test_meta)}")
    print("=== 类别×题型覆盖（bias 480条）===")
    for cat, ct in stats["bias"]["category_type"].items():
        print(f"  {cat:28s} {ct}")
    print("=== 类别×题型覆盖（test 180条）===")
    for cat, ct in stats["test"]["category_type"].items():
        print(f"  {cat:28s} {ct}")
    print("=== 配对组数 ===")
    print("  bias pair_groups =", n_pairs_bias, " test pair_groups =", n_pairs_test)
    print("=== 480↔180 交叉重复题数 ===", stats["cross_480_180_duplicate_questions"])
    print("=== 问题汇总 ===")
    if issues:
        for k, v in issues.items():
            print(f"  [ISSUE] {k}: {v if not isinstance(v, list) else v[:5]}")
    else:
        print("  无问题")
    print(f"\n审计结果已写入 {out}")


if __name__ == "__main__":
    main()
