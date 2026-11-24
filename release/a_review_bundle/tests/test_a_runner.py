import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
class RunnerTests(unittest.TestCase):
    def test_duplicate_uid_rejected_before_model_load(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)
            data=path/'input.json'
            data.write_text(json.dumps([{'uid':'a'},{'uid':'a'}]))
            result=subprocess.run([sys.executable,str(ROOT/'experiments/run_a.py'),'--input',str(data),'--output',str(path/'out')],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('duplicate uid',result.stderr)
            self.assertFalse((path/'out').exists())

    def test_rag_cannot_run_without_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)
            (path/'input.json').write_text(json.dumps([{'uid':'a'}]))
            (path/'config.json').write_text(json.dumps([{'retrieval':True}]))
            result=subprocess.run([sys.executable,str(ROOT/'experiments/run_a.py'),'--input',str(path/'input.json'),'--configs',str(path/'config.json'),'--output',str(path/'out')],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('KeyError',result.stderr)
            self.assertFalse((path/'out').exists())

    def test_analysis_keeps_failures_and_unscored_pairs_separate(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)
            rows=[{'uid':'a','config':'E0','category':'normal','status':'ok','call_count':1,'latency_s':2,'response':'x','calls':[{'output_tokens':3,'truncated':False}]},{'uid':'a','config':'basic','status':'error','error':'test'}]
            (path/'outputs.jsonl').write_text('\n'.join(json.dumps(r) for r in rows))
            subprocess.run([sys.executable,str(ROOT/'experiments/analyze_a.py'),str(path)],check=True,capture_output=True)
            summary=json.loads((path/'cost_summary.json').read_text())
            self.assertEqual(summary['basic'],{'records':1,'ok':0,'errors':1})
            self.assertFalse((path/'paired_scores.json').exists())
            self.assertIn('reviewer',(path/'review.csv').read_text(encoding='utf-8-sig'))

if __name__=='__main__':unittest.main()
