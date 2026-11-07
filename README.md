# K3 Egyptian fractions — genus-two exceptional locus, 2026-11-07

Main new research note: `GENUS_TWO_EXCEPTIONAL_LOCUS_AND_GCD_MINIMALITY.md`.

Reproducible exact computer checks: `verify_genus_two_and_mod53.py` (Python 3.10+ and SymPy).

Run from this folder:

    python verify_genus_two_and_mod53.py

Saved output: `verification-report.txt`.

Previous references are in `reference/`, including the already established Haar arc and gcd classification. `HANDOFF_20261107.md` summarizes the new result and the next tasks.

Scope: Mathematical proof of a genus-two obstruction and consequences using the standard Faltings and Siegel theorems. The verifier checks algebraic formulas and local congruences; it does not algorithmically certify Faltings or establish literature priority. Absolute uniqueness of ordinary Egyptian decompositions remains unproved.

Small-instance exhaustive integer counts: `python verify_small_t_decomposition_counts.py`; output in `small-t-count-report.txt` (t=1..8: 85, 5, 1, 1, 1, 1, 2, 1 unordered representations).
