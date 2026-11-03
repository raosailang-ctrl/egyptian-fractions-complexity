# Current research status

Last consolidated: 2026-11-03.

## Main decision problem

**TWO-EGYPTIAN:** Given reduced integers 0 < a < b, decide whether there are distinct positive integers u,v such that a/b = 1/u + 1/v.

## Results ledger

| Item | Status | Notes |
|---|---|---|
| Factor criterion | **PROVED** | Equivalent to r|b^2, r!=b, r==-b (mod a). |
| Coprime-divisor-pair criterion | **PROVED / LITERATURE** | Equivalent to d1,d2|b, gcd(d1,d2)=1, a|(d1+d2); Chen-Koo (2013), Theorem 4. |
| TWO-EGYPTIAN belongs to NP | **PROVED** | A divisor r or coprime divisor pair is a polynomial-bit certificate. |
| Signed SUBSET SUM encoding | **PROVED** | Weights B^i and B^i+a_i, B=8(A+1), C=L+T. |
| Odd-square cyclic subgroup | **PROVED** | For odd h>1, omega=1+h has order h modulo h^2 and -1 is outside its subgroup. |
| Algebraic reduction given prime representatives | **PROVED** | Directly via the coprime-divisor-pair criterion. |
| Square-modulus average prime distribution input | **THEOREM-DEPENDENT** | Baier-Zhao (2006), Theorem 4. Exact application recorded in randomized-reduction.md. |
| Las Vegas randomized reduction | **CANDIDATE / NEAR-COMPLETE AUDIT** | Expected-polynomial-time, zero-error construction with finite exact fallback; requires formal machine-level audit. |
| Fixed odd-prime numerator criterion | **PROVED** | For q odd prime, discrete logs to a primitive root reduce the factor criterion to a target sum modulo q-1. |
| Fixed-prime finite-state DP | **PROVED, GIVEN FACTORIZATION** | q-1 states; O_q(log b) transitions once the prime factorization of b is supplied. |
| q=11,13,19 CRT instances | **COMPUTATION-VERIFIED** | Ten-, twelve-, and eighteen-state examples; exact witnesses and expansions are recorded. |
| Earlier parity-only q=11 classification | **WITHDRAWN** | It loses the mod-5 component; retain the full congruence modulo 10. |
| Standard deterministic NP-hardness | **OPEN** | No deterministic polynomial many-one reduction established. |
| Fixed numerator T_a in NP intersect coNP | **PROVED, subject to certificate model** | YES divisor certificate; NO full factorization plus finite-group DP. |
| MIN-EGYPT belongs to NP | **THEOREM-DEPENDENT** | Follows from O(log log b) short-expansion theorem plus a denominator-bit bound; see minimum-term-decision.md. |
| Standard NP-completeness of MIN-EGYPT | **OPEN** | Only Las Vegas randomized NP-hardness route currently available. |
| P vs NP | **OPEN** | No result resolving it. |
| Reproducible signed-reduction experiments | **VERIFIED SMALL INSTANCES** | experiments_signed.py uses exact integer arithmetic and trial-division primality tests; it does not test asymptotic prime distribution. |
| Reproducible fixed-prime DP examples | **VERIFIED SMALL INSTANCES** | fixed-prime-dp.py checks the DP witness against the divisor criterion and exact fraction identity for q=11,13,19. |

## Complexity interpretation

If the Las Vegas reduction is fully validated and TWO-EGYPTIAN has a deterministic polynomial-time algorithm, then SUBSET SUM is in ZPP. Since SUBSET SUM is NP-complete and ZPP is contained in NP intersect coNP, this implies NP=coNP. It does **not** directly imply P=NP.

A Las Vegas randomized reduction is not a standard deterministic Karp reduction. Do not label TWO-EGYPTIAN standard NP-complete without a deterministic polynomial-time reduction.

## Corrections and cautions

1. The square-modulus construction removes the need for a prime modulus and finite-field root, but still needs primes in prescribed residue classes.
2. Baier-Zhao Theorem 4 is an average theorem, not a pointwise theorem for every modulus.
3. Its constants are ineffective. A finite-trial plus exact fallback is proposed; the expected-time argument needs a formal machine-level audit.
4. Earlier large numerical examples from chat are not accepted as verified until scripts and certificates are committed.
5. Restricted-denominator Egyptian subset sum being NP-complete does not by itself prove hardness of unrestricted shortest Egyptian fractions.
6. The fixed-prime DP does not remove the cost of factoring b; its stated O_q(log b) bound is conditional on a supplied factorization.
7. For q=11, do not use the withdrawn parity-only classification; the full modulus-10 target condition is required.
