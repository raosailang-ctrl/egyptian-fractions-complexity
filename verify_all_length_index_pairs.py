#!/usr/bin/env python3
"""Exact verification of selected length-index Egyptian-fraction examples.

The general theorem and proof are recorded in all-length-index-spectrum.md.
This script checks concrete instances only; it does not implement the
Dirichlet prime search used in the existence proof.
"""
from itertools import product
from math import gcd, prod

CASES = [
    {
        "L": 5, "R": 2, "r": 23, "q": 139, "gamma": 2,
        "primes": [419, 223, 331, 823, 1499],
    },
    {
        "L": 6, "R": 3, "r": 13, "q": 131, "gamma": 2,
        "primes": [919, 1039, 499, 571, 509, 307],
    },
    {
        "L": 7, "R": 3, "r": 2001, "q": 20011, "gamma": 12,
        "primes": [20023, 108377, 168227, 71333, 652601, 240853, 229799],
    },
    {
        "L": 8, "R": 3, "r": 2001, "q": 20011, "gamma": 12,
        "primes": [20023, 108377, 168227, 71333, 652601, 240853, 439573, 97169],
    },
    {
        "L": 8, "R": 4, "r": 17, "q": 239, "gamma": 7,
        "primes": [4787, 547, 2797, 461, 2837, 787, 929, 1031],
    },
]


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def prime_factors(n: int):
    factors = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


def is_primitive_root(g: int, q: int) -> bool:
    if not is_prime(q):
        return False
    order = q - 1
    return all(pow(g, order // p, q) != 1 for p in prime_factors(order))


def build_exponents(L: int, R: int, r: int):
    k = 2 * R - 1
    N = L - 2 * R
    if N < 0:
        raise ValueError("Need L >= 2R")
    m = k * r
    small = [(2 * k + 1) * (3 ** i) for i in range(N)]
    S = sum(small)
    c = m - k - S
    exponents = [1 + r * j + m * (j % 2) for j in range(k)]
    exponents.extend(small)
    exponents.append(c)
    return k, m, small, c, exponents


def verify_case(case):
    L, R, r, q, gamma = (
        case[key] for key in ("L", "R", "r", "q", "gamma")
    )
    primes = case["primes"]
    k, m, small, c, exponents = build_exponents(L, R, r)
    S = sum(small)

    assert 1 <= R <= L // 2
    assert k == 2 * R - 1 and k % 2 == 1
    assert r > 2 * k + 2 * S
    assert q == 2 * k * r + 1 and is_prime(q)
    assert len(exponents) == L
    assert len(set(exponents)) == L
    assert all(0 < e < 2 * m for e in exponents)
    assert sum(exponents) % (2 * m) == m
    assert is_primitive_root(gamma, q)

    classes = [pow(gamma, e, q) for e in exponents]
    assert len(set(classes)) == L
    assert len(primes) == L and len(set(primes)) == L
    assert all(is_prime(p) and p > q for p in primes)
    assert [p % q for p in primes] == classes

    # The projected sequence in C_m is minimal zero-sum.
    projected = [e % m for e in exponents]
    assert all(a != 0 for a in projected)
    assert sum(projected) % m == 0
    for mask in range(1, (1 << L) - 1):
        subset_sum = sum(projected[i] for i in range(L) if (mask >> i) & 1)
        assert subset_sum % m != 0

    # Compute the index exactly over all generators of C_m.
    norms = set()
    for t in range(1, m):
        if gcd(t, m) == 1:
            norm = sum(((t * a - 1) % m) + 1 for a in projected)
            norms.add(norm)
    index = min(norms) // m
    assert min(norms) == R * m
    assert index == R

    # The lifted signed congruence has exactly the two full-support solutions.
    solutions = []
    for xs in product((-1, 0, 1), repeat=L):
        if sum(x * e for x, e in zip(xs, exponents)) % (2 * m) == m:
            solutions.append(xs)
    expected = {(1,) * L, (-1,) * L}
    assert set(solutions) == expected

    # Convert the residue classes into a squarefree denominator.
    b = prod(primes)
    assert gcd(q, b) == 1 and b % q == q - 1
    u = (b + 1) // q
    v = b * u
    assert u != v and q * u * v == b * (u + v)

    return {
        "L": L,
        "R": R,
        "q": q,
        "m": m,
        "k": k,
        "small_split_terms": small,
        "residual_term": c,
        "exponents": exponents,
        "projected_sequence": projected,
        "index_norms": sorted(norms),
        "primes": primes,
        "b": b,
        "u": u,
        "v": v,
        "signed_solution_count": len(solutions),
    }


if __name__ == "__main__":
    for case in CASES:
        result = verify_case(case)
        print("PASS", result)
