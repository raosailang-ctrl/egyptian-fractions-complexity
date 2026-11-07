#!/usr/bin/env python3
"""Exact algebraic and modular certificates for the genus-two obstruction.

Uses Python 3.10+ and SymPy; does not purport to prove Faltings or Siegel
computationally.  Those are named external theorems in the research note.
"""
from __future__ import annotations
from fractions import Fraction
from math import gcd, isqrt
import sympy as sp

a, b, c, t, z, kval, C = sp.symbols("a b c t z kval C")


def symbolic_resonance_and_genus_two() -> None:
    pi = a*b*c
    sig = (pi-1)**2 / pi
    kappa = sum(2+r+1/r for r in (a,b,c)) - sig - 4
    conic = a*b*(1+a*b)*c*c+(a+b)*(a*b-1)*c-(1+a*b)
    T = 2*(a+b)*(a*a*b*b+1)
    U = a*b*(a*b+1)
    # Identity holds OFF the resonance locus; the error term is a multiple of it.
    assert sp.cancel(kappa - 4 - T/U + (a*b-1)*conic/(a*b*c*(a*b+1))) == 0
    R = sp.expand(T*T+128*U*U)
    assert sp.degree(R, b) == 6
    disc = sp.factor(sp.discriminant(R, b))
    expected = (-2**47 * a**20 * (a-1)**2 * (a+1)**2
                * (a**4+4*a*a+1)**2 * (a**4+52*a*a+1)**2)
    assert sp.factor(disc-expected) == 0
    print("UNIVERSAL_KAPPA_ELIMINATION: PASS")
    print("GENUS_TWO_SEXTIC_DISCRIMINANT: PASS")
    print("  discr_b R_a =", sp.factor(disc))

    n = sp.expand(sp.cancel(R.subs(a, sp.Rational(1, 6)) * 11664))
    R6 = (36*b**6 +12*b**5+3745*b**4+14688*b**3
          +88200*b**2+15552*b+1296)
    assert sp.expand(n-R6)==0
    assert sp.degree(sp.gcd(R6, sp.diff(R6,b)), b)==0
    assert sp.degree(sp.gcd(sp.Poly(R6,b,modulus=13),
                            sp.Poly(sp.diff(R6,b),b,modulus=13)),b)==0
    kap6 = sp.factor((4*U+T).subs(a,sp.Rational(1,6))/U.subs(a,sp.Rational(1,6)))
    assert sp.factor(kap6-(6*b**3+13*b*b+288*b+36)/(3*b*(b+6))) == 0
    assert sp.factor(kap6.subs(b,4)-sp.Rational(89,6))==0
    qkap6 = sp.factor((kap6*kap6-8*kap6+144).subs(b,4))
    assert qkap6 == sp.Rational(8833,36)
    assert sp.factorint(8833)=={11:2,73:1}
    print("SPECIAL_FIBER_a_1_6: PASS")
    print("  R_1/6(b) * 11664 =", R6)
    print("  b=4: kappa=89/6, Q(kappa)=8833/36 = (11/6)^2*73")


def verify_quartic_discriminant() -> None:
    f = (4*z+1)*(2+kval*z)**2+C*z**4
    bk = (-kval**4+16*kval**3+224*kval**2
          -2304*kval+6912)
    bracket = -64*C*C+bk*C+4*kval**3*(kval-8)**3
    assert sp.factor(sp.discriminant(f,z)+256*C*bracket)==0
    assert sp.factor(sp.discriminant(bracket,C) -
                     (kval-4)**2*(kval*kval-8*kval+144)**3)==0
    print("GENUS_ONE_QUARTIC_DISCRIMINANT: PASS")


# Integral E0: y^2=x^3+1441 x^2 -513648 x+57526848
A2,A4,A6=1441,-513648,57526848
D_E=7270291997982720000


def mod_inv(x:int,p:int)->int:
    assert x%p!=0
    return pow(x%p,-1,p)


def ec_add(P,Q,p):
    if P is None:return Q
    if Q is None:return P
    x,y=P; u,v=Q
    if x==u and (y+v)%p==0:return None
    if x==u: slope=(3*x*x+2*A2*x+A4)*mod_inv(2*y,p)%p
    else: slope=(v-y)*mod_inv(u-x,p)%p
    X=(slope*slope-A2-x-u)%p
    Y=(-y+slope*(x-X))%p
    assert (Y*Y-X**3-A2*X*X-A4*X-A6)%p==0
    return X,Y


def quartic_and_kappa_mod(P,p):
    x,y=P
    bval=(33*x-y-7704)*mod_inv(12*(x+352),p)%p
    Y=(x*mod_inv(12,p)-6*bval*bval+33*bval)%p
    cval=(-6*bval*bval+35*bval+6+Y)*mod_inv(2*bval*(bval+6),p)%p
    aval=mod_inv(6,p)
    Pi=aval*bval*cval%p
    assert Pi!=0
    sigma=(Pi-1)**2*mod_inv(Pi,p)%p
    kval=(sum(2+r+mod_inv(r,p) for r in (aval,bval,cval))
          -sigma-4)%p
    Qk=(kval*kval-8*kval+144)%p
    return bval,cval,kval,Qk


def verify_mod53_sieve() -> None:
    p=53
    assert D_E%p!=0
    Q=(888%p,-37920%p)
    assert (Q[1]**2-Q[0]**3-A2*Q[0]**2-A4*Q[0]-A6)%p==0
    P=None
    expected=[((40,28),(4,2,6,26)),
              ((33,13),(35,13,27,21)),
              ((33,40),(32,21,4,22)),
              ((40,25),(16,25,25,39))]
    for i,(coords,vals) in enumerate(expected,1):
        P=ec_add(P,Q,p)
        assert P==coords,(i,P,coords)
        assert quartic_and_kappa_mod(P,p)==vals,(i,P)
        assert sp.legendre_symbol(vals[-1],p)==-1
        print(f"  m mod 5={i}: P={P}, (b,c,kappa,Q)={vals}, nonsquare: PASS")
    assert ec_add(P,Q,p) is None
    print("MOD53_ORDER5_AND_FOUR_NONSQUARE_CLASSES: PASS")


def verify_central_integer_family() -> None:
    h=t*(12*t+1)
    F=(1+3*t)*(1+14*t)*(1+60*t)*(1+36*t)
    G=(4*t-1)*(1+84*t)*(1+15*t)*(1+18*t)
    D=sp.expand(F*G)
    M=h*h
    lam=1260
    assert sp.expand(F+G-lam*M)==0
    assert sp.expand(F-G-(24*t+1)*(2+178*h))==0
    assert sp.degree(M,t)==4 and sp.degree(D,t)==8
    assert sp.LC(sp.Poly(D,t))==8230118400
    assert gcd(int(D.subs(t,420)),int(M.subs(t,420)))==1
    tv=420
    fv=int(F.subs(t,tv));gv=int(G.subs(t,tv))
    u=lam*fv;v=lam*gv
    assert gcd(u,v)==lam
    assert int(M.subs(t,tv))*u*v==int(D.subs(t,tv))*(u+v)
    assert (u,v)==(3560697657393736860,3555910693494103140)
    print("CENTRAL_FAMILY_EXPLICIT_IDENTITY: PASS")
    print("  t=420: h=",int(h.subs(t,tv)))
    print("  gcd(u,v) =",gcd(u,v))
    print("  bitlength: M~4log2(t), D~8log2(t), total~12log2(t)")


def scan_small_rational_b(max_q=60,max_p=600):
    # Exploratory only. A finite search never proves completeness.
    found=[]
    for q in range(1,max_q+1):
        for p in range(-max_p,max_p+1):
            if gcd(p,q)!=1:continue
            rh=36*p**6+12*p**5*q+3745*p**4*q*q+14688*p**3*q**3+88200*p*p*q**4+15552*p*q**5+1296*q**6
            if rh>=0 and isqrt(rh)**2==rh:
                found.append((p,q))
    print("EXPLORATORY_RATIONAL_SQUARE_B_SCAN (NOT COMPLETE):",found)


def main():
    symbolic_resonance_and_genus_two()
    verify_quartic_discriminant()
    verify_mod53_sieve()
    verify_central_integer_family()
    scan_small_rational_b()
    print("ALL_EXACT_CERTIFICATES_PASSED")
    print("NOTE: Faltings/Siegel finiteness and Weyl equidistribution are external mathematical theorems.")


if __name__=="__main__":main()
