#!/usr/bin/env python3
"""Exact fixed-prime numerator DP for two-term Egyptian fractions.

Input to the DP is a supplied prime factorization b = product p**alpha.
The script does not factor b and makes no claim about polynomial-time
factorization. It verifies the DP witness against the divisor criterion and
checks the resulting unit-fraction identity using integer arithmetic.
"""
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


def prime_divisors(n: int):
    out = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        out.append(n)
    return out


def is_primitive_root(g: int, q: int) -> bool:
    if not is_prime(q) or q < 3:
        return False
    order = q - 1
    if pow(g, order, q) != 1:
        return False
    return all(pow(g, order // ell, q) != 1
               for ell in prime_divisors(order))


def find_primitive_root(q: int) -> int:
    for g in range(2, q):
        if is_primitive_root(g, q):
            return g
    raise ValueError("No primitive root found; q must be prime")


def crt_target(q: int):
    """Return (2-adic modulus, target, odd modulus, target)."""
    m = q - 1
    power_two = 1
    while m % (2 * power_two) == 0:
        power_two *= 2
    odd_part = m // power_two
    return power_two, power_two // 2, odd_part, 0


def positive_first_deltas(alpha: int):
    """Deterministic tie-break order: 0,+1,-1,+2,-2,... ."""
    values = [0]
    for k in range(1, alpha + 1):
        values.extend((k, -k))
    return values


def fixed_prime_dp(q: int, factorization, g=None):
    """Return an exact witness or NO for q/b as two distinct unit fractions.

    factorization is a sequence of distinct (prime, exponent) pairs.
    The full factorization is assumed to be supplied by the caller.
    """
    if not is_prime(q) or q == 2:
        raise ValueError("q must be an odd prime")
    if not factorization:
        raise ValueError("factorization must be nonempty")

    seen = set()
    normalized = []
    for p, alpha in factorization:
        if p in seen or not is_prime(p) or alpha <= 0:
            raise ValueError("Use distinct prime factors with positive exponents")
        if p == q:
            raise ValueError("The fraction q/b must be reduced")
        seen.add(p)
        normalized.append((p, alpha))

    if g is None:
        g = find_primitive_root(q)
    if not is_primitive_root(g, q):
        raise ValueError("g is not a primitive root modulo q")

    order = q - 1
    log_table = {pow(g, t, q): t for t in range(order)}
    if len(log_table) != order:
        raise AssertionError("primitive-root discrete-log table is incomplete")

    b = prod(p ** alpha for p, alpha in normalized)
    if gcd(b, q) != 1:
        raise ValueError("q and b must be coprime")

    logs = [log_table[p % q] for p, _ in normalized]

    # dp[residue] stores one delta-prefix reaching that residue.
    dp = {0: ()}
    for (p, alpha), t in zip(normalized, logs):
        nxt = {}
        for residue, prefix in dp.items():
            for delta in positive_first_deltas(alpha):
                new_residue = (residue + delta * t) % order
                if new_residue not in nxt:
                    nxt[new_residue] = prefix + (delta,)
        dp = nxt

    target = order // 2
    deltas = dp.get(target)
    result = {
        "q": q,
        "b": b,
        "factorization": tuple(normalized),
        "primitive_root": g,
        "discrete_logs": tuple(logs),
        "modulus": order,
        "target": target,
        "crt_target": crt_target(q),
        "state_count": order,
        "deltas": deltas,
        "answer": deltas is not None,
    }

    if deltas is None:
        return result

    exponents = tuple(alpha + delta
                      for (_, alpha), delta in zip(normalized, deltas))
    if any(e < 0 or e > 2 * alpha
           for e, (_, alpha) in zip(exponents, normalized)):
        raise AssertionError("delta vector did not define a divisor of b^2")

    r = prod(p ** e for (p, _), e in zip(normalized, exponents))
    b2 = b * b
    if b2 % r:
        raise AssertionError("constructed r does not divide b^2")
    s = b2 // r

    if r == b or r % q != (-b) % q or s % q != (-b) % q:
        raise AssertionError("constructed divisor pair failed the factor criterion")

    u_num = r + b
    v_num = s + b
    if u_num % q or v_num % q:
        raise AssertionError("unit-fraction denominators are not integral")
    u = u_num // q
    v = v_num // q
    if u <= 0 or v <= 0 or u == v:
        raise AssertionError("constructed denominators are not distinct positive integers")
    if q * u * v != b * (u + v):
        raise AssertionError("exact unit-fraction identity failed")

    result.update({
        "divisor_exponents": exponents,
        "r": r,
        "complementary_divisor": s,
        "unit_denominators": (u, v),
    })
    return result


def run_examples():
    examples = [
        (11, [(2, 1), (5, 1), (23, 1)]),
        (11, [(2, 4)]),  # NO: no delta in [-4,4] reaches 5 modulo 10.
        (13, [(2, 1), (19, 1)]),
        (13, [(17, 1), (29, 1)]),
        (19, [(2, 9)]),
    ]
    for q, factorization in examples:
        result = fixed_prime_dp(q, factorization, g=2)
        print("\nq =", q, " b =", result["b"])
        print("factorization =", result["factorization"])
        print("primitive_root =", result["primitive_root"])
        print("discrete_logs =", result["discrete_logs"])
        print("CRT target (2^s, target, odd_part, target) =", result["crt_target"])
        print("DP states =", result["state_count"])
        print("target =", result["target"])
        print("deltas =", result["deltas"])
        print("answer =", result["answer"])
        if result["answer"]:
            print("divisor exponents =", result["divisor_exponents"])
            print("r =", result["r"])
            print("b^2/r =", result["complementary_divisor"])
            print("unit-fraction denominators =", result["unit_denominators"])
            u, v = result["unit_denominators"]
            print(f"{q}/{result['b']} = 1/{u} + 1/{v}")


if __name__ == "__main__":
    run_examples()
