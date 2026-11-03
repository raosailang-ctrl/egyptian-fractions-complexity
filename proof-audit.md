# Proof audit and corrections

## A. Algebraic core

The following are elementary and can be treated as proved once the displayed derivations are checked:
- two-term factor criterion;
- ternary-exponent positional encoding;
- order of 1+h modulo h^2;
- reduction from the group-product condition to the factor criterion.

## B. Analytic number theory

Baier-Zhao Theorem 4 (Acta Arith. 125.2, 2006) is an average estimate for square moduli. The sum is over base moduli q, with square moduli q^2 and a weight q. It is not pointwise for every modulus. The paper notes ineffectivity due to Siegel-Walfisz.

The proposed application uses two fixed endpoints Y and Y/2. Do not silently replace the theorem by a version with a maximum over all endpoints unless separately justified.

## C. Randomized prime search

The argument that each good modulus has many primes in every reduced residue class must:
1. subtract the total contribution of proper prime powers from the von Mangoldt sum;
2. convert the remaining weighted prime sum into a count by dividing by log Y;
3. bound the number of candidate integers in a residue class;
4. state the sampling distribution exactly.

The argument appears plausible with Y=(4X)^6, X=4W, and h in (X,2X), but should be independently checked line by line.

## D. Ineffective constants and fallback

The finite-trial plus exhaustive fallback is designed to handle the unknown threshold in the average theorem. A formal proof must specify the exact random machine, caps on searches and rounds, exhaustive fallback, asymptotic expected-time bound for large inputs, and why inputs below the unknown threshold form a finite family with bounded n.

Do not claim a deterministic polynomial-time reduction.

## E. Numerical experiments

Earlier conversational messages contained large numerical examples without committed source code or independent primality certificates. These are not verified and are intentionally not recorded as established facts.

Only reproducible experiments with exact scripts and certificates should be added.

## F. Complexity language

Use “Las Vegas randomized reduction” if expected-time and zero-error arguments are complete; use “candidate reduction” while audit remains open.

Do not say standard NP-complete unless a deterministic polynomial many-one reduction is proved. Do not say P=NP is solved. Do not infer unrestricted shortest Egyptian fraction hardness from the restricted-denominator subset-sum problem.
