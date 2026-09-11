# Determinant regression corpus

The 30 cases in `tests/fixtures/determinants.json` are original synthetic examples. They are not retrieved JEE questions and do not measure general JEE accuracy. Each stores its origin, a fixed exact answer and a short mathematical derivation. Expected answers were authored from scalar values, ad-bc, cofactor expansion, triangular/block products, permutation parity or row/column dependence; tests never derive expectations by calling the production determinant solver.

Coverage: orders 1–6; positive/negative/zero integers; rationals; a large exact integer; zero pivot; row swaps and additions; singular matrices; triangular and block structure; duplicate rows/columns.

Run `python -m unittest discover -s tests -v` from the project root. Every corpus case is a separate test D01–D30. As of 2026-09-10: 30/30 exact answers correct, 30/30 verified, 0 abstentions, 0 verifier failures on this corpus. Unsupported-topic tests are separate and excluded from this score. Total suite: 44 passing tests. Forced failure, inconclusive and timeout tests check status behavior rather than measuring natural occurrence rates.

These are curated regression examples, not a held-out evaluation set. A broader JEE benchmark, worker time limits, and topic-specific performance measurements remain future work.
