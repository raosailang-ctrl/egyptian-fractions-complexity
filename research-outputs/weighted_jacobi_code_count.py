#!/usr/bin/env python3
"""Exact weighted MacWilliams count for Jacobi-passing divisors q|D.

Requires SymPy. The program compares the code-enumerator identity with direct
enumeration for selected central K3 parameters.
"""
from __future__ import annotations
from itertools import product
from math import prod
import argparse
from sympy import factorint, legendre_symbol

DEFAULT_T=(3,7,17,69,137,185,609,1105,1285,1457,5957,6215,6657)

def family(t):
    L=(1+3*t,1+14*t,1+60*t,1+36*t,4*t-1,1+84*t,1+15*t,1+18*t)
    return L,prod(L),t*(12*t+1)

def rank_basis(rows,n):
    mat=list(rows); pivots=[]; rank=0
    for col in range(n):
        pivot=next((i for i in range(rank,len(mat)) if (mat[i]>>col)&1),None)
        if pivot is None: continue
        mat[rank],mat[pivot]=mat[pivot],mat[rank]
        for i in range(len(mat)):
            if i!=rank and ((mat[i]>>col)&1): mat[i]^=mat[rank]
        pivots.append(col); rank+=1
        if rank==len(mat): break
    return mat[:rank],rank,pivots

def rowspace(basis):
    out=[0]
    for b in basis: out += [x^b for x in out]
    return out

def analyze(t):
    L,D,h=family(t)
    factors={}
    for value in L:
        for p,e in factorint(value).items():
            factors[int(p)]=factors.get(int(p),0)+int(e)
    items=sorted(factors.items())
    ps=sorted(map(int,factorint(h)))
    rows=[]
    for p in ps:
        row=0
        for i,(ell,_) in enumerate(items):
            if legendre_symbol(ell,p)==-1: row|=1<<i
        rows.append(row)
    basis,rank,_=rank_basis(rows,len(items))
    R=rowspace(basis)
    alpha=[a//2+1 for _,a in items]
    beta=[(a+1)//2 for _,a in items]
    numerator=0
    for y in R:
        term=1
        for i in range(len(items)):
            term*=alpha[i]+(beta[i] if not ((y>>i)&1) else -beta[i])
        numerator+=term
    assert numerator%(1<<rank)==0
    weighted=numerator//(1<<rank)

    # Simplified form: y must vanish on odd-exponent coordinates.
    odd=[i for i,(_,a) in enumerate(items) if a&1]
    even=[i for i,(_,a) in enumerate(items) if not (a&1)]
    W=[y for y in R if all(not ((y>>i)&1) for i in odd)]
    numerator2=0
    for y in W:
        term=prod(items[i][1]+1 for i in odd)
        for i in even:
            a=items[i][1]
            term*=1 if ((y>>i)&1) else (a+1)
        numerator2+=term
    assert numerator2%(1<<rank)==0
    simplified=numerator2//(1<<rank)
    assert simplified==weighted

    # Direct exact divisor count.
    direct=0
    for exps in product(*[range(a+1) for _,a in items]):
        q=prod(p**e for (p,_),e in zip(items,exps))
        if all(legendre_symbol(q,p)==1 for p in ps):
            direct+=1
    assert direct==weighted,(t,direct,weighted)

    # Exponent-one submatrix rank: this is the rank that supports the
    # simple tau(D)/2^r1 bound by independent binary choices.
    one_cols=[i for i,(_,a) in enumerate(items) if a==1]
    rows1=[]
    for row in rows:
        v=0
        for j,i in enumerate(one_cols):
            if (row>>i)&1: v|=1<<j
        rows1.append(v)
    _,rank1,_=rank_basis(rows1,len(one_cols))
    tau=prod(a+1 for _,a in items)
    bound=tau//(1<<rank1)
    assert weighted<=bound

    return dict(t=t,n=len(items),rank=rank,nullity=len(items)-rank,
      odd_exp=len(odd),even_exp=len(even),rowspace_size=len(R),
      W_dim=rank-rank_basis([[((row>>i)&1) for i in []] for row in []],0)[1] if False else len(W).bit_length()-1,
      W_size=len(W),tau=tau,rank_exp1=rank1,exp1_bound=bound,
      exact=weighted,direct=direct)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--values",nargs="*",type=int,default=DEFAULT_T)
    args=ap.parse_args()
    print("t,n,rank_full,odd_exp,even_exp,rowspace,W_size,tau,rank_exp1,exp1_bound,exact")
    for t in args.values:
        x=analyze(t)
        print(f"{t},{x['n']},{x['rank']},{x['odd_exp']},{x['even_exp']},"
          f"{x['rowspace_size']},{x['W_size']},{x['tau']},{x['rank_exp1']},"
          f"{x['exp1_bound']},{x['exact']}")
    print("WEIGHTED_CODE_ENUMERATOR_CHECKS: PASS")

if __name__=="__main__": main()
