Current question:
For the central K3-derived Egyptian-fraction family, rigorously exploit the eight linear denominator factors and the congruence d ≡ -D (mod M=t^2(12t+1)^2) to constrain ordinary two-unit-fraction representations; then study prime-factor partial splitting.

Completed:
- Read this research_state.md and the latest pre-research repository commit 7318fcfeb82ef9c82cdd06fce60f716dddd9dcbd (Chrome sync changes, not mathematics), together with the prior divisor count, resultant certificates, and genus-two/gcd notes.
- Proved a new all-parameter block-divisor rigidity theorem: for every integer t>=3, if d=prod_{i=1}^8 L_i(t)^{e_i}, e_i in {0,1,2}, satisfies d ≡ -D(t) (mod M(t)), its exponent vector is precisely F(t)^2 or G(t)^2; with d<=D, only G(t)^2. This does NOT prove uniqueness among all positive integer decompositions because other divisors may split primes inside a linear factor.
- Proved the theorem by t=0 and t=-1/12 local jets plus an exhaustive finite certificate: e5 odd impossible for t>=3; e5 even forces t|q1 with |q1|<=234; q1=0 gives 18 vectors; root value zero gives 64; only two vectors have both jets zero; other q1=0 root numerators <=259; 332 necessary (t,e) pairs across 62 t-values remain for 3<=t<=234, none satisfy full mod M congruence.
- Improved the previous universal upper-bound coefficient from 16 log 2 to 8 log 3 using tau(D^2)<=d_3(D) (a prime-power inequality) and the classical fixed-k divisor maximal-order theorem: log N(t)<=(8 log3+o(1))log t/loglog t.
- Implemented exact meet-in-the-middle divisor-residue counting with prime-power splitting, modular inverses, grouped residues and binary searches. Verified t=1,...,1000 completely: only t=1,2,7,69 have multiple ordinary unordered decompositions; counts 85,5,2,2 respectively. The other 996 t-values have one in this FINITE range. Total representations over this range: 1090.
- Identified explicit genuine noncanonical examples t=7 and t=69; the t=69 standard gcd is 176400, while a noncanonical decomposition has gcd 3470764.
- Produced a standalone pure-Python proof certificate, a SymPy-assisted MITM counter, machine-readable exact census, verification logs, a Chinese research note, a handoff, and a verified ZIP archive. All outputs were checked locally. Published all six text/source/data files to GitHub and fetched several back to verify presence.
- Browser attachment automation remains paused; no real sync was performed.

Evidence:
- Main note: research-outputs/BLOCK_DIVISOR_RIGIDITY_AND_SHARPER_COUNT_2026-11-08.md, commit b3a4af7811f5c271db487183586c8e39f9892993.
- Pure Python certificate: research-outputs/verify_block_divisor_rigidity.py, commit 38f5e7e0cc30e9ea9db2a339921d59c3a7646126.
- MITM counter: research-outputs/count_by_mitm.py, commit 2b8ecd84f83279712fde42016f81c025c543d494.
- Handoff note: research-outputs/RESEARCH_HANDOFF_2026-11-08.md, commit 720d7a463cae3a97a2cb6c12d139dcb18f5d9a9a.
- Full 1000-row census: research-outputs/census_t1_1000.jsonl, commit e95c7b45bafd017188670deae0a3cbbfe0380f49.
- Run log: research-outputs/mitm_1000_verification.txt, commit 266d57458c6a2aec75a775b77ecd0851b82d1cdd.
- Local certificate output: FIRST_DERIVATIVE_ZERO_COUNT 18; ROOT_VALUE_ZERO_COUNT 64; DOUBLE_JET_ZERO_EXACTLY_CANONICAL 2; FINITE_NECESSARY_CANDIDATES 332; RESIDUAL_FULL_M_EXCLUSION PASS; BLOCK_DIVISOR_RIGIDITY_FOR_ALL_t_GE_3 PASS.
- Exact MITM: CENSUS_PASSED t=1..1000; nonunique=[(1,85),(2,5),(7,2),(69,2)]; max tau(D^2)=9207215325, max half-divisors=120285; all rows pass N<=tau(D^2)<=d3(D).
- Verified local ZIP /mnt/data/K3_block_divisor_rigidity_MITM_2026-11-08.zip, 6 entries, zip test passed, SHA256 6ec383944c1e959023b9a488b9ddea46fd60f5119ee797a0ae7b4d99e5bde984.
- External fixed-k divisor maximal order reference: Paul Pollack (2020), https://pollack.uga.edu/largedk3.pdf; this mathematical theorem is classical, not original here.
- Previous pairwise resultant note: research-outputs/PAIRWISE_FACTOR_RESULTANTS_2026-11-07.md with overlapping prime support only {2,3,5,7,11,19,23}.

Open problems:
- ALL ordinary integer decompositions are NOT proved unique for any infinite t-subfamily. Values t=7 and t=69 prove the entire t>=3 family is not pointwise unique.
- The block theorem only excludes products of complete linear factors with exponents 0,1,2. Genuine noncanonical d may select proper prime-power divisors of individual L_i(t)^2; this is the main arithmetic gap.
- No proven uniform/asymptotic improvement of the restricted divisor count beyond d3(D) from the congruence condition itself.
- The Siegel gcd-escape threshold remains ineffective; no power lower bound for noncanonical gcd. Genus-two rational-point classification and literature priority audit remain open.
- The MITM algorithm needs factorization of D and does NOT establish polynomial-time complexity or a #P-hardness result.

Next step:
Use the seven overlap primes {2,3,5,7,11,19,23} to separate small shared factors and pairwise-disjoint prime supports of the eight L_i(t). Develop and verify a rigorous obstruction for candidates that partially split only one linear factor, using congruences modulo t^2 and (12t+1)^2. Test each proposed obstruction on the genuine t=7 and t=69 noncanonical witnesses. Seek a stronger bound on the full congruence-restricted divisor count; do not infer infinite uniqueness from the finite t<=1000 census.

Artifacts:
- research-outputs/BLOCK_DIVISOR_RIGIDITY_AND_SHARPER_COUNT_2026-11-08.md
- research-outputs/verify_block_divisor_rigidity.py
- research-outputs/count_by_mitm.py
- research-outputs/census_t1_1000.jsonl
- research-outputs/mitm_1000_verification.txt
- research-outputs/RESEARCH_HANDOFF_2026-11-08.md
- /mnt/data/K3_block_divisor_rigidity_MITM_2026-11-08.zip
