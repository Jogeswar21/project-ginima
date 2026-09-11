from .models import SolveResult
from .parsing import matrix_entries
from .solvers.determinants import solve_determinant

def solve(problem):
    if not isinstance(problem, dict):
        return SolveResult("invalid_input", reason="Problem must be a JSON object").to_dict()
    topic = problem.get("topic")
    topic_label = topic if isinstance(topic, str) else None
    if set(problem) - {"topic", "matrix"}:
        return SolveResult("invalid_input", topic=topic_label, reason="Unknown problem fields").to_dict()
    if topic != "determinant":
        return SolveResult("unsupported", topic=topic_label, reason="Only explicit topic='determinant' is supported").to_dict()
    try:
        rows = matrix_entries(problem.get("matrix"))
    except ValueError as error:
        return SolveResult("invalid_input", topic=topic, reason=str(error)).to_dict()
    try:
        return solve_determinant(rows)
    except TimeoutError:
        return SolveResult("timeout", topic=topic, reason="Solver exceeded its time budget").to_dict()
    except Exception:
        # Keep implementation traces out of the public result contract.
        return SolveResult("internal_error", topic=topic, reason="Solver failed unexpectedly").to_dict()
