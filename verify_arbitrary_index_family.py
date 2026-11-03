#!/usr/bin/env python3
"""Exact checks for the arbitrary-index/minimum-support family.

This script verifies four concrete instances. It does not implement the
Dirichlet prime search for arbitrary parameters; the prime representatives
are explicitly listed for reproducibility.
"""
from itertools import product
from math import gcd, prod

CASES = [
    {
        "R": 2, "k": 3, "r": 11, "q": 67, "gamma": 2,
        "primes": [2, 661, 7, 293],
    },
    {
        "R": 3, "k": 5, "r": 13, "q": 131, "gamma": 2,
        "primes": [2, 1039, 499, 47, 509, 307],
    },
    {
        "R": 4, "k": 7, "r": 17, "q": 239, "gamma": 7,
        "primes": [7, 547, 2797, 461, 2837, 787, 929, 1031],
    },
    {
        "R": 5, "k": 9, "r": 21, "q": 379, "gamma": 2,
        "primes": [2, 89, 739, 1997, 3023, 547, 1033, 3331, 1367, 701],
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


def primitive_root_check(g: int, q: int) -> bool:
    if not is_prime(q):
        return False
    n = q - 1
    factors = []
    x = n
    d = 2
    while d * d <= x:
        if x % d == 0:
            factors.append(d)
            while x % d == 0:
                x //= d
        d += 1
    if x > 1:
        factors.append(x)
    return all(pow(g, n // p, q) != 1 for p in factors)


def verify_case(case):
    R, k, r, q, gamma = (case[key] for key in ("R", "k", "r", "q", "gamma"))
    ps = case["primes"]
    m = k * r
    assert k == 2 * R - 1 and k % 2 == 1
    assert r > 2 * k
    assert q == 2 * k * r + 1 and is_prime(q)
    assert primitive_root_check(gamma, q)
    assert len(ps) == k + 1 and len(set(ps)) == k + 1
    assert all(is_prime(p) for p in ps)

    a = [1 + r * j for j in range(k)] + [k * (r - 1)]
    eps = [j % 2 for j in range(k)] + [0]
    s = [x + m * e for x, e in zip(a, eps)]

    # The projected sequence is minimal zero-sum.
    assert sum(a) == R * m
    for mask in range(1, (1 << (k + 1)) - 1):
        sub_sum = sum(a[i] for i in range(k + 1) if (mask >> i) & 1)
        assert sub_sum % m != 0

    # Every generator gives norm exactly R*m.
    norms = {
        sum(((t * x - 1) % m) + 1 for x in a)
        for t in range(1, m) if gcd(t, m) == 1
    }
    assert norms == {R * m}

    # Lifted exponents have exactly two signed solutions to target m.
    assert sum(s) % (2 * m) == m
    solutions = []
    for xs in product((-1, 0, 1), repeat=k + 1):
        if sum(x * y for x, y in zip(xs, s)) % (2 * m) == m:
            solutions.append(xs)
    assert solutions == [(-1,) * (k + 1), (1,) * (k + 1)] or set(solutions) == {
        (-1,) * (k + 1), (1,) * (k + 1)
    }

    # Prime representatives have the required distinct residues.
    classes = [pow(gamma, e, q) for e in s]
    assert len(set(classes)) == k + 1
    assert [p % q for p in ps] == classes

    b = prod(ps)
    assert b % q == q - 1
    u = (b + 1) // q
    v = b * u
    assert q * u * v == b * (u + v)
    assert u != v

    return {
        "R": R, "k": k, "q": q, "m": m,
        "projected_sequence": a,
        "lifted_exponents": s,
        "prime_representatives": ps,
        "b": b, "u": u, "v": v,
        "signed_solution_count": len(solutions),
        "index_norms": sorted(norms),
    }


if __name__ == "__main__":
    for case in CASES:
        result = verify_case(case)
        print("PASS", result)
