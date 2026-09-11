"""Independent determinant algorithm; shared exact arithmetic, no Matrix.det call."""
from itertools import permutations
from sympy import Integer

def determinant_by_permutations(rows):
    total = Integer(0)
    n = len(rows)
    for permutation in permutations(range(n)):
        inversions = sum(permutation[i] > permutation[j] for i in range(n) for j in range(i + 1, n))
        product = Integer(-1 if inversions % 2 else 1)
        for row, column in enumerate(permutation):
            product *= rows[row][column]
        total += product
    return total
