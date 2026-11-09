#!/usr/bin/env python3
"""Gray-code kernel traversal for exact square-root transport in the K3 family.

Requires SymPy. Exact finite search; not a polynomial-time algorithm.
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

def subset_products(values):
    out=[1]
    for value in values: out += [x*value for x in out]
    return out

def all_roots_crt(A,hf):
    moduli=[]; root_lists=[]
    for p,a in sorted(hf.items()):
        mod=int(p)**(2*int(a))
        roots=sqrt_mod(int(A)%mod,mod,all_roots=True)
        if roots is None: return []
        moduli.append(mod); root_lists.append([int(x) for x in roots])
    out=[]
    for choice in product(*root_lists):
        x,_=crt(moduli,choice); out.append(int(x))
    return sorted(set(out))

def one_root_crt(A,hf):
    moduli=[]; roots=[]
    for p,a in sorted(hf.items()):
        mod=int(p)**(2*int(a))
        x=sqrt_mod(int(A)%mod,mod,all_roots=False)
        if x is None: return None
        moduli.append(mod); roots.append(int(x))
    x,_=crt(moduli,roots)
    return int(x)

def nullspace_basis(rows,n):
    mat=list(rows); pivots=[]; rank=0
    for col in range(n):
        pivot=next((i for i in range(rank,len(mat)) if (mat[i]>>col)&1),None)
        if pivot is None: continue
        mat[rank],mat[pivot]=mat[pivot],mat[rank]
        for i in range(len(mat)):
            if i!=rank and ((mat[i]>>col)&1): mat[i]^=mat[rank]
        pivots.append(col); rank+=1
        if rank==len(mat): break
    pivot_set=set(pivots)
    basis=[]
    for free in (j for j in range(n) if j not in pivot_set):
        v=1<<free
        for i,pivot in enumerate(pivots):
            if (mat[i]>>free)&1: v|=1<<pivot
        basis.append(v)
    return basis,rank,pivots

def character_kernel(items,ps):
    rows=[]
    for p in ps:
        row=0
        for j,(ell,_) in enumerate(items):
            if legendre_symbol(ell,p)==-1: row|=1<<j
        rows.append(row)
    basis,rank,pivots=nullspace_basis(rows,len(items))
    return rows,basis,rank,pivots

def gray_root_multipliers(items,basis,M,hf):
    """Map each kernel parity vector v to w_v with w_v^2=q_v^(-1) mod M."""
    basis_roots=[]
    for b in basis:
        B=prod(ell for j,(ell,_) in enumerate(items) if (b>>j)&1)
        w=one_root_crt(pow(B,-1,M),hf)
        assert w is not None and (w*w*B-1)%M==0
        basis_roots.append(w)
    d=len(basis); multipliers={0:1}
    current=1; parity=0; prev_gray=0; counts=[0]*len(items)
    for i in range(1,1<<d):
        gray=i^(i>>1); changed=gray^prev_gray; j=changed.bit_length()-1
        if (gray>>j)&1:
            current=current*basis_roots[j]%M; delta=1
        else:
            current=current*pow(basis_roots[j],-1,M)%M; delta=-1
        parity ^= basis[j]
        for k in range(len(items)):
            if (basis[j]>>k)&1: counts[k]+=delta
        # Correct overlaps among basis supports: C^2 removes even exponents.
        correction=1
        for k,(ell,_) in enumerate(items):
            correction=correction*pow(ell,counts[k]//2,M)%M
        multipliers[parity]=current*correction%M
        prev_gray=gray
    return multipliers,basis_roots

def brute(R,M,blocks):
    if not blocks: return []
    hits=[]
    for mask in range(1<<(len(blocks)-1)):
        x=blocks[0]
        for j in range(1,len(blocks)):
            if (mask>>(j-1))&1: x*=blocks[j]
        y=R//x; r,s=(x,y) if x<=y else (y,x)
        if (r*r+R)%M==0: hits.append((r,s))
    return hits

def mitm(R,M,blocks,roots):
    cut=len(blocks)//2
    left=subset_products(blocks[:cut]); right=subset_products(blocks[cut:])
    table={}
    for y in right: table.setdefault(y%M,[]).append(y)
    hits=[]
    for x in left:
        inv=pow(x,-1,M)
        for z in roots:
            for y in table.get(z*inv%M,()):
                r=x*y
                if r*r<=R: hits.append((r,R//r))
    return hits

def analyze(t,audit=False):
    L,D,h,M=family(t); hf=factorint(h)
    if 2 in hf: raise ValueError("odd t required")
    ps=sorted(map(int,hf)); items=factor_blocks(L)
    rows,basis,rank,pivots=character_kernel(items,ps)
    multipliers,basis_roots=gray_root_multipliers(items,basis,M,hf)
    base_roots=all_roots_crt(-D,hf)
    assert base_roots
    reps=[]; qpass=mitm_q=brute_q=0; parity_seen=set()
    started=perf_counter()
    for q,exps in divisors_with_exponents(items):
        if not all(legendre_symbol(q,p)==1 for p in ps): continue
        qpass+=1
        parity=sum((e&1)<<j for j,e in enumerate(exps))
        assert parity in multipliers
        parity_seen.add(parity)
        square_part=prod(p**(e//2) for (p,_),e in zip(items,exps))
        w=multipliers[parity]*pow(square_part,-1,M)%M
        roots=[z*w%M for z in base_roots]
        R=D//q
        blocks=[p**(a-e) for (p,a),e in zip(items,exps) if a-e]
        m=len(blocks); rho=len(roots)
        mitm_est=(1<<(m//2))+(1<<((m+1)//2))+rho*(1<<(m//2))
        brute_est=(1<<(m-1)) if m else 0
        if m and mitm_est<brute_est:
            mitm_q+=1; found=mitm(R,M,blocks,roots)
            if audit: assert set(found)==set(brute(R,M,blocks)),(t,q)
        else:
            brute_q+=1; found=brute(R,M,blocks)
        reps.extend((q,r,s) for r,s in found)
        if audit and t in (7,69):
            assert set(roots)==set(all_roots_crt(-R,hf)),(t,q)
    elapsed=perf_counter()-started
    reps=sorted(set(reps))
    assert len(parity_seen)==len(multipliers)
    assert all(q*r*s==D and gcd(r,s)==1 and r<=s and (r+s)%M==0 for q,r,s in reps)
    return dict(t=t,ncols=len(items),rank=rank,nullity=len(basis),
      parity_classes=len(multipliers),qpass=qpass,mitm_q=mitm_q,brute_q=brute_q,
      basis=basis,basis_roots=basis_roots,reps=reps,seconds=elapsed,audit=audit)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--values",nargs="*",type=int,default=DEFAULT_T)
    ap.add_argument("--audit",nargs="*",type=int,default=[])
    args=ap.parse_args()
    print("t,ncols,rank,nullity,parity_classes,qpass,mitm_q,brute_q,reps,seconds")
    for t in args.values:
        x=analyze(t,audit=t in args.audit)
        print(f"{t},{x['ncols']},{x['rank']},{x['nullity']},{x['parity_classes']},"
          f"{x['qpass']},{x['mitm_q']},{x['brute_q']},{len(x['reps'])},{x['seconds']:.3f}")
        print("  kernel basis:",x["basis"])
        print("  basis root multipliers:",x["basis_roots"])
        print("  representations:",x["reps"])
        if x["audit"]: print("  direct-root and brute-force audits: PASS")
    print("GRAY_KERNEL_ROOT_TRANSPORT_CHECKS: PASS")

if __name__=="__main__": main()
