import json
import sys
from .engine import solve
from .models import SolveResult

def main():
    try:
        source = sys.stdin.read(65537)
        if len(source) > 65536:
            raise ValueError("Input exceeds 64 KiB character limit")
        result = solve(json.loads(source))
    except (ValueError, RecursionError) as error:
        result = SolveResult("invalid_input", reason=str(error)).to_dict()
    print(json.dumps(result))
    return 0 if result["status"] == "solved" else 2

if __name__ == "__main__":
    sys.exit(main())
