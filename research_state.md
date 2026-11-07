Current question:
For the central K3-derived Egyptian-fraction family, improve the understanding of ordinary two-unit-fraction representations beyond gcd-minimal uniqueness. In particular, exploit the exact divisor parametrization to bound the number of representations and study the congruence-restricted divisor count.

Completed:
- Resumed the mathematical branch; the Chrome synchronizer issue is paused and is not the active research task.
- Proved a general bijection for coprime positive integers M,D: unordered positive integer representations M/D=1/u+1/v correspond exactly to divisors d|D^2 with d<=D and d == -D (mod M), via d=Mu-D and D^2/d=Mv-D.
- Derived the exact count formula N(M,D)=#{d|D^2 : d<=D, d == -D (mod M)} and the upper bound N(M,D)<=tau(D^2).
- Applied Wigert's maximal-order theorem to the central family, where D(t) has degree 8 and leading coefficient 8230118400. Obtained log N(t) <= (16 log 2 + o(1)) log t/loglog t, hence N(t)=t^{o(1)}.
- Derived the cumulative bound T <= sum_{t<=T}N(t) <= T^{1+o(1)}.
- Identified the canonical representation in the divisor parametrization: d=G(t)^2 and its complementary divisor is F(t)^2.
- Combined the divisor bound with the earlier Siegel gcd-escape result: for a fixed nonsquare template, any noncanonical representations that continue to exist must have gcd tending to infinity, while their total number is subpower.
- Re-ran exact symbolic and finite enumeration checks for t=1,...,8; all passed.

Evidence:
- Research report commit: 1f2b48ba969d366cbb29b4370370b6e6393c31c7.
- Exact verifier commit: 8cd5db6b7867834445f41be761996879c3797eb7.
- Report: research-outputs/SUBPOLYNOMIAL_ORDINARY_DECOMPOSITION_BOUND_2026-11-07.md.
- Verifier: research-outputs/verify_divisor_parametrization.py.
- Container verifier output:
  SYMBOLIC_F_PLUS_G: PASS
  D == -1 (mod h), hence gcd(D,M)=1: PASS
  deg(M)=4, deg(D)=8, LC(D)=8230118400: PASS
  Exact counts for t=1,...,8: 85,5,1,1,1,1,2,1; all match complete divisor enumeration.
- Wigert reference: S. Wigert (1907); modern exposition/result in P. Pollack, Journal of the Ramanujan Mathematical Society 35 (2020), no. 4, 341-345.

Open problems:
- The subpower bound tau(D^2) is generic and likely crude; the key remaining arithmetic problem is to bound the restricted divisor count with d == -D (mod M) and d<=D.
- The Siegel gcd-escape theorem is ineffective; no explicit threshold T(B0) or quantitative lower bound for noncanonical gcd is known.
- Complete ordinary integer uniqueness remains unproved; high-gcd noncanonical representations have not been excluded.
- The explicit rational-point classification of the genus-two exceptional curve and the international literature-priority audit remain open.
- The Chrome attachment automation remains paused; no real sync has been performed.

Next step:
Study the special congruence-restricted divisor count
N(t)=#{d|D(t)^2 : d<=D(t), d == -D(t) mod M(t)}
for the central family. First analyze the eight linear factors of D(t), their pairwise gcd/resultants, and the residue classes modulo M(t); seek a bound stronger than Wigert's generic tau(D^2). Then test whether the method extends to other K3-derived families.

Artifacts:
- research-outputs/SUBPOLYNOMIAL_ORDINARY_DECOMPOSITION_BOUND_2026-11-07.md
- research-outputs/verify_divisor_parametrization.py
- Previous genus-two/gcd results in GENUS_TWO_EXCEPTIONAL_LOCUS_AND_GCD_MINIMALITY.md and related research notes.
