#!/usr/bin/env python3
"""Pure-Python exact proof certificate: eight-block divisor rigidity for t>=3.

This checks a bounded residual search after a symbolic elementary reduction.
For e_i in {0,1,2}, if P_e(t)+D(t) is divisible by M(t), then
  - t^2 divides P_e(t)+D(t) and (12t+1) divides it;
  - t>=3 forces e_5 even;
  - t| q_1(e) with |q_1(e)|<=234;
  - (12t+1)|numerator(P_e(-1/12)+D(-1/12)).
The only vectors with q_1=0 and this numerator 0 are the two canonical ones.
Every other vector has t<=234. We sieve all these bounded candidates and
check the exact congruence modulo M. No noncanonical vector survives.

The result DOES NOT cover arbitrary divisors of D^2; only whole blocks L_i^e_i.
"""
from collections import Counter
from fractions import Fraction
from itertools import product
from math import prod

A = (3,14,60,36,-4,84,15,18)
VALUES_AT_MINUS_ONE_TWELFTH = (
    Fraction(3,4), Fraction(-1,6), Fraction(-4), Fraction(-2),
    Fraction(-4,3), Fraction(-6), Fraction(-1,4), Fraction(-1,2)
)
CANONICAL = {
    (0,0,0,0,2,2,2,2), # G^2
    (2,2,2,2,0,0,0,0), # F^2
}


def blocks(t):
    return (1+3*t, 1+14*t, 1+60*t, 1+36*t,
            4*t-1, 1+84*t, 1+15*t, 1+18*t)


def jets(e):
    """For e_5 even: Q(0)=0, Q'(0)=q_1, Q(-1/12)=C rational."""
    q1 = sum(v*w for v,w in zip(e,A)) - 226
    root = prod((v**w for v,w in zip(VALUES_AT_MINUS_ONE_TWELFTH,e)),
                start=Fraction(1)) - 1
    return q1, root


def main():
    # Product and derivative at t=0 of D=(4t-1)*product(1+a_i*t).
    assert sum(A[i] for i in range(8) if i != 4) == 230
    assert prod(VALUES_AT_MINUS_ONE_TWELFTH) == -1
    assert len(CANONICAL) == 2

    # Odd e5: P_e(0)+D(0)=-2, hence t|2. Thus no t>=3.
    # Even e5: Q(0)=0, and Q'(0)=sum e_i a_i-226;
    # t^2|Q(t) => t|Q'(0). Moreover |Q'(0)|<=234.
    stage2 = Counter()
    candidates = []
    stationary = []
    zero_at_root = 0
    q1_zero = 0

    for e in product(range(3), repeat=8):
        if e[4] % 2:
            continue
        q1, C = jets(e)
        assert abs(q1) <= 234
        if q1 == 0:
            q1_zero += 1
        if C == 0:
            zero_at_root += 1
        if q1 == 0 and C == 0:
            stationary.append(e)
            continue
        # If q1!=0, t<=234. If q1=0 and C!=0, the bounded
        # numerator of C imposes a finite t-bound as well.
        for t in range(3,235):
            if q1 % t:
                continue
            H = 12*t+1
            # Numerator denominator has only prime factors 2 and 3,
            # so gcd(denominator, H)=1.
            numerator = C.numerator
            if numerator and numerator % H:
                continue
            stage2[t] += 1
            candidates.append((t,e))

    assert set(stationary) == CANONICAL
    assert q1_zero == 18, q1_zero
    assert zero_at_root == 64, zero_at_root
    assert len(candidates) == 332, len(candidates)
    assert len(stage2) == 62, len(stage2)

    # Infinite tail t>=235 is already covered by the jets above:
    # for q1!=0, t<=234; for q1=0 and C!=0, the 16 rational
    # C's have numerators |numerator|<=259, while 12*235+1>259.
    max_num_stationary_nonzero = max(
        abs(jets(e)[1].numerator)
        for e in product(range(3), repeat=8)
        if e[4] % 2 == 0 and jets(e)[0] == 0 and jets(e)[1] != 0
    )
    assert max_num_stationary_nonzero == 259
    assert 12*235+1 > max_num_stationary_nonzero

    # The residual 332 candidates are rejected by full M-divisibility.
    for t,e in candidates:
        L = blocks(t)
        D = prod(L)
        M = (t*(12*t+1))**2
        val = prod(v**w for v,w in zip(L,e))
        assert (val+D) % M != 0, (t,e)
    print('JET_0_PRIME_FILTER: PASS: e5 even and |q1|<=234')
    print(f'FIRST_DERIVATIVE_ZERO_COUNT: {q1_zero}')
    print(f'ROOT_VALUE_ZERO_COUNT: {zero_at_root}')
    print(f'DOUBLE_JET_ZERO_EXACTLY_CANONICAL: {len(stationary)}')
    print(f'MAX_NONCANONICAL_ZERO_Q1_ROOT_NUMERATOR: {max_num_stationary_nonzero}')
    print(f'FINITE_NECESSARY_CANDIDATES: {len(candidates)} across {len(stage2)} t-values')
    print('RESIDUAL_FULL_M_EXCLUSION: PASS (332 / 332 excluded)')
    print('BLOCK_DIVISOR_RIGIDITY_FOR_ALL_t_GE_3: PASS')

    # Show exact number of block divisor representations at t=1,2
    # and independent spot checks at t=3,7,234.
    for t in (1,2,3,7,234):
        L = blocks(t); D=prod(L); M=(t*(12*t+1))**2
        matches=[]
        values=[]
        for e in product(range(3),repeat=8):
            v=prod(x**w for x,w in zip(L,e))
            if v<=D and (v+D)%M==0:
                matches.append(e)
                values.append(v)
        expected={1:28,2:5,3:1,7:1,234:1}[t]
        distinct_expected={1:20,2:3,3:1,7:1,234:1}[t]
        assert len(matches)==expected,(t,len(matches))
        assert len(set(values))==distinct_expected,(t,len(set(values)))
        if t>=3:assert matches == [(0,0,0,0,2,2,2,2)]
        print(f't={t}: {len(matches)} qualifying block vectors, {len(set(values))} distinct values')

if __name__=='__main__':
    main()