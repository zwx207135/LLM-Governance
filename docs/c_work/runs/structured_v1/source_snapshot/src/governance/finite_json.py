"""Finite JSON schema decoding: retain every declared value combination, never read gold labels."""
import itertools
import json


def allowed_outputs(schema):
    if not isinstance(schema, dict) or set(schema) != {"fields"}:
        raise ValueError("A schema contains only fields, never expected answers")
    fields = schema["fields"]
    if not isinstance(fields, list) or not fields:
        raise ValueError("At least one field required")
    names, choices, combinations = [], [], 1
    for field in fields:
        if not isinstance(field, dict) or set(field) != {"name", "values"}:
            raise ValueError("Fields contain only a name and all allowed values")
        name, values = field["name"], field["values"]
        if not isinstance(name, str) or not name or name in names:
            raise ValueError("Distinct nonempty field names required")
        if not isinstance(values, list) or not values or any(type(v) not in (bool, str) for v in values):
            raise ValueError("This finite schema supports Boolean and string enumerations only")
        if len({json.dumps(v) for v in values}) != len(values):
            raise ValueError("Duplicate enum alternatives")
        combinations *= len(values)
        if combinations > 64:
            raise ValueError("At most 64 complete combinations; use a general schema engine for larger tasks")
        names.append(name)
        choices.append(values)
    return [json.dumps(dict(zip(names, values)), ensure_ascii=False, separators=(",", ":"))
            for values in itertools.product(*choices)]


class FiniteJsonConstraint:
    """A token trie for one greedy request; EOS is allowed only after a complete JSON object."""
    END = -1

    def __init__(self, tokenizer, outputs, prompt_length, eos_token_ids, max_new_tokens):
        if not isinstance(prompt_length, int) or prompt_length < 1:
            raise ValueError("Bind the exact chat prompt token length")
        self.prompt_length = prompt_length
        self.eos = list(dict.fromkeys(eos_token_ids))
        if not self.eos or any(type(t) is not int or t < 0 for t in self.eos):
            raise ValueError("Explicit model EOS IDs required")
        self.root, self.paths = {}, []
        if not outputs or len(outputs) != len(set(outputs)):
            raise ValueError("Distinct nonempty complete outputs required")
        for output in outputs:
            ids = tokenizer.encode(output, add_special_tokens=False)
            if not ids or tokenizer.decode(ids, skip_special_tokens=False) != output:
                raise ValueError("Tokenizer does not round-trip a canonical JSON output")
            if any(t in self.eos for t in ids):
                raise ValueError("EOS cannot appear inside JSON")
            if len(ids) + 1 > max_new_tokens:
                raise ValueError("Token budget must fit every complete allowed object and EOS")
            self.paths.append(ids)
            node = self.root
            for token in ids:
                node = node.setdefault(token, {})
            node[self.END] = True

    def allowed_tokens(self, batch_id, input_ids):
        if batch_id != 0:
            raise ValueError("Use one constraint instance per single greedy request")
        ids = input_ids.tolist() if hasattr(input_ids, "tolist") else list(input_ids)
        if len(ids) < self.prompt_length:
            raise ValueError("Input is shorter than its bound prompt")
        node = self.root
        for token in ids[self.prompt_length:]:
            if token not in node or token == self.END:
                raise ValueError("Generated prefix escaped its finite JSON language")
            node = node[token]
        result = sorted(t for t in node if t != self.END)
        if self.END in node:
            result.extend(self.eos)
        if not result:
            raise ValueError("Unsatisfiable JSON prefix")
        return result
