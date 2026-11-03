#!/usr/bin/env python3
"""Exact verifier for the signed-divisor-pair form of the reduction.

This verifies the algebraic construction on tiny examples. It does not
verify the analytic prime-distribution theorem or the Las Vegas runtime.
"""
from itertools import product
from math import gcd, prod


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d*d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def first_prime_in_class(c: int, modulus: int, lower: int) -> int:
    k = max(0, (lower-c+modulus-1)//modulus)
    while True:
        x = c+k*modulus
        if x >= lower and is_prime(x):
            return x
        k += 1


def build_weights(items):
    A = sum(items)
    B = 8*(A+1)
    L = sum(B**i for i in range(1, len(items)+1))
    W = 2*L+A
    weights = [(B**i, B**i+items[i-1]) for i in range(1,len(items)+1)]
    return A,B,L,W,weights


def subset_sum_yes(items, T):
    n=len(items)
    return any(sum(items[i] for i in range(n) if mask>>i & 1)==T
               for mask in range(1<<n))


def verify(items, T, h):
    A,B,L,W,weights=build_weights(items)
    assert 1 <= T <= A
    assert h%2==1 and h>2*W
    M=h*h
    omega=1+h
    assert pow(omega,h,M)==1
    # The exact order h follows from (1+h)^k == 1+kh (mod h^2);
    # test representative exponents here rather than looping over all k.
    for k in (1, 2, h//2, h-1):
        assert pow(omega,k,M)==(1+k*h)%M

    flat=[w for pair in weights for w in pair]
    assert len(set(flat))==len(flat)
    assert 0 < min(flat) <= max(flat) < W < h
    C=L+T
    assert 0<C<W<h

    classes=[pow(omega,w,M) for w in flat]+[(-pow(omega,C,M))%M]
    assert len(set(classes))==len(classes)
    assert all(gcd(c,M)==1 for c in classes)

    # Find explicit small prime representatives. This is NOT the random
    # prime-search algorithm used in the asymptotic reduction.
    primes=[first_prime_in_class(c,M,M+1) for c in classes]
    assert len(set(primes))==len(primes)
    assert all(is_prime(p) and p%M==c for p,c in zip(primes,classes))
    P=primes[:-1]
    R=primes[-1]
    D=R*prod(P)
    assert gcd(D,M)==1 and D>M

    # Verify the signed subset-product equation directly.
    flat_weights = [w for pair in weights for w in pair]
    signed_yes = any(
        sum(x*w for x, w in zip(xs, flat_weights)) == C
        for xs in product((-1, 0, 1), repeat=len(flat_weights))
    )
    assert signed_yes == subset_sum_yes(items, T)

    # Enumerate all assignments of each prime factor to d1, d2, or neither.
    # 0=neither, 1=in d1, 2=in d2.
    witnesses=[]
    for assignment in product((0,1,2), repeat=len(primes)):
        d1=prod(p for p,s in zip(primes,assignment) if s==1)
        d2=prod(p for p,s in zip(primes,assignment) if s==2)
        if gcd(d1,d2)==1 and (d1+d2)%M==0:
            witnesses.append((assignment,d1,d2))

    answer=subset_sum_yes(items,T)
    assert bool(witnesses)==answer

    expansion=None
    if witnesses:
        assignment,d1,d2=witnesses[0]
        u=D*(d1+d2)//(d1*M)
        v=D*(d1+d2)//(d2*M)
        assert D*(d1+d2)%(d1*M)==0
        assert D*(d1+d2)%(d2*M)==0
        assert u!=v and u>0 and v>0
        assert M*u*v==D*(u+v)
        expansion=(u,v)

    return {
        "items":items,"target":T,"answer":answer,"A":A,"B":B,
        "L":L,"W":W,"C":C,"h":h,"M":M,"omega":omega,
        "weights":weights,"classes":classes,"primes":primes,
        "D":D,"signed_encoding_yes":signed_yes,"witness_count":len(witnesses),
        "first_witness":witnesses[0] if witnesses else None,
        "two_term_denominators":expansion,
    }


if __name__=="__main__":
    tests=[([1],1,67),([2],1,101),([2,3,7],5,4543161)]
    for items,T,h in tests:
        result=verify(items,T,h)
        print("\n", "YES" if result["answer"] else "NO")
        for key,value in result.items():
            print(f"{key} = {value}")
