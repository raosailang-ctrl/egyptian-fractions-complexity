# Research roadmap

## Priority 1 — Finish the Las Vegas reduction audit
1. Verify Baier-Zhao Theorem 4 hypotheses and endpoint ranges at Y and Y/2.
2. Formalize the bad-modulus count from the weighted average error sum.
3. Give an explicit proper-prime-power bound.
4. Specify exact uniform sampling from each arithmetic progression.
5. Formalize the finite-round exhaustive fallback as an expected-time machine.
6. Reproduce and extend experiments_signed.py with exact certificates.

## Priority 2 — Develop the fixed-prime criterion
1. Compare the general primitive-root/discrete-log criterion with the existing literature, including Chen-Koo.
2. Independently verify the q=11,13,19 examples and the CRT state encodings.
3. Test the DP on more small factorizations and additional fixed odd primes.
4. Keep the q=11 parity-only classification withdrawn; any simplification must preserve the full modulus-10 condition.
5. Investigate whether useful criteria can be obtained without first factoring b.

## Priority 3 — Improve the number-theoretic construction
1. Seek a deterministic construction of primes in the required square-modulus residue classes.
2. Investigate whether the coprime-divisor-pair formulation permits a construction avoiding prime search.
3. Study the finite-group signed subset-product problem separately.

## Priority 4 — General minimum-term decision
1. Use the short Egyptian fraction theorem and the residual denominator bound to establish NP membership carefully.
2. Distinguish this from NP-hardness; the current reduction only gives randomized hardness at threshold k=2.
3. Search for a deterministic reduction if standard NP-completeness is the goal.
