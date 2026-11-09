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
Optimize the MITM core rather than broaden claims. First derive incremental root updates across q-divisors: if q is changed by one prime factor, relate roots of -D/q modulo each p^(2a) to roots already computed, and identify when square-root lifting can be updated by multiplying by a precomputed square root of the q-ratio. In parallel, replace equal-count splitting by a bit-weight-balanced split of the prime-power blocks. Benchmark both on t=69 and the 13-parameter set, and retain direct enumeration as a correctness oracle on small cases. Do not claim polynomial time or uniqueness.

Artifacts:
- research-outputs/LOCAL_JACOBI_AP_THEOREM_AND_RANK_SURVEY_2026-11-08.md
- research-outputs/verify_arithmetic_progression_jacobi_sieve.py
- research-outputs/survey_jacobi_rank.py
- research-outputs/verify_selected_q_sieve_counts.py
- research-outputs/LOCAL_GLOBAL_SIEVE_13_PARAMETERS_2026-11-08.md
- research-outputs/verify_local_global_sieve.py
- research-outputs/ADAPTIVE_MITM_LOCAL_GLOBAL_SIEVE_2026-11-09.md
- research-outputs/adaptive_mitm_local_global_sieve.py
