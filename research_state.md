Current question:
For the central K3-derived Egyptian-fraction family, exploit the exact gcd–coprime-factor parametrization D=qrs, gcd(r,s)=1, r+s=kM to further constrain noncanonical decompositions and improve the ordinary representation-count bound.

Completed:
- Read research_state.md and the latest commit 7318fcfeb82ef9c82cdd06fce60f716dddd9dcbd, then reviewed the prior divisor bijection, block-divisor rigidity proof, MITM counter, and pairwise resultant certificate.
- Proved an exact bijection: every unordered positive-integer representation M/D=1/u+1/v corresponds uniquely to q,r,s,k with qrs=D, gcd(r,s)=1, r+s=kM; denominators are {qkr,qks}, and gcd(u,v)=qk.
- Derived gcd(k,rs)=1 and the necessary modular square-root condition r^2 == -D/q (mod M).
- Used F+G=1260M to prove D=FG<=630^2 M^2, so r<=630M.
- A unit square congruence modulo M has at most 4*2^omega(M) roots; each root class has at most 630 representatives in [1,630M]. Therefore N(t)<=2520*tau(D(t))*2^omega(M(t)).
- Since deg D=8, M=[t(12t+1)]^2, and gcd(t,12t+1)=1, classical maximal-order bounds imply log N(t)<=(10 log 2+o(1))*log t/loglog t. This improves the previous 8 log 3 coefficient by about 21.1%.
- Also derived the exact combinatorial bound N(M,D)<=(tau(D^2)-1)/2 by counting coprime prime-power partitions for each q|D.
- Reconstructed q,r,s,k for all 1000 representations found in the exact MITM census for 3<=t<=1000; all checks passed. The only nonunique t in this interval remain 7 and 69.
- Verified canonical formula: if g=gcd(F,G), then q=g^2, r=G/g, s=F/g, k=1260/g, and standard gcd is qk=1260g.
- Decomposed both known noncanonical examples: t=7 has q=16814886,k=103; t=69 has q=3470764,k=1. Both satisfy the exact parameterization.
- Created and ZIP-verified a research package.

Evidence:
- Main report: research-outputs/K3_QRS_GCD_PARAMETERIZATION_2026-11-08.md, commit 6395767b505bb336abcf738a61c030fbea6af69a.
- Exact verifier: research-outputs/verify_qrs_parametrization.py, commit e755c811816231d56d3144e3e638e8b941fc72f9.
- Handoff: research-outputs/QRS_RESEARCH_HANDOFF_2026-11-08.md, commit e7dff11f42e03258be3847c2301732f2816c6412.
- Verification output: QRS_BIJECTION_AND_ROOT_CONGRUENCE PASS; 1000 representations checked; nonunique parameters [(7,2),(69,2)]; combinatorial/root count bounds PASS; canonical qrs formula PASS.
- Local ZIP: /mnt/data/K3_QRS_GCD_PARAMETERIZATION_2026-11-08.zip; SHA256 ad5047a1d1d646829ab6a3bb435a17ba46677b7be3214c5445bd89ad79d86473; ZIP integrity test passed.
- Classical divisor maximum: P. Pollack (2020), https://pollack.uga.edu/largedk3.pdf.
- Classical maximal order of omega: Hildebrand, Introduction to Analytic Number Theory lecture notes, https://eclass-b.uoa.gr/modules/document/file.php/MATH717/04.%20%CE%92%CE%BF%CE%B7%CE%B8%CE%AE%CE%BC%CE%B1%CF%84%CE%B1/Analytic-number-theory-Hildebrand.pdf.

Open problems:
- Complete ordinary integer uniqueness is still unproved; t=7 and t=69 are explicit counterexamples to any claim that all t>=3 are unique.
- Need constrain q|D for which -D/q is a square modulo M and whose square-root class contains a divisor r of D/q with s=(D/q)/r and r+s=kM.
- Need exploit the seven overlap primes {2,3,5,7,11,19,23} and eight nearly disjoint linear-factor prime supports to strengthen the q-sieve.
- The new 10 log 2 bound is an upper bound, not known sharp; no density or lower bound for N(t) is established.
- Siegel gcd-escape remains ineffective; genus-two rational point classification and literature-priority audit remain open.

Next step:
For each q|D, solve r^2 == -D/q (mod M), then impose r|D/q, r<=sqrt(D/q), and gcd(r,(D/q)/r)=1. Separate q's exponents at the seven overlap primes from the eight pairwise-disjoint factor supports. Build an exact local square-character sieve, first test it on all q/r/s of t=7 and t=69, then measure the reduction on t<=1000. Seek a theorem that bounds admissible q, not merely a finite census. Do not claim uniqueness or polynomial-time complexity.

Artifacts:
- research-outputs/K3_QRS_GCD_PARAMETERIZATION_2026-11-08.md
- research-outputs/verify_qrs_parametrization.py
- research-outputs/QRS_RESEARCH_HANDOFF_2026-11-08.md
- research-outputs/BLOCK_DIVISOR_RIGIDITY_AND_SHARPER_COUNT_2026-11-08.md
- research-outputs/count_by_mitm.py
- research-outputs/census_t1_1000.jsonl
- /mnt/data/K3_QRS_GCD_PARAMETERIZATION_2026-11-08.zip
