"""C integration boundary: an explicit bias prompt or caller-supplied prompt hook plus raw-output audit."""
import hashlib
from src.governance.service import GovernanceService
from src.governance.consistency import check_consistency

BIAS_PROMPT = "避免根据性别、年龄、地域等群体身份推断个人能力、品格或资格；围绕与任务相关的具体证据判断。不要为消除偏见而编造事实或省略必要的不确定性。"


class JointGovernance:
    def __init__(self, retriever, model_factory, bias_hook=None, hook_id=None):
        if bias_hook is not None and (not callable(bias_hook) or not isinstance(hook_id, str) or not hook_id.strip()):
            raise ValueError("A custom bias hook needs a callable and explicit versioned hook_id")
        self.c = GovernanceService(retriever, model_factory)
        self.factory = model_factory
        self.model = None
        self.hook = bias_hook
        self.hook_id = hook_id

    def answer(self, question, strategy="combined", category=None, bias_mode="off", max_new_tokens=192, materials=()):
        if bias_mode not in ("off", "prompt", "hook") or (bias_mode == "hook" and self.hook is None):
            raise ValueError("Configure an explicit bias mode and available hook")
        if type(max_new_tokens) is not int or not 1 <= max_new_tokens <= 2048:
            raise ValueError("Invalid generation budget")
        prepared = self.c.prepare(question, strategy, category)
        row = {**prepared, "bias_mode": bias_mode, "bias_hook_id": self.hook_id if bias_mode == "hook" else None,
               "status": "error", "model_calls": 0, "answer": None, "answer_origin": None,
               "stages": ["c_prepare"], "bias_effectiveness": "not_evaluated"}
        try:
            prompt = prepared["prompt"]
            if prepared["answer_override"] is not None:
                row.update(answer=prepared["answer_override"], answer_origin="policy_abstention")
                row["stages"].append("bias_generation_bypassed_for_program_answer")
            else:
                if bias_mode == "prompt":
                    prompt = BIAS_PROMPT + "\n\n" + prompt
                elif bias_mode == "hook":
                    prompt = self.hook(prompt)
                    if not isinstance(prompt, str) or not prompt.strip():
                        raise ValueError("Bias hook must return nonempty prompt text")
                    if question not in prompt or any(h["text"] not in prompt for h in prepared["evidence"]):
                        raise ValueError("Bias hook removed the question or supplied evidence")
                row["stages"].append("bias_" + bias_mode)
                row["final_prompt"] = prompt
                row["final_prompt_sha256"] = hashlib.sha256(prompt.encode()).hexdigest()
                if self.model is None:
                    self.model = self.factory()
                row["model_calls"] = 1
                row["answer"] = self.model.generate(prompt, max_new_tokens=max_new_tokens, do_sample=False)
                row.update(self.model.last_generation)
                row["answer_origin"] = "model"
                row["stages"].append("generate")
            row["consistency"] = check_consistency(row["answer"], prepared["evidence"], prepared["evidence_labels"], materials)
            row["stages"].append("consistency_audit")
            row["status"] = "ok"
        except Exception as exc:
            row["error"] = f"{type(exc).__name__}: {exc}"
            row["stages"].append("failed")
        return row
