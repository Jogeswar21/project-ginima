"""Versioned public result contract, including unsuccessful outcomes."""
from dataclasses import asdict, dataclass, field
from typing import Literal

Status = Literal["solved", "invalid_input", "unsupported", "verification_failed", "unverified", "timeout", "internal_error"]
VerificationStatus = Literal["passed", "failed", "inconclusive", "not_run"]

@dataclass(frozen=True)
class Verification:
    status: VerificationStatus = "not_run"
    method: str | None = None

    def __post_init__(self):
        if self.status not in {"passed", "failed", "inconclusive", "not_run"}:
            raise ValueError("Unknown verification state")

@dataclass(frozen=True)
class SolveResult:
    status: Status
    topic: str | None = None
    answer: str | None = None
    reason: str | None = None
    verification: Verification = field(default_factory=Verification)
    assumptions: tuple[str, ...] = ()
    domain: str | None = None
    method: str | None = None
    provenance: str = "ginima/0.2.0"
    schema_version: str = "1.0"

    def __post_init__(self):
        if self.status not in {"solved", "invalid_input", "unsupported", "verification_failed", "unverified", "timeout", "internal_error"}:
            raise ValueError("Unknown solve state")
        if self.status == "solved" and (self.answer is None or self.verification.status != "passed"):
            raise ValueError("Solved results require an answer and passed verification")
        if self.status != "solved" and self.answer is not None:
            raise ValueError("Unsuccessful results cannot expose an answer")
        if self.verification.status == "passed" and self.status != "solved":
            raise ValueError("Passed verification requires a solved result")
        if (self.status == "verification_failed") != (self.verification.status == "failed"):
            raise ValueError("Verification failure states must agree")
        if (self.status == "unverified") != (self.verification.status == "inconclusive"):
            raise ValueError("Inconclusive results must be unverified")

    def to_dict(self):
        result = asdict(self)
        result["assumptions"] = list(self.assumptions)
        return result
