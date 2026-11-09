Current question:
Can the local-global search for the central K3 Egyptian-fraction family be made substantially more efficient by matching half-products modulo M, while retaining exactness and all known noncanonical representations?

Completed:
- Proved an arbitrary-fixed-rank arithmetic-progression theorem: for every s>=1, there is a positive-density AP t ≡ t_s (mod Q_s) such that h(t) contains s chosen odd primes p_i, D(t) contains s chosen primes ell_j with valuation exactly one, and the Legendre-character matrix is I_s.
- The CRT/Dirichlet construction avoids pairwise-resultant prime support {2,3,5,7,11,19,23}; it imposes t=0 mod p_i, t=1 mod 2, and t ≡ -3^{-1}+ell_j mod ell_j^2. Exactly tau(D)/2^s divisors q|D pass the selected s Jacobi conditions.
- Hensel refinement: for odd t, each unit square-root congruence modulo p^(2a), p^a||h, has either zero or exactly two roots. Thus at most 2^omega(h) roots modulo M=h^2. On the constructed APs, N(t) <= 630 tau(D(t)) 2^(omega(h(t))-s).
- Explicit CRT certificates for s=1,...,5 verified.
- Finite F2 rank survey for odd t<=10000: full row rank 4835/5000 (96.7%), 165 deficient, maximum deficiency 2. This is finite evidence only.
- Exact local-global sieve: for q|D passing all necessary Jacobi conditions, enumerate unitary splits R=D/q=rs with gcd(r,s)=1 and test r^2+R == 0 mod M. Since gcd(r,M)=1, this is equivalent to r+s == 0 mod M. On 13 selected parameters this reproduces 2 representations at t=7 and t=69, and one at each of the other 11 values.
- New adaptive MITM algorithm: split the distinct prime-power blocks of R into two halves, hash right-half subset products modulo M, and match left-half products against the roots z of z^2 == -R (mod M) via Y == z*X^{-1} (mod M). Roots are constructed prime-power-wise and combined by CRT.
- Adaptive strategy estimates brute cost 2^(m-1) against MITM cost 2^ceil(m/2)+(1+rho)2^floor(m/2), where m=omega(R) and rho<=2^omega(h). It chooses the lower estimated method per q.
- On all 13 selected parameters, the adaptive solver reproduced the prior exact representation counts and all known (q,r,s) outputs. For t=7, every MITM-selected q was cross-checked against direct enumeration; audit passed.
- Across the 13 cases, the rough work counter was 3,198,033 for the adaptive hybrid versus 4,536,321 direct split checks, a reduction of about 29.5%. For t=69 alone: 2,595,895 hybrid work units versus 3,925,863 direct checks, about 33.9% lower. These are operation proxies, not wall-clock speedup guarantees; actual runtime includes root construction and hash overhead.
- The noncanonical solutions remain protected: t=7 has (324,11893677,12888073) and (16814886,81,36464494); t=69 has (19600,14663540485,14784049124) and (3470764,430908401,2841046000).

Evidence:
- Arbitrary-rank AP theorem and rank survey: research-outputs/LOCAL_JACOBI_AP_THEOREM_AND_RANK_SURVEY_2026-11-08.md
- AP verifier: research-outputs/verify_arithmetic_progression_jacobi_sieve.py
- Rank survey: research-outputs/survey_jacobi_rank.py
- Exact local-global report and verifier: research-outputs/LOCAL_GLOBAL_SIEVE_13_PARAMETERS_2026-11-08.md; research-outputs/verify_local_global_sieve.py
- New adaptive MITM report: research-outputs/ADAPTIVE_MITM_LOCAL_GLOBAL_SIEVE_2026-11-09.md
- New adaptive MITM verifier: research-outputs/adaptive_mitm_local_global_sieve.py
- MITM t=7 direct regression audit: PASS.
- All 13 adaptive solver runs: ADAPTIVE_LOCAL_GLOBAL_EXACT_CHECKS: PASS.
- Previous arbitrary-rank theorem's Dirichlet source: MIT 18.785, Number Theory I, Lecture 18, Theorem 18.1: https://math.mit.edu/classes/18.785/2021fa/LectureNotes18.pdf.
- Latest research-state commit before this update: db63539c1ada51768e3a8cced082d3b28d870162.

Open problems:
- This is still an exact exponential search; no polynomial-time algorithm or P/NP conclusion follows.
- Per-q root construction currently recomputes square roots modulo p^(2a) and CRT for every q. Incremental root updates may remove a significant overhead.
- Equal split by number of prime-power blocks is not necessarily optimal; balance by block bit-length and residue collisions may improve memory/time.
- The 29.5% figure is a proxy-work reduction on 13 selected parameters, not a general asymptotic theorem or wall-clock guarantee.
- Local Jacobi conditions remain necessary, not sufficient; ordinary integer decomposition uniqueness remains unproved. t=7 and t=69 are explicit nonunique cases.
- The arbitrary-rank AP theorem gives fixed s and an infinite sequence with relative local saving tending to zero, but no quantitative s-versus-t relation or positive-density growing-rank set.
- The 96.7% rank survey is only for odd t<=10000 and proves no asymptotic density.
- Siegel gcd-escape, genus-two rational point classification, and literature-priority audit remain open.

Next step:
Derive and exploit common square-class root transport across all q passing the Jacobi filter. Proved: if q,q' both satisfy (q/p)=(q'/p)=1 for every p|h, then q/q' is a square modulo M=h^2; multiplication by a square root of q/q' bijects the roots of x^2=-D/q with those of x^2=-D/q'. Use q'=1 as a common anchor: compute roots of -D once, then for each passing q compute one multiplier w_q^2=q^(-1) mod M and transport the complete root set. Implemented and tested on all 13 selected parameters. For every passing q at t=7 and t=69, transported roots were compared with direct roots and matched exactly; MITM-selected q were also compared with direct unitary-split enumeration. All tests pass and known noncanonical solutions remain. Next: seek Gray-code/kernel traversal to update w_q incrementally, then bit-weight-balanced MITM partitioning. Do not claim polynomial time or uniqueness.

Artifacts:
- research-outputs/LOCAL_JACOBI_AP_THEOREM_AND_RANK_SURVEY_2026-11-08.md
- research-outputs/verify_arithmetic_progression_jacobi_sieve.py
- research-outputs/survey_jacobi_rank.py
- research-outputs/verify_selected_q_sieve_counts.py
- research-outputs/LOCAL_GLOBAL_SIEVE_13_PARAMETERS_2026-11-08.md
- research-outputs/verify_local_global_sieve.py
- research-outputs/ADAPTIVE_MITM_LOCAL_GLOBAL_SIEVE_2026-11-09.md
- research-outputs/adaptive_mitm_local_global_sieve.py


Latest root-transport result:
- Report: research-outputs/ROOT_TRANSPORT_MITM_LOCAL_GLOBAL_SIEVE_2026-11-09.md
- Verifier: research-outputs/root_transport_mitm_local_global_sieve.py
- Root transport lemma: for q,q' passing all local Jacobi rows, q/q' is a square mod M; if w^2=q/q', then z -> wz maps roots of -D/q bijectively to roots of -D/q'. With anchor q'=1, roots(-D/q)=w_q*roots(-D), w_q^2=q^(-1) mod M.
- Verified all 13 parameter outputs against previous exact representation counts. For t=7 and t=69, every passing q's transported root set was compared with a freshly computed root set; all equal. MITM cases were cross-checked against direct unitary-split enumeration.
- t=7 retains both (q,r,s)=(324,11893677,12888073) and (16814886,81,36464494); t=69 retains (19600,14663540485,14784049124) and (3470764,430908401,2841046000).
- Timing observation on SymPy 1.14.0: t=69 approx 8.4s without full root-set audit, 12.6s with audit; not a comparative speedup claim.
- Latest commits: root-transport verifier 8e368df1864689ab46b83da111c1e81528ad768c; corrected theorem report 0c2deff2f3bcf0163223550950e60bffa9254b2c.

New open problem:
- The root multiplier w_q is still recomputed separately for each q. The passing exponent vectors solve an affine F_2 system; investigate Gray-code traversal of its kernel and precomputed square roots of kernel-supported prime products to update w_q by multiplication rather than repeated local square-root extraction.


Latest Gray-code kernel root-transport result (2026-11-09):
- Full Jacobi parity matrix A has one column for every distinct prime ell|D and one row for every distinct p|h; A_{p,ell}=1 iff (ell/p)=-1. A divisor q passes all local Jacobi rows iff its exponent parity vector v lies in ker_F2(A).
- Let b_1,...,b_d be a kernel basis, B_j=product_{i:b_ji=1} ell_i, and choose u_j^2=B_j^(-1) mod M. For a coefficient vector c, put n_i=sum_j c_j b_ji and v_i=n_i mod 2. The overlap correction C(v)=product_i ell_i^{floor(n_i/2)} gives w_v=C(v)*product_{j:c_j=1}u_j, with w_v^2=q_v^(-1) mod M for q_v=product_i ell_i^{v_i}. This correction is essential because basis supports overlap.
- For an actual q with exponents e_i=2f_i+v_i, let S_q=product_i ell_i^{f_i}; then w_q=S_q^(-1)w_v and roots(-D/q)=w_q*roots(-D). Thus root square-root extraction is needed only for the d kernel basis vectors plus the one base root set, not separately for every passing q.
- Gray code traverses all 2^d kernel coefficient vectors, toggling one basis vector at a time; the implementation updates the basis-root product and overlap counts, then applies C(v).
- Exact tests on all 13 selected parameters reproduce all previous representation counts. For t=7 and t=69, all passing q have transported root sets compared against direct local-root+CRT construction; all equal. All MITM-selected q are compared against direct unitary-split enumeration in audit mode; all pass.
- t=7: n=9, rank=3, nullity=6, 64 parity classes, 576 passing q, 2 representations.
- t=69: n=13, rank=3, nullity=10, 1024 parity classes, 21504 passing q, 2 representations.
- All 13 rows: parity class counts are respectively 32,64,64,1024,256,256,256,64,128,64,64,128,64; q-pass counts and representation counts match prior reports. Full run output ends GRAY_KERNEL_ROOT_TRANSPORT_CHECKS: PASS.
- New report: research-outputs/GRAY_KERNEL_ROOT_TRANSPORT_2026-11-09.md
- New verifier: research-outputs/gray_kernel_root_transport_sieve.py
- Latest commits: verifier 03d922ed487460271f309b9fda9da0edf1d391be; report 02ec05fc49a41f8a1811964baa05cd44a03b65db.
- This reduces root-extraction/CRT setup from per-q to per-kernel-basis-vector, but no wall-clock speedup is claimed. The Gray class enumeration remains exponential in nullity d, and per-q split search remains exponential.


Latest weighted Jacobi code-enumerator result (2026-11-09):
- Let D=product_i ell_i^{a_i}, with distinct prime factors ell_i, and let A_{ji}=1 iff (ell_i/p_j)=-1 for distinct p_j|h. A divisor q=product ell_i^{e_i} passes every local Jacobi condition iff v_i=e_i mod 2 lies in ker_F2(A).
- Define alpha_i=floor(a_i/2)+1 and beta_i=ceil(a_i/2). Exact survivor count:
  Q_pass = sum_{v in ker A} product_{v_i=0} alpha_i product_{v_i=1} beta_i.
- Weighted MacWilliams identity:
  Q_pass = 2^{-r} sum_{y in Row(A)} product_i (alpha_i + (-1)^{y_i} beta_i), r=rank(A).
- Let O={i:a_i odd}, E={i:a_i even}. Since alpha_i=beta_i for i in O, only rowspace vectors supported entirely on E contribute. Hence:
  Q_pass = (product_{i in O}(a_i+1))/2^r * sum_{y in Row(A), supp(y) subset E} product_{i in E,y_i=0}(a_i+1).
  The contributing subspace has dimension r-rank(A_O), where A_O is the submatrix of odd-exponent columns. Thus the exact sum has at most 2^(r-rank(A_O)) terms.
- Independently verified both the weighted rowspace formula and simplified formula against direct enumeration of all divisors q on 13 selected t values. All checks pass.
- Exact counts: t=3 216; 7 576; 17 352; 69 21504; 137 768; 185 768; 609 1792; 1105 1920; 1285 1536; 1457 256; 5957 256; 6215 288; 6657 1056.
- Full A ranks / W sizes for these 13 values: (t=3:2/1), (7:3/1), (17:2/1), (69:3/1), (137:3/1), (185:2/1), (609:3/1), (1105:5/4), (1285:4/4), (1457:3/1), (5957:5/2), (6215:3/1), (6657:6/4). For t=1105,1285,5957,6657, nonzero contributing rowspace vectors add weighted terms.
- Important distinction: the earlier rank survey's rank is based on exponent-one prime columns, which gives a valid simple upper bound tau(D)/2^r1. The new full matrix A includes all distinct prime columns; because divisor choices are weighted by exponent parity, tau(D)/2^rank(A) is not generally a valid bound. The weighted MacWilliams formula resolves this distinction.
- New report: research-outputs/WEIGHTED_JACOBI_CODE_ENUMERATOR_2026-11-09.md
- New verifier: research-outputs/weighted_jacobi_code_count.py
- Verification run: WEIGHTED_CODE_ENUMERATOR_CHECKS: PASS.

Next step:
Use the weighted rowspace formula to characterize exactly when Q_pass=tau(D)/2^r and when nonzero even-exponent coordinates create extra terms. Then combine the small contributing subspace W=Row(A) intersect F_2^E with Gray-code root transport: organize q by parity codeword v, weighted exponent lifts, and the global unitary-split condition. Seek a theorem bounding the number of W-classes that can contain actual global representations; preserve t=7 and t=69 as nonuniqueness counterexamples. Do not infer uniqueness from the 13 samples.

Artifacts:
- research-outputs/weighted_jacobi_code_count.py
- research-outputs/WEIGHTED_JACOBI_CODE_ENUMERATOR_2026-11-09.md


Latest unified group-algebra formulation (2026-11-09):
- Write D=product_i ell_i^a_i, q=product ell_i^e_i, and choose epsilon_i=1 if the full remaining prime power ell_i^(a_i-e_i) is assigned to r, else 0 (assigned to s). Then r=product ell_i^((a_i-e_i)epsilon_i), s=product ell_i^((a_i-e_i)(1-epsilon_i)), so qrs=D and gcd(r,s)=1.
- Since gcd(qr,M)=1, the global condition r+s=0 mod M is equivalent to q*r^2=-D mod M.
- Let c_i be the i-th column of the Legendre syndrome matrix A. Each local choice (e_i,epsilon_i) contributes syndrome (e_i mod 2)c_i in F_2^m and multiplicative residue ell_i^[e_i+2(a_i-e_i)epsilon_i] in G=(Z/MZ)^×.
- Define P_i=sum_{e=0}^{a_i} sum_{epsilon=0}^1 [(e mod2)c_i, ell_i^(e+2(a_i-e)epsilon) mod M] in Z[F_2^m x G], and P=product_i P_i. The coefficient of [0,-D] in P counts ordered triples (q,r,s) satisfying all Jacobi conditions and the global congruence. Since r=s=1 is impossible for M>2 and gcd(r,s)=1, each unordered representation corresponds to exactly two orientations; hence N(t)=1/2 * coeff_[0,-D] P.
- Fourier expansion over F_2 syndromes and characters of G gives an exact product formula for this coefficient. This is a formulation, not yet a new bound or complexity improvement.
- Key interpretation: Jacobi survivor count is total mass of the syndrome-zero layer over all group residues; true representations are the mass at the single target residue -D. The local-global gap is therefore a concentration/distribution problem in the multiplicative subgroup H=<ell_i> of G.
- New report: research-outputs/GROUP_ALGEBRA_GLOBAL_SIEVE_2026-11-09.md
- Latest commit: ee3ec7e995b5ec17117c43b387707c7a729de509.

Next step:
For t=7 and t=69, compute exact syndrome-zero multiplicative residue distributions using sparse dynamic programming in the subgroup generated by ell_i modulo M. Compare the target residue -D with the distribution's maximum atom, support size, collision counts, and additive/multiplicative character sums. First verify that the DP's coefficient at -D equals 2N(t) from direct unitary-split enumeration. If sparse state explosion occurs, restrict to meet-in-the-middle convolution of the local factors. Do not infer a general bound from these two cases.


Critical correction to group-algebra formulation (2026-11-09):
- Found an endpoint overcount in the first group-algebra report: when e_i=a_i, the remaining prime-power block ell_i^(a_i-e_i)=1, so epsilon_i=0 and 1 are not two distinct orientations. The old local factor counted this choice twice and its target coefficient was not a valid representation count.
- Correct local factor for coordinate i:
  P_i = sum_{e=0}^{a_i-1} ([(e mod 2)c_i, ell_i^e] + [(e mod 2)c_i, ell_i^(2a_i-e)]) + [(a_i mod 2)c_i, ell_i^a_i],
  with residues modulo M. It has exactly 2a_i+1 terms.
- Corrected theorem: N(t)=1/2 * coefficient_[0,-D] product_i P_i. Proof uses the unique orientation when e_i<a_i and the single choice when e_i=a_i; every valid unordered representation still has exactly two orientations globally because r=s=1 cannot satisfy M|r+s for M>2.
- Corrected Fourier factor:
  F_i(u,chi)=sum_{e=0}^{a_i-1} (-1)^{u.c_i(e mod2)}(chi(ell_i)^e+chi(ell_i)^(2a_i-e)) + (-1)^{u.c_i(a_i mod2)}chi(ell_i)^a_i.
  This replaces the old formula which double-counted the terminal e=a_i term.
- Corrected report: research-outputs/GROUP_ALGEBRA_GLOBAL_SIEVE_2026-11-09.md (commit 6cb7232504e7dbd421e466c84053b820c25f4ec3).
- Added exact sparse-state MITM verifier: research-outputs/corrected_group_algebra_mitm.py (commit eab06e09fa759c8870129ba316552fc8c6af6d3d). It aggregates half-configurations by (F2 syndrome, residue mod M) and matches complementary states to extract [0,-D]P. It independently enumerates q and unitary splits to check coefficient=2N for t=7 and t=69.
- Added verification protocol report: research-outputs/CORRECTED_GROUP_ALGEBRA_MITM_2026-11-09.md (commit 8a0c971993db5a3c58df4f773278c2f73960ab0a).
- Important status: the corrected theorem is proved algebraically, but the new MITM script has not yet been executed in this environment. Its claimed output is not yet verified; next action is run it, check the target coefficient is 4 for both t=7 and t=69, and compare the recovered representations with the known two cases.

Next step:
Execute corrected_group_algebra_mitm.py on t=7 and t=69. If the state tables are too large, split the local factors by product of branching counts (not just number of factors), and report actual state counts and runtime. Confirm the corrected target coefficient equals 4 in each case, matching 2N with N=2. Only after successful execution should the group-algebra computational validation be marked complete.

- Further Fourier-sign correction: because the target group element is -D, the character factor is chi((-D)^(-1)) = chi(-1)chi(D^(-1)); omitting chi(-1) is incorrect for characters nontrivial on -1. Corrected in the group-algebra report, commit 97b37ea4be205551ed55659e8f655bc402e37059.


Executed corrected group-algebra MITM validation (2026-11-09):
- Ran corrected_group_algebra_mitm.py successfully on t=7 and t=69.
- t=7: local factors [5,11,7,3,3,3,3,3,3], raw half configurations 20x21, aggregated sparse states 297x945, total local configurations 280,665, Jacobi-passing q=576, corrected target coefficient [0,-D]P=4, independent direct N=2. Recovered (q,r,s): (324,11893677,12888073) and (16814886,81,36464494).
- t=69: local factors [13,7,5,7,3,3,3,3,3,3,3,3,3], raw half configurations 30x29, aggregated sparse states 5,265x11,907, total local configurations 62,690,355, Jacobi-passing q=21,504, corrected target coefficient [0,-D]P=4, independent direct N=2. Recovered (19600,14663540485,14784049124) and (3470764,430908401,2841046000).
- Both exact checks satisfy coefficient=2N(t); output: CORRECTED_GROUP_ALGEBRA_MITM_CHECKS: PASS.
- The corrected theorem and Fourier sign are now reflected in GROUP_ALGEBRA_GLOBAL_SIEVE_2026-11-09.md (correction commits 6cb7232504e7dbd421e466c84053b820c25f4ec3 and 97b37ea4be205551ed55659e8f655bc402e37059).
- Executed-results report: research-outputs/CORRECTED_GROUP_ALGEBRA_MITM_RESULTS_2026-11-09.md (commit 10561665180e520611c08e5f0ab2968c9e6d5c63).
- Important boundary: only t=7 and t=69 are validated; no general asymptotic or uniqueness claim. State aggregation is exact but not proven polynomial-time; state spaces can grow.

Next step:
Generalize sparse group-algebra coefficient extraction to more parameters and study the syndrome-zero residue distribution: support size, maximum atom, collision count, target atom at -D, and compare target frequency with average mass. Use t=7 and t=69 as validated anchors; add t=3,17,137,185 and then larger manageable cases. Preserve independent direct enumeration as an oracle and stop when state growth becomes impractical. Seek a structural character-sum bound, not just numerical observations.


Executed syndrome-zero residue distribution experiment (2026-11-09):
- Added sparse MITM full residue-distribution program: research-outputs/syndrome_zero_residue_distribution.py (commit 7fdf3816259844fa5620c2b2fca3350acd3f6f10).
- Added report: research-outputs/SYNDROME_ZERO_RESIDUE_DISTRIBUTION_2026-11-09.md (commit 1263ec67f90bb99dc3a868c9be58a2dd10f0c231).
- Computed exact syndrome-zero residue distributions for t=3,7,17,69,137,185. For each, target atom mu_0(-D)=2N(t) and agrees with independently enumerated representations.
- Results (t: total syndrome-zero mass / support / target atom / max atom / average / target-to-average / collision pairs):
  3: 6012 / 1950 / 2 / 8 / 3.0831 / 0.649 / 8195;
  7: 36138 / 21242 / 4 / 6 / 1.7013 / 2.351 / 20140;
  17: 11637 / 11526 / 2 / 2 / 1.0096 / 1.981 / 111;
  69: 7851726 / 7720655 / 4 / 4 / 1.0170 / 3.932 / 131902;
  137: 82452 / 82375 / 2 / 2 / 1.0009 / 2.000 / 77;
  185: 54981 / 54936 / 2 / 2 / 1.0008 / 2.000 / 45.
- Important falsification: the target residue -D is not generally a low-frequency atom. For t=7 it is above average; for t=17,69,137,185 it is a maximum atom. Thus abandon the conjecture that true representations arise from systematically rare residues. For t=3 it is below average.
- The distribution is close to injective for t=17,69,137,185 (support close to total mass); t=7 has much more concentration. This is only finite evidence, not a general theorem.
- Corrected group-algebra MITM had already been executed: t=7 and t=69 target coefficients both equal 4=2N(t), with independent direct representation checks.
- Next step: explain target atom maximality in most samples. Investigate involutions and local-factor symmetries, especially the two orientation choices for e<a and the unique terminal e=a choice; derive autocorrelation/collision identities and characterize when multiple configurations collide at the target. Avoid the disproved low-frequency heuristic.
