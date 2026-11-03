# Current research status

Last consolidated: 2026-11-02.

## Main decision problem

**TWO-EGYPTIAN:** Given reduced integers 0 < a < b, decide whether there are distinct positive integers u,v such that

    a/b = 1/u + 1/v.

## Results ledger

| Item | Status | Notes |
|---|---|---|
| Two-term factor criterion | PROVED | Equivalent to a divisor r of b^2 with r != b and r == -b (mod a). |
| TWO-EGYPTIAN is in NP | PROVED | r <= b^2 is a polynomial-bit certificate. |
| Ternary-exponent SUBSET SUM encoding | PROVED | Positional-weight construction with B=8(A+1). |
| Odd-square cyclic subgroup | PROVED | For odd h>1, M=h^2 and omega=1+h has order h modulo M; -1 is not in its subgroup. |
| Algebraic reduction, conditional on prime representatives | PROVED | Requires distinct primes in prescribed residue classes. |
| Square-modulus average prime distribution input | THEOREM-DEPENDENT | Baier-Zhao (2006), Theorem 4; exact hypotheses and endpoint use need audit. |
| Las Vegas randomized reduction | CANDIDATE / AUDIT REQUIRED | Plausible expected-polynomial-time construction; not independently reviewed. |
| Standard deterministic NP-hardness | OPEN | No deterministic polynomial many-one reduction established. |
| P vs NP | OPEN | No result resolving it. |
| Fixed numerator language T_a in NP intersect coNP | PROVED, subject to stated certificate model | YES certificate is r; NO certificate is a complete factorization of b plus finite-group DP. |
| Reproducible numerical experiments | OPEN | Previous chat examples lack committed scripts and independent primality certificates. |

## Complexity interpretation

If the Las Vegas reduction is fully validated and TWO-EGYPTIAN has a deterministic polynomial-time algorithm, then SUBSET SUM is in ZPP. Since SUBSET SUM is NP-complete and ZPP is contained in NP intersect coNP, this implies NP = coNP.

It does **not** directly imply P = NP.

A Las Vegas randomized reduction is not the same as a standard deterministic Karp reduction. Do not label TWO-EGYPTIAN standard NP-complete without a deterministic polynomial-time reduction.

## Corrections to earlier discussion

1. The square-modulus construction removes the need for a prime modulus and finite-field root. It does not remove the need to find prime factors in prescribed residue classes.
2. Baier-Zhao is an average theorem for square moduli, not a pointwise theorem for every modulus.
3. Its implied constants are ineffective due to Siegel-Walfisz input. A finite-trial plus exhaustive fallback was proposed, but its expected-time proof needs a formal machine-level audit.
4. Earlier numerical examples in chat are not accepted as verified until scripts and primality certificates are committed.
5. The restricted-denominator Egyptian subset-sum problem being NP-complete does not by itself prove hardness of the unrestricted minimum-term problem.
