#!/usr/bin/env python3
"""Exact q,r,s parametrization and modular-root bound checks.

Requires SymPy and the existing count_by_mitm.py in the same directory.
Run from the repository root:
    python research-outputs/verify_qrs_parametrization.py
"""
from collections import Counter
from math import gcd, isqrt, prod
from sympy import factorint
from count_by_mitm import count_egyptian


def family(t):
    L=(1+3*t,1+14*t,1+60*t,1+36*t,4*t-1,1+84*t,1+15*t,1+18*t)
    D=prod(L); M=(t*(12*t+1))**2
    F=prod(L[:4]); G=prod(L[4:])
    assert F+G==1260*M and gcd(D,M)==1
    return L,D,M,F,G


def check_rep(t, witness):
    d, reported_gcd, u, v = witness
    _,D,M,F,G=family(t)
    e=D*D//d
    assert d*e==D*D and d<=D
    assert (d+D)%M==0 and (e+D)%M==0
    q=gcd(d,e)
    r=isqrt(d//q); s=isqrt(e//q)
    assert r*r==d//q and s*s==e//q
    assert gcd(r,s)==1 and q*r*s==D
    assert (r+s)%M==0
    k=(r+s)//M
    assert gcd(k,r*s)==1
    assert u==q*k*r and v==q*k*s
    assert gcd(u,v)==q*k==reported_gcd
    assert (r*r + D//q)%M==0
    return q,r,s,k,gcd(u,v),u,v


def main():
    total=0
    nonunique=[]
    examples={}
    for t in range(3,1001):
        n,tau_d2,ta,tb,witnesses,d3=count_egyptian(t,return_witnesses=True)
        assert len(witnesses)==n, (t,n,len(witnesses))
        assert n <= (tau_d2-1)//2
        L,D,M,F,G=family(t)
        fac=Counter()
        for block in L: fac.update(factorint(block))
        tau_d=prod(int(e)+1 for e in fac.values())
        omega_h=len(factorint(t*(12*t+1)))
        assert n <= 2520*tau_d*(2**omega_h)
        assert D <= (630*M)**2
        for witness in witnesses:
            data=check_rep(t,witness)
            total+=1
            if t in (7,69): examples.setdefault(t,[]).append(data)
        if n>1: nonunique.append((t,n))
    assert nonunique==[(7,2),(69,2)],nonunique
    assert total==1000,total
    print("QRS_BIJECTION_AND_ROOT_CONGRUENCE: PASS")
    print("REPRESENTATIONS_CHECKED_t3_TO_1000:",total)
    print("NONUNIQUE_PARAMETERS:",nonunique)
    print("COMBINATORIAL_AND_ROOT_COUNT_BOUNDS: PASS")
    print("AM_GM_BOUND_D_LE_630_SQUARED_M_SQUARED: PASS")
    for t,items in examples.items():
        print("T=",t)
        for item in items: print("q,r,s,k,gcd,u,v =",item)
    for t in (3,7,69,100,1000):
        _,D,M,F,G=family(t)
        g=gcd(F,G); q=g*g; r=G//g; s=F//g; k=1260//g
        assert q*r*s==D and gcd(r,s)==1 and r+s==k*M
        assert q*k==1260*g
    print("CANONICAL_QRS_FORMULA: PASS")


if __name__=="__main__":
    main()
