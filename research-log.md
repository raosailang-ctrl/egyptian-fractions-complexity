# Research log

## 2026-11-03 — Signed divisor-pair reduction

### New literature connection
Chen and Koo (2013), Theorem 4, parameterize solutions of 1/x+1/y=m/n by coprime divisors d1,d2 of n satisfying m|(d1+d2). This is equivalent to the earlier factor criterion and gives a cleaner route for the reduction.

### Preferred signed encoding
For SUBSET SUM input a_i,T, let A=sum a_i, B=8(A+1), L=sum B^i, w_(i,0)=B^i, w_(i,1)=B^i+a_i, W=2L+A, and C=L+T. Then

    exists x_(i,j) in {-1,0,1}: sum x_(i,j)w_(i,j)=C

iff the source subset sum is YES. The proof uses positional dominance: c_i=x_(i,0)+x_(i,1)-1 and |delta|<=2A force c_i=0, so each pair is (1,0) or (0,1).

### Algebraic reduction
For odd h>2W, M=h^2, omega=1+h, and distinct primes P_(i,j),R congruent to omega^w_(i,j) and -omega^C (mod M), respectively, let D=R product P. In any coprime divisor pair d1,d2|D with M|(d1+d2), exactly one divisor contains R. The quotient condition becomes a signed sum of the weights modulo h. Since h>2W, it becomes the exact equation sum xw=C, hence SUBSET SUM.

### Exact experiment
Added experiments_signed.py. It checks examples [1],T=1 (YES), [2],T=1 (NO), and [2,3,7],T=5 (YES), using exact integer arithmetic, trial-division primality tests, and exhaustive divisor-pair assignments. These examples validate the algebraic construction only, not the analytic prime-distribution argument.

### Complexity status
The square-modulus Las Vegas route still uses Baier-Zhao Theorem 4 to show most odd h have many primes in every reduced class modulo h^2. The finite-trial exhaustive fallback is intended to handle the ineffective threshold. This remains a proof-audit task, not a standard deterministic NP-hardness result.

## 2026-11-03 — Fixed odd-prime numerator criterion and CRT dynamic programming

### General criterion
For a fixed odd prime q and a supplied factorization b=product p_i^alpha_i, choose a primitive root g modulo q and write p_i=g^t_i (mod q). The factor criterion r|b^2, r!=b, r==-b (mod q) becomes

    exists delta_i in [-alpha_i,alpha_i]: sum delta_i*t_i == (q-1)/2 (mod q-1).

This follows by writing r=b*product p_i^delta_i. The target is nonzero modulo q-1, so a valid witness cannot be the central divisor r=b.

### DP
A direct cyclic DP has q-1 states. Starting with residue 0, for each prime power p_i^alpha_i add every shift delta*t_i modulo q-1 for -alpha_i<=delta<=alpha_i. Store predecessors to recover a witness. For fixed q, this takes O_q(sum_i(2 alpha_i+1))=O_q(log b) transitions after the factorization of b is supplied.

### CRT form
Write q-1=2^s*m with m odd. The target (q-1)/2 is 2^(s-1) modulo 2^s and 0 modulo m. The same delta-vector must satisfy both components.

- q=11: 10 states; target 5 modulo 10, or (1 mod 2, 0 mod 5).
- q=13: 12 states; target 6 modulo 12, or (0 mod 3, 2 mod 4).
- q=19: 18 states; target 9 modulo 18, or (1 mod 2, 0 mod 9).

### Corrected q=11 example
For b=230=2*5*23, using primitive root 2 modulo 11 gives discrete-log residues t=(1,4,0). The vector delta=(1,1,0) reaches 5 modulo 10. It gives r=2300|230^2, r==1==-230 (mod 11), and the exact expansion 11/230=1/230+1/23. A previous simplified parity-only classification was withdrawn: parity loses the mod-5 component of the modulus-10 condition, so distinct odd logarithm residues such as 3 and 5 cannot be grouped as equivalent.

### q=13 examples
For b=38=2*19, t=(1,5), and delta=(1,1) reaches 6 modulo 12. The witness r=1444 and complement 1 give 13/38=1/114+1/3.

For b=493=17*29, t=(2,4), and delta=(1,1) also reaches 6 modulo 12. The witness r=493^2 and complement 1 give 13/493=1/18734+1/38.

### q=19 example
For b=512=2^9, t=1 and delta=9 reaches 9 modulo 18, equivalently (1 mod 2,0 mod 9). The witness r=2^18 and complement 1 give 19/512=1/13824+1/27.

### Verification and limits
Added fixed-prime-dp.py and fixed-prime-examples.txt. The script checks the DP witness, the divisor congruence, and the exact unit-fraction identity. These are finite exact examples. The general criterion is an elementary consequence of the factor criterion; the DP is exact after factorization. No polynomial-time factorization result is claimed, and no conclusion about P vs NP follows.
