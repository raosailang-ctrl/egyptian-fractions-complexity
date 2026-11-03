# Proof audit and corrections

## A. Algebraic core — proved

- Two-term factor criterion: r|b^2, r!=b, r==-b (mod a).
- Equivalent coprime-divisor-pair criterion: d1,d2|b, gcd(d1,d2)=1, a|(d1+d2), from Chen-Koo (2013), Theorem 4.
- Signed SUBSET SUM encoding with weights B^i and B^i+a_i.
- For odd h, omega=1+h has exact order h modulo h^2 and -1 is outside its subgroup.
- Conditional algebraic reduction from SUBSET SUM to TWO-EGYPTIAN once the required prime representatives exist.

## B. Analytic number theory

Baier-Zhao Theorem 4 (Acta Arith. 125.2, 2006) states

    sum_{q<=x^(2/9-epsilon)} q max_{(c,q)=1} |psi(x;q^2,c)-x/phi(q^2)| <<_(epsilon,A) x/(log x)^A.

The sum is over base moduli q, with square moduli q^2 and weight q. The theorem is average, not pointwise. The paper notes ineffectivity due to Siegel-Walfisz.

The application uses two fixed endpoints Y and Y/2. Verify both ranges explicitly. With epsilon=1/18 and Y=(4X)^6, the upper limits are 4X and 4X/2^(1/6), both exceeding 2X.

## C. Prime-count conversion

For a good h, the endpoint estimates give a lower bound for the von Mangoldt sum in each reduced class. The proof must then:

1. subtract all proper prime powers in (Y/2,Y], globally bounded by O(sqrt(Y) log^2 Y);
2. divide the remaining weighted prime sum by log Y;
3. bound the number of candidate integers in the class by Y/h^2;
4. sample exactly uniformly from those candidates.

The scale check is Y/h^2 >= 1024 X^4, while sqrt(Y) log^2 Y = O(X^3 log^2 X), so prime powers are negligible for large X.

## D. Las Vegas fallback

The finite-trial plus exhaustive fallback handles the ineffective threshold:

- at most 2n rounds;
- each round has a fixed cap K per residue class;
- if all rounds fail, solve SUBSET SUM exactly and output a fixed target YES or NO instance;
- for large X, failure probability is at most (5/8)^(2n), and expected exhaustive cost is O((25/32)^n poly(N));
- below the unknown threshold, X=4W>=8B^n and B>=16 force n and A to be bounded, so there are only finitely many such inputs.

This argument is plausible and substantially specified, but should be formalized as an exact probabilistic Turing machine before publication.

## E. Numerical experiments for the signed reduction

experiments_signed.py checks the signed encoding, constructs small prime representatives by trial division, and exhaustively enumerates all assignments of prime factors to d1, d2, or neither. It verifies tiny YES and NO instances with exact integer arithmetic. It does not validate the asymptotic prime-distribution theorem or the Las Vegas success probability.

## F. Complexity language

Use "Las Vegas randomized expected-polynomial-time reduction" if the expected-time and zero-error proof is complete. Do not call it a standard deterministic Karp reduction. Do not claim P=NP. Do not infer unrestricted shortest-expansion NP-hardness from the restricted-denominator subset-sum problem.

## G. Fixed odd-prime numerator criterion — proved, given factorization

Let q be an odd prime and b=product p_i^alpha_i with gcd(q,b)=1. Choose a primitive root g modulo q and write p_i=g^t_i (mod q). Every divisor r|b^2 can be written as

    r=b*product p_i^delta_i,  -alpha_i<=delta_i<=alpha_i.

The factor criterion r==-b (mod q) is therefore equivalent to

    sum delta_i*t_i == (q-1)/2 (mod q-1).

A cyclic DP over Z/(q-1) with q-1 states decides this condition and reconstructs a delta-vector. For fixed q, it takes O_q(log b) transitions after the factorization of b is supplied. It does not factor b.

If q-1=2^s*m with m odd, the target is 2^(s-1) modulo 2^s and 0 modulo m. The same delta-vector must satisfy both CRT components.

### Exact instances

- q=11, b=230=2*5*23: t=(1,4,0), delta=(1,1,0), target 5 modulo 10, r=2300, b^2/r=23, and 11/230=1/230+1/23.
- q=13, b=38=2*19: t=(1,5), delta=(1,1), target 6 modulo 12, r=1444, b^2/r=1, and 13/38=1/114+1/3.
- q=13, b=493=17*29: t=(2,4), delta=(1,1), target 6 modulo 12, r=493^2, b^2/r=1, and 13/493=1/18734+1/38.
- q=19, b=512=2^9: t=1, delta=9, target 9 modulo 18, r=2^18, b^2/r=1, and 19/512=1/13824+1/27.

### q=11 correction

The earlier parity-only simplification for q=11 is withdrawn. The target 5 modulo 10 has both a parity component and a mod-5 component; parity alone cannot decide it. Distinct odd logarithm residues such as 3 and 5 are not interchangeable. The ten-state DP and the exact congruence modulo 10 remain valid.

### Scope caveat

The general criterion is an elementary reformulation of the factor criterion. The displayed examples are computation-verified, not a complete classification of all denominators for q=11,13,19. No polynomial-time factoring algorithm or P-vs-NP consequence is claimed.
