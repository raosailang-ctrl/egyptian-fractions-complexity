#!/usr/bin/env python3
"""Exact local-global sieve for the central K3 Egyptian-fraction family.

Requires SymPy. Exhaustive verifier, not a polynomial-time algorithm.
"""
from __future__ import annotations
import argparse
from itertools import product
from math import prod, gcd
from sympy import factorint, legendre_symbol

DEFAULT_T=(3,7,17,69,137,185,609,1105,1285,1457,5957,6215,6657)

def family(t):
    L=(1+3*t,1+14*t,1+60*t,1+36*t,4*t-1,1+84*t,1+15*t,1+18*t)
    D=prod(L); h=t*(12*t+1)
    return L,D,h,h*h

def f2_rank(L, ps):
    exponents={}
    for value in L:
        for p,e in factorint(value).items():
            exponents[int(p)]=exponents.get(int(p),0)+int(e)
    pivots={}
    for ell,e in sorted(exponents.items()):
        if e!=1: continue
        v=0
        for i,p in enumerate(ps):
            if legendre_symbol(ell,p)==-1: v|=1<<i
        while v:
            bit=v.bit_length()-1
            if bit in pivots: v^=pivots[bit]
            else: pivots[bit]=v; break
    return len(pivots)

def divisors_with_exponents(items):
    for exps in product(*[range(a+1) for _,a in items]):
        yield prod(p**e for (p,_),e in zip(items,exps)), exps

def unitary_splits(items, exps):
    powers=[p**(a-e) for (p,a),e in zip(items,exps) if a-e]
    R=prod(powers)
    if R==1: return
    for mask in range(1<<len(powers)):
        r=1
        for j,power in enumerate(powers):
            if (mask>>j)&1: r*=power
        if r*r<=R: yield r,R//r

def analyze(t, audit_all_q=False):
    L,D,h,M=family(t)
    hf=factorint(h)
    if 2 in hf: raise ValueError(f"t={t} is not an odd-parameter case")
    # Factor linear factors separately; do not factor their large product D.
    df={}
    for block in L:
        for p,e in factorint(block).items():
            df[int(p)]=df.get(int(p),0)+int(e)
    items=sorted(df.items())
    ps=sorted(map(int,hf))
    tau=prod(a+1 for _,a in items)
    rank=f2_rank(L,ps)
    q_pass=split_candidates=root_hits=0
    reps=[]
    for q,exps in divisors_with_exponents(items):
        if not all(legendre_symbol(q,p)==1 for p in ps): continue
        q_pass+=1
        R=D//q
        for r,s in unitary_splits(items,exps):
            split_candidates+=1
            if (r*r+R)%M==0:
                root_hits+=1
                reps.append((q,r,s))
    bound=(tau+(1<<rank)-1)//(1<<rank)
    assert q_pass<=bound,(t,q_pass,bound,rank)
    assert all(q*r*s==D and gcd(r,s)==1 and (r+s)%M==0 for q,r,s in reps)
    if audit_all_q:
        all_reps=[]
        for q,exps in divisors_with_exponents(items):
            R=D//q
            for r,s in unitary_splits(items,exps):
                if (r*r+R)%M==0: all_reps.append((q,r,s))
        assert set(all_reps)==set(reps),(t,all_reps,reps)
    return dict(t=t,tau_D=tau,omega_h=len(ps),rank=rank,
      jacobi_passing_q=q_pass,jacobi_upper_bound=bound,
      unitary_split_candidates_after_jacobi=split_candidates,
      root_hit_splits=root_hits,representations=reps,all_q_audit=audit_all_q)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--values",nargs="*",type=int,default=DEFAULT_T)
    ap.add_argument("--audit-all-q",nargs="*",type=int,default=[])
    args=ap.parse_args()
    print("t,tau_D,omega_h,rank,q_pass,q_bound,unitary_splits,root_hits,reps")
    for t in args.values:
        x=analyze(t,audit_all_q=t in args.audit_all_q)
        print(f"{t},{x['tau_D']},{x['omega_h']},{x['rank']},"
          f"{x['jacobi_passing_q']},{x['jacobi_upper_bound']},"
          f"{x['unitary_split_candidates_after_jacobi']},"
          f"{x['root_hit_splits']},{len(x['representations'])}")
        print("  representations:",x["representations"])
        if x["all_q_audit"]: print("  all-q exhaustive audit: PASS")
    print("LOCAL_GLOBAL_SIEVE_EXACT_CHECKS: PASS")

if __name__=="__main__": main()
