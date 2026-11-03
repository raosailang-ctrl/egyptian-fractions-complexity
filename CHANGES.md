# Update contents

This update records the fixed odd-prime numerator work developed after the repository's 2026-11-03 00:29 UTC commit.

## Modified files

- README.md: adds links to the fixed-prime DP verifier and updates the project status summary.
- fixed-numerator.md: adds the primitive-root/discrete-log criterion, CRT decomposition, q=11/13/19 examples, and the q=11 correction.
- research-status.md: adds proved, computation-verified, withdrawn, and factorization-dependent status entries.
- research-log.md: records the derivation and examples.
- research-roadmap.md: adds next steps for the fixed-prime criterion.
- proof-audit.md: records the proof and scope caveats.

## New files

- fixed-prime-dp.py: exact finite-state DP and integer-arithmetic verifier.
- fixed-prime-examples.txt: captured output from the verifier.
- APPLY_UPDATE.md: overlay instructions.

## Important limitation

The DP assumes that the complete prime factorization of b is already known. It does not solve integer factorization and does not establish an unconditional polynomial-time algorithm for TWO-EGYPTIAN or resolve P vs NP.
