#!/usr/bin/env python3
"""Exact small-instance verifier for the square-modulus algebraic encoding.

This is an algebraic experiment only. It does not test the asymptotic
prime-distribution theorem or the Las Vegas runtime bound.
"""
from itertools import product
from math import gcd, prod


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


def prime_in_class(c: int, modulus: int, lower: int) -> int:
    """Find the first prime >= lower congruent to c modulo modulus."""
    k = max(0, (lower - c + modulus - 1) // modulus)
    while True:
        candidate = c + k * modulus
        if candidate >= lower and is_prime(candidate):
            return candidate
        k += 1


def encode(items, target):
    n = len(items)
    A = sum(items)
    if not (1 <= target <= A):
        raise ValueError("Use a nontrivial SUBSET SUM target")
    B = 8 * (A + 1)
    L = sum(B**i for i in range(1, n + 1))
    W = 2 * L - A
    S = L - target
    weights = [(B**i, B**i - items[i - 1]) for i in range(1, n + 1)]
    return B, L, W, S, weights


def subset_sum_yes(items, target):
    n = len(items)
    return any(sum(items[i] for i in range(n) if mask >> i & 1) == target
               for mask in range(1 << n))


def bounded_exponent_yes(weights, S):
    flat = [w for pair in weights for w in pair]
    return any(sum(e*w for e, w in zip(exps, flat)) == S
               for exps in product(range(3), repeat=len(flat)))


def run_instance(items, target, h):
    B, L, W, S, weights = encode(items, target)
    assert h % 2 == 1 and h > 2*W
    M = h*h
    omega = 1+h
    assert pow(omega, h, M) == 1
    assert all(pow(omega, k, M) != 1 for k in range(1, h))

    flat = [w for pair in weights for w in pair]
    assert len(set(flat)) == len(flat)
    assert max(flat) < W < h
    C = h + S - W
    classes = [pow(omega, w, M) for w in flat] + [(-pow(omega, C, M)) % M]
    assert len(set(classes)) == len(classes)
    assert all(gcd(c, M) == 1 for c in classes)

    # Keep candidates small for a transparent exact experiment.
    lower = M + 1
    primes = [prime_in_class(c, M, lower) for c in classes]
    assert len(set(primes)) == len(primes)
    assert all(is_prime(p) and p % M == c for p, c in zip(primes, classes))

    P = primes[:-1]
    R = primes[-1]
    D = R * prod(P)
    assert gcd(D, M) == 1
    assert D % M == (-pow(omega, S, M)) % M

    # Enumerate every divisor exponent vector of D^2 and test r == -D mod M.
    hits = []
    for exps in product(range(3), repeat=len(primes)):
        r = prod(p**e for p, e in zip(primes, exps))
        if r % M == (-D) % M:
            hits.append((exps, r))
    algebraic_yes = bool(hits)
    expected = subset_sum_yes(items, target)
    bounded_yes = bounded_exponent_yes(weights, S)
    assert expected == bounded_yes == algebraic_yes

    # For YES, construct the two unit-fraction denominators from r and D^2/r.
    fraction = None
    if hits:
        exps, r = hits[0]
        assert (D*D) % r == 0
        s = D*D // r
        assert r != D
        assert r % M == (-D) % M and s % M == (-D) % M
        u = (r + D) // M
        v = (s + D) // M
        assert (r + D) % M == 0 and (s + D) % M == 0
        assert u != v and u > 0 and v > 0
        assert M*u*v == D*(u+v)
        fraction = (u, v)

    return {
        "items": items, "target": target, "answer": expected,
        "B": B, "L": L, "W": W, "S": S, "h": h, "M": M,
        "omega": omega, "C": C, "residue_classes": classes,
        "prime_representatives": primes, "D": D,
        "matching_exponent_vectors": [x[0] for x in hits],
        "two_term_denominators": fraction,
    }


if __name__ == "__main__":
    # {1}, target 1 is YES; {2}, target 1 is NO.
    yes = run_instance([1], 1, 67)
    no = run_instance([2], 1, 101)
    for label, result in (("YES", yes), ("NO", no)):
        print(f"[{label}]")
        for key, value in result.items():
            print(f"{key} = {value}")
