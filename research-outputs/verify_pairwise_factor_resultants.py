#!/usr/bin/env python3
"""Exact pairwise resultant certificate for the central denominator factors."""
import sympy as sp
from math import prod

t=sp.symbols("t")
L=[1+3*t,1+14*t,1+60*t,1+36*t,4*t-1,1+84*t,1+15*t,1+18*t]
expected={
(1,2):-11,(1,3):-57,(1,4):-33,(1,5):-7,(1,6):-81,(1,7):-12,(1,8):-15,
(2,3):-46,(2,4):-22,(2,5):-18,(2,6):-70,(2,7):-1,(2,8):-4,
(3,4):24,(3,5):-64,(3,6):-24,(3,7):45,(3,8):42,
(4,5):-40,(4,6):-48,(4,7):21,(4,8):18,
(5,6):88,(5,7):19,(5,8):22,(6,7):69,(6,8):66,(7,8):-3}
actual={}
for i in range(8):
    for j in range(i+1,8):
        actual[(i+1,j+1)]=int(sp.resultant(L[i],L[j],t))
assert actual==expected
support=set()
for r in actual.values():
    support.update(int(p) for p in sp.factorint(abs(r)))
assert support=={2,3,5,7,11,19,23}
h=t*(12*t+1)
D=sp.prod(L)
assert sp.rem(D+1,h,t)==0
for f in L:
    # A polynomial resultant with h is nonzero; D == -1 mod h proves
    # the evaluated integer gcd is 1 for every integer t.
    assert sp.gcd(sp.Poly(f,t),sp.Poly(h,t)).degree()==0
print("PAIRWISE_RESULTANTS: PASS")
print("OVERLAP_PRIME_SUPPORT:",sorted(support))
print("D == -1 mod h; all L_i coprime to h: PASS")
