#!/usr/bin/env python3
"""Verify explicit positive-density APs with s independent Jacobi rows."""
from math import gcd, prod

BAD={2,3,5,7,11,19,23}
CASES={
1:{"p":[3],"ell":[17],"t0":1269,"Q":1734,"mods":[2,3,289],"rems":[1,0,113]},
2:{"p":[3,5],"ell":[41,37],"t0":29828265,"Q":69038670,"mods":[2,3,5,1681,1369],"rems":[1,0,0,601,493]},
3:{"p":[3,5,7],"ell":[71,127,31],"t0":6102567122925,"Q":16408422183090,"mods":[2,3,5,7,5041,16129,961],"rems":[1,0,0,0,1751,5503,351]},
4:{"p":[3,5,7,11],"ell":[3851,3697,661,211],"t0":1545737855811022572272136255,"Q":9108057167759147616947010390,"mods":[2,3,5,7,11,14830201,13667809,436921,44521],"rems":[1,0,0,0,0,4947251,4559633,146301,15051]},
5:{"p":[3,5,7,11,13],"ell":[20021,6007,51481,16381,97021],"t0":2838849652333845661868392015617839988177612605385,"Q":2907691921644767708900421268599249709752384865470,"mods":[2,3,5,7,11,13,400840441,36084049,2650293361,268337161,9413074441],"rems":[1,0,0,0,0,0,133633501,12034023,883482601,89462101,3137788501]},
}
def is_prime(n):
    if n<2:return False
    if n%2==0:return n==2
    d=3
    while d*d<=n:
        if n%d==0:return False
        d+=2
    return True
def legendre(a,p):
    x=pow(a%p,(p-1)//2,p)
    return 0 if x==0 else (1 if x==1 else -1)
def L(t):
    return (1+3*t,1+14*t,1+60*t,1+36*t,4*t-1,1+84*t,1+15*t,1+18*t)
def verify(s,c):
    ps,ells,t0,Q=c["p"],c["ell"],c["t0"],c["Q"]
    assert len(ps)==len(ells)==s
    assert all(is_prime(p) for p in ps+ells)
    assert len(set(ps+ells))==2*s
    assert all(e not in BAD for e in ells)
    assert Q==prod(c["mods"])
    for i,m in enumerate(c["mods"]):
        assert all(gcd(m,n)==1 for n in c["mods"][i+1:])
        assert t0%m==c["rems"][i]
    assert 0<t0<Q and t0%2==1 and all(t0%p==0 for p in ps)
    vals=L(t0)
    for ell in ells:
        assert vals[0]%ell==0 and vals[0]%(ell*ell)!=0
        assert all(vals[i]%ell!=0 for i in range(1,8))
    matrix=[[0 if legendre(ell,p)==1 else 1 for ell in ells] for p in ps]
    assert matrix==[[int(i==j) for j in range(s)] for i in range(s)]
    t1=t0+Q
    assert t1%2==1 and all(t1%p==0 for p in ps)
    for ell in ells:
        assert (1+3*t1)%ell==0 and (1+3*t1)%(ell*ell)!=0
    return matrix
def main():
    for s,c in CASES.items():
        verify(s,c)
        print(f"s={s}: p={c['p']}; ell={c['ell']}; t={c['t0']} (mod {c['Q']}); sieve factor={2**s}")
    print("ARITHMETIC_PROGRESSION_JACOBI_CERTIFICATES: PASS")
if __name__=="__main__":main()
