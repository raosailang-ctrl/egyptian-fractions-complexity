[object Object]

Latest multiplicative subgroup obstruction (2026-11-09):
- Define H=<ell_1,...,ell_n> inside G=(Z/MZ)^×. Since D=product ell_i^a_i belongs to H, the target -D belongs to H iff -1 belongs to H.
- Every realizable residue product product ell_i^k_i lies in H. Therefore -1 not in H implies N(t)=0. This is a necessary condition only, not sufficient.
- Choose invariant factor decomposition H ≅ direct sum_j Z/d_j. Let v_i be the coordinate vector of ell_i and b the coordinate vector of -D. The multiplicative target condition is exactly sum_i k_i v_i = b modulo the d_j. Combined with Jacobi, the exact problem becomes bounded mixed-modulus linear system: A k=0 mod2, V k=b mod (d_j), 0<=k_i<=2a_i.
- Orientation reflection k_i -> 2a_i-k_i preserves the target -D and pairs all target solutions; the center k_i=a_i maps to D, not -D, so no target solution is fixed. Hence target solution count is even.
- New report: research-outputs/MULTIPLICATIVE_SUBGROUP_OBSTRUCTION_2026-11-09.md (commit 4744739ebb7f0d0df4e04262529afecc246cfd30).
- No sample subgroup invariant factors or membership certificates have yet been computed.

Next step:
Compute H=<ell_i> and test -1 membership for t=3,7,17,69,137,185. Prefer an exact constructive method: express subgroup generators in the finite abelian unit group modulo M, derive invariant factors / Smith normal form, and produce a certificate for membership or nonmembership. Then compare subgroup membership with bounded-system feasibility; do not assume -1 in H is sufficient.
