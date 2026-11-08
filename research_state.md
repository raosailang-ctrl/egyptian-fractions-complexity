Current question:
For the central K3-derived Egyptian-fraction family, combine the q,r,s parametrization with local Jacobi-character conditions and the global square-root/divisibility constraints, seeking stronger restrictions on noncanonical representations.

Completed:
- Read this research_state.md and the latest pre-research commit 19ccc5caf572aaa12099a49980fecf11db684e4a (a ChatGPT syncer update, not a mathematical change), then reviewed the qrs report, local Jacobi lemma, and pairwise-resultant certificate.
- Proved a new arbitrary-fixed-rank arithmetic-progression theorem: for every s>=1, there is a positive-density AP t ≡ t_s (mod Q_s) such that h(t) contains s chosen odd primes p_i, D(t) contains s chosen primes ell_j with valuation exactly one, and the Legendre-character matrix (epsilon_{p_i}(ell_j)) is the identity.
- Construction: choose ell_j in prescribed invertible residue classes mod P=product p_i using Dirichlet's theorem; avoid the finite resultant prime support {2,3,5,7,11,19,23}; impose t=0 mod p_i, t=1 mod 2, and t ≡ -3^{-1}+ell_j mod ell_j^2. Then v_{ell_j}(1+3t)=1 and no other L_i is divisible by ell_j.
- Proved that exactly tau(D(t))/2^s divisors q|D(t) pass the s selected local Jacobi conditions (q/p_i)=1, because the selected exponent-one prime columns form I_s over F2.
- Combined with the prior modular square-root count to obtain, throughout each such AP:
  N(t) <= 2520 tau(D(t)) 2^(omega(M(t))-s).
- By selecting one increasing t_s from the AP for each s, obtained an infinite sequence t_s->infinity on which the relative local sieve saving is at least 2^-s -> 0. This is not a uniqueness theorem and does not give a density for the union of the APs.
- Constructed and exactly verified explicit CRT certificates for s=1,...,5.
- Surveyed the F2 character rank for all 5000 odd t in 1<=t<=10000. Full row rank occurred for 4835 (96.7%); 165 were deficient; maximum deficiency was 2. Rank-deficiency-two cases: 609,1105,1285,1457,5957,6215,6657. This is finite data only.
- Exactly enumerated q-divisors for 13 selected parameters, verifying the rank-r upper bound tau(D)/2^r; full-rank examples t=7 and 69 attain tau(D)/8.
- Created a report, CRT verifier, rank-survey program, selected-q exact verifier, and handoff. The local ZIP passed integrity checking.

Evidence:
- Main theorem/report: research-outputs/LOCAL_JACOBI_AP_THEOREM_AND_RANK_SURVEY_2026-11-08.md, commit c105296ad23e12c1d4931a2332d4171876a3d03b.
- Explicit CRT verifier: research-outputs/verify_arithmetic_progression_jacobi_sieve.py, commit 07cb3e30aa77b105c55d3440ecff97b019416d41.
- Rank survey: research-outputs/survey_jacobi_rank.py, commit 2df2a647f9bad7e27cc527999fe47de8a5d4048e.
- Exact selected q counts: research-outputs/verify_selected_q_sieve_counts.py, commit 1c9ea1bf65ac08499e6ef5668f9bd0294d028cfd.
- Handoff: research-outputs/LOCAL_JACOBI_AP_HANDOFF_2026-11-08.md, commit 111f13d38e43cbbb5fac7ec192ec73a0deb713ba.
- CRT verifier output: s=1..5 all pass; character matrices exactly identity.
- Rank survey output: 4835/5000 full rank (96.7%); 165 deficient; maximum deficiency 2.
- Exact q-filter counts: t=7: 576/4608; t=69: 21504/172032; selected deficient-rank examples satisfy #passing q <= ceil(tau(D)/2^r).
- External Dirichlet theorem source: MIT 18.785, Number Theory I, Lecture 18, Theorem 18.1: https://math.mit.edu/classes/18.785/2021fa/LectureNotes18.pdf.
- Pairwise-resultant prime support certificate: research-outputs/PAIRWISE_FACTOR_RESULTANTS_2026-11-07.md.
- Local ZIP: /mnt/data/K3_LOCAL_JACOBI_AP_RANK_2026-11-08.zip; SHA256 efe95d90c608e81f6efab32bbc0ad1bf2bdc2464ec7776304add7d55fc93ef32; unzip integrity test passed.

Open problems:
- Local Jacobi conditions are necessary, not sufficient; the square-root class must also contain a divisor r|D/q with r<=sqrt(D/q), gcd(r,D/(qr))=1, and r+s=kM.
- The AP theorem gives arbitrary fixed s and an infinite sequence with relative sieve saving tending to zero, but no quantitative relation between s and t_s and no positive-density set with s growing.
- The 96.7% full-rank observation is only for odd t<=10000; it does not prove an asymptotic density or universal rank statement.
- Ordinary integer decomposition uniqueness remains unproved; t=7 and t=69 are explicit nonunique cases.
- Need exploit prime-power information modulo p_i^2 and the eight linear-factor supports to further eliminate q,r pairs.
- Siegel gcd-escape remains ineffective; genus-two rational point classification and literature-priority audit remain open.

Next step:
Lift the selected Jacobi constraints from mod p_i to mod p_i^2. For each selected p_i|t and each q passing (q/p_i)=1, analyze whether -D/q is a square modulo p_i^2, then combine the local roots modulo p_i^2 with the global requirement r|D/q and r<=sqrt(D/q). Build a CRT/valuation sieve for q,r, test it on t=7 and t=69 (both must survive), and then measure its exact reduction on selected AP examples. Do not infer full uniqueness or a global density theorem.

Artifacts:
- research-outputs/LOCAL_JACOBI_AP_THEOREM_AND_RANK_SURVEY_2026-11-08.md
- research-outputs/verify_arithmetic_progression_jacobi_sieve.py
- research-outputs/survey_jacobi_rank.py
- research-outputs/verify_selected_q_sieve_counts.py
- research-outputs/LOCAL_JACOBI_AP_HANDOFF_2026-11-08.md
- /mnt/data/k3_jacobi_rank_20261108/jacobi_rank_odd_t_10000.jsonl
- /mnt/data/K3_LOCAL_JACOBI_AP_RANK_2026-11-08.zip
