Current question:
For the central K3-derived Egyptian-fraction family, improve the understanding of ordinary two-unit-fraction representations by exploiting the exact divisor parametrization and the congruence-restricted divisor count.

Completed:
- Paused the Chrome attachment-automation branch; resumed the mathematical research branch.
- Proved a general bijection for coprime positive integers M,D: unordered positive integer representations M/D=1/u+1/v correspond exactly to divisors d|D^2 with d<=D and d == -D (mod M), via d=Mu-D and D^2/d=Mv-D.
- Derived N(M,D)=#{d|D^2 : d<=D, d == -D (mod M)} and N(M,D)<=tau(D^2).
- Applied Wigert's maximal-order theorem to the central family, where D(t) has degree 8 and leading coefficient 8230118400. Obtained log N(t)<=(16 log 2+o(1))log t/loglog t, hence N(t)=t^{o(1)}.
- Derived the cumulative bound T<=sum_{t<=T}N(t)<=T^{1+o(1)}.
- Identified the canonical representation in the divisor parametrization: d=G(t)^2 and complementary divisor F(t)^2.
- Combined the divisor bound with the earlier Siegel gcd-escape theorem: for a fixed nonsquare template, if noncanonical representations persist, their minimum gcd tends to infinity, while their total count per input is subpower.
- Computed all 28 pairwise resultants of the eight linear factors of D(t). Their prime support is exactly {2,3,5,7,11,19,23}; therefore a prime outside this set cannot divide two distinct factors.
- Proved each linear factor L_i(t) is coprime to h(t)=t(12t+1), since L_i divides D and D == -1 (mod h).
- Re-ran exact symbolic and finite divisor enumeration for t=1,...,8; all passed.

Evidence:
- Main report commit: 1f2b48ba969d366cbb29b4370370b6e6393c31c7.
- Exact divisor verifier commit: 8cd5db6b7867834445f41be761996879c3797eb7.
- Pairwise resultant note: research-outputs/PAIRWISE_FACTOR_RESULTANTS_2026-11-07.md (commit f8b5ba938e933bb8b56827a23bc440b1e24ec91c).
- Resultant verifier: research-outputs/verify_pairwise_factor_resultants.py (commit 36135567aa93f46a5cc8a37eae378dc64d2025e1).
- Local research package: /mnt/data/k3_divisor_bound_20261107/K3_SUBPOLYNOMIAL_DECOMPOSITION_BOUND_2026-11-07.zip.
- Exact verifier output: SYMBOLIC_F_PLUS_G PASS; D == -1 mod h PASS; degree/leading coefficient PASS; all 28 resultants PASS; overlap-prime support [2,3,5,7,11,19,23]; exact t=1,...,8 counts [85,5,1,1,1,1,2,1] PASS.
- Wigert reference: S. Wigert (1907); P. Pollack, Journal of the Ramanujan Mathematical Society 35 (2020), no. 4, 341-345.

Open problems:
- The generic bound tau(D^2) is crude. The main target is a stronger estimate for N(t)=#{d|D(t)^2 : d<=D(t), d == -D(t) mod M(t)}.
- The eight factor prime supports overlap only at seven fixed primes, but this has not yet been converted into a sharper count.
- Siegel gcd escape remains ineffective; no explicit threshold T(B0) or quantitative lower bound for noncanonical gcd is known.
- Complete ordinary integer uniqueness remains unproved; high-gcd noncanonical representations have not been excluded.
- Explicit rational-point classification of the genus-two exceptional curve and international literature-priority audit remain open.
- Chrome attachment automation remains paused; no real sync has been performed.

Next step:
Exploit the pairwise-resultant decomposition of D(t). Separate the seven overlap primes {2,3,5,7,11,19,23} from the eight pairwise-disjoint prime supports. For each divisor d|D^2, encode its prime-exponent choices by factor L_i(t), then study the multiplicative residue condition d == -D (mod h^2). Start with exact finite t experiments and local multiplicative-order bounds; seek a genuine improvement over Wigert's generic tau(D^2) estimate, without assuming random distribution of divisors.

Artifacts:
- research-outputs/SUBPOLYNOMIAL_ORDINARY_DECOMPOSITION_BOUND_2026-11-07.md
- research-outputs/verify_divisor_parametrization.py
- research-outputs/PAIRWISE_FACTOR_RESULTANTS_2026-11-07.md
- research-outputs/verify_pairwise_factor_resultants.py
- Previous genus-two/gcd results in GENUS_TWO_EXCEPTIONAL_LOCUS_AND_GCD_MINIMALITY.md and related research notes.
