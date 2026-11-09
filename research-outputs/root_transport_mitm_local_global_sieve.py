#!/usr/bin/env python3
"""Exact local-global MITM solver with transported square-root classes.

Requires SymPy. Exhaustive finite solver, not a polynomial-time algorithm.
"""
from __future__ import annotations
from itertools import product
from math import prod, gcd
from time import perf_counter
import argparse
from sympy import factorint, legendre_symbol, sqrt_mod
from sympy.ntheory.modular import crt

DEFAULT_T=(3,7,17,69,137,185,609,1105,1285,1457,5957,6215,6657)

def family(t):
    L=(1+3*t,1+14*t,1+60*t,1+36*t,4*t-1,1+84*t,1+15*t,1+18*t)
    D=prod(L); h=t*(12*t+1)
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

def unitary_blocks(items,exps):
    return [p**(a-e) for (p,a),e in zip(items,exps) if a-e]

def subset_products(values):
    out=[1]
    for value in values:
        out += [x*value for x in out]
    return out

def one_root_crt(A,hf):
    """One root of x^2=A modulo h^2, by prime-power roots and CRT."""
    moduli=[]; roots=[]
    for p,a in sorted(hf.items()):
        modulus=int(p)**(2*int(a))
        root=sqrt_mod(int(A)%modulus,modulus,all_roots=False)
        if root is None:
            return None
        moduli.append(modulus); roots.append(int(root))
    value,_=crt(moduli,roots)
    return int(value)

def all_roots_crt(A,hf):
    """All roots of x^2=A modulo h^2."""
    moduli=[]; root_lists=[]
    for p,a in sorted(hf.items()):
        modulus=int(p)**(2*int(a))
        roots=sqrt_mod(int(A)%modulus,modulus,all_roots=True)
        if roots is None:
            return []
        moduli.append(modulus); root_lists.append([int(x) for x in roots])
    out=[]
    for choice in product(*root_lists):
        value,_=crt(moduli,choice)
        out.append(int(value))
    return sorted(set(out))

def brute(R,M,blocks):
    """Reference enumeration; each unordered split appears once."""
    if not blocks:
        return []
    hits=[]
    for mask in range(1<<(len(blocks)-1)):
        x=blocks[0]
        for j in range(1,len(blocks)):
            if (mask>>(j-1))&1:
                x*=blocks[j]
        y=R//x
        r,s=(x,y) if x<=y else (y,x)
        if (r*r+R)%M==0:
            hits.append((r,s))
    return hits

def mitm(R,M,blocks,roots):
    cut=len(blocks)//2
    left=subset_products(blocks[:cut])
    right=subset_products(blocks[cut:])
    table={}
    for y in right:
        table.setdefault(y%M,[]).append(y)
    hits=[]
    for x in left:
        inverse=pow(x,-1,M)
        for root in roots:
            target=root*inverse%M
            for y in table.get(target,()):
                r=x*y
                if r*r<=R:
                    hits.append((r,R//r))
    return hits

def jacobi_rank(L,ps):
    exponents=dict(factor_blocks(L))
    pivots={}
    for ell,e in sorted(exponents.items()):
        if e!=1:
            continue
        vector=0
        for i,p in enumerate(ps):
            if legendre_symbol(ell,p)==-1:
                vector|=1<<i
        while vector:
            bit=vector.bit_length()-1
            if bit in pivots:
                vector^=pivots[bit]
            else:
                pivots[bit]=vector
                break
    return len(pivots)

def analyze(t,audit=False):
    L,D,h,M=family(t)
    hf=factorint(h)
    if 2 in hf:
        raise ValueError("odd t required")
    ps=sorted(map(int,hf))
    items=factor_blocks(L)
    passing=[(q,exps) for q,exps in divisors_with_exponents(items)
             if all(legendre_symbol(q,p)==1 for p in ps)]
    if not passing:
        return None

    # q=1 always passes (q/p)=1. Construct its root set only once.
    base_roots=all_roots_crt(-D,hf)
    assert base_roots
    root_transports=0
    brute_q=mitm_q=0
    representations=[]
    started=perf_counter()

    for q,exps in passing:
        R=D//q
        blocks=unitary_blocks(items,exps)
        m=len(blocks)

        # Since q passes every Jacobi row, q is a square modulo every
        # p^(2a)||M. Thus w^2=q^(-1) mod M and roots(-D/q)=w*roots(-D).
        ratio=pow(q,-1,M)
        multiplier=one_root_crt(ratio,hf)
        assert multiplier is not None
        assert (multiplier*multiplier-ratio)%M==0
        roots=sorted({(z*multiplier)%M for z in base_roots})
        assert len(roots)==len(base_roots)
        root_transports+=1

        mitm_est=(1<<(m//2))+(1<<((m+1)//2))+(len(roots)*(1<<(m//2)))
        brute_est=(1<<(m-1)) if m else 0
        if m and mitm_est<brute_est:
            mitm_q+=1
            found=mitm(R,M,blocks,roots)
            if audit:
                reference=brute(R,M,blocks)
                assert set(found)==set(reference),(t,q,found,reference)
        else:
            brute_q+=1
            found=brute(R,M,blocks)
        representations.extend((q,r,s) for r,s in found)

        if audit:
            direct_roots=all_roots_crt(-R,hf)
            assert set(roots)==set(direct_roots),(t,q,roots,direct_roots)

    elapsed=perf_counter()-started
    representations=sorted(set(representations))
    assert all(q*r*s==D and gcd(r,s)==1 and r<=s and (r+s)%M==0
               for q,r,s in representations)
    return dict(t=t,q_pass=len(passing),base_root_count=len(base_roots),
      root_transports=root_transports,brute_q=brute_q,mitm_q=mitm_q,
      representations=representations,seconds=elapsed,audited=audit)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--values",nargs="*",type=int,default=DEFAULT_T)
    parser.add_argument("--audit",nargs="*",type=int,default=[])
    args=parser.parse_args()
    print("t,q_pass,base_roots,root_transports,brute_q,mitm_q,reps,seconds")
    for t in args.values:
        row=analyze(t,audit=t in args.audit)
        print(f"{t},{row['q_pass']},{row['base_root_count']},"
          f"{row['root_transports']},{row['brute_q']},{row['mitm_q']},"
          f"{len(row['representations'])},{row['seconds']:.3f}")
        print("  representations:",row["representations"])
        if row["audited"]:
            print("  direct-root and brute-force audit: PASS")
    print("ROOT_TRANSPORT_MITM_EXACT_CHECKS: PASS")

if __name__=="__main__":
    main()
