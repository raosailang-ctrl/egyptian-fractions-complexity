# Research roadmap

## Priority 1 - Complete the square-modulus Las Vegas reduction audit

1. Transcribe Baier-Zhao Theorem 4 exactly and verify its hypotheses at Y and Y/2.
2. Check the good-modulus count from the weighted average error sum.
3. Give an explicit bound for proper prime powers in (Y/2,Y].
4. Specify unbiased sampling from the arithmetic progression inside the interval.
5. Prove the prime-search success probability and union bound.
6. Formalize the finite-trial exact fallback and expected runtime.
7. Implement a small exact verifier for the algebraic map, independent of prime generation.

## Priority 2 - Fixed numerator classification

1. Compare the DP observation with Chen-Koo (2013) and older work on two-term Egyptian fractions.
2. Determine whether fixed-a languages have known classifications beyond a=3,4,6.
3. Clarify the relationship to integer factorization; do not infer equivalence without a reduction.
4. Explore whether the DP can be improved without factoring b.

## Priority 3 - Standard deterministic NP-hardness

1. Seek a deterministic construction of primes in the required residue classes.
2. Explore a composite-factor construction that preserves exponents {0,1,2}.
3. Study the finite-group three-valued product problem separately.
4. Do not claim standard NP-hardness until a deterministic Karp reduction is explicit.

## Priority 4 - Shortest Egyptian fraction problem

The minimum-term problem is distinct from TWO-EGYPTIAN. A short-expansion upper bound may help prove certificate-length bounds for the general minimum-term decision problem, but NP-hardness does not follow from the restricted-denominator subset-sum problem.

## Immediate next experiment

Implement a script that takes a small SUBSET SUM instance; constructs B,L,W,S; checks the equivalence with the bounded-exponent equation by exhaustive enumeration; for a chosen odd h>2W computes M=h^2 and omega=1+h; searches for small prime representatives in each required class; verifies primality, pairwise distinctness, gcd(M,D)=1, and D==-omega^S modulo M; and enumerates all 3^(2n+1) exponent vectors for tiny instances.

All outputs should use exact integer arithmetic. Commit the script and logs together.
