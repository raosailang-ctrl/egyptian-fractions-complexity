#!/usr/bin/env python3
"""Exact meet-in-the-middle divisor-residue count, for central K3 fractions.

Given coprime M,D and factorization D=prod p^e, split prime powers of
D^2 into A,B with gcd(A,B)=1; enumerate a|A and b|B independently.
Then d=ab is admissible iff a*b <= D and a == -D*b^{-1} mod M.
Group a values by residue and use bisect_right for the bound a<=D//b.
Time O(tau(A)log tau(A)+tau(B)log tau(A)), memory O(tau(A)).
The partition is chosen to roughly balance tau(A),tau(B).
"""
import argparse
import json
from pathlib import Path
from bisect import bisect_right
from collections import defaultdict, Counter
from math import gcd, prod
from sympy import factorint


def data(t):
    linear=(1+3*t,1+14*t,1+60*t,1+36*t,4*t-1,1+84*t,1+15*t,1+18*t)
    D=prod(linear)
    M=(t*(12*t+1))**2
    F=prod(linear[:4]); G=prod(linear[4:])
    assert gcd(M,D)==1 and F+G==1260*M
    return D,M,F,G,linear


def balanced_factor_groups(factors):
    A=[];B=[];sa=1;sb=1
    for p,e in sorted(factors.items(),key=lambda kv:2*kv[1]+1,reverse=True):
        v=2*e+1
        if sa<=sb:
            A.append((int(p),2*int(e)));sa*=v
        else:
            B.append((int(p),2*int(e)));sb*=v
    return A,B,sa,sb


def enumerate_divisors(prime_powers):
    values=[1]
    for prime,exponent in prime_powers:
        powers=[prime**a for a in range(exponent+1)]
        values=[v*x for v in values for x in powers]
    return values


def count_egyptian(t, return_witnesses=False):
    D,M,F,G,blocks=data(t)
    fact=Counter()
    # Factor each small linear block rather than the degree-8 integer D.
    for v in blocks:
        fact.update(factorint(v))
    assert prod(int(p)**int(e) for p,e in fact.items()) == D
    d3_bound=prod(((e+1)*(e+2))//2 for e in fact.values())
    left,right,ta,tb=balanced_factor_groups(fact)
    ad=enumerate_divisors(left)
    bd=enumerate_divisors(right)
    assert len(ad)==ta and len(bd)==tb
    left_index=defaultdict(list)
    for a in ad:
        if a<=D:
            left_index[a%M].append(a)
    for values in left_index.values():
        values.sort()
    count=0;witnesses=[]
    for b in bd:
        if b>D:continue
        residue=(-D*pow(b,-1,M))%M
        arr=left_index.get(residue, ())
        if not arr:continue
        n=bisect_right(arr,D//b)
        count+=n
        if return_witnesses and len(witnesses)<20:
            for a in arr[:min(n,20-len(witnesses))]:
                d=a*b
                e=D*D//d
                u=(D+d)//M;v=(D+e)//M
                assert d<=D and (d+D)%M==0 and M*u*v==D*(u+v)
                witnesses.append((d,gcd(u,v),u,v))
    assert count <= ta*tb <= d3_bound
    return count,ta*tb,ta,tb,witnesses,d3_bound


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--max-t',type=int,default=100)
    parser.add_argument('--jsonl',type=str,default=None,
                        help='Optional output path for full exact per-t results')
    args=parser.parse_args()
    expected=(85,5,1,1,1,1,2,1)
    rows=[]
    for t in range(1,args.max_t+1):
        n,total,ta,tb,wit,d3=count_egyptian(t)
        if t<=8:assert n==expected[t-1]
        rows.append((t,n,total,ta,tb,d3))
    print('CENSUS_PASSED t=1..'+str(args.max_t))
    print('nonunique=',[(t,n) for t,n,*_ in rows if n>1])
    print('max tau(D^2)=',max(row[2] for row in rows))
    print('max half-divisors=',max(max(row[3],row[4]) for row in rows))
    print('max N=',max(n for _,n,*_ in rows))
    for row in rows[:15]:print(*row)
    if args.jsonl:
        output=Path(args.jsonl)
        with output.open('w',encoding='utf-8') as f:
            for t,n,tau,ta,tb,d3 in rows:
                f.write(json.dumps({'t':t,'unordered_pairs':n,
                                    'tau_D_squared':tau,
                                    'three_fold_divisor_bound':d3,
                                    'left_divisors':ta,
                                    'right_divisors':tb})+'\n')
        print('FULL_CENSUS_JSONL:',output)
    for t,n,*_ in rows:
        if t>8 and n>1:
            count,_,_,_,witnesses,_=count_egyptian(t,return_witnesses=True)
            print('FIRST EXTRA AT t=',t,'count',count,'witnesses gcd',[(d,g) for d,g,*_ in witnesses[:8]])
            break

if __name__=='__main__':main()