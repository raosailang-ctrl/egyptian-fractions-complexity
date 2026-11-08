# Research handoff — K3 q,r,s parametrization

Current question: exploit the exact parametrization D=qrs, gcd(r,s)=1, r+s=kM to further constrain noncanonical decompositions.

Completed:
- Every ordinary decomposition M/D=1/u+1/v corresponds bijectively to q|D and an unordered coprime factor pair {r,s} of D/q with r+s divisible by M.
- Denominators are {qkr,qks}, where k=(r+s)/M, and gcd(u,v)=qk.
- Every admissible r satisfies r^2 == -D/q (mod M).
- Since D=FG and F+G=1260M, D<=630^2 M^2, hence r<=630M.
- A unit square congruence modulo M has at most 4*2^omega(M) roots. This yields N(t)<=2520*tau(D)*2^omega(M).
- Asymptotically log N(t)<=(10 log 2+o(1))*log t/loglog t, improving the previous 8 log 3 coefficient.
- Exact q,r,s reconstruction passed for all 1000 representations found for 3<=t<=1000, including t=7 and t=69 counterexamples.

Next: for each q|D, sieve roots of r^2 == -D/q mod M and impose r|D/q, s=(D/q)/r, r+s=kM. Separate the seven overlap primes from the pairwise-disjoint supports of the eight linear factors. Check all proposed filters against the known t=7 and t=69 noncanonical solutions.

Do not claim full uniqueness or polynomial-time complexity.
