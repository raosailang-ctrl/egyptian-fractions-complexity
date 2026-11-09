#!/usr/bin/env python3
"""Exact meet-in-the-middle coefficient extraction in the corrected group algebra.

Requires SymPy. Verifies the target coefficient [0,-D] equals 2*N(t) for
selected central K3 parameters. State keys are (F2 syndrome, unit residue mod M).
"""
from __future__ import annotations
from collections import defaultdict
from math import prod
import argparse
from sympy import factorint, legendre_symbol

DEFAULT_T=(7,69)

def family(t):
    L=(1+3*t,1+14*t,1+60*t,1+36*t,4*t-1,1+84*t,1+15*t,1+18*t)
    return L,prod(L),t*(12*t+1)

def make_factors(t):
    L,D,h=family(t)
    M=h*h
    exponents={}
    for x in L:
        for p,a in factorint(x).items():
            exponents[int(p)]=exponents.get(int(p),0)+int(a)
    items=sorted(exponents.items())
    ps=sorted(map(int,factorint(h)))
    columns=[]
    for ell,a in items:
        col=0
        for j,p in enumerate(ps):
            if legendre_symbol(ell,p)==-1:
                col |= 1<<j
        columns.append((ell,a,col))
    factors=[]
    for ell,a,col in columns:
        opts=[]
        for e in range(a):
            syn=col if e&1 else 0
            opts.append((syn,pow(ell,e,M)))
            opts.append((syn,pow(ell,2*a-e,M)))
        syn=col if a&1 else 0
        opts.append((syn,pow(ell,a,M)))
        factors.append((ell,a,opts))
    return D,M,items,ps,factors

def balance_halves(factors):
    # Greedy by logarithmic local branching factor, preserving deterministic order.
    left=[]; right=[]; wl=wr=0
    for f in sorted(factors,key=lambda z:len(z[2]),reverse=True):
        w=len(f[2])
        if wl<=wr: left.append(f); wl+=w
        else: right.append(f); wr+=w
    return left,right,wl,wr

def build_states(factors,M):
    states={(0,1):1}
    for _,_,opts in factors:
        nxt=defaultdict(int)
        for (syn,res),count in states.items():
            for ds,dr in opts:
                nxt[(syn^ds,(res*dr)%M)] += count
        states=dict(nxt)
    return states

def direct_representations(t):
    # Independent q + unitary split enumeration using exact integer arithmetic.
    L,D,h=family(t); M=h*h
    exponents={}
    for x in L:
        for p,a in factorint(x).items():
            exponents[int(p)]=exponents.get(int(p),0)+int(a)
    items=sorted(exponents.items())
    ps=sorted(map(int,factorint(h)))
    reps=[]
    from itertools import product
    for es in product(*[range(a+1) for _,a in items]):
        q=prod(p**e for (p,_),e in zip(items,es))
        if not all(legendre_symbol(q,p)==1 for p in ps):
            continue
        blocks=[p**(a-e) for (p,a),e in zip(items,es) if a-e]
        R=D//q
        if not blocks:
            continue
        # Each unordered unitary split once: fix first block in r.
        for mask in range(1<<(len(blocks)-1)):
            r=blocks[0]
            for j in range(1,len(blocks)):
                if (mask>>(j-1))&1:r*=blocks[j]
            s=R//r
            if r>s:r,s=s,r
            if (r+s)%M==0:
                reps.append((q,r,s))
    return sorted(set(reps))

def analyze(t):
    D,M,items,ps,factors=make_factors(t)
    left,right,wl,wr=balance_halves(factors)
    A=build_states(left,M)
    B=build_states(right,M)
    target=(-D)%M
    coefficient=0
    for (syn,res),count in A.items():
        need=(syn,(target*pow(res,-1,M))%M)
        coefficient += count*B.get(need,0)
    reps=direct_representations(t)
    assert coefficient==2*len(reps),(t,coefficient,reps)
    total_options=prod(len(opts) for _,_,opts in factors)
    assert total_options==prod(2*a+1 for _,a in items)
    # Independently compute local Jacobi survivor count via exponent parity enumeration.
    qpass=0
    from itertools import product
    for es in product(*[range(a+1) for _,a in items]):
        q=prod(p**e for (p,_),e in zip(items,es))
        if all(legendre_symbol(q,p)==1 for p in ps):qpass+=1
    return dict(t=t,n=len(items),m=len(ps),factor_options=[len(x[2]) for x in factors],
      left_states=len(A),right_states=len(B),left_raw=wl,right_raw=wr,
      total_local_configurations=total_options,syndrome_zero_q_count=qpass,
      target_coefficient=coefficient,N=len(reps),representations=reps)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--values",nargs="*",type=int,default=DEFAULT_T)
    args=ap.parse_args()
    for t in args.values:
        x=analyze(t)
        print(f"t={t}: n={x['n']} rows={x['m']} local_options={x['factor_options']}")
        print(f"  raw half products={x['left_raw']} x {x['right_raw']}")
        print(f"  aggregated states={x['left_states']} x {x['right_states']}")
        print(f"  total configurations={x['total_local_configurations']}")
        print(f"  Jacobi-passing q={x['syndrome_zero_q_count']}")
        print(f"  corrected group-algebra target coefficient={x['target_coefficient']}")
        print(f"  direct N={x['N']} representations={x['representations']}")
        print("  coefficient identity: PASS")
    print("CORRECTED_GROUP_ALGEBRA_MITM_CHECKS: PASS")

if __name__=="__main__":main()
