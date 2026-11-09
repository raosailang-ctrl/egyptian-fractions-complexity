Current question:
For the central K3-derived Egyptian-fraction family, combine the q,r,s parametrization with local Jacobi-character conditions and global square-root/divisibility constraints, seeking stronger restrictions on noncanonical representations.

Completed:
- Proved an arbitrary-fixed-rank arithmetic-progression theorem: for every s>=1, there is a positive-density AP t ≡ t_s (mod Q_s) such that h(t) contains s chosen odd primes p_i, D(t) contains s chosen primes ell_j with valuation exactly one, and the Legendre-character matrix is I_s.
- Construction uses CRT and Dirichlet's theorem, avoiding pairwise-resultant prime support {2,3,5,7,11,19,23}; impose t=0 mod p_i, t=1 mod 2, and t ≡ -3^{-1}+ell_j mod ell_j^2. Then v_ell_j(D(t))=1.
- Exactly tau(D(t))/2^s divisors q|D(t) pass the s selected Jacobi conditions on these APs.
- Hensel refinement: for odd t, each unit square-root congruence modulo p^(2a), p^a||h, has either zero or exactly two roots. Hence at most 2^omega(h) roots modulo M=h^2, and on the constructed APs N(t) <= 630 tau(D(t)) 2^(omega(h(t))-s).
- Choosing an increasing t_s from each AP gives an infinite sequence with relative local sieve saving at least 2^-s -> 0. This is not a uniqueness theorem and gives no density for the union of APs.
- Explicit CRT certificates for s=1,...,5 were verified.
- Finite F2 rank survey for odd t<=10000: full row rank 4835/5000 (96.7%), 165 deficient, maximum deficiency 2. This is finite evidence only.
- Exact selected q-divisor counts on 13 parameters verify the rank-based upper bound; t=7 and t=69 attain tau(D)/8.
- New local-global exact sieve: for q|D passing the Jacobi conditions, enumerate unitary splits R=D/q=rs with gcd(r,s)=1 and r<=s, then test r^2+R == 0 mod M. Since gcd(r,M)=1, this is exactly equivalent to r+s == 0 mod M. This recovers every representation and is not merely a heuristic filter.
- Ran the optimized SymPy verifier on all 13 selected parameters. Results (t: Jacobi-passing q / unitary splits tested / root hits): 3: 216/3006/1; 7: 576/18069/2; 17: 352/5818/1; 69: 21504/3925863/2; 137: 768/41226/1; 185: 768/27490/1; 609: 1792/117612/1; 1105: 1920/137497/1; 1285: 1536/87885/1; 1457: 256/8514/1; 5957: 256/19026/1; 6215: 288/13905/1; 6657: 1056/130410/1.
- The two known noncanonical representations are preserved: t=7 has 2 representations and t=69 has 2; the other 11 selected parameters have one each. This is a finite sample, not a uniqueness theorem.
- Optimized verifier factors the eight linear factors separately, merges valuations, and avoids factoring the large product D as a single integer.

Evidence:
- Main AP theorem and rank survey: research-outputs/LOCAL_JACOBI_AP_THEOREM_AND_RANK_SURVEY_2026-11-08.md
- AP verifier: research-outputs/verify_arithmetic_progression_jacobi_sieve.py
- Rank survey: research-outputs/survey_jacobi_rank.py
- Selected q counts: research-outputs/verify_selected_q_sieve_counts.py
- Exact local-global report: research-outputs/LOCAL_GLOBAL_SIEVE_13_PARAMETERS_2026-11-08.md
- Exact local-global verifier: research-outputs/verify_local_global_sieve.py
- Handoff: research-outputs/LOCAL_JACOBI_AP_HANDOFF_2026-11-08.md
- Latest local-global verifier run: LOCAL_GLOBAL_SIEVE_EXACT_CHECKS: PASS; all 13 rows reproduced.
- Latest research-state commit before this update: 791750a5b36858a53c49b906e52eac08fc110cd0.
- External Dirichlet theorem source: MIT 18.785, Number Theory I, Lecture 18, Theorem 18.1: https://math.mit.edu/classes/18.785/2021fa/LectureNotes18.pdf.
- Pairwise-resultant certificate: research-outputs/PAIRWISE_FACTOR_RESULTANTS_2026-11-07.md.
- Prior ZIP: /mnt/data/K3_LOCAL_JACOBI_AP_RANK_2026-11-08.zip (SHA256 b9f6cb8a6b086ffa7c7b646ec11e6a676d11abd750d018b1915df2adb2349a2f).

Open problems:
- Local Jacobi conditions are necessary, not sufficient; even after local filtering, many unitary factor splits remain, and the exact congruence is highly selective in the 13 tested cases.
- Need avoid enumerating all 2^omega(R) unitary splits for each q; develop a meet-in-the-middle or product-set method modulo M.
- The AP theorem gives arbitrary fixed s but no quantitative relation between s and t_s and no positive-density set with s growing.
- The 96.7% rank observation is only for odd t<=10000; no asymptotic density or universal rank statement is proved.
- Ordinary integer decomposition uniqueness remains unproved; t=7 and t=69 are explicit nonunique cases.
- Siegel gcd-escape, genus-two rational point classification, and literature-priority audit remain open.

Next step:
Reformulate the global step as a modular subset-product problem. For fixed q, write the distinct prime-power blocks of R=D/q as A_1,...,A_m. A unitary split is a subset product X=product_{i in S} A_i; it is valid precisely when X^2 ≡ -R (mod M) and X<=sqrt(R). Build a meet-in-the-middle algorithm by splitting the A_i into two halves, storing subset products modulo M, and matching complementary products to target square-root residues. First benchmark on t=69 and the 13-parameter set, preserving both noncanonical solutions. Do not claim polynomial time or uniqueness.

Artifacts:
- research-outputs/LOCAL_JACOBI_AP_THEOREM_AND_RANK_SURVEY_2026-11-08.md
- research-outputs/verify_arithmetic_progression_jacobi_sieve.py
- research-outputs/survey_jacobi_rank.py
- research-outputs/verify_selected_q_sieve_counts.py
- research-outputs/LOCAL_GLOBAL_SIEVE_13_PARAMETERS_2026-11-08.md
- research-outputs/verify_local_global_sieve.py
- research-outputs/LOCAL_JACOBI_AP_HANDOFF_2026-11-08.md
- /mnt/data/K3_LOCAL_JACOBI_AP_RANK_2026-11-08.zip
