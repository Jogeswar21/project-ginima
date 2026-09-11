import json
import random
import subprocess
import sys
import unittest
from unittest.mock import patch
from ginima import solve

def determinant(matrix):
    return solve({"topic": "determinant", "matrix": matrix})

class SolverTests(unittest.TestCase):
    def test_known_answers(self):
        for matrix, expected in [([[7]], "7"), ([[1, 2], [3, 4]], "-2"),
                                 ([[1, 2], [2, 4]], "0"),
                                 ([[0, 1], [1, 0]], "-1"),
                                 ([["1/2", 0], [0, "2/3"]], "1/3"),
                                 ([[2, 1, 3], [0, 4, 2], [0, 0, -3]], "-24")]:
            with self.subTest(matrix=matrix):
                result = determinant(matrix)
                self.assertEqual(result["answer"], expected)
                self.assertEqual(result["verification"]["status"], "passed")

    def test_invalid_entries(self):
        for entry in [True, 0.5, "1/0", "x", "__import__('os').system('echo unsafe')", 2**300, None]:
            with self.subTest(entry=entry):
                self.assertEqual(determinant([[entry]])["status"], "invalid_input")

    def test_invalid_shapes(self):
        for matrix in [[], [[1, 2]], [[1], [2, 3]], [[1]*7]*7, "matrix"]:
            self.assertEqual(determinant(matrix)["status"], "invalid_input")

    def test_routing_abstains(self):
        for topic in ["calculus", "probability", "graph", None, ["determinant"]]:
            self.assertEqual(solve({"topic": topic})["status"], "unsupported")
        self.assertEqual(solve("find determinant")["status"], "invalid_input")

    def test_unknown_fields(self):
        self.assertEqual(solve({"topic": "determinant", "matrix": [[1]], "ignored": True})["status"], "invalid_input")

    def test_verification_failure_blocks_answer(self):
        with patch("ginima.solvers.determinants.determinant_by_permutations", return_value=999):
            result = determinant([[1]])
            self.assertEqual(result["status"], "verification_failed")
            self.assertIsNone(result["answer"])

    def test_row_swap_and_duplicate_properties(self):
        rng = random.Random(21)
        for n in range(2, 7):
            for _ in range(5):
                matrix = [[rng.randint(-5, 5) for _ in range(n)] for _ in range(n)]
                original = determinant(matrix)
                self.assertEqual(original["status"], "solved")
                swapped = [row[:] for row in matrix]
                swapped[0], swapped[1] = swapped[1], swapped[0]
                self.assertEqual(int(determinant(swapped)["answer"]), -int(original["answer"]))
                matrix[1] = matrix[0][:]
                self.assertEqual(determinant(matrix)["answer"], "0")

    def test_cli(self):
        for payload, code, status in [('{"topic":"determinant","matrix":[[2]]}', 0, "solved"),
                                      ('broken json', 2, "invalid_input"),
                                      ('{"topic":"graph"}', 2, "unsupported")]:
            result = subprocess.run([sys.executable, "-m", "ginima.cli"], input=payload, text=True, capture_output=True)
            self.assertEqual(result.returncode, code)
            self.assertEqual(json.loads(result.stdout)["status"], status)

if __name__ == "__main__":
    unittest.main()
