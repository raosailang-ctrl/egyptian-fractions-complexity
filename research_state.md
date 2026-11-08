Current question:
For the central K3-derived Egyptian-fraction family, exploit the exact gcd–coprime-factor parametrization D=qrs, gcd(r,s)=1, r+s=kM to constrain noncanonical decompositions and improve the ordinary representation-count bound; develop local Jacobi-character sieves for q.

Completed:
- Read research_state.md and latest prior repository commit 7318fcfeb82ef9c82cdd06fce60f716dddd9dcbd, then reviewed the divisor bijection, block-divisor rigidity, MITM counter, and pairwise resultants.
- Proved exact bijection: every unordered positive-integer representation M/D=1/u+1/v corresponds uniquely to q,r,s,k with qrs=D, gcd(r,s)=1, r+s=kM; denominators are {qkr,qks}, and gcd(u,v)=qk.
- Derived gcd(k,rs)=1 and the necessary modular square-root condition r^2 == -D/q (mod M).
- Used F+G=1260M to prove D=FG<=630^2 M^2, so r<=630M.
- A unit square congruence modulo M has at most 4*2^omega(M) roots; each root class has at most 630 representatives in [1,630M]. Therefore N(t)<=2520*tau(D(t))*2^omega(M(t)).
- Since deg D=8, M=[t(12t+1)]^2, and gcd(t,12t+1)=1, classical maximal-order bounds imply log N(t)<=(10 log 2+o(1))*log t/loglog t. This improves the previous 8 log 3 coefficient by about 21.1%.
- Derived exact combinatorial bound N(M,D)<=(tau(D^2)-1)/2 by counting coprime prime-power partitions for each q|D.
- Reconstructed q,r,s,k for all 1000 representations in the exact MITM census for 3<=t<=1000; all checks passed. Nonunique t in this interval remain 7 and 69.
- Verified canonical formula: if g=gcd(F,G), then q=g^2, r=G/g, s=F/g, k=1260/g, and standard gcd is qk=1260g.
- Decomposed noncanonical examples: t=7 has q=16814886,k=103; t=69 has q=3470764,k=1.
- Added a conditional F2 Jacobi-character sieve lemma: if h has s distinct odd prime factors and D has s exponent-one prime factors whose Legendre-character vectors form a basis of F2^s, exactly tau(D)/2^s divisors q|D satisfy the necessary local square-residue conditions.
- Verified the lemma exactly for t=7 and t=69. In each case s=3, the local filter retains exactly 1/8 of all q divisors (576/4608 and 21504/172032 respectively); both canonical and noncanonical q values pass, so no known solution is incorrectly excluded.
- Created reports, verifiers, handoff, and a ZIP archive; integrity test passed.

Evidence:
- Main qrs report: research-outputs/K3_QRS_GCD_PARAMETERIZATION_2026-11-08.md, commit 6395767b505bb336abcf738a61c030fbea6af69a.
- qrs verifier: research-outputs/verify_qrs_parametrization.py, commit e755c811816231d56d3144e3e638e8b941fc72f9.
- qrs handoff: research-outputs/QRS_RESEARCH_HANDOFF_2026-11-08.md, commit e7dff11f42e03258be3847c2301732f2816c6412.
- Local Jacobi note: research-outputs/LOCAL_JACOBI_SIEVE_2026-11-08.md, commit df659af1b005ea5b273cf9ba28b3dae65df6ff1b.
- Local Jacobi verifier: research-outputs/verify_local_jacobi_sieve.py, commit 4be161ba5f87127d58d4bf4113c72eed55abf0b2.
- qrs verification: QRS_BIJECTION_AND_ROOT_CONGRUENCE PASS; 1000 representations checked; nonunique parameters [(7,2),(69,2)]; count bounds PASS; canonical formula PASS.
- Jacobi verification: t=7 h-primes [5,7,17], basis vectors from D-primes (19,23,31), 576/4608 q pass; t=69 h-primes [3,23,829], basis vectors from D-primes (967,41,37), 21504/172032 q pass; LOCAL_JACOBI_SIEVE_CERTIFICATES PASS.
- Updated local ZIP: /mnt/data/K3_QRS_GCD_PARAMETERIZATION_2026-11-08.zip; SHA256 fd9b356752fd9e0f60773137593667ae70ac8e325d1964d46ec762a47a1c8da5; ZIP integrity test passed.
- Classical divisor maximum: P. Pollack (2020), https://pollack.uga.edu/largedk3.pdf.
- Classical maximal order of omega: Hildebrand, Introduction to Analytic Number Theory lecture notes, https://eclass-b.uoa.gr/modules/document/file.php/MATH717/04.%20%CE%92%CE%BF%CE%B7%CE%B8%CE%AE%CE%BC%CE%B1%CF%84%CE%B1/Analytic-number-theory-Hildebrand.pdf.

Open problems:
- Complete ordinary integer uniqueness is unproved; t=7 and t=69 are explicit counterexamples.
- Need constrain q|D for which -D/q is a square modulo M and whose square-root class contains a divisor r of D/q with r<=sqrt(D/q), gcd(r,(D/q)/r)=1, and r+s=kM.
- The local Jacobi filter is only necessary. Need establish for a general or positive-density set of t that the F2 character matrix has full rank, using exponent-one prime factors from the eight linear factors.
- The 10 log 2 upper bound is not known sharp; no density or lower bound for N(t) is established.
- Siegel gcd-escape threshold remains ineffective; genus-two rational point classification and literature-priority audit remain open.

Next step:
For varying t, factor h=t(12t+1) and D(t), form the F2 Legendre-character matrix with rows indexed by p|h and columns indexed by exponent-one primes ell|D. Study its rank and its dependence on the eight linear factors, especially after separating the seven overlap primes {2,3,5,7,11,19,23}. If full row rank can be proved on a positive-density or infinite explicit parameter set, the q-candidate count drops exactly by 2^omega(h) on that set. Then combine this q sieve with the root classes r^2 == -D/q (mod M), and test against t=7 and t=69. Do not infer uniqueness merely from the local sieve.

Artifacts:
- research-outputs/K3_QRS_GCD_PARAMETERIZATION_2026-11-08.md
- research-outputs/verify_qrs_parametrization.py
- research-outputs/QRS_RESEARCH_HANDOFF_2026-11-08.md
- research-outputs/LOCAL_JACOBI_SIEVE_2026-11-08.md
- research-outputs/verify_local_jacobi_sieve.py
- research-outputs/BLOCK_DIVISOR_RIGIDITY_AND_SHARPER_COUNT_2026-11-08.md
- research-outputs/count_by_mitm.py
- research-outputs/census_t1_1000.jsonl
- /mnt/data/K3_QRS_GCD_PARAMETERIZATION_2026-11-08.zip
