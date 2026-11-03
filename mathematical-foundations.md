# Mathematical foundations

## 1. Exact criterion for two distinct unit fractions

Let 0 < a < b and gcd(a,b)=1. Then

    a/b = 1/u + 1/v, with u,v positive and u != v

if and only if there is a positive integer r such that

    r | b^2,   r != b,   r == -b (mod a).

### Forward direction

From auv=b(u+v), obtain

    (au-b)(av-b)=b^2.

Put r=au-b and s=av-b. Since each unit fraction is smaller than a/b, r,s are positive. Thus rs=b^2 and r == -b (mod a). If r=b, then s=b as rs=b^2, hence u=v, a contradiction.

### Reverse direction

Given r|b^2, set s=b^2/r. Since r == -b (mod a) and gcd(a,b)=1, r is invertible modulo a, and

    s == b^2*(-b)^(-1) == -b (mod a).

Define u=(r+b)/a and v=(s+b)/a. These are positive integers. The identity rs=b^2 implies auv=b(u+v), hence a/b=1/u+1/v. Since r != b, r != s and u != v.

## 2. TWO-EGYPTIAN is in NP

A certificate can be r. Since r|b^2, 1 <= r <= b^2, so its binary length is O(log b). Verify divisibility, congruence, and r != b in polynomial time.

## 3. Ternary-exponent encoding of SUBSET SUM

Take a positive-integer SUBSET SUM instance a_1,...,a_n,T, with A=sum(a_i) and 1 <= T <= A. Set

    B=8(A+1), L=sum_{i=1}^n B^i, W=2L+A, S=L+T,
    w_{i,0}=B^i, w_{i,1}=B^i+a_i.

Then

    exists e_{i,j} in {0,1,2}:
    sum_i(e_{i,0}w_{i,0}+e_{i,1}w_{i,1})=S

if and only if the original SUBSET SUM instance is YES.

### Proof

Expanding gives

    sum_i c_i B^i + delta = 0,

where c_i=e_{i,0}+e_{i,1}-1 is in {-1,0,1,2,3}, and delta=sum_i e_{i,1}a_i-T, with |delta|<=2A.

If k is the largest index with c_k != 0, then

    B^k <= |c_k|B^k <= 3 sum_{i<k}B^i + 2A < B^k,

contradiction. The last strict inequality follows from B=8(A+1). Thus every c_i=0, so e_{i,0}+e_{i,1}=1. Each pair is either (1,0) or (0,1), and delta=0 says exactly that the selected a_i sum to T. The converse is immediate.

## 4. Odd-square cyclic subgroup

For any odd integer h>1, set M=h^2 and omega=1+h. By the binomial theorem,

    (1+h)^k == 1+kh (mod h^2).

Thus omega^h == 1 (mod h^2), while no 0<k<h gives 1. Therefore ord_{h^2}(omega)=h. Every power of omega is 1 modulo h, whereas -1 is not 1 modulo h for odd h>1. Hence -1 is not in H=<omega>.

## 5. Algebraic encoding, conditional on prime selection

Let h>2W be odd and put C=h+S-W. Suppose there are pairwise distinct primes P_{i,j},R, all coprime to M=h^2, satisfying

    P_{i,j} == omega^(w_{i,j}) (mod M),
    R == -omega^C (mod M).

Let D=R*product(P_{i,j}). Then

    D == -omega^(C+W) == -omega^(h+S) == -omega^S (mod M).

Because D is square-free, every divisor of D^2 has a unique form

    r=R^e0 * product(P_{i,j}^e_{i,j}),

where all exponents belong to {0,1,2}. The condition r == -D (mod M) is equivalent to

    (-1)^e0 * omega^(e0*C + sum(e_{i,j}w_{i,j})) == omega^S.

Since H and -H are disjoint, e0 is 0 or 2.

- If e0=0, the exponent congruence gives sum(e_{i,j}w_{i,j})=S, since both sides lie in [0,2W] and h>2W.
- If e0=2, it gives sum(e_{i,j}w_{i,j})=2W-S. Replacing every exponent by 2-e_{i,j} gives a solution of sum S.

Thus

    exists r|D^2, r == -D (mod M)

if and only if

    exists e_{i,j} in {0,1,2}: sum(e_{i,j}w_{i,j})=S.

The factor criterion then yields SUBSET SUM YES iff M/D is a sum of two distinct unit fractions.

This is a proved algebraic implication **provided the required primes can be generated**. It is not by itself a polynomial-time reduction.
