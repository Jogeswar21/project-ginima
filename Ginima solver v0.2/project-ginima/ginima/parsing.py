"""Restricted exact-number input. Never evaluate user expression strings."""
import re
from sympy import Rational

NUMBER = re.compile(r"[+-]?\d+(?:/[+-]?\d+)?\Z")

def exact_number(value):
    if type(value) is int:
        if value.bit_length() > 256:
            raise ValueError("Integer exceeds 256-bit limit")
        return Rational(value)
    if isinstance(value, str) and len(value) <= 80 and NUMBER.fullmatch(value):
        parts = value.split("/")
        numerator = int(parts[0])
        denominator = int(parts[1]) if len(parts) == 2 else 1
        if not denominator or max(abs(numerator).bit_length(), abs(denominator).bit_length()) > 256:
            raise ValueError("Invalid denominator or number too large")
        return Rational(numerator, denominator)
    raise ValueError("Entries must be integers or exact rational strings such as '2/3'")

def matrix_entries(value):
    if not isinstance(value, list) or not 1 <= len(value) <= 6:
        raise ValueError("Matrix must have 1 to 6 rows")
    n = len(value)
    if any(not isinstance(row, list) or len(row) != n for row in value):
        raise ValueError("Matrix must be square")
    return [[exact_number(entry) for entry in row] for row in value]
