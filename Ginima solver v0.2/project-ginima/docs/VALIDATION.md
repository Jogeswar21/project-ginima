# Local validation — 0.2.0

Executed on 2026-09-10 with Python 3.12.14 and SymPy 1.14.0.

`python -m unittest discover -s tests -v`: **44 tests passed** in 1.035 seconds on the local execution environment. This includes 30 fixed-answer determinant cases, 6 contract/corpus tests and 8 existing engine/CLI tests (with subcases and 25 seeded matrix property checks).

Verified: known rational/integer answers, result field consistency, rejected unknown fields, no false success after verifier mismatch or inconclusive check, distinct timeout/internal-error outcomes via injected exceptions, and CLI behavior.

Dependencies were exposed via a temporary PYTHONPATH. Editable installation, Python 3.10 and hosted GitHub Actions have not been executed. A real worker time limit is not implemented; timeout tests exercise exception conversion only. No original Ginima repository was inspected or tested. All corpus examples are synthetic; these results make no general JEE accuracy claim.
