# Fixed numerator: finite-group dynamic programming

Fix a positive integer a. Let T_a be the language of denominators b>a, gcd(a,b)=1, for which a/b is a sum of two distinct unit fractions.

By the two-term criterion, this is equivalent to existence of

    r|b^2, r!=b, r==-b (mod a).

## 1. Dynamic programming given the factorization of b

Suppose b=product_i p_i^(alpha_i). Every divisor of b^2 has the form r=product_i p_i^(e_i), with 0<=e_i<=2alpha_i. All p_i are units modulo a.

Use states DP_i(g,delta), where g is the product residue after the first i primes and delta=1 means at least one selected exponent differs from the central exponent alpha_j. Initialize DP_0(1,0)=1. For each prime power, transition over e=0,...,2alpha_i:

    g'=g*p_i^e mod a,
    delta'=delta OR (e!=alpha_i).

A proper divisor with target residue exists exactly when DP_s(-b mod a,1)=1. The flag excludes the unique central exponent vector (alpha_1,...,alpha_s), representing r=b.

The number of group operations is O(phi(a)*sum_i(2alpha_i+1))=O_a(log b). For variable a, this is pseudo-polynomial in a, not polynomial in log a.

## 2. Membership in NP intersect coNP for fixed a

- YES certificate: a divisor r|b^2 with r!=b and r==-b (mod a). Its bit length is at most 2log_2(b)+O(1).
- NO certificate: a complete prime factorization of b. The verifier checks each listed prime using a deterministic polynomial-time primality test, checks the product, and runs the finite-state DP. If no noncentral exponent vector reaches -b modulo a, the instance is NO.

The factorization certificate has polynomial bit length. Therefore, for each fixed a, T_a is in NP intersect coNP.

This does not prove T_a is in P, because finding the factorization of b is not known to have a deterministic polynomial-time algorithm in general.

## 3. Special cases

For a=3, a classical criterion says that 3/b has a two-term expansion iff b has a prime factor congruent to 2 modulo 3 (for reduced fractions with 3 not dividing b). Eppstein records this criterion and notes its connection to integer factorization.

For a=4 and odd b, the corresponding criterion is that b==3 modulo 4, or b has a prime factor congruent to 3 modulo 4. See references.md.
