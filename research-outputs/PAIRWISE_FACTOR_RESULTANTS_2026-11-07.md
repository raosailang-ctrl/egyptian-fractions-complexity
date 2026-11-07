# Pairwise resultant structure of the eight central denominator factors

Date: 2026-11-07

For the central family,
D(t)=product_{i=1}^8 L_i(t), where
L=(1+3t, 1+14t, 1+60t, 1+36t, 4t-1, 1+84t, 1+15t, 1+18t).

The complete pairwise resultants are:

| i,j | Res(L_i,L_j) | i,j | Res(L_i,L_j) |
|---|---:|---|---:|
| 1,2 | -11 | 1,3 | -57 |
| 1,4 | -33 | 1,5 | -7 |
| 1,6 | -81 | 1,7 | -12 |
| 1,8 | -15 | 2,3 | -46 |
| 2,4 | -22 | 2,5 | -18 |
| 2,6 | -70 | 2,7 | -1 |
| 2,8 | -4 | 3,4 | 24 |
| 3,5 | -64 | 3,6 | -24 |
| 3,7 | 45 | 3,8 | 42 |
| 4,5 | -40 | 4,6 | -48 |
| 4,7 | 21 | 4,8 | 18 |
| 5,6 | 88 | 5,7 | 19 |
| 5,8 | 22 | 6,7 | 69 |
| 6,8 | 66 | 7,8 | -3 |

For every integer t, gcd(L_i(t),L_j(t)) divides Res(L_i,L_j). Hence a prime outside
{2,3,5,7,11,19,23} cannot divide two distinct factors. Apart from these seven fixed
primes, the prime supports of the eight linear factors are pairwise disjoint.

Also gcd(L_i(t),h(t))=1 for every i, where h=t(12t+1): each L_i divides D and
D == -1 (mod h). Thus each factor is a unit modulo h and M=h^2.

This does not yet improve the generic Wigert bound. It gives a concrete structural
starting point for the next problem: estimate the restricted divisor count
N(t)=#{d|D(t)^2 : d<=D(t), d == -D(t) mod M(t)}
using eight essentially disjoint prime supports, with only seven possible overlap primes.

Exact verification is in research-outputs/verify_pairwise_factor_resultants.py.
