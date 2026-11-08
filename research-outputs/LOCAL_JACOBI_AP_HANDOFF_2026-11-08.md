# Research handoff — local Jacobi full-rank arithmetic progressions

Current question: combine the selected Jacobi conditions with r² ≡ -D/q (mod M), r|D/q, gcd(r,D/(qr))=1, and r+s=kM.

Completed:
- Proved for every fixed s>=1 there is a positive-density arithmetic progression t ≡ t_s (mod Q_s) on which h has s specified prime factors p_i and D has s specified exponent-one primes ell_j.
- Used Dirichlet's theorem to choose ell_j with prescribed quadratic-character vectors and CRT to impose v_ell_j(1+3t)=1.
- Excluded all other linear factors using the pairwise resultant prime support {2,3,5,7,11,19,23}.
- The selected Jacobi matrix is I_s, so exactly tau(D)/2^s divisors q pass the s local conditions.
- Derived N(t) <= 2520 tau(D) 2^(omega(M)-s) on each progression.
- By choosing one increasing t_s from each progression, the relative local sieve saving tends to zero.
- Surveyed 5000 odd parameters t<=10000: full rank in 4835 (96.7%); 165 deficient; max deficiency 2. This is finite data only.
- Verified explicit CRT progressions for s=1,...,5 and exact q-sieve counts for 13 selected t values.

Next:
Combine local Jacobi constraints with the global square-root/divisibility conditions. Investigate whether the selected prime rows can be lifted from mod p to mod p² and whether r|D/q eliminates most remaining q. Protect the known noncanonical solutions t=7 and t=69. Do not claim full uniqueness or natural-density rank results.

Artifacts:
- LOCAL_JACOBI_AP_THEOREM_AND_RANK_SURVEY_2026-11-08.md
- verify_arithmetic_progression_jacobi_sieve.py
- survey_jacobi_rank.py
- verify_selected_q_sieve_counts.py
- jacobi_rank_odd_t_10000.jsonl
- rank_survey_summary.log
- ap_certificates.log
- selected_q_sieve_counts.log
