# Fixed-gcd extremality and elliptic-curve obstruction in the K3-derived Egyptian fraction family

Date: 2026-11-06. Project-internal exact research note, subject to mathematical peer review and literature-priority audit.

## Summary

For the second explicit two-parameter family derived from the resonance elliptic K3 section P_a-R_a (see SECOND_SECTION_POLYNOMIAL_RIGIDITY.md), let n >= 8 be fixed, let t be a positive integer, and write

    M(t) = h(t)^2,    h(t) = t(A*t+1),
    D(t) = F(t)*G(t),  F(t)+G(t) = lambda*M(t),
    M(t)/D(t) = 1/(lambda*F(t)) + 1/(lambda*G(t)).

All A, lambda, F and G are the explicit integer expressions in the earlier note. The known unit-fraction denominators are lambda*F and lambda*G. We establish:

1. Every positive integer representation M/D = 1/u+1/v has gcd(u,v) >= lambda for all t beyond an effective threshold t0(n). Equality forces the known unordered representation.
2. gcd(F(t),G(t)) = gcd(F(t),lambda). The known pair has denominator gcd exactly lambda for an exactly computable, positive natural density of t. For n=8 the density is 43008/274417 (~15.67%), and the explicit sufficient threshold is t >= 13.
3. For n=8, for every fixed bound C0, there are only finitely many t admitting a *noncanonical* representation with gcd(u,v) <= C0. The proof invokes Siegel's theorem for integral points on a genus-one curve. Consequently all noncanonical representations, if any, eventually have gcd > lambda^2, whereas the canonical pair always has gcd <= lambda^2.
4. The same bounded-gcd finiteness holds for every n >= 8 satisfying a checkable rational nonsquare condition. In particular it holds for infinitely many n: n congruent to 4 or 5 modulo 7.

The results do **not** establish uniqueness among all integer representations for infinitely many t. The elliptic finiteness step is not an explicit cutoff algorithm.

## 1. Exact algebraic input

For n >= 8 define K = n^3-7n^2-n-1 and

    A = 2*n*(n-1)*(n-3)*(n+1)*(3*n+1)*(n^2+1),
    B = 2*n*(n-3)*(n+1)*(3*n+1)*K,
    S = (n-3)*(n+1)*K^2.

Define the three alpha_i, beta_i and lambda as in SECOND_SECTION_POLYNOMIAL_RIGIDITY.md. Put

    F = (1+B*t)*product_i(1+alpha_i*t),
    G = ((B+S)*t-1)*product_i(1+beta_i*t).

The previous exact symbolic verification proves F*G=D>0, F+G=lambda*h^2 and F>G>0. Since D=(S*h-1)*product(1+w_i*h), D is congruent to -1 mod h. Thus gcd(D,h^2)=1.

Let Delta=F-G and M=h^2. By exact coefficient comparison in Z[n,t], we obtain the useful *new* normal form

    Delta(t) = (2*A*t+1)*(2+kappa*A*h(t)),

where

    kappa(n) =
    (5n^8 - 12n^6 - 40n^5 + 206n^4 + 16n^3 + 52n^2 + 24n + 5)
    / [n(n-3)(n-1)(n+1)(3n+1)(n^2+1)].

This formula is checked symbolically in verify_minimal_gcd_and_siegel.py. In particular Delta is a polynomial of degree 3 with strictly positive coefficients for n >= 8, whereas M has degree 4 and positive coefficients. Hence Delta/M -> 0 as t -> infinity, and

    4D = lambda^2*M^2 - Delta^2.

## 2. Classification lemma for arbitrary integer representations

Let M,D be positive coprime integers and suppose M/D=1/u+1/v for positive integers u,v. Write g=gcd(u,v), u=g*r, v=g*s, gcd(r,s)=1. The equation becomes

    M*g*r*s = D*(r+s).

Since gcd(r*s,r+s)=1, we have r*s | D. Set k=D/(r*s) in Z_{>0}. Then

    M*g = k*(r+s).

Because k|D and gcd(M,D)=1, gcd(k,M)=1, so k|g. Put ell=g/k in Z_{>0}. Therefore EVERY positive integer representation is encoded by

    D=k*r*s,    r+s=ell*M,    gcd(r,s)=1,
    gcd(u,v)=g=k*ell.

The arithmetic-geometric mean inequality gives

    M*g = k*(r+s) >= 2*sqrt(k*D) >= 2*sqrt(D).

## 3. Effective minimal-gcd extremality

Let lambda >= 4, and suppose t is large enough that

    Delta(t)^2 < (2*lambda-1)*M(t)^2.               (E)

Then 4D/M^2 = lambda^2-(Delta/M)^2 > (lambda-1)^2, so 2sqrt(D)/M > lambda-1. By the classification lemma, every integer gcd g satisfies g > lambda-1, hence g>=lambda.

Moreover lambda >= 4 implies 2(lambda-1)^2 > lambda^2. Thus (E) also implies 8D > lambda^2*M^2. If g=lambda, then lambda*M = k(r+s)>=2sqrt(kD); k>=2 contradicts 8D>lambda^2*M^2. Therefore k=1, r*s=D, r+s=lambda*M. The unordered pair (r,s) is uniquely determined as the two roots of x^2-lambda*M*x+D, which are precisely F,G. Hence the ONLY possible representation with gcd exactly lambda is {lambda*F,lambda*G}.

A completely effective sufficient threshold is obtained from the positive coefficients of Delta. For t >= 1,

    Delta(t) <= Delta(1)*t^3,   M(t) >= A^2*t^4.

Put m=floor(sqrt(2*lambda-1)) and

    t0(n) = 1+floor(Delta(1)/(A^2*m)).

Then (E) holds for every integer t>=t0(n). Examples:

    n=8: t0=13;   n=9: t0=9; n=10: t0=8;
    n=11: t0=7;   n=12: t0=7; n=13: t0=6.

## 4. Exact positive density for minimal-gcd representations

Because D=F*G and gcd(D,M)=1,

    gcd(F,G) = gcd(F,F+G) = gcd(F,lambda*M) = gcd(F,lambda).

Consequently the known denominators have gcd

    gcd(lambda*F,lambda*G)=lambda*gcd(F,lambda).

The gcd is periodic as a function of t modulo lambda. Its minimal value lambda occurs exactly when gcd(F(t),lambda)=1.

For a prime p dividing lambda, the bad residues mod p are

    R_p = {-c^{-1} mod p : c in {B,alpha_1,alpha_2,alpha_3}, p does not divide c}.

Let r_p be the number of distinct residues in R_p. The Chinese Remainder Theorem gives the exact natural density

    delta_n = product_{p|lambda} (1-r_p/p) > 0.

The density is positive since residue t=0 mod p is always good.

For n=8,

    A=8190000, lambda=340362835312500,
    lambda = 2^2*3^4*5^7*7^2*11*13*19*101,
    (p,r_p) = (2,1),(3,1),(5,0),(7,1),(11,3),(13,1),(19,3),(101,3),
    delta_8 = 43008/274417 = 0.1567249842393146...

For n=9 the corresponding exact density is 4579328/14074193 (~32.54%). Along the explicit progression t=lambda*k, k>=1, gcd(F,G)=1 without any factoring or primality assumptions. Thus there are infinitely many, indeed a positive-density set of, t for which the canonical pair is the unique *gcd-minimal* representation.

## 5. Elliptic-curve obstruction to bounded-gcd extra representations

Continue with the classification D=k*r*s, r+s=ell*M, gcd(r,s)=1. The square of the difference is

    (r-s)^2 = ell^2*M^2 - 4D/k.

Using 4D=lambda^2*M^2-Delta^2, obtain

    k*(r-s)^2 = Delta^2 + c*M^2,
    c=k*ell^2-lambda^2 in Z.

If c=0, then k*ell^2=lambda^2; as k is an integer rational square, k=m^2 for some positive integer m and ell=lambda/m. Therefore the pair (r,s) must be (F/m,G/m) up to order, so (u,v)=(lambda*F,lambda*G). Hence every *noncanonical* representation has c != 0.

Set z=A*h=A*t*(A*t+1). Since (2At+1)^2=4z+1, Delta=(2At+1)(2+kappa*z), and M^2=h^4=z^4/A^4. The equation becomes

    k*(r-s)^2 = (4z+1)*(2+kappa*z)^2 + C*z^4,
    C=c/A^4 in Q\{0}.

Write kappa=p/q in lowest terms. Multiplying by k*q^2*A^4 gives the integral model

    Y^2 = k*A^4*(4z+1)*(2q+p*z)^2 + k*q^2*c*z^4,
    Y = k*q*A^2*(r-s) in Z,   z=A*h in Z.

Consider the quartic f_C(z)=(4z+1)*(2+kappa*z)^2+C*z^4. Its discriminant is

    disc_z(f_C) = -256*C*[ -64*C^2 + b(kappa)*C
                             + 4*kappa^3*(kappa-8)^3 ],
    b(kappa)=-kappa^4+16*kappa^3+224*kappa^2-2304*kappa+6912.

The discriminant of the quadratic bracket in C factors as

    (kappa-4)^2 * (kappa^2 - 8*kappa + 144)^3.

If kappa != 4 and Q(kappa):=kappa^2-8*kappa+144 is NOT a rational square, that quadratic has no rational roots. Therefore for every rational C !=0, f_C is squarefree and has degree 3 or 4. The smooth projective curve y^2=f_C(z) then has genus one.

Siegel's theorem states that for every fixed such nonsingular cubic/quartic over Q the equation y^2=f_C(z) has finitely many integral solutions, after clearing denominators (see Silverman, The Arithmetic of Elliptic Curves, 2nd ed., Chapter IX, Theorem 4.3). In our case, for any fixed bound B0, there are finitely many possible gcd values g<=B0, with k|g and ell=g/k. Each produces one fixed C and hence one fixed nonsingular genus-one curve. For each such curve there are finitely many integral z, and z=A*t*(At+1) strictly increases with t>=1. Hence there are only finitely many t admitting a noncanonical representation with gcd <= B0.

Thus, for each admissible n and every constant B0, all sufficiently large t have the property that every noncanonical representation (if any) has gcd >B0. In particular, taking B0=lambda^2, the known representation, whose gcd never exceeds lambda^2, eventually is the only representation with gcd <=lambda^2.

This is a genuine pointwise integer-fraction conclusion and is unconditional once the checkable nonsquare criterion holds. However, Siegel's finiteness theorem by itself does not provide an explicit threshold beyond which all noncanonical bounded-gcd representations disappear.

### Explicit n=8 certificate

For n=8,

    kappa = 642281/32760,
    Q(kappa) = 398739212881/1073217600.

The denominator is 32760^2; and

    631458^2 < 398739212881 < 631459^2.

Thus Q(kappa) is not a rational square. The elliptic bounded-gcd escape theorem holds for n=8.

### Infinitely many eligible n

For n>=8 congruent to 4 or 5 modulo 7, the rational expression kappa(n) has denominator nonzero mod 7. Exact polynomial reduction gives respectively

    kappa(n) mod 7 = 2 or 6.

In either case Q(kappa)=kappa^2-8kappa+144 is congruent to 6 mod 7. Since quadratic residues mod 7 are 0,1,2,4, Q(kappa) cannot be a rational square. Also kappa !=4. Hence the bounded-gcd escape theorem holds for EVERY n>=8 satisfying n mod 7 in {4,5}. These n form an infinite positive-density subset of the integer n parameters.

## 6. What is, and is not, proved

- New unconditional statement: positive-density gcd-minimal *unique* representations for each fixed n>=8, with effective parameter threshold.
- New unconditional statement: for n=8 and all n>=8 with n mod 7 in {4,5}, extra representations with bounded denominator gcd occur only for finitely many t (Siegel theorem).
- NOT proved: existence of infinitely many t with **exactly one representation among all integer pairs**. Extra pairs whose gcd grows with t are not excluded.
- NOT proved: an effective upper bound on the exceptional t in the Siegel part, new complexity-theoretic hardness, or worldwide priority. The original K3 and Mordell-Weil proofs have their own audit status.

## 7. Reproducibility and reference

Run:

    python verify_second_section_and_polynomial_rigidity.py
    python verify_minimal_gcd_and_siegel.py

The new verifier checks the normal-form identity over Q[n,t], the exact thresholds, gcd/density residue formulas and samples, the general quartic discriminant factorization, n=8 nonsquare arithmetic, and the n mod 7 infinite subclass. Siegel's theorem and the general gcd classification are mathematical arguments in this note; the script does not pretend to algorithmically prove Siegel's theorem.

Reference: Joseph H. Silverman, *The Arithmetic of Elliptic Curves*, 2nd edition, Springer, 2009, Chapter IX, Theorem 4.3 (Siegel's theorem for hyperelliptic equations with distinct roots):
https://www.math.ens.psl.eu/~obenoist/refs/Silverman.pdf

