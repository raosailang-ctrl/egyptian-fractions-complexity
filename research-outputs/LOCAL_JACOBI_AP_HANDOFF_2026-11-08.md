# Research handoff — Local Jacobi full-rank arithmetic progressions

## Current question
Combine selected Jacobi conditions with the global square-root/divisibility constraints to further constrain noncanonical representations.

## New theorem
For every fixed s>=1, choose distinct odd primes p_1,...,p_s. For each j, use CRT to choose a unit residue class a_j modulo P=product p_i with Legendre vector equal to the j-th standard basis vector. By Dirichlet's theorem, choose a prime ell_j in each class, avoiding the finite pairwise-resultant prime support {2,3,5,7,11,19,23} and all p_i.

Impose t=0 mod p_i, t=1 mod 2, and t=-3^{-1}+ell_j mod ell_j^2. CRT gives a positive-density arithmetic progression. In it, p_i|h and v_ell_j(D)=1, and the selected Legendre-character matrix is I_s. Exactly tau(D)/2^s divisors q|D pass the s selected local conditions.

Because t is odd on these progressions, h and M=h^2 are odd. For each p^a||h, a unit is a square modulo p^(2a) iff its Legendre symbol modulo p is +1; Hensel lifting gives exactly two roots when it is a square. Thus the number of roots modulo M is at most 2^omega(h). Combining with r<=630M gives the sharper AP bound:
N(t) <= 630 tau(D(t)) 2^(omega(h(t))-s).

Choosing an increasing t_s from the progression for each s gives t_s->infinity and a relative sieve saving at least 2^-s -> 0. This does not prove uniqueness or a positive-density statement for the union of the progressions.

## Finite rank survey
For odd t=1,...,10000, exact factorization and F2 elimination show full row rank for 4835/5000 (96.7%); 165 cases are deficient; maximum deficiency is 2. Rank-deficiency-two parameters: 609,1105,1285,1457,5957,6215,6657. This is finite evidence only.

Selected exact q-divisor checks (13 values) verify the rank-r upper bound tau(D)/2^r; t=7 and t=69 attain tau(D)/8.

## Important local observation
For odd p, if a unit is a quadratic residue mod p, Hensel's lemma lifts its square root to every p^n. Thus checking p^2 after a successful Legendre test adds no new obstruction. The next useful filter must involve the global requirement that a root r of r^2 == -D/q (mod M) also divide D/q, with gcd(r,(D/q)/r)=1 and r+s=kM.

## Artifacts
- research-outputs/LOCAL_JACOBI_AP_THEOREM_AND_RANK_SURVEY_2026-11-08.md
- research-outputs/verify_arithmetic_progression_jacobi_sieve.py
- research-outputs/survey_jacobi_rank.py
- research-outputs/verify_selected_q_sieve_counts.py
- jacobi_rank_odd_t_10000.jsonl
- rank_survey_summary.log
- ap_certificates.log
- selected_q_sieve_counts.log

## Next step
For each q passing the selected Jacobi rows, enumerate or characterize roots modulo M and test which root classes contain divisors r|D/q with gcd(r,(D/q)/r)=1. Build an exact local-global sieve and protect the known noncanonical examples t=7 and t=69. Do not claim full uniqueness or natural-density rank results.
