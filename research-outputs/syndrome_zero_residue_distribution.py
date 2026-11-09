#!/usr/bin/env python3
"""Sparse MITM distribution of the corrected group-algebra syndrome-zero layer.

Requires SymPy. Reports the full residue distribution on the subgroup generated
by the prime factors of D, then compares the target residue -D with its atoms.
"""
from __future__ import annotations
from collections import defaultdict, Counter
from math import prod
import argparse, time
from sympy import factorint, legendre_symbol

DEFAULT_T=(3,7,17,69,137,185)

def family(t):
    L=(1+3*t,1+14*t,1+60*t,1+36*t,4*t-1,1+84*t,1+15*t,1+18*t)
    return L,prod(L),t*(12*t+1)

def local_factors(t):
    L,D,h=family(t); M=h*h
    exponents={}
    for x in L:
        for p,a in factorint(x).items():
            exponents[int(p)]=exponents.get(int(p),0)+int(a)
    ps=sorted(map(int,factorint(h)))
    fs=[]
    for ell,a in sorted(exponents.items()):
        syndrome=0
        for j,p in enumerate(ps):
            if legendre_symbol(ell,p)==-1: syndrome|=1<<j
        opts=[]
        for e in range(a):
            syn=syndrome if e&1 else 0
            opts.append((syn,pow(ell,e,M)))
            opts.append((syn,pow(ell,2*a-e,M)))
        opts.append((syndrome if a&1 else 0,pow(ell,a,M)))
        fs.append((ell,a,opts))
    return D,M,ps,fs

def sparse_states(factors,M):
    states={(0,1):1}
    for _,_,opts in factors:
        nxt=defaultdict(int)
        for (syn,res),weight in states.items():
            for ds,dr in opts:
                nxt[(syn^ds,res*dr%M)]+=weight
        states=dict(nxt)
    return states

def balance(factors):
    left=[];right=[];wl=wr=1
    for f in sorted(factors,key=lambda x:len(x[2]),reverse=True):
        if wl<=wr:left.append(f);wl*=len(f[2])
        else:right.append(f);wr*=len(f[2])
    return left,right,wl,wr

def analyze(t):
    D,M,ps,factors=local_factors(t)
    left,right,raw_left,raw_right=balance(factors)
    start=time.perf_counter()
    A=sparse_states(left,M); B=sparse_states(right,M)
    build_seconds=time.perf_counter()-start
    by_syn=defaultdict(list)
    for (syn,res),weight in B.items():
        by_syn[syn].append((res,weight))
    distribution=defaultdict(int)
    pair_states=0
    for (syn,x),wx in A.items():
        for y,wy in by_syn.get(syn,()):
            distribution[x*y%M]+=wx*wy
            pair_states+=1
    combine_seconds=time.perf_counter()-start-build_seconds
    masses=list(distribution.values())
    total_mass=sum(masses)
    support=len(distribution)
    target=(-D)%M
    target_mass=distribution.get(target,0)
    max_atom=max(masses)
    collisions=sum(v*(v-1)//2 for v in masses)
    histogram=Counter(masses)
    # Exact independent count of q passing the Jacobi conditions.
    from itertools import product
    items=[(ell,a) for ell,a,_ in factors]
    qpass=0
    for es in product(*[range(a+1) for _,a in items]):
        q=prod(p**e for (p,_),e in zip(items,es))
        if all(legendre_symbol(q,p)==1 for p in ps):qpass+=1
    assert target_mass%2==0
    return dict(t=t,n=len(factors),rows=len(ps),raw_left=raw_left,raw_right=raw_right,
      left_states=len(A),right_states=len(B),pair_states=pair_states,
      build_seconds=build_seconds,combine_seconds=combine_seconds,
      syndrome_zero_mass=total_mass,support=support,target_mass=target_mass,
      max_atom=max_atom,average=total_mass/support,
      target_over_average=target_mass/(total_mass/support),
      target_over_max=target_mass/max_atom,collision_pairs=collisions,
      histogram=sorted(histogram.items()),qpass=qpass,
      target_N=target_mass//2)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--values",nargs="*",type=int,default=DEFAULT_T)
    args=ap.parse_args()
    print("t,n,rows,left_states,right_states,syndrome_mass,support,target,max,avg,target/avg,collisions,N")
    for t in args.values:
        x=analyze(t)
        print(f"{t},{x['n']},{x['rows']},{x['left_states']},{x['right_states']},"
          f"{x['syndrome_zero_mass']},{x['support']},{x['target_mass']},"
          f"{x['max_atom']},{x['average']:.6f},{x['target_over_average']:.6f},"
          f"{x['collision_pairs']},{x['target_N']}")
        print("  raw halves:",x["raw_left"],x["raw_right"],
              "pair states:",x["pair_states"],
              "build/combine seconds:",f"{x['build_seconds']:.4f}",f"{x['combine_seconds']:.4f}")
        print("  atom histogram:",x["histogram"])
    print("SYNDROME_ZERO_RESIDUE_DISTRIBUTION_CHECKS: PASS")

if __name__=="__main__":main()
