# Egyptian Fractions and Computational Complexity

Research archive on Egyptian-fraction representations and computational complexity, especially the decision problem of representing a rational number as the sum of two distinct unit fractions.

**Status:** exploratory mathematical research. The square-modulus reduction is a candidate Las Vegas randomized reduction and still requires a formal proof audit. The fixed-prime dynamic programs below are exact once the factorization of the denominator is supplied.

## Start here

- [Current status](research-status.md)
- [Core mathematics and signed reduction](mathematical-foundations.md)
- [Square-modulus randomized reduction](randomized-reduction.md)
- [Fixed numerator](fixed-numerator.md)
- [Minimum-term decision problem](minimum-term-decision.md)
- [Proof audit](proof-audit.md)
- [Research roadmap](research-roadmap.md)
- [Research log](research-log.md)
- [References](references.md)
- [Exact signed-reduction verifier](experiments_signed.py)
- [Fixed-prime numerator DP verifier](fixed-prime-dp.py)
- [Fixed-prime example output](fixed-prime-examples.txt)

## Evidence labels

- **PROVED:** a complete elementary derivation is recorded.
- **THEOREM-DEPENDENT:** depends on a cited published theorem; hypotheses and application require audit.
- **COMPUTATION-VERIFIED:** exact computation with reproducible code; this does not replace a general proof.
- **OPEN:** not established.
- **WITHDRAWN:** a previous claim was found to be incorrect and must not be reused.

Do not describe the current work as a standard deterministic NP-completeness proof or as a solution to P vs NP. The strongest current hardness route is a candidate Las Vegas randomized expected-polynomial-time reduction from SUBSET SUM to TWO-EGYPTIAN.

The fixed-prime DP result is a separate structural result: for a fixed odd prime numerator q, it gives an O_q(log b)-time finite-state computation **when the prime factorization of b is already supplied**. It does not provide a polynomial-time factorization algorithm.
