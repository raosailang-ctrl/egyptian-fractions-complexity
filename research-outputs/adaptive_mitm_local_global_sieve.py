#!/usr/bin/env python3
"""Adaptive exact brute-force / meet-in-the-middle solver for central K3 family.

Requires SymPy. This is an exact finite solver, not a polynomial-time algorithm.
"""
from __future__ import annotations
import argparse
from itertools import product
from math import prod, gcd
from time import perf_counter
from sympy import factorint, legendre_symbol, sqrt_mod
from sympy.ntheory.modular import crt

DEFAULT_T=(3,7,17,69,137,185,609,1105,1285,1457,5957,6215,6657)


def family(t):
    L=(1+3*t,1+14*t,1+60*t,1+36*t,4*t-1,1+84*t,1+15*t,1+18*t)
    D=prod(L)
    h=t*(12*t+1)
    return L,D,h,h*h


def factor_blocks(L):
    exponents={}
    for value in L:
        for p,e in factorint(value).items():
            exponents[int(p)]=exponents.get(int(p),0)+int(e)
    return sorted(exponents.items())


def divisors_with_exponents(items):
    for exps in product(*[range(a+1) for _,a in items]):
        yield prod(p**e for (p,_),e in zip(items,exps)),exps


def remaining_prime_powers(items,exps):
    return [p**(a-e) for (p,a),e in zip(items,exps) if a-e]


def subset_products(values):
    out=[1]
    for value in values:
        out += [x*value for x in out]
    return out


def roots_crt(A,hf):
    """All roots x^2=A modulo h^2, assembled from prime powers by CRT."""
    moduli=[]
    root_lists=[]
    for p,a in sorted(hf.items()):
        modulus=int(p)**(2*int(a))
        roots=sqrt_mod(int(A)%modulus,modulus,all_roots=True)
        if roots is None:
            return []
        moduli.append(modulus)
        root_lists.append([int(x) for x in roots])
    result=[]
    for choice in product(*root_lists):
        value,_=crt(moduli,choice)
        result.append(int(value))
    return result


def brute(R,M,blocks):
    """Reference method; fix first block to count each unordered split once."""
    if not blocks:
        return [],0
    hits=[]
    checks=1<<(len(blocks)-1)
    for mask in range(checks):
        x=blocks[0]
        for j in range(1,len(blocks)):
            if (mask>>(j-1))&1:
                x*=blocks[j]
        y=R//x
        r,s=(x,y) if x<=y else (y,x)
        if (r*r+R)%M==0:
            hits.append((r,s))
    return hits,checks


def mitm(R,M,hf,blocks):
    """Hash right-half products and match them to all modular square roots."""
    cut=len(blocks)//2
    left=subset_products(blocks[:cut])
    right=subset_products(blocks[cut:])
    table={}
    for y in right:
        table.setdefault(y%M,[]).append(y)
    roots=roots_crt(-R,hf)
    if not roots:
        return [],len(left)+len(right),0,0
    hits=[]
    lookups=matches=0
    for x in left:
        xinv=pow(x,-1,M)
        targets={root*xinv%M for root in roots}
        lookups+=len(targets)
        for target in targets:
            for y in table.get(target,()):
                matches+=1
                r=x*y
                if r*r<=R:
                    assert (r*r+R)%M==0
                    hits.append((r,R//r))
    return hits,len(left)+len(right),lookups,matches


def jacobi_rank(L,ps):
    exponents=dict(factor_blocks(L))
    pivots={}
    for ell,e in sorted(exponents.items()):
        if e!=1:
            continue
        v=0
        for i,p in enumerate(ps):
            if legendre_symbol(ell,p)==-1:
                v|=1<<i
        while v:
            bit=v.bit_length()-1
            if bit in pivots:
                v^=pivots[bit]
            else:
                pivots[bit]=v
                break
    return len(pivots)


def analyze(t,audit=False):
    L,D,h,M=family(t)
    hf=factorint(h)
    if 2 in hf:
        raise ValueError("odd t required")
    ps=sorted(map(int,hf))
    items=factor_blocks(L)
    qpass=brute_checks=mitm_subsets=lookups=matches=0
    brute_q=mitm_q=0
    representations=[]
    start=perf_counter()
    rho=1<<len(hf)
    for q,exps in divisors_with_exponents(items):
        if not all(legendre_symbol(q,p)==1 for p in ps):
            continue
        qpass+=1
        R=D//q
        blocks=remaining_prime_powers(items,exps)
        m=len(blocks)
        if not blocks:
            continue
        # Conservative operation proxy; hash lookups are not unit-cost in practice.
        mitm_est=(1<<(m//2))+(1<<((m+1)//2))+rho*(1<<(m//2))
        brute_est=1<<(m-1)
        if mitm_est < brute_est:
            mitm_q+=1
            hits,subset_count,lookup_count,match_count=mitm(R,M,hf,blocks)
            mitm_subsets+=subset_count
            lookups+=lookup_count
            matches+=match_count
            if audit:
                reference,_=brute(R,M,blocks)
                assert set(reference)==set(hits),(t,q,reference,hits)
        else:
            brute_q+=1
            hits,checks=brute(R,M,blocks)
            brute_checks+=checks
        representations.extend((q,r,s) for r,s in hits)
    elapsed=perf_counter()-start
    representations=sorted(set(representations))
    assert all(q*r*s==D and gcd(r,s)==1 and r<=s and (r+s)%M==0
               for q,r,s in representations)
    tau=prod(a+1 for _,a in items)
    rank=jacobi_rank(L,ps)
    assert qpass <= (tau+(1<<rank)-1)//(1<<rank)
    return dict(t=t,q_pass=qpass,brute_q=brute_q,mitm_q=mitm_q,
      brute_checks=brute_checks,mitm_subsets=mitm_subsets,
      target_lookups=lookups,residue_matches=matches,rank=rank,
      representations=representations,seconds=elapsed,audited=audit)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--values",nargs="*",type=int,default=DEFAULT_T)
    parser.add_argument("--audit",nargs="*",type=int,default=[])
    args=parser.parse_args()
    print("t,qpass,brute_q,mitm_q,brute_checks,mitm_subsets,target_lookups,root_matches,reps,seconds")
    for t in args.values:
        row=analyze(t,audit=t in args.audit)
        print(f"{t},{row['q_pass']},{row['brute_q']},{row['mitm_q']},"
          f"{row['brute_checks']},{row['mitm_subsets']},{row['target_lookups']},"
          f"{row['residue_matches']},{len(row['representations'])},{row['seconds']:.3f}")
        print("  representations:",row["representations"])
        if row["audited"]:
            print("  brute-force regression audit: PASS")
    print("ADAPTIVE_LOCAL_GLOBAL_EXACT_CHECKS: PASS")


if __name__=="__main__":
    main()
