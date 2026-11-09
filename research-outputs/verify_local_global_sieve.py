#!/usr/bin/env python3
"""Exact local-global sieve for the central K3 Egyptian-fraction family.

Requires SymPy. This is an exhaustive verifier, not a polynomial-time algorithm.
It filters q|D by the necessary Jacobi conditions (q/p)=1 for p|h, then
intersects the resulting square-root congruence classes with unitary divisor
splits R=rs, gcd(r,s)=1, r<=s.
"""
from __future__ import annotations
import argparse
from itertools import product
from math import prod, gcd
from sympy import factorint, legendre_symbol

DEFAULT_T = (3, 7, 17, 69, 137, 185, 609, 1105, 1285, 1457, 5957, 6215, 6657)


def family(t: int):
    L = (1+3*t, 1+14*t, 1+60*t, 1+36*t,
         4*t-1, 1+84*t, 1+15*t, 1+18*t)
    D = prod(L)
    h = t*(12*t+1)
    return L, D, h, h*h


def f2_rank(L, h_primes):
    exponent = {}
    for value in L:
        for p, e in factorint(value).items():
            exponent[int(p)] = exponent.get(int(p), 0) + int(e)
    pivots = {}
    for ell, e in sorted(exponent.items()):
        if e != 1:
            continue
        v = 0
        for i, p in enumerate(h_primes):
            if legendre_symbol(ell, p) == -1:
                v |= 1 << i
        while v:
            b = v.bit_length()-1
            if b in pivots:
                v ^= pivots[b]
            else:
                pivots[b] = v
                break
    return len(pivots)


def divisors_with_exponents(factors):
    items = list(factors.items())
    for exps in product(*[range(a+1) for _, a in items]):
        q = prod(p**e for (p, _), e in zip(items, exps))
        yield q, exps


def unitary_splits_from_remaining(items, exps):
    """Yield each unordered coprime split r*s=R once, with r<=s."""
    powers = [p**(a-e) for (p, a), e in zip(items, exps) if a-e]
    R = prod(powers)
    if R == 1:
        return
    for mask in range(1 << len(powers)):
        r = 1
        for j, power in enumerate(powers):
            if (mask >> j) & 1:
                r *= power
        if r*r <= R:
            yield r, R//r


def analyze(t: int, audit_all_q: bool = False):
    L, D, h, M = family(t)
    df = factorint(D)
    hf = factorint(h)
    if 2 in hf:
        raise ValueError(f"t={t} is not an odd-parameter case")
    items = sorted((int(p), int(a)) for p, a in df.items())
    ps = sorted(map(int, hf))
    tau = prod(a+1 for _, a in items)
    rank = f2_rank(L, ps)

    q_pass = 0
    split_candidates = 0
    root_hits = 0
    reps = []
    for q, exps in divisors_with_exponents(dict(items)):
        if not all(legendre_symbol(q, p) == 1 for p in ps):
            continue
        q_pass += 1
        R = D//q
        for r, s in unitary_splits_from_remaining(items, exps):
            split_candidates += 1
            # Since gcd(r,M)=1, this is equivalent to M | (r+s).
            if (r*r + R) % M == 0:
                root_hits += 1
                reps.append((q, r, s))

    bound = (tau + (1 << rank)-1) // (1 << rank)
    assert q_pass <= bound, (t, q_pass, bound, rank)
    assert all(q*r*s == D and gcd(r, s) == 1 and (r+s) % M == 0
               for q, r, s in reps)

    if audit_all_q:
        all_reps = []
        for q, exps in divisors_with_exponents(dict(items)):
            R = D//q
            for r, s in unitary_splits_from_remaining(items, exps):
                if (r*r + R) % M == 0:
                    all_reps.append((q, r, s))
        assert set(all_reps) == set(reps), (t, all_reps, reps)

    return {
        "t": t, "tau_D": tau, "omega_h": len(ps), "rank": rank,
        "jacobi_passing_q": q_pass, "jacobi_upper_bound": bound,
        "unitary_split_candidates_after_jacobi": split_candidates,
        "root_hit_splits": root_hits, "representations": reps,
        "all_q_audit": audit_all_q,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--values", nargs="*", type=int, default=DEFAULT_T)
    ap.add_argument("--audit-all-q", nargs="*", type=int, default=[])
    args = ap.parse_args()
    print("t,tau_D,omega_h,rank,q_pass,q_bound,unitary_splits,root_hits,reps")
    for t in args.values:
        row = analyze(t, audit_all_q=t in args.audit_all_q)
        print(f"{t},{row['tau_D']},{row['omega_h']},{row['rank']},"
              f"{row['jacobi_passing_q']},{row['jacobi_upper_bound']},"
              f"{row['unitary_split_candidates_after_jacobi']},"
              f"{row['root_hit_splits']},{len(row['representations'])}")
        print("  representations:", row["representations"])
        if row["all_q_audit"]:
            print("  all-q exhaustive audit: PASS")
    print("LOCAL_GLOBAL_SIEVE_EXACT_CHECKS: PASS")


if __name__ == "__main__":
    main()
