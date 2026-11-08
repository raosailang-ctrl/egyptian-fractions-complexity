#!/usr/bin/env python3
"""Exact q,r,s parametrization and modular-root upper-bound checks.

Requires SymPy. Run from repository root:
    python research-outputs/verify_qrs_parametrization.py
"""
from collections import Counter, defaultdict
from bisect import bisect_right
from math import gcd, prod, isqrt
from sympy import factorint


def family(t):
    L=(1+3*t,1+14*t,1+60*t,1+36*t,4*t-1,1+84*t,1+15*t,1+18*t)
    D=prod(L); M=(t*(12*t+1))**2
    F=prod(L[:4]); G=prod(L[4:])
    assert F+G==1260*M and gcd(D,M)==1
    return L,D,M,F,G


def divisors_from_prime_powers(items):
    out=[1]
    for p,e in items:
        powers=[p**j for j in range(e+1)]
        out=[x*y for x in out for y in powers]
    return out


def exact_representations(t):
    L,D,M,F,G=family(t)
    fac=Counter()
    for block in L: fac.update(factorint(block))
    factors=[(int(p),2*int(e)) for p,e in fac.items()]
    left=[]; right=[]; sl=sr=1
    for p,e in sorted(factors,key=lambda pe:pe[1]+1,reverse=True):
        n=e+1
        if sl<=sr: left.append((p,e)); sl*=n
        else: right.append((p,e)); sr*=n
    ld=divisors_from_prime_powers(left)
    rd=divisors_from_prime_powers(right)
    by_residue=defaultdict(list)
    for x in ld:
        if x<=D: by_residue[x%M].append(x)
    for xs in by_residue.values(): xs.sort()
    reps=[]
    for y in rd:
        if y>D: continue
        residue=(-D*pow(y,-1,M))%M
        xs=by_residue.get(residue,())
        upto=bisect_right(xs,D//y)
        for x in xs[:upto]:
            d=x*y; e=D*D//d
            u=(D+d)//M; v=(D+e)//M
            reps.append((d,e,u,v))
    tau_d2=prod(2*int(e)+1 for e in fac.values())
    tau_d=prod(int(e)+1 for e in fac.values())
    omega_h=len(factorint(t*(12*t+1)))
    return reps,fac,tau_d2,tau_d,omega_h


def check_rep(t, rep):
    d,e,u,v=rep
    _,D,M,F,G=family(t)
    assert d*e==D*D and d<=D and (d+D)%M==0 and (e+D)%M==0
    q=gcd(d,e)
    r=isqrt(d//q); s=isqrt(e//q)
    assert r*r==d//q and s*s==e//q
    assert gcd(r,s)==1 and q*r*s==D
    assert (r+s)%M==0
    k=(r+s)//M
    assert gcd(k,r*s)==1
    assert u==q*k*r and v==q*k*s
    assert gcd(u,v)==q*k
    assert (r*r + D//q)%M==0
    return q,r,s,k,gcd(u,v),u,v


def main():
    total=0; nonunique=[]; examples={}
    for t in range(3,1001):
        reps,fac,tau_d2,tau_d,omega_h=exact_representations(t)
        # The independent full census previously established at most two here.
        assert len(reps)<=2,(t,len(reps))
        for rep in reps:
            data=check_rep(t,rep)
            total+=1
            if t in (7,69): examples.setdefault(t,[]).append(data)
        if len(reps)>1: nonunique.append((t,len(reps)))
        # Exact combinatorial bound from coprime prime-power partitions.
        assert len(reps)<=(tau_d2-1)//2
        # Root-count bound: <= 4*630*2^omega(M) choices per q|D.
        assert len(reps)<=2520*tau_d*(2**omega_h)
        _,D,M,_,_=family(t)
        assert D<=(630*M)**2
    assert nonunique==[(7,2),(69,2)],nonunique
    assert total==1000,total
    print('QRS_BIJECTION_AND_ROOT_CONGRUENCE: PASS')
    print('REPRESENTATIONS_CHECKED_t3_TO_1000:',total)
    print('NONUNIQUE_PARAMETERS:',nonunique)
    print('COUNT_BOUNDS_AND_AM_GM_SCALE: PASS')
    for t,items in examples.items():
        print('T=',t)
        for item in items: print('q,r,s,k,gcd,u,v =',item)
    # Canonical formula q=g^2, r=G/g, s=F/g, k=1260/g.
    for t in (3,7,69,100,1000):
        _,D,M,F,G=family(t)
        g=gcd(F,G); q=g*g; r=G//g; s=F//g; k=1260//g
        assert q*r*s==D and gcd(r,s)==1 and r+s==k*M
        assert q*k==1260*g
    print('CANONICAL_QRS_FORMULA: PASS')

if __name__=='__main__': main()
