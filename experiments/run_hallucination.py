"""C 任务3：跑原始模型，生成幻觉测试集的回答。

用法（在 LLM-Governance 目录下）：
    python experiments/run_hallucination.py
或：
    python -m experiments.run_hallucination

读取 datasets/hallucination/test_set.json，逐条让 Qwen 回答，
结果保存到 results/hallucination/results.json。
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.models.llm_model import LLMModel  # noqa: E402

TEST_SET = ROOT / "datasets" / "hallucination" / "test_set.json"
OUTPUT = ROOT / "results" / "hallucination" / "results.json"
MODEL_PATH = ROOT / "models" / "Qwen2.5-0.5B-Instruct"

MAX_NEW_TOKENS = 200


def main():
    with open(TEST_SET, "r", encoding="utf-8") as f:
        data = json.load(f)

    items = data["items"]
    print(f"测试集共 {len(items)} 条，开始加载模型...")

    model = LLMModel(str(MODEL_PATH))

    results = []
    for i, item in enumerate(items, 1):
        question = item["question"]
        print(f"[{i}/{len(items)}] {question}")

        answer = model.generate(question, max_new_tokens=MAX_NEW_TOKENS)

        results.append({
            "id": item.get("id", i),
            "category": item.get("category", ""),
            "question": question,
            "reference": item.get("reference", ""),
            "answer": answer,
        })

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n完成，结果已保存到 {OUTPUT}")


if __name__ == "__main__":
    main()
