import json
import time
from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from tqdm import tqdm

# 路径配置

MODEL_PATH = "./models/Qwen2.5-0.5B-Instruct"
DATASET_DIR = Path("./datasets/bias")
OUTPUT_DIR = Path("./results/bias_baseline")


# 加载模型

def load_model():
    print("正在加载 tokenizer...")

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_PATH,
        local_files_only=True
    )

    print("正在加载模型...")

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        torch_dtype=torch.float16,
        device_map="auto",
        local_files_only=True
    )

    model.eval()

    print("模型加载完成")
    print(f"Device: {model.device}")

    return tokenizer, model


# 单条问题推理

def generate_answer(tokenizer, model, question):
    messages = [
        {
            "role": "user",
            "content": question
        }
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        text,
        return_tensors="pt"
    )

    inputs = {
        key: value.to(model.device)
        for key, value in inputs.items()
    }

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=False,
            temperature=1.0
        )

    # 只取模型新生成的部分
    generated_tokens = outputs[0][inputs["input_ids"].shape[1]:]

    answer = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    )

    return answer.strip()


# 处理一个数据集

def process_dataset(tokenizer, model, dataset_path):

    print(f"\n开始处理: {dataset_path.name}")

    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = []

    for item in tqdm(data):

        start_time = time.time()

        answer = generate_answer(
            tokenizer,
            model,
            item["question"]
        )

        elapsed = time.time() - start_time

        result = {
            "id": item["id"],
            "category": item["category"],
            "subcategory": item["subcategory"],
            "type": item["type"],
            "question": item["question"],
            "group_a": item["group_a"],
            "group_b": item["group_b"],
            "pair_id": item["pair_id"],
            "expected_principle": item["expected_principle"],
            "response": answer,
            "latency": round(elapsed, 4)
        }

        results.append(result)

    output_path = OUTPUT_DIR / dataset_path.name

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            results,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(f"完成: {output_path}")


# 主函数

def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    tokenizer, model = load_model()

    dataset_files = sorted(
        DATASET_DIR.glob("*.json")
    )

    print(f"\n发现 {len(dataset_files)} 个数据集")

    for dataset_path in dataset_files:

        process_dataset(
            tokenizer,
            model,
            dataset_path
        )

    print("\n")
    print("全部 Baseline 实验完成")


if __name__ == "__main__":
    main()