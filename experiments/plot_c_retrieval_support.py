"""C retrieval evidence figure; counts are developer judgments, not accuracy."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    payload = json.loads((ROOT / "docs/c_work/retrieval_support_30_v1.json").read_text(encoding="utf-8"))
    categories = [("supports_core", "支持核心问题"), ("supports_core_with_scope", "需组合证据并保留范围"),
                  ("supports_premise_correction_only", "仅支持纠正前提"), ("topic_only_insufficient", "主题相关但主体证据不足"),
                  ("no_retrieved_evidence", "未召回资料"), ("retrieval_miss_with_available_evidence", "库中有资料但检索漏掉")]
    values = [payload["counts"].get(key, 0) for key, _ in categories]
    if sum(values) != 30:
        raise ValueError("Figure must account for exactly thirty inspected queries")
    font = FontProperties(fname="C:/Windows/Fonts/msyh.ttc")
    fig, ax = plt.subplots(figsize=(11.5, 6.4), dpi=150)
    fig.subplots_adjust(left=.30, right=.94, top=.81, bottom=.19)
    bars = ax.barh(range(len(categories)), values, color=["#397b9a", "#6098ae", "#a2b9c8", "#d5b36a", "#c77c65", "#9d5e64"], height=.62)
    ax.invert_yaxis()
    ax.set_yticks(range(len(categories)), [label for _, label in categories], fontproperties=font, fontsize=11)
    ax.set_xlim(0, 18)
    ax.set_xticks(range(0, 19, 3))
    ax.set_xlabel("查询条数（合计30条）", fontproperties=font, labelpad=10)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0, pad=10)
    ax.grid(axis="x", alpha=.16)
    ax.set_axisbelow(True)
    for bar, value in zip(bars, values):
        ax.text(value + .2, bar.get_y() + bar.get_height() / 2, str(value), va="center", fontsize=11)
    fig.text(.04, .93, "30条开发查询：V2检索证据支持范围", fontproperties=font, fontsize=19, weight="bold")
    fig.text(.04, .87, "AI开发诊断 · 不是模型正确率 · 独立人工复核为0", fontproperties=font, fontsize=11, color="#555555")
    fig.text(.04, .07, "已暴露开发案例；每个问题归入一个主类别。漏检1条在后续年份别名修复中召回。", fontproperties=font, fontsize=10, color="#555555")
    folder = ROOT / "docs/c_work/figures"
    folder.mkdir(exist_ok=True)
    for extension in ("png", "svg"):
        fig.savefig(folder / ("c_retrieval_support_30." + extension), facecolor="white")
    plt.close(fig)
    print("C retrieval figure saved as PNG and SVG")


if __name__ == "__main__":
    main()
