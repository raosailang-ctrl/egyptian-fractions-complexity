# Arbitrary index and unbounded minimum support in TWO-EGYPTIAN

Date: 2026-11-03

## 1. Main result

We construct, for every integer `R >= 2`, infinitely many reduced fractions `q/b` with prime numerator `q` such that:

1. `q/b` has a two-term Egyptian-fraction expansion;
2. that expansion is unique up to exchanging its two unit fractions;
3. the denominator `b` is squarefree with exactly `2R` distinct prime factors;
4. every two-term factor witness uses all `2R` prime factors;
5. the associated projected minimal zero-sum sequence in a cyclic group has index exactly `R`.

Thus the minimum support in the signed factor criterion is unbounded, and the projected zero-sum index can be arbitrarily large.

This is an existence theorem using Dirichlet's theorem twice. It is not an efficient prime-representative construction and gives no NP-hardness result by itself.

## 2. A family of extremal-index minimal zero-sum sequences

Fix `R >= 2` and put

    k = 2R - 1.

Let `r > 2k` be an integer and put

    m = k r.

In the cyclic group `C_m`, consider

    A = (1, 1+r, 1+2r, ..., 1+(k-1)r, k(r-1)).

This sequence has length `k+1 = 2R`.

### 2.1 It is minimal zero-sum

Its ordinary sum is

    sum(A) = [k + r k(k-1)/2] + k(r-1)
           = r k(k+1)/2
           = R m.

So it is a zero-sum sequence in `C_m`.

Take a subsequence containing `j` of the first `k` terms and, optionally, the final term. Modulo `r`, its sum is

    j - k*epsilon,

where `0 <= j <= k` and `epsilon` is 0 or 1. Since `r > 2k`, this is divisible by `r` only when `j=0, epsilon=0` or `j=k, epsilon=1`. Thus no nonempty proper subsequence sums to zero even modulo `r`, hence none sums to zero modulo `m`. Therefore `A` is minimal zero-sum.

### 2.2 Its index is exactly R

Let `t` be any unit modulo `m`. Write `u` for the least positive residue of `t` modulo `r`, so `1 <= u <= r-1`.

Because `gcd(t,k)=1`, multiplication by `t` permutes the `k` residue classes indexed by `j` modulo `k`. Consequently, the least positive representatives of

    t(1+rj) mod kr,  0 <= j < k,

are exactly

    u, u+r, ..., u+(k-1)r.

Their sum is

    k u + r k(k-1)/2.

For the last term, since `(r-1)t == -t == r-u (mod r)`, the least positive representative of `t*k(r-1)` modulo `kr` is `k(r-u)`. Hence the sum of all least positive representatives is

    k u + r k(k-1)/2 + k(r-u)
      = r k(k+1)/2
      = Rm.

This holds for every unit `t`. Therefore

    ind(A) = R.

In particular, the index is independent of the choice of generator. The sequence has length `2R` and index `R`.

## 3. Lift A to the exponent group C_(2m)

Set `epsilon_j = j mod 2` for `0 <= j < k`, and `epsilon_k=0`. Define

    s_j = 1+rj + m*epsilon_j,  0 <= j < k,
    s_k = k(r-1).

Then `s_j mod m` is the corresponding term of `A`. There are `(k-1)/2 = R-1` odd values of `j` in `0,...,k-1`, so

    sum(s_i) = Rm + (R-1)m = (2R-1)m = k m.

Since `k` is odd,

    sum(s_i) == m (mod 2m).

### Signed uniqueness lemma

Suppose `x_i` belongs to `{-1,0,1}` and

    sum_{i=0}^k x_i s_i == m (mod 2m).

Let

    K = sum_{j=0}^{k-1} x_j.

Reducing modulo `r`, and using `m=kr`, gives

    K - k*x_k == 0 (mod r).

But `|K-k*x_k| <= 2k < r`, so in fact

    K = k*x_k.

If `x_k=1`, then `K=k`, forcing every one of `x_0,...,x_(k-1)` to equal 1. If `x_k=-1`, every one must equal -1.

It remains to rule out `x_k=0`. In that case `K=0`, and

    sum x_i s_i
      = r * sum_{j=0}^{k-1} (j + k*epsilon_j) x_j.

Since `k` is odd and `epsilon_j == j (mod 2)`, every coefficient `j+k*epsilon_j` is even. Thus the expression in parentheses is even. But congruence to `m=kr` modulo `2m=2kr` would require that parenthesized integer to be congruent to the odd integer `k` modulo `2k`, impossible.

Therefore the only signed solutions are

    (x_0,...,x_k) = (1,...,1) or (-1,...,-1).

This is the key lifting property: the projected sequence has index `R`, and the lifted target congruence has minimum support exactly `k+1=2R`.

## 4. Convert the lifted sequence into an Egyptian fraction

Now suppose

    q = 2kr + 1

is prime, with `r > 2k`. Then `q-1=2m`. Choose a primitive root `gamma` modulo `q`.

The exponents `s_0,...,s_k` are distinct modulo `2m`. Indeed:

- for even `j`, `s_j=1+rj` lies below `m`;
- for odd `j`, `s_j=1+rj+m` lies above `m` but below `2m`;
- the last exponent `s_k=m-k` lies below `m` and cannot equal an even-indexed `s_j`, because that would require `r(k-j)=k+1`, impossible when `r>2k`.

Thus the residue classes `gamma^(s_i) mod q` are distinct and nonzero.

By Dirichlet's theorem on primes in arithmetic progressions, choose distinct primes

    p_i == gamma^(s_i) (mod q),  0 <= i <= k.

They can be chosen larger than `q`. Set

    b = product_{i=0}^k p_i.

Then

    b == gamma^(sum s_i)
      == gamma^(k m)
      == (gamma^m)^k
      == (-1)^k
      == -1 (mod q),

because `gamma` has order `2m` and `k` is odd.

Consequently, with

    u = (b+1)/q,   v = b(b+1)/q,

we have the exact expansion

    q/b = 1/u + 1/v.

### Why this expansion is unique and uses every prime factor

For squarefree `b=product p_i`, the two-term factor criterion says that `q/b` has a two-term expansion if and only if there are `x_i in {-1,0,1}` such that

    product p_i^(x_i) == -1 (mod q).

Since `p_i == gamma^(s_i)` and `gamma` has order `2m`, this is equivalent to

    sum x_i s_i == m (mod 2m).

The signed uniqueness lemma shows that the only solutions are the all-`+1` and all-`-1` vectors. They correspond to the complementary divisor choices `b^2` and `1`, which give the same unordered pair `(u,v)`.

Therefore the two-term expansion is unique up to order, and every witness has support `k+1=2R`.

## 5. Infinitely many examples for every R

Fix `R`, hence fix `k=2R-1`. Dirichlet's theorem gives infinitely many primes

    q == 1 (mod 2k).

For sufficiently large such `q`, write `q=2kr+1` with `r>2k`. For each such `q`, Dirichlet's theorem again supplies infinitely many primes in each of the distinct classes `gamma^(s_i) mod q`.

Thus, for every fixed `R >= 2`, there are infinitely many prime-numerator fractions `q/b` with a unique two-term Egyptian expansion and minimum support exactly `2R`.

This establishes unbounded minimum support in TWO-EGYPTIAN. It does not prove NP-hardness or provide a polynomial-time way to find the primes.

## 6. Explicit exact examples

The verification script `verify_arbitrary_index_family.py` checks the following instances by exact integer arithmetic, exhaustive signed-vector enumeration, and exact prime tests.

| R | k=2R-1 | r | q | m=kr | minimum support |
|---:|---:|---:|---:|---:|---:|
| 2 | 3 | 11 | 67 | 33 | 4 |
| 3 | 5 | 13 | 131 | 65 | 6 |
| 4 | 7 | 17 | 239 | 119 | 8 |
| 5 | 9 | 21 | 379 | 189 | 10 |

### R=3 example

Take `q=131`, `k=5`, `r=13`, `m=65`, and primitive root `gamma=2` modulo 131.

The projected sequence is

    A = (1,14,27,40,53,60) in C_65,

and its index is exactly 3. The lifted exponents are

    s = (1,79,27,105,53,60) in C_130.

Choose the six primes

    p = (2,1039,499,47,509,307),

which satisfy

    p_i mod 131 = (2,122,106,47,116,45) = 2^(s_i) mod 131.

Their product is

    b = 7,615,529,496,842 == -1 (mod 131).

Thus

    u = 58,133,812,953,
    v = 442,719,767,307,467,032,194,426,

and

    131/b = 1/u + 1/v.

The verifier finds exactly two signed exponent vectors, the all-ones and all-minus-ones vectors. Hence the minimum support is 6 and the unordered two-term expansion is unique.

## 7. Interpretation and limitations

- The index `R` is the index of the projected minimal zero-sum sequence in `C_m`; it is not itself the number of Egyptian-fraction terms.
- The Egyptian fraction always has two unit-fraction terms. The number `2R` counts distinct prime factors that must participate in the divisor witness.
- The construction proves that this support parameter is unbounded, even among fractions with prime numerator and a unique two-term expansion.
- The prime choices use Dirichlet's theorem and are not an efficient algorithm. This construction is not a deterministic or randomized NP-hardness proof.
- The zero-sum sequence construction may have antecedents in the literature; this note records the derivation and the Egyptian-fraction lift, without claiming priority for the abstract sequence alone.

## 8. Literature connection

The projected objects belong to the classical theory of minimal zero-sum sequences over finite cyclic groups. In particular, Zeng, Yuan, and Li (2016) construct index-three examples of much greater length and study long unsplittable sequences. The present construction supplies a different explicit family with length `2R` and index `R`, then adds a parity-controlled lift to the order-doubled group required by the Egyptian-fraction factor criterion.

Reference:

- Xiangneng Zeng, Pingzhi Yuan, and Yuanlin Li, “On the structure of long unsplittable minimal zero-sum sequences,” *Acta Arithmetica* 176 (2016), 131–159, DOI: 10.4064/aa8228-5-2016. See Example 5.1 for a known index-three construction and the discussion of index-one/index-two thresholds.
- Tieling Chen and Reginald Koo, “Two-term Egyptian fractions,” *Notes on Number Theory and Discrete Mathematics* 19(2) (2013), 15–25. The coprime-divisor-pair criterion is equivalent to the factor criterion used here.
