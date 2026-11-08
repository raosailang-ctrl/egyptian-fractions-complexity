#!/usr/bin/env python3
"""Survey F2 Legendre-character ranks for odd t in the central K3 family.
Requires SymPy. This is finite computation, not an asymptotic theorem.
"""
import argparse,json
from collections import Counter
from math import prod
from pathlib import Path
from sympy import factorint,legendre_symbol

def f2_basis(columns):
    pivots={};selected=[]
    for prime,vector in columns:
        x=vector
        while x:
            pivot=x.bit_length()-1
            if pivot in pivots:x^=pivots[pivot]
            else:
                pivots[pivot]=x;selected.append((prime,vector));break
    return len(pivots),selected

def analyze(t):
    L=(1+3*t,1+14*t,1+60*t,1+36*t,4*t-1,1+84*t,1+15*t,1+18*t)
    h=t*(12*t+1);hfac=factorint(h)
    if 2 in hfac:raise ValueError("Only odd t are included")
    ps=sorted(map(int,hfac));exponent=Counter()
    for block in L:exponent.update({int(p):int(e) for p,e in factorint(block).items()})
    cols=[]
    for ell,e in sorted(exponent.items()):
        if e!=1:continue
        vector=0
        for i,p in enumerate(ps):
            if legendre_symbol(ell,p)==-1:vector|=1<<i
        cols.append((ell,vector))
    rank,basis=f2_basis(cols);D=prod(L);target=0
    for i,p in enumerate(ps):
        if legendre_symbol(-D,p)==-1:target|=1<<i
    tau=prod(e+1 for e in exponent.values())
    return {"t":t,"h_prime_factors":ps,"omega_h":len(ps),
      "D_exponent_one_primes":[p for p,_ in cols],"column_count":len(cols),
      "rank":rank,"rank_deficiency":len(ps)-rank,"full_rank":rank==len(ps),
      "basis_primes":[p for p,_ in basis],"basis_vectors":[v for _,v in basis],
      "target_vector":target,"D":D,"M":h*h,"tau_D":tau,
      "q_pass_upper_bound":(tau+(1<<rank)-1)//(1<<rank)}

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--max-t",type=int,default=10000)
    ap.add_argument("--jsonl",default="jacobi_rank_odd_t_10000.jsonl");args=ap.parse_args()
    rows=[analyze(t) for t in range(1,args.max_t+1,2)]
    hist=Counter((x["omega_h"],x["rank"]) for x in rows)
    full=sum(x["full_rank"] for x in rows)
    with Path(args.jsonl).open("w",encoding="utf-8") as f:
        for x in rows:f.write(json.dumps(x,separators=(",",":"))+"\n")
    print("ODD_PARAMETERS:",len(rows))
    print("FULL_RANK:",full)
    print("FULL_RANK_FRACTION:",f"{full}/{len(rows)}={full/len(rows):.6%}")
    print("RANK_DEFICIENT:",len(rows)-full)
    print("MAX_RANK_DEFICIENCY:",max(x["rank_deficiency"] for x in rows))
    print("HISTOGRAM_OMEGA_RANK:",sorted((s,r,n) for (s,r),n in hist.items()))
    print("DEFICIENCY_2_PARAMETERS:",[x["t"] for x in rows if x["rank_deficiency"]==2])
if __name__=="__main__":main()
