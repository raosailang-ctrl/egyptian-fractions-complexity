# Research log

## 2026-11-03 — Signed divisor-pair reduction

### New literature connection
Chen and Koo (2013), Theorem 4, parameterize solutions of 1/x+1/y=m/n by coprime divisors d1,d2 of n satisfying m|(d1+d2). This is equivalent to the earlier factor criterion and gives a cleaner route for the reduction.

### Preferred signed encoding
For SUBSET SUM input a_i,T, let A=Σa_i, B=8(A+1), L=ΣB^i, w_{i,0}=B^i, w_{i,1}=B^i+a_i, W=2L+A, and C=L+T. Then

    exists x_{i,j} in {-1,0,1}: Σ x_{i,j}w_{i,j}=C

iff the source subset sum is YES. The proof uses positional dominance: c_i=x_{i,0}+x_{i,1}-1 and |δ|≤2A force c_i=0, so each pair is (1,0) or (0,1).

### Algebraic reduction
For odd h>2W, M=h², omega=1+h, and distinct primes P_{i,j}≡omega^{w_{i,j}} and R≡-omega^C (mod M), let D=RΠP. In any coprime divisor pair d1,d2|D with M|(d1+d2), exactly one divisor contains R. The quotient condition becomes a signed sum of the weights modulo h. Since h>2W, it becomes the exact equation Σxw=C, hence SUBSET SUM.

### Exact experiment
Added experiments_signed.py. It checks examples [1],T=1 (YES), [2],T=1 (NO), and [2,3,7],T=5 (YES), using exact integer arithmetic, trial-division primality tests, and exhaustive divisor-pair assignments. These examples validate the algebraic construction only, not the analytic prime-distribution argument.

### Complexity status
The square-modulus Las Vegas route still uses Baier–Zhao Theorem 4 to show most odd h have many primes in every reduced class modulo h². The finite-trial exhaustive fallback is intended to handle the ineffective threshold. This remains a proof-audit task, not a standard deterministic NP-hardness result.
