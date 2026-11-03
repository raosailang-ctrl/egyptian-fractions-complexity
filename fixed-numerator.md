# Fixed numerator: finite-group dynamic programming and known criteria

Fix a positive integer a. Let T_a be the language of denominators b>a, gcd(a,b)=1, for which a/b is a sum of two distinct unit fractions.

By the factor criterion, this is equivalent to existence of

    r | b^2, r != b, r == -b (mod a).

## 1. Dynamic programming given the factorization of b

Suppose

    b = product_i p_i^alpha_i.

Every divisor of b^2 has the form

    r = product_i p_i^e_i,  0 <= e_i <= 2 alpha_i.

All p_i are units modulo a.

Use states DP_i(g, delta), where:

- g in (Z/aZ)^* is the product residue after the first i prime powers;
- delta=1 means at least one chosen exponent differs from its central exponent alpha_j.

Initialize DP_0(1,0)=1. For each prime power, transition over e=0,...,2 alpha_i:

    g' = g p_i^e (mod a),
    delta' = delta OR (e != alpha_i).

A proper divisor with target residue exists exactly when

    DP_s(-b mod a, 1) = 1.

The flag excludes the unique central exponent vector (alpha_1,...,alpha_s), which represents r=b.

The number of group operations is

    O(phi(a) sum_i (2 alpha_i+1)) = O_a(log b).

For variable a, this is pseudo-polynomial in a, not polynomial in log a.

## 2. Membership in NP intersect coNP for fixed a

- **YES certificate:** a divisor r | b^2 with r != b and r == -b (mod a). Its bit length is at most 2 log_2 b + O(1).
- **NO certificate:** a complete prime factorization of b. The verifier checks each listed prime using a deterministic polynomial-time primality test, checks the product, and runs the finite-state DP. If no noncentral exponent vector reaches -b mod a, the instance is NO.

The factorization certificate has polynomial bit length. Therefore, for each fixed a,

    T_a is in NP intersect coNP.

This does not prove T_a is in P, because finding the factorization of b is not known to have a deterministic polynomial-time algorithm in general.

## 3. Known special numerators in the literature

Chen and Koo (2013), Theorems 9-10, prove the following:

- If every prime factor of b is congruent to +/-1 (mod a), then a/b has a proper two-term expansion if and only if b has a prime factor congruent to -1 (mod a).
- In particular, for reduced fractions:

    3/b has a two-term expansion iff b has a prime factor == 2 (mod 3),
    4/b has a two-term expansion iff b has a prime factor == 3 (mod 4),
    6/b has a two-term expansion iff b has a prime factor == 5 (mod 6).

These special-numerator criteria are established literature, not new results of this project. The general fixed-a NP intersect coNP observation is an algorithmic consequence of the factor criterion and finite-group DP; its novelty should be checked against the literature before publication.

Reference: Chen and Koo, "Two-term Egyptian fractions," Notes on Number Theory and Discrete Mathematics 19(2), 2013, pp. 15-25, especially Theorems 4 and 9-10.

## 4. Exact criterion for a fixed odd-prime numerator

Let q be an odd prime, gcd(q,b)=1, and suppose the complete factorization of b is supplied:

    b = product_{i=1}^n p_i^alpha_i.

Choose a primitive root g modulo q. For each prime factor p_i, let t_i be the unique residue modulo q-1 such that

    p_i == g^t_i (mod q).

Then the following are equivalent:

1. q/b is a sum of two distinct unit fractions;
2. there are integers delta_i in [-alpha_i, alpha_i] such that

       sum_i delta_i t_i == (q-1)/2 (mod q-1).

### Proof

The factor criterion says that the desired expansion exists exactly when there is an r | b^2, r != b, with r == -b (mod q).

Write the exponent of p_i in r as alpha_i+delta_i. Since 0 <= v_{p_i}(r) <= 2 alpha_i, each delta_i lies in [-alpha_i,alpha_i], and

    r = b product_i p_i^delta_i.

Because b is invertible modulo q, the congruence r == -b (mod q) is equivalent to

    product_i p_i^delta_i == -1 (mod q).

Using p_i == g^t_i and the fact that g has order q-1, this is equivalent to

    sum_i delta_i t_i == (q-1)/2 (mod q-1),

because g^((q-1)/2) == -1 (mod q). Conversely, any such delta-vector defines an integer divisor r of b^2 with the required congruence. The target (q-1)/2 is nonzero modulo q-1, so r cannot equal b. The factor criterion then gives two distinct unit fractions.

For an arbitrary odd prime q, use a primitive root g; 2 is not a primitive root modulo every prime. In the worked examples q=11,13,19, the choice g=2 is valid.

## 5. Finite-state DP and CRT form

Put m=q-1. Define reachable residue sets by

    S_0 = {0},
    S_i = {s + delta*t_i (mod m): s in S_(i-1), -alpha_i <= delta <= alpha_i}.

The answer is YES exactly when m/2 belongs to S_n. Storing one predecessor for each reached residue reconstructs a witnessing delta-vector.

There are m=q-1 states. For fixed q, the number of transitions is

    O_q(sum_i (2 alpha_i+1)) = O_q(log b).

This running-time statement assumes that the factorization of b has already been provided. Factoring b is not part of this DP and is not known to be deterministic polynomial time in log b.

The target has a useful CRT description. Write

    q-1 = 2^s * m_odd, with m_odd odd.

Then

    (q-1)/2 == 2^(s-1) (mod 2^s),
    (q-1)/2 == 0 (mod m_odd).

The same delta-vector must satisfy both congruences. The CRT split changes the representation of the state; it does not permit choosing independent delta-vectors for the two components.

For the three primes studied so far:

| Numerator q | q-1 | CRT target | Number of DP states |
|---|---:|---|---:|
| 11 | 10 = 2*5 | 1 (mod 2), 0 (mod 5) | 10 |
| 13 | 12 = 4*3 | 0 (mod 3), 2 (mod 4) | 12 |
| 19 | 18 = 2*9 | 1 (mod 2), 0 (mod 9) | 18 |

## 6. Exact examples and the q=11 correction

All examples below use g=2, which is a primitive root for q=11,13,19. They are exact finite computations after the displayed factorization is supplied.

### Numerator 11: retain the full ten-state condition

Take b=230=2*5*23. Modulo 11,

    2 == 2^1, 5 == 2^4, 23 == 2^0.

Thus t=(1,4,0). The vector delta=(1,1,0) gives

    1*1 + 1*4 + 0*0 == 5 (mod 10).

It yields r=2^2*5^2*23=2300, while b^2/r=23. Hence

    11/230 = 1/230 + 1/23.

**Correction:** an earlier simplified classification for q=11 based only on odd/even residue grouping was withdrawn. Parity alone loses the mod-5 component of the condition modulo 10; in particular, distinct odd logarithm residues such as 3 and 5 cannot be treated as interchangeable. The exact condition remains the ten-state congruence sum(delta_i*t_i) == 5 (mod 10). Do not reuse the withdrawn parity classification.

### Numerator 13: twelve states, CRT target (0 mod 3, 2 mod 4)

For b=38=2*19, the discrete-log residues modulo 12 are t=(1,5). The vector delta=(1,1) gives 1+5=6 (mod 12), equivalently 0 (mod 3) and 2 (mod 4). It yields r=38^2=1444 and b^2/r=1, so

    13/38 = 1/114 + 1/3.

A second example is b=493=17*29. Modulo 13, 17==2^2 and 29==2^4. Again delta=(1,1) reaches 6 modulo 12. Here r=493^2 and b^2/r=1, giving

    13/493 = 1/18734 + 1/38.

### Numerator 19: eighteen states, CRT target (1 mod 2, 0 mod 9)

Take b=2^9=512. Since 2 is the chosen primitive root, t_1=1. The allowed delta range is [-9,9], and delta_1=9 reaches 9 modulo 18, equivalently 1 modulo 2 and 0 modulo 9. It yields r=2^18=262144 and b^2/r=1, so

    19/512 = 1/13824 + 1/27.

The examples and DP implementation are in fixed-prime-dp.py; the recorded exact output is in fixed-prime-examples.txt.

## 7. Interpretation and limits

The fixed-prime criterion is a proved reformulation of the factor criterion. The finite-state DP is exact for a supplied factorization of b. The displayed q=11,13,19 examples are computation-verified instances, not a classification of all denominators for those numerators.

For fixed q, the DP has a constant number q-1 of states and O_q(log b) transitions after factorization. This is not an unconditional polynomial-time algorithm for the original input b, because the factorization may not be available. The criterion also does not resolve P vs NP.
