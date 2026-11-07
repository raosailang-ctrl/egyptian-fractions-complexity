# Ordinary two-unit-fraction representations: divisor parametrization and subpower bound

Date: 2026-11-07
Status: exact new parametrization; asymptotic upper bound from Wigert's classical maximal-order theorem. This does not prove absolute uniqueness.

## 1. Exact divisor parametrization

Let M,D be coprime positive integers and suppose
M/D = 1/u + 1/v with positive integers u,v. Order u<=v and set
d=Mu-D, e=Mv-D. From Muv=D(u+v),
de=(Mu-D)(Mv-D)=D^2.
Also 0<d<=D and d == -D (mod M).

Conversely, if d|D^2, d<=D, and d == -D (mod M), set e=D^2/d.
Since gcd(D,M)=1, e == -D (mod M). Then
u=(D+d)/M, v=(D+e)/M
are positive integers and directly satisfy M/D=1/u+1/v.

Thus unordered positive integer representations are in bijection with
{d | D^2 : d<=D, d == -D (mod M)}. In particular,
N(M,D) <= tau(D^2).

## 2. Position of the canonical solution

For the central K3-derived family:
h=t(12t+1), M=h^2,
F=(1+3t)(1+14t)(1+60t)(1+36t),
G=(4t-1)(1+84t)(1+15t)(1+18t),
D=FG, and F+G=1260M.

Also D == -1 (mod h), hence gcd(M,D)=1. For t>=1, F>G.
The known pair {1260F,1260G} corresponds exactly to d=G^2 and its
complementary divisor D^2/d=F^2.

## 3. Subpower bound on the number of ordinary representations

D(t) has degree 8 and leading coefficient 8230118400, so
log(D(t)^2)=16 log t+O(1).
Wigert's maximal-order theorem gives
log tau(n) <= (log 2 + o(1)) log n / log log n.
Consequently
log N(t) <= (16 log 2 + o(1)) log t / log log t,
or
N(t) <= exp((16 log 2+o(1)) log t/log log t) = t^{o(1)}.

For S(T)=sum_{t<=T}N(t), each t has at least its canonical representation,
so T<=S(T). The pointwise bound gives S(T)<=T^{1+o(1)}. Hence
T <= S(T) <= T^{1+o(1)}.

## 4. Combination with the existing Siegel gcd-escape result

For a fixed non-square resonance template, the earlier genus-one/Siegel
argument proves that for every fixed B0, only finitely many t admit a
noncanonical representation with gcd(u,v)<=B0. Thus, if g*(t) is the
minimum gcd among noncanonical representations (and +infinity if none),
g*(t)->+infinity.

Together, these statements say:
- each input has at most t^{o(1)} ordinary representations;
- every fixed gcd bound eventually excludes all noncanonical solutions;
- any remaining noncanonical solutions must have gcd tending to infinity.

This does NOT exclude high-gcd noncanonical representations and does NOT
prove complete integer uniqueness.

## 5. Exact finite checks

The accompanying verifier checks F+G=1260M, D == -1 mod h, the degree and
leading coefficient of D, and exhaustively enumerates all divisor candidates
for t=1,...,8. Results:

t | N(t) | tau(D(t)^2)
1 | 85 | 26325
2 | 5 | 10125
3 | 1 | 23625
4 | 1 | 54675
5 | 1 | 78975
6 | 1 | 127575
7 | 2 | 280665
8 | 1 | 127575

The finite census is not an asymptotic proof. The Wigert bound is a general
divisor-function theorem, not a new result specific to this family.

## 6. Next mathematical question

Improve the generic bound tau(D^2) by exploiting the congruence:
N(t)=#{d|D(t)^2 : d<=D(t), d == -D(t) mod M(t)}.
The eight linear factors of D(t) and M(t)=t^2(12t+1)^2 may impose
additional structure on this restricted divisor count.

References:
- S. Wigert, Arkiv för Matematik, Astronomi och Fysik 3 (1907), no. 18, 1-9.
- P. Pollack, "The maximal size of the k-fold divisor function for very large k,"
  Journal of the Ramanujan Mathematical Society 35 (2020), no. 4, 341-345.
- Existing project note: GENUS_TWO_EXCEPTIONAL_LOCUS_AND_GCD_MINIMALITY.md.
