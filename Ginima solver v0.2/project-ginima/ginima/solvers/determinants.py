from sympy import Matrix
from ..models import SolveResult, Verification
from ..verification import determinant_by_permutations

def solve_determinant(rows):
    answer = Matrix(rows).det(method="bareiss")
    reference = determinant_by_permutations(rows)
    if reference is None:
        state, verification = "unverified", "inconclusive"
    elif answer == reference:
        state, verification = "solved", "passed"
    else:
        state, verification = "verification_failed", "failed"
    return SolveResult(
        status=state,
        topic="determinant",
        answer=str(answer) if state == "solved" else None,
        reason=None if state == "solved" else "Independent verification did not establish the answer",
        verification=Verification(verification, "independent_permutation_expansion"),
        assumptions=("Exact rational entries", "Square matrix of order 1 through 6"),
        domain="rational square matrices of order 1 through 6",
        method="SymPy Matrix.det(method='bareiss')",
    ).to_dict()
