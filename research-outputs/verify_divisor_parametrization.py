#!/usr/bin/env python3
"""Exact checks for the divisor parametrization of two-unit-fraction solutions."""
from math import gcd, prod
import sympy as sp
from sympy import divisors, factorint

t = sp.symbols("t", integer=True, positive=True)
h = t * (12*t + 1)
M = sp.expand(h*h)
F = (1 + 3*t) * (1 + 14*t) * (1 + 60*t) * (1 + 36*t)
G = (4*t - 1) * (1 + 84*t) * (1 + 15*t) * (1 + 18*t)
D = sp.expand(F*G)
LAMBDA = 1260


def symbolic_checks():
    assert sp.expand(F + G - LAMBDA*M) == 0
    assert sp.rem(D + 1, h, t) == 0
    assert sp.degree(M, t) == 4
    assert sp.degree(D, t) == 8
    assert sp.LC(sp.Poly(D, t)) == 8230118400
    assert prod([3, 14, 60, 36, 4, 84, 15, 18]) == 8230118400
    print("SYMBOLIC_F_PLUS_G: PASS")
    print("D == -1 (mod h), hence gcd(D,M)=1: PASS")
    print("deg(M)=4, deg(D)=8, LC(D)=8230118400: PASS")


def enumerate_for_t(tv):
    hv = tv * (12*tv + 1)
    mv = hv*hv
    fv = (1 + 3*tv) * (1 + 14*tv) * (1 + 60*tv) * (1 + 36*tv)
    gv = (4*tv - 1) * (1 + 84*tv) * (1 + 15*tv) * (1 + 18*tv)
    dv = fv*gv
    assert fv + gv == LAMBDA*mv
    assert gcd(mv, dv) == 1
    assert dv % hv == hv - 1

    fac = factorint(dv)
    tau_d2 = prod(2*e + 1 for e in fac.values())
    ds = divisors(dv*dv)
    assert len(ds) == tau_d2
    count = 0
    seen_pairs = set()
    for d in ds:
        if d > dv:
            break
        if (dv + d) % mv:
            continue
        e = dv*dv // d
        assert (dv + e) % mv == 0
        u = (dv + d) // mv
        v = (dv + e) // mv
        assert u > 0 and v > 0
        assert mv*u*v == dv*(u+v)
        pair = tuple(sorted((u, v)))
        assert pair not in seen_pairs
        seen_pairs.add(pair)
        count += 1

    assert fv > gv
    d0 = gv*gv
    assert d0 <= dv and (dv+d0) % mv == 0
    u0 = (dv+d0)//mv
    e0 = dv*dv//d0
    v0 = (dv+e0)//mv
    assert tuple(sorted((u0,v0))) == tuple(sorted((LAMBDA*fv,LAMBDA*gv)))
    assert d0 == gv*gv and e0 == fv*fv
    return count, tau_d2


def main():
    symbolic_checks()
    expected = [85, 5, 1, 1, 1, 1, 2, 1]
    print("t  exact_pairs  tau(D^2)  bound_check")
    for tv, want in enumerate(expected, 1):
        count, tau_d2 = enumerate_for_t(tv)
        assert count == want
        assert count <= tau_d2
        print(f"{tv}  {count}  {tau_d2}  PASS")
    print("DIVISOR_BIJECTION_AND_CENTRAL_CENSUS: PASS")


if __name__ == "__main__":
    main()
