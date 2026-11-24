"""Offline A experiments; never treats heuristic screening as effectiveness scoring."""
import argparse
import hashlib
import json
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.governance.interventions import answer

def digest(obj):
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True).encode()).hexdigest()

def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

class LocalGenerator:
    def __init__(self, model_path, tokens, seed):
        import torch
        import transformers
        self.torch = torch
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(model_path, local_files_only=True)
        self.model = transformers.AutoModelForCausalLM.from_pretrained(model_path, local_files_only=True, torch_dtype='auto', device_map='auto').eval()
        self.tokens = tokens
        self.versions = {'torch': torch.__version__, 'transformers': transformers.__version__, 'python': platform.python_version(), 'device': str(self.model.device)}

    def sync(self):
        if self.torch.cuda.is_available():
            self.torch.cuda.synchronize()

    def __call__(self, messages):
        text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = self.tokenizer(text, return_tensors='pt').to(self.model.device)
        self.sync()
        start = time.perf_counter()
        with self.torch.inference_mode():
            output = self.model.generate(**inputs, max_new_tokens=self.tokens, do_sample=False, temperature=1.0, top_p=1.0, top_k=0, pad_token_id=self.tokenizer.eos_token_id)
        self.sync()
        elapsed = time.perf_counter() - start
        ids = output[0, inputs.input_ids.shape[1]:]
        return {'text': self.tokenizer.decode(ids, skip_special_tokens=True).strip(), 'latency_s': elapsed, 'input_tokens': inputs.input_ids.shape[1], 'output_tokens': len(ids), 'truncated': len(ids) == self.tokens and int(ids[-1]) != self.tokenizer.eos_token_id}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--configs', default=str(ROOT / 'configs/a/candidates.json'))
    p.add_argument('--output', required=True)
    p.add_argument('--evidence', help='C export: sample uid -> {chunks:[{source_id,text,source,version,collected_at}], snapshot, retrieval_parameters}')
    p.add_argument('--model', default=str(ROOT / 'models/Qwen2.5-0.5B-Instruct'))
    p.add_argument('--max-new-tokens', type=int, default=128)
    p.add_argument('--seed', type=int, default=42)
    args = p.parse_args()
    items, configs = load(args.input), load(args.configs)
    if len({i['uid'] for i in items}) != len(items):
        raise ValueError('duplicate uid')
    evidence = load(args.evidence) if args.evidence else {}
    for config in configs:
        if config['retrieval']:
            for item in items:
                e = evidence[item['uid']]
                for key in ('chunks', 'snapshot', 'retrieval_parameters'):
                    assert key in e, key
                for chunk in e['chunks']:
                    assert all(chunk.get(k) for k in ('source_id','text','source','version','collected_at'))
    out = Path(args.output)
    # Exclusive directory creation prevents accidental reruns / mixed configurations.
    out.mkdir(parents=True, exist_ok=False)
    snapshot = out/'source_snapshot'
    snapshot.mkdir()
    for source in (Path(__file__),ROOT/'src/governance/interventions.py',ROOT/'experiments/analyze_a.py'):
        shutil.copy2(source,snapshot/source.name)
    shutil.copy2(args.input,snapshot/'input.json')
    shutil.copy2(args.configs,snapshot/'configs.json')
    if args.evidence:
        shutil.copy2(args.evidence,snapshot/'evidence.json')
    generation = {'do_sample': False, 'max_new_tokens': args.max_new_tokens, 'seed': args.seed}
    metadata = {'input_sha256': digest(items), 'config_sha256': digest(configs), 'evidence_sha256': digest(evidence), 'generation': generation, 'configs': configs, 'model': args.model, 'git_commit': subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip(), 'git_dirty': bool(subprocess.check_output(['git','status','--porcelain'], cwd=ROOT)), 'script_sha256': digest(Path(__file__).read_text()), 'governance_sha256': digest((ROOT/'src/governance/interventions.py').read_text()), 'model_files': {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in Path(args.model).iterdir() if f.is_file()}}
    (out/'manifest.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')
    start = time.perf_counter()
    generate = LocalGenerator(args.model, args.max_new_tokens, args.seed)
    metadata['load_s'] = time.perf_counter() - start
    start = time.perf_counter()
    generate([{'role':'user','content':'你好'}])
    metadata['warmup_s'] = time.perf_counter() - start
    metadata['runtime'] = generate.versions
    (out/'manifest.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')
    failures = 0
    with (out/'outputs.jsonl').open('w', encoding='utf-8') as f:
        for item in items:
            for config in configs:
                try:
                    result = answer(item, config, generate, evidence.get(item['uid']) if config['retrieval'] else None)
                    row = {'uid': item['uid'], 'category': item['category'], 'type': item.get('type'), 'question': item['question'], 'config': config['name'], 'status': 'ok', **result}
                except Exception as exc:
                    failures += 1
                    row = {'uid': item['uid'], 'config': config['name'], 'status': 'error', 'error': repr(exc)}
                f.write(json.dumps(row, ensure_ascii=False) + '\n')
                f.flush()
                print(item['uid'], config['name'], row['status'], flush=True)
    if failures:
        raise SystemExit(f'{failures} failed records; see outputs.jsonl')

if __name__ == '__main__':
    main()
