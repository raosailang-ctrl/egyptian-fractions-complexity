#!/usr/bin/env python3
"""Exact F_2 Jacobi-character sieve certificates for t=7 and t=69."""
from collections import Counter
from math import prod
from sympy import factorint, divisors, legendre_symbol


def family(t):
    L=(1+3*t,1+14*t,1+60*t,1+36*t,4*t-1,1+84*t,1+15*t,1+18*t)
    D=prod(L); h=t*(12*t+1)
    return L,D,h


def rank_f2(vectors):
    basis={}; rank=0
    for vec in vectors:
        x=sum((int(bit)&1)<<i for i,bit in enumerate(vec))
        while x:
            pivot=x.bit_length()-1
            if pivot in basis: x ^= basis[pivot]
            else:
                basis[pivot]=x; rank+=1; break
    return rank


def certificate(t, chosen):
    L,D,h=family(t)
    hfac=factorint(h)
    assert all(p%2 for p in hfac), "certificate assumes odd h"
    mod_primes=sorted(map(int,hfac))
    df=Counter()
    for x in L: df.update(factorint(x))
    vectors={}
    for ell,exp in df.items():
        vectors[int(ell)]=tuple(0 if legendre_symbol(int(ell),p)==1 else 1 for p in mod_primes)
    for ell in chosen: assert df[ell]==1
    basis=[vectors[p] for p in chosen]
    assert rank_f2(basis)==len(mod_primes)==len(chosen)
    target=tuple(0 if legendre_symbol(-D,p)==1 else 1 for p in mod_primes)
    qs=divisors(D); passed=[]
    for q in qs:
        vec=[0]*len(mod_primes)
        for ell,e in factorint(q).items():
            v=vectors[int(ell)]
            for i,b in enumerate(v): vec[i]^=(int(e)&1)*b
        if tuple(vec)==target: passed.append(q)
    assert len(passed)*2**len(chosen)==len(qs)
    M=h*h
    for q in passed:
        x=(-D*pow(q,-1,M))%M
        for p in hfac: assert legendre_symbol(x,int(p))==1
    return len(qs),len(passed),mod_primes,basis,target


def main():
    cases={7:(19,23,31),69:(967,41,37)}
    for t,chosen in cases.items():
        total,passed,ps,basis,target=certificate(t,chosen)
        print(f"t={t}: h-primes={ps}")
        print("independent squarefree D-primes:",chosen)
        print("F2 character vectors:",basis)
        print("target:",target)
        print(f"q divisors passing Jacobi sieve: {passed}/{total} = 1/8")
    print("LOCAL_JACOBI_SIEVE_CERTIFICATES: PASS")


if __name__=="__main__": main()
