#!/usr/bin/env python3
"""Verify the Jacobi-compatible square roots of D^2 modulo h^2.

For odd h, every root g^2=D^2 mod p^(2a) is g=+D or -D.
The script compares the CRT sign formula with direct SymPy roots.
"""
from itertools import product
from math import prod
import argparse
from sympy import factorint, legendre_symbol, sqrt_mod
from sympy.ntheory.modular import crt

DEFAULT_T=(3,7,17,69,137,185)

def family(t):
    L=(1+3*t,1+14*t,1+60*t,1+36*t,4*t-1,1+84*t,1+15*t,1+18*t)
    return prod(L),t*(12*t+1)

def analyze(t):
    D,h=family(t); M=h*h
    hf=sorted((int(p),int(a)) for p,a in factorint(h).items())
    if any(p==2 for p,a in hf):
        raise ValueError("This verifier assumes odd h.")
    moduli=[p**(2*a) for p,a in hf]
    local_roots=[]
    for p,a in hf:
        mod=p**(2*a)
        roots=[int(x) for x in sqrt_mod(D*D,mod,all_roots=True)]
        assert set(roots)=={D%mod,(-D)%mod}
        local_roots.append(roots)
    all_roots=[]
    compatible=[]
    local_data=[]
    for p,a in hf:
        d=int(legendre_symbol(D,p))
        choices=[sign for sign in (1,-1) if int(legendre_symbol(sign*D,p))==1]
        local_data.append((p,a,p%4,d,len(choices)))
    for signs in product((1,-1),repeat=len(hf)):
        residues=[(sign*D)%mod for sign,mod in zip(signs,moduli)]
        g,_=crt(moduli,residues)
        g=int(g)%M
        all_roots.append(g)
        if all(legendre_symbol(g,p)==1 for p,a in hf):
            compatible.append(g)
    direct=[]
    for roots in product(*local_roots):
        g,_=crt(moduli,roots)
        direct.append(int(g)%M)
    assert set(direct)==set(all_roots)
    assert set(compatible)=={g for g in all_roots
                             if all(legendre_symbol(g,p)==1 for p,a in hf)}
    formula=prod(n for _,_,_,_,n in local_data)
    assert formula==len(compatible)
    return dict(t=t,D=D,h=h,M=M,omega=len(hf),root_count=len(all_roots),
                compatible_count=len(compatible),local_data=local_data,
                compatible_roots=sorted(compatible))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--values",nargs="*",type=int,default=DEFAULT_T)
    args=ap.parse_args()
    for t in args.values:
        x=analyze(t)
        print(f"t={t}: omega(h)={x['omega']}, all roots={x['root_count']}, "
              f"Jacobi-compatible roots={x['compatible_count']}")
        print("  local (p,a,p mod4,(D/p),choices):",x["local_data"])
        print("  compatible CRT roots:",x["compatible_roots"])
        print("  direct CRT / Legendre audit: PASS")
    print("JACOBI_COMPATIBLE_FIXED_ROOT_CHECKS: PASS")

if __name__=="__main__": main()
