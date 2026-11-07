#!/usr/bin/env python3
"""Exact 20-prime finite-field sieve for the genus-two nonsquare condition.

Requires Python 3.10+, SymPy, and NumPy. All finite-field operations and CRT
class counts are exact; NumPy is used only to store/filter integer residue arrays.
"""
from __future__ import annotations
from math import gcd, lcm
from fractions import Fraction
import numpy as np

A2, A4, A6 = 1441, -513648, 57526848
DISC_E = 7270291997982720000
Q0 = (888, -37920)
BASE_PRIMES = (13,17,31,47,53,67,107,151,229,383,421,449,463,593)
EXT_PRIMES = (29,97,131,139,149,157)


def is_prime(n):
    if n<2:return False
    d=2
    while d*d<=n:
        if n%d==0:return False
        d+=1
    return True


def inv(x,p):
    x%=p
    assert x
    return pow(x,-1,p)


def ec_add(P,Q,p):
    if P is None:return Q
    if Q is None:return P
    x,y=P;u,v=Q
    if x==u and (y+v)%p==0:return None
    if x==u:
        assert y%p
        slope=(3*x*x+2*A2*x+A4)*inv(2*y,p)%p
    else:slope=(v-y)*inv(u-x,p)%p
    X=(slope*slope-A2-x-u)%p
    Y=(-y+slope*(x-X))%p
    assert (Y*Y-X**3-A2*X*X-A4*X-A6)%p==0
    return X,Y


def legendre(x,p):
    x%=p
    if x==0:return 0
    return 1 if pow(x,(p-1)//2,p)==1 else -1


def kappa_mod(P,p):
    x,y=P
    den=12*(x+352)%p
    if den==0:return None
    b=(33*x-y-7704)*inv(den,p)%p
    if b==0 or (b+6)%p==0:return None
    a=inv(6,p);ab=a*b%p
    if (ab+1)%p==0:return None
    kap=(4+2*(a+b)*(ab*ab+1)*inv(ab*(ab+1),p))%p
    return legendre(kap*kap-8*kap+144,p)


def orbit_data(p):
    assert is_prime(p) and DISC_E%p
    Q=(Q0[0]%p,Q0[1]%p)
    assert (Q[1]**2-Q[0]**3-A2*Q[0]**2-A4*Q[0]-A6)%p==0
    P=None; nonsq=set(); bad=set();zero=set();square=set();order=0
    while True:
        P=ec_add(P,Q,p);order+=1
        if P is None:break
        ls=kappa_mod(P,p)
        if ls is None:bad.add(order)
        elif ls==-1:nonsq.add(order)
        elif ls==0:zero.add(order)
        else:square.add(order)
    assert 1+len(nonsq)+len(bad)+len(zero)+len(square)==order
    return order,nonsq,bad,zero,square


def main():
    # Rebuild the first 14-prime sieve exactly; it leaves three classes.
    L=1; S={0}
    all_primes=BASE_PRIMES+EXT_PRIMES
    data={}
    for p in all_primes:
        N,E,bad,zero,sq=orbit_data(p)
        data[p]=(N,E,bad,zero,sq)
        newL=lcm(L,N)
        newS=set()
        for r in S:
            for m in range(r,newL,L):
                if m%N not in E:newS.add(m)
        S,L=newS,newL
        print(f"p={p:3d} ord={N:3d} nonres={len(E):3d} poles={len(bad):2d} zero={len(zero):2d} L={L} survivors={len(S)}")
    assert L==220492499507280
    assert len(S)==11053350
    certified=L-len(S)
    assert Fraction(certified,L)==Fraction(31817097901,31817099496)
    good_arc=Fraction(certified,L*48000)
    assert good_arc==Fraction(31817097901,1527220775808000)
    print("FINAL MODULUS",L)
    print("SURVIVORS",len(S))
    print("CERTIFIED FRACTION",Fraction(certified,L))
    print("GOOD-ARC DENSITY LOWER BOUND",good_arc)
    print("ALL 20-PRIME CHECKS: PASS")

if __name__=='__main__':main()
