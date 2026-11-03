# Proof audit and corrections

## A. Algebraic core — proved

- Two-term factor criterion: r|b², r≠b, r≡-b (mod a).
- Equivalent coprime-divisor-pair criterion: d1,d2|b, gcd(d1,d2)=1, a|(d1+d2), from Chen–Koo (2013), Theorem 4.
- Signed SUBSET SUM encoding with weights B^i and B^i+a_i.
- For odd h, omega=1+h has exact order h modulo h² and -1 is outside its subgroup.
- Conditional algebraic reduction from SUBSET SUM to TWO-EGYPTIAN once the required prime representatives exist.

## B. Analytic number theory

Baier–Zhao Theorem 4 (Acta Arith. 125.2, 2006) states
\[
\sum_{q\le x^{2/9-\epsilon}}q\max_{(c,q)=1}\left|\psi(x;q^2,c)-x/\varphi(q^2)\right|\ll_{\epsilon,A}x/(\log x)^A.
\]
The sum is over base moduli q, with square moduli q² and weight q. The theorem is average, not pointwise. The paper notes ineffectivity due to Siegel–Walfisz.

The application uses two fixed endpoints Y and Y/2. Verify both ranges explicitly. With epsilon=1/18 and Y=(4X)^6, the upper limits are 4X and 4X/2^(1/6), both exceeding 2X.

## C. Prime-count conversion

For a good h, the endpoint estimates give a lower bound for the von Mangoldt sum in each reduced class. The proof must then:
1. subtract all proper prime powers in (Y/2,Y], globally bounded by O(sqrt(Y) log²Y);
2. divide the remaining weighted prime sum by logY;
3. bound the number of candidate integers in the class by Y/h²;
4. sample exactly uniformly from those candidates.

The scale check is Y/h² >= 1024 X^4, while sqrt(Y) log²Y = O(X^3 log²X), so prime powers are negligible for large X.

## D. Las Vegas fallback

The finite-trial plus exhaustive fallback handles the ineffective threshold:
- at most 2n rounds;
- each round has a fixed cap K per residue class;
- if all rounds fail, solve SUBSET SUM exactly and output a fixed target YES or NO instance;
- for large X, failure probability is at most (5/8)^(2n), and expected exhaustive cost is O((25/32)^n poly(N));
- below the unknown threshold, X=4W>=8B^n and B>=16 force n and A to be bounded, so there are only finitely many such inputs.

This argument is plausible and substantially specified, but should be formalized as an exact probabilistic Turing machine before publication.

## E. Numerical experiments

`experiments_signed.py` checks the signed encoding, constructs small prime representatives by trial division, and exhaustively enumerates all assignments of prime factors to d1, d2, or neither. It verifies tiny YES and NO instances with exact integer arithmetic. It does **not** validate the asymptotic prime-distribution theorem or the Las Vegas success probability.

## F. Complexity language

Use “Las Vegas randomized expected-polynomial-time reduction” if the expected-time and zero-error proof is complete. Do not call it a standard deterministic Karp reduction. Do not claim P=NP. Do not infer unrestricted shortest-expansion NP-hardness from the restricted-denominator subset-sum problem.
