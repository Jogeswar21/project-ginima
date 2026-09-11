import json
from pathlib import Path
import unittest
from unittest.mock import patch
from ginima import solve
from ginima.models import SolveResult, Verification

CASES = json.loads((Path(__file__).parent/'fixtures/determinants.json').read_text())
FIELDS = {'status','topic','answer','reason','verification','assumptions','domain','method','provenance','schema_version'}

class RegressionTests(unittest.TestCase):
    pass

def make_test(case):
    def test(self):
        result = solve({'topic':'determinant','matrix':case['matrix']})
        self.assertEqual(result['status'], 'solved')
        self.assertEqual(result['answer'], case['expected'], case['derivation'])
        self.assertEqual(result['verification']['status'], 'passed')
        self.assertEqual(set(result), FIELDS)
        self.assertTrue(case['source'])
    return test

for case in CASES:
    setattr(RegressionTests, 'test_'+case['id'], make_test(case))

class ContractTests(unittest.TestCase):
    def test_corpus_inventory(self):
        self.assertEqual(len(CASES), 30)
        self.assertEqual(len({c['id'] for c in CASES}), 30)

    def test_public_outcomes_have_same_fields(self):
        for problem in [None, {'topic':'graph'}, {'topic':'determinant','matrix':[]}, {'topic':'determinant','matrix':[[1]]}]:
            result = solve(problem)
            self.assertEqual(set(result), FIELDS)
            self.assertEqual(json.loads(json.dumps(result)), result)

    def test_unknown_fields_rejected_for_unsupported_topics(self):
        self.assertEqual(solve({'topic':'graph','surprise':True})['status'], 'invalid_input')

    def test_inconclusive_never_solved(self):
        with patch('ginima.solvers.determinants.determinant_by_permutations', return_value=None):
            result = solve({'topic':'determinant','matrix':[[1]]})
        self.assertEqual(result['status'], 'unverified')
        self.assertEqual(result['verification']['status'], 'inconclusive')
        self.assertIsNone(result['answer'])

    def test_failures_are_distinguished(self):
        for error, status in [(TimeoutError(), 'timeout'), (RuntimeError('private details'), 'internal_error')]:
            with patch('ginima.engine.solve_determinant', side_effect=error):
                result = solve({'topic':'determinant','matrix':[[1]]})
            self.assertEqual(set(result), FIELDS)
            self.assertEqual(result['status'], status)
            self.assertEqual(result['verification']['status'], 'not_run')
            self.assertNotIn('private details', json.dumps(result))

    def test_contract_rejects_false_success(self):
        for kwargs in [dict(status='solved',answer='1'), dict(status='unsupported',answer='1'),
                       dict(status='solved',answer='1',verification=Verification('inconclusive')),
                       dict(status='verification_failed'), dict(status='unverified')]:
            with self.assertRaises(ValueError):
                SolveResult(**kwargs)
