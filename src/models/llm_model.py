import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


class LLMModel:
    def __init__(self, model_path):
        print("========== 加载模型 ==========")

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print("设备:", self.device)

        if self.device == "cuda":
            print("GPU:", torch.cuda.get_device_name(0))

        # 加载 tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)

        # 加载模型
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype="auto",
            device_map="auto"
        )

        # 推理模式
        self.model.eval()

        print("模型加载成功！")

    def generate(self, prompt, max_new_tokens=200):
        """
        输入一个问题，让模型生成回答
        """

        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]

        # 按照 Qwen 的聊天格式组织输入
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        # 转成模型输入
        inputs = self.tokenizer(
            [text],
            return_tensors="pt"
        ).to(self.model.device)

        # 生成
        with torch.no_grad():
            generated_ids = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens
            )

        # 去掉输入部分，只保留模型生成的内容
        generated_ids = [
            output_ids[len(input_ids):]
            for input_ids, output_ids in zip(
                inputs.input_ids,
                generated_ids
            )
        ]

        # 转回字符串
        response = self.tokenizer.batch_decode(
            generated_ids,
            skip_special_tokens=True
        )[0]

        return response