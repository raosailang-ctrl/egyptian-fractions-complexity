[object Object]

Multiplicative subgroup membership computation (2026-11-09):
- Computed H=<ell_i> mod M for t=3,7,17,69,137,185 using CRT decomposition of the unit group into cyclic groups modulo p^(2a)||M.
- For each component, chose a primitive root, computed discrete logs of every ell_i and target -D, and tested integer lattice membership in B=[V|-diag(phi(p^(2a)))].
- Exact criterion: for full-row-rank B, target b belongs to its column lattice iff gcd of all maximal minors of B equals gcd of all maximal minors of [B|b]. This is an exact determinantal-divisor/Smith-normal-form criterion.
- Results: t=3 gcd 1=1; t=7 1=1; t=17 2=2; t=69 1=1; t=137 2=2; t=185 2=2. Thus -1 in H for all six parameters.
- This falsifies usefulness of the simple subgroup obstruction on these six samples: it is necessary but too weak to distinguish represented from unrepresented Jacobi-compatible fixed roots. It does not imply bounded exponent or Jacobi-compatible solution exists.
- New verifier: research-outputs/multiplicative_subgroup_membership.py (commit 0477a54e3b9af1aa19f24c5e2d3c3cfe40f8938c).
- New report: research-outputs/MULTIPLICATIVE_SUBGROUP_MEMBERSHIP_2026-11-09.md (commit 859c0cd70d9497df8289610839a298e01ac23f2f).
- Next step: solve the full mixed-modulus bounded system A k=0 mod2, V k=b mod cyclic orders, 0<=k_i<=2a_i for t=69 and 137. Separate unrestricted integer lattice solvability (already true at subgroup level) from bounded-box feasibility and syndrome restrictions. Seek certificates of infeasibility for the Jacobi-compatible fixed roots absent from actual support.
