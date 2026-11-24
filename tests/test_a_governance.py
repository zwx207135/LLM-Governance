import unittest
from src.governance.interventions import answer

class GovernanceTests(unittest.TestCase):
    def run_case(self, **overrides):
        config = dict(fairness=True, strategy='basic',self_check=False,anti_hallucination=False)
        config.update(overrides)
        calls=[]
        def generate(messages):
            calls.append(messages)
            return {'text':f'answer{len(calls)}','latency_s':0.1,'input_tokens':10,'output_tokens':2,'truncated':False}
        result=answer({'question':'比较两位候选人','type':'pair','category':'gender'},config,generate)
        return result,calls

    def test_baseline_has_no_intervention(self):
        result,calls=self.run_case(fairness=False)
        self.assertEqual(calls,[[{'role':'user','content':'比较两位候选人'}]])
        self.assertEqual(result['call_count'],1)

    def test_self_check_keeps_all_stages(self):
        result,calls=self.run_case(self_check=True)
        self.assertEqual((result['draft'],result['check'],result['response']),('answer1','answer2','answer3'))
        self.assertEqual(result['call_count'],3)
        self.assertIn('answer1',str(calls[1]))
        self.assertIn('answer2',str(calls[2]))
        self.assertIn('比较两位候选人',str(calls[2]))

    def test_joint_preserves_both_constraints(self):
        result,calls=self.run_case(anti_hallucination=True,strategy='typed')
        self.assertIn('核对问题前提',calls[0][0]['content'])
        self.assertIn('交换群体属性',calls[0][0]['content'])

    def test_evidence_never_injects_reference_fields(self):
        def generate(messages):
            self.assertNotIn('SECRET_REFERENCE',str(messages))
            self.assertIn('[s1]',str(messages))
            return {'text':'ok'}
        result=answer({'question':'问题','reference':'SECRET_REFERENCE'},dict(fairness=False,anti_hallucination=True,self_check=False),generate,{'chunks':[{'source_id':'s1','text':'证据'}]})
        self.assertEqual(result['response'],'ok')

if __name__=='__main__': unittest.main()
