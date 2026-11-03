# Square-modulus randomized reduction: candidate proof

This note records the candidate Las Vegas reduction from SUBSET SUM to TWO-EGYPTIAN. The algebraic part is in mathematical-foundations.md; this file concerns prime selection and complexity.

## 1. Analytic input

Baier and Zhao (2006), Theorem 4, give an average estimate of the form

    sum_{q <= x^(2/9-epsilon)} q * max_{(c,q)=1}
      |psi(x;q^2,c)-x/phi(q^2)| << x/(log x)^A

for fixed positive epsilon and A. Here psi is the Chebyshev function in a reduced residue class. The paper notes that the implied constants are ineffective because Siegel-Walfisz is used. The exact theorem statement and all parameter hypotheses must be checked against the original paper before publication.

## 2. Parameters and good moduli

Construct W as in mathematical-foundations.md and set

    X=4W, Y=(4X)^6.

Choose an odd h uniformly from (X,2X), and set M=h^2. Take epsilon=1/18. Then Y^(2/9-1/18)=Y^(1/6)=4X, so h lies in the stated modulus range at endpoints Y and Y/2.

Define E_h as the maximum over reduced residue classes modulo h^2 of the two endpoint errors at Y and Y/2:

    E_h=max_c max(|psi(Y;h^2,c)-Y/phi(h^2)|,
                  |psi(Y/2;h^2,c)-Y/(2phi(h^2))|).

Applying the average theorem separately at Y and Y/2 is intended to give

    sum_{h<=2X} h E_h <<_A Y/(log Y)^A.

Call h good if E_h <= Y/(100h^2). A bad h contributes hE_h > Y/(100h) >= Y/(200X), hence the number of bad h is O_A(X/(log Y)^A). Since there are Theta(X) odd integers in (X,2X), a random odd h is good with probability 1-O_A((logY)^(-A)). The threshold is ineffective.

## 3. Prime density in every required residue class

For good h and every reduced residue class c modulo h^2, the endpoint estimates are intended to imply

    psi(Y;h^2,c)-psi(Y/2;h^2,c)
      >= Y/(2phi(h^2)) - Y/(50h^2)
      >= 0.48Y/h^2.

The total von Mangoldt contribution from proper prime powers in (Y/2,Y] is O(sqrt(Y)(logY)^2). Since h<2X and Y=(4X)^6, this is o(Y/h^2). For sufficiently large X, the number of primes in each reduced residue class in the interval is therefore at least

    0.4Y/(h^2 logY).

There are at most Y/h^2 candidate integers in that class and interval. Thus a uniformly sampled candidate is prime with probability at least 1/(4logY).

The required classes are omega^(w_{i,j}) modulo M and -omega^C modulo M. The weights are pairwise distinct and lie in (0,W), while h>2W. The first 2n classes are distinct in H=<omega>; the final class lies in -H, disjoint from H. All classes are reduced modulo M.

Sample at most K=ceil(16 logY log(8n)) candidates in each class, independently and uniformly from the integers in [Y/2,Y] in that class. If a prime is found, retain it; otherwise declare the round a failure. The failure probability for one class is at most (8n)^(-4), so by the union bound all 2n+1 classes succeed with probability greater than 3/4.

For sufficiently large X, a round succeeds with probability at least 9/16, hence at least 3/8.

## 4. Las Vegas fallback for the ineffective threshold

The theorem's constants are ineffective, so the algorithm does not know the threshold beyond which the per-round success bound holds.

Proposed repair:
1. Run at most 2n independent construction rounds.
2. If one succeeds, output M/D, where D=R*product(P_{i,j}).
3. If all rounds fail, solve the original SUBSET SUM instance by exhaustive search and output a fixed TWO-EGYPTIAN YES instance 1/2=1/3+1/6, or a fixed NO instance 3/7.

For sufficiently large instances, the probability of exhaustive fallback is at most (5/8)^(2n). The fallback costs O(2^n poly(N)), so its expected contribution is O((25/32)^n poly(N)). For instances below the unknown fixed threshold, X=4W and B>=16 imply n is bounded by an absolute constant; exhaustive fallback then has finite constant cost. This needs a formal machine-level audit.

Every successful round is checked with deterministic primality testing (e.g. AKS). Failed rounds never produce an incorrect answer.

## 5. Complexity consequence

If this Las Vegas reduction is fully validated and TWO-EGYPTIAN has a deterministic polynomial-time algorithm, then SUBSET SUM is in ZPP. Since SUBSET SUM is NP-complete and ZPP is contained in NP intersect coNP, this implies NP=coNP.

This is **not** a proof that P=NP, and it is not a standard deterministic Karp reduction. Describe the current result as a candidate Las Vegas randomized reduction pending full audit.

## 6. Outstanding checks

- Verify every hypothesis and endpoint convention in Baier-Zhao Theorem 4.
- Formalize the prime-power subtraction with explicit constants.
- Specify exact uniform sampling from the arithmetic progression inside the interval.
- Audit the finite-trial fallback as an expected-time Turing-machine bound.
- Verify that selected primes are pairwise distinct (distinct residue classes suffice).
- Produce reproducible code and exact primality certificates for sample instances.
