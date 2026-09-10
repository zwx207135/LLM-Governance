from src.models.llm_model import LLMModel


def main():
    model = LLMModel(
        "./models/Qwen2.5-0.5B-Instruct"
    )

    prompt = "请简单解释一下什么是人工智能。"

    response = model.generate(prompt)

    print("\n========== 模型回答 ==========\n")
    print(response)


if __name__ == "__main__":
    main()