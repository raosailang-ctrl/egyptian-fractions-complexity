#!/usr/bin/env python3
"""Complete finite checks of ordinary two-unit-fraction counts for t=1,...,8.

Unlike the genus-two theorem, this is *only* a finite integer census.
Factorization is validated and all positive divisors of D^2 are enumerated.
"""
from math import gcd,prod
from sympy import factorint,divisors,isprime

EXPECTED=[85,5,1,1,1,1,2,1]

def main():
    print('t  unordered_pairs  tau(D^2)')
    for t,exp in enumerate(EXPECTED,1):
        h=t*(12*t+1); M=h*h
        F=(1+3*t)*(1+14*t)*(1+60*t)*(1+36*t)
        G=(4*t-1)*(1+84*t)*(1+15*t)*(1+18*t)
        D=F*G
        fac=factorint(D)
        assert prod(int(p)**int(e) for p,e in fac.items())==D
        assert all(isprime(p) for p in fac)
        assert gcd(M,D)==1 and F+G==1260*M
        ds=divisors(D*D)
        tau=prod(2*int(e)+1 for e in fac.values())
        assert len(ds)==tau
        count=0
        for d in ds:
            if d>D:break
            if (D+d)%M:continue
            e=D*D//d
            assert (D*D)%d==0 and (D+e)%M==0
            u=(D+d)//M;v=(D+e)//M
            assert M*u*v==D*(u+v)
            count+=1
        assert count==exp,(t,count,exp)
        print(t,count,tau)
    print('SMALL_T_EXHAUSTIVE_ORDINARY_COUNTS: PASS')

if __name__=='__main__':main()
