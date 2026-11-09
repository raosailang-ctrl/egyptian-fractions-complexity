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
