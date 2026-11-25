import unittest

from experiments.report_c_structured import schema_conformant


class StructuredReportTests(unittest.TestCase):
    def setUp(self):
        self.schema = {"fields": [{"name": "exists", "values": [True, False]},
                                  {"name": "identity", "values": ["supported", "refuted", "not_established"]}]}

    def test_wrong_semantic_choice_can_still_conform_to_schema(self):
        self.assertTrue(schema_conformant('{"exists":false,"identity":"refuted"}', self.schema))

    def test_numeric_boolean_is_not_schema_conformant(self):
        self.assertFalse(schema_conformant('{"exists":1,"identity":"supported"}', self.schema))

    def test_unknown_enum_or_extra_keys_do_not_conform(self):
        for answer in ('{"exists":true,"identity":"maybe"}', '{"exists":true,"identity":"supported","reason":"X"}'):
            self.assertFalse(schema_conformant(answer, self.schema))

    def test_code_fence_is_not_a_bare_schema_object(self):
        self.assertFalse(schema_conformant('```json\n{"exists":true,"identity":"supported"}\n```', self.schema))

    def test_duplicate_keys_do_not_create_false_schema_compliance(self):
        self.assertFalse(schema_conformant('{"exists":false,"exists":true,"identity":"supported"}', self.schema))
