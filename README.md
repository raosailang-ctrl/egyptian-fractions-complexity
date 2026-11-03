# Egyptian Fractions and Computational Complexity

Research archive on Egyptian-fraction representations, especially the decision problem of representing a rational number as the sum of two distinct unit fractions.

**Status:** exploratory research notes; the randomized reduction still requires a formal proof audit.

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
- [Exact small-instance verifier](experiments_signed.py)

## Evidence labels

- **PROVED:** complete elementary derivation is recorded.
- **THEOREM-DEPENDENT:** depends on a cited published theorem; hypotheses and application require audit.
- **COMPUTATION-VERIFIED:** exact computation with reproducible code; does not replace a general proof.
- **OPEN:** not established.

Do not describe the current work as a standard deterministic NP-completeness proof or a solution to P vs NP. The strongest current target is a Las Vegas randomized expected-polynomial-time reduction from SUBSET SUM to TWO-EGYPTIAN.
