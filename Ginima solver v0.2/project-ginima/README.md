# Project Ginima 0.2.0

An exact, verifiable foundation for a JEE mathematics solver.

This is a NEW starter project, not an audit, copy, or reconstruction of the original Ginima code. The original repository could not be identified through the connected GitHub account. No original notebooks, solver implementations, tests, or issues were inspected. This archive has not been published to GitHub.

## First working milestone

Structured JSON input → explicit topic routing → exact determinant calculation → independent algorithm check → JSON result.

Supports square matrices of order 1–6 containing integers or rational strings. Rejects floats, symbolic strings, non-square matrices, oversized integers, and unknown fields. Unsupported topics return `unsupported`, never a guessed answer. SymPy computes the determinant; a separate permutation expansion checks it. Both share SymPy rational arithmetic, so verification is algorithmically independent, not an independent CAS.

## Run

Python 3.10 or later:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e .
python -m ginima.cli < examples/determinant.json
python -m unittest discover -s tests -v
```

The example returns answer `-2` with verification status `passed`. In PowerShell use `Get-Content examples/determinant.json | python -m ginima.cli`.

## Layout

| Path | Purpose |
|---|---|
| `ginima/engine.py` | Structured routing and input error handling |
| `ginima/parsing.py` | Restricted integer/rational parser and size limits |
| `ginima/solvers/determinants.py` | Exact SymPy determinant solver |
| `ginima/verification.py` | Independent determinant expansion |
| `ginima/cli.py` | JSON stdin/stdout interface and exit codes |
| `tests/test_engine.py` | Known answers, invalid inputs, properties, verifier failure, CLI |
| `docs/BUILD_PLAN.md` | Prioritized topic backlog and acceptance checks |

## Deliberate limitations

No natural-language/LaTeX parser, symbolic determinant parameters, graph analysis, probability or calculus solver, notebook collection, pedagogical step generator, API, or web UI yet. No JEE benchmark accuracy claim. Result schema 1.0 is shared by every engine and CLI outcome. Timeout handling is defined, but a worker enforcing a time budget is still planned. The verifier is factorial-time and deliberately limited to order 6.

## Publish as a new GitHub repository

Create an empty repository named `project-ginima` under your account (private is a reasonable initial choice), extract this archive, and run inside the project folder:

```bash
git init
git add .
git commit -m "Add verified determinant solver foundation and build plan"
git branch -M main
git remote add origin https://github.com/Jogeswar21/project-ginima.git
git push -u origin main
```

Use this URL only after creating the repository under that account. The bundled Actions workflow runs tests on pushes and pull requests; hosted CI has not run yet.

## Result contract and examples

Every result has `schema_version`, `status`, `topic`, `answer`, `reason`, `verification`, `assumptions`, `domain`, `method`, and `provenance`. An answer is exposed only for `solved` with verification `passed`. Other verification states are `failed`, `inconclusive`, and `not_run`.

### Successful

Input:
```json
{"topic": "determinant", "matrix": [[1, 2], [3, 4]]}
```
Output:
```json
{
  "status": "solved",
  "topic": "determinant",
  "answer": "-2",
  "reason": null,
  "verification": {
    "status": "passed",
    "method": "independent_permutation_expansion"
  },
  "assumptions": [
    "Exact rational entries",
    "Square matrix of order 1 through 6"
  ],
  "domain": "rational square matrices of order 1 through 6",
  "method": "SymPy Matrix.det(method='bareiss')",
  "provenance": "ginima/0.2.0",
  "schema_version": "1.0"
}
```

### Invalid

Input:
```json
{"topic": "determinant", "matrix": [[0.5]]}
```
Output:
```json
{
  "status": "invalid_input",
  "topic": "determinant",
  "answer": null,
  "reason": "Entries must be integers or exact rational strings such as '2/3'",
  "verification": {
    "status": "not_run",
    "method": null
  },
  "assumptions": [],
  "domain": null,
  "method": null,
  "provenance": "ginima/0.2.0",
  "schema_version": "1.0"
}
```

### Unsupported

Input:
```json
{"topic": "calculus"}
```
Output:
```json
{
  "status": "unsupported",
  "topic": "calculus",
  "answer": null,
  "reason": "Only explicit topic='determinant' is supported",
  "verification": {
    "status": "not_run",
    "method": null
  },
  "assumptions": [],
  "domain": null,
  "method": null,
  "provenance": "ginima/0.2.0",
  "schema_version": "1.0"
}
```

The regression corpus has 30 original synthetic problems with fixed expected answers and mathematical derivations. These are not official JEE questions. See `docs/BENCHMARK.md`.
