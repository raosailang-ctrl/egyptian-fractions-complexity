# Square-modulus Las Vegas reduction: current proof draft

This note combines the algebraic reduction in `mathematical-foundations.md` with a randomized prime-selection procedure. The aim is an expected-polynomial-time, zero-error many-one reduction from SUBSET SUM to TWO-EGYPTIAN. This is not a standard deterministic Karp reduction.

## 1. Analytic input: Baier–Zhao Theorem 4

Baier and Zhao (2006), Theorem 4, state that for every fixed \(\varepsilon>0\) and \(A>0\),
\[
\sum_{q\le x^{2/9-\varepsilon}}q\max_{(c,q)=1}
\left|\psi(x;q^2,c)-\frac{x}{\varphi(q^2)}\right|
\ll_{\varepsilon,A}\frac{x}{(\log x)^A}.
\]
Here \(\psi\) is the von Mangoldt Chebyshev function. The paper explicitly notes that the implied constants in Theorems 2 and 4 are ineffective because of Siegel–Walfisz input. See `references.md`.

## 2. Parameters and good moduli

Construct \(W\) as in `mathematical-foundations.md` and put
\[
X=4W,\qquad Y=(4X)^6.
\]
Choose an odd integer \(h\) uniformly from \((X,2X)\), and set \(M=h^2\). Take \(\varepsilon=1/18\), so \(2/9-\varepsilon=1/6\). We have
\[
Y^{1/6}=4X,\qquad (Y/2)^{1/6}=4X/2^{1/6}>2X.
\]
Thus every \(h\in(X,2X)\) is in the theorem's range at both endpoints \(Y\) and \(Y/2\).

Let \(E_h\) be the maximum over reduced classes modulo \(h^2\) of the two endpoint errors:
\[
E_h=\max_{(c,h)=1}\max\left\{
\left|\psi(Y;h^2,c)-\frac{Y}{\varphi(h^2)}\right|,
\left|\psi(Y/2;h^2,c)-\frac{Y}{2\varphi(h^2)}\right|
\right\}.
\]
Applying Theorem 4 separately at \(Y\) and \(Y/2\), and using \(\max(x,y)\le x+y\), gives
\[
\sum_{h\le2X}hE_h\ll_A\frac{Y}{(\log Y)^A}.
\]
Call \(h\) good if \(E_h\le Y/(100h^2)\). If \(h\) is bad, then
\[
hE_h>\frac{Y}{100h}\ge\frac{Y}{200X}.
\]
Consequently the number of bad \(h\le2X\) is \(O_A(X/(\log Y)^A)\). There are \(\asymp X\) odd integers in \((X,2X)\), so a uniformly random odd \(h\) is good with probability \(1-O_A((\log Y)^{-A})\). For sufficiently large \(X\), this is at least \(3/4\). The threshold is ineffective.

## 3. Every reduced residue class contains many primes for a good h

For good \(h\), and every \((c,h)=1\),
\[
\begin{aligned}
\psi(Y;h^2,c)-\psi(Y/2;h^2,c)
&\ge\frac{Y}{2\varphi(h^2)}-\frac{Y}{50h^2}\\
&\ge0.48\frac{Y}{h^2},
\end{aligned}
\]
using \(\varphi(h^2)\le h^2\).

The total von Mangoldt contribution of proper prime powers in \((Y/2,Y]\), over all residue classes, is \(O(\sqrt Y(\log Y)^2)\). Since \(h<2X\) and \(Y=(4X)^6\),
\[
\frac{Y}{h^2}\ge\frac{Y}{4X^2}=1024X^4,
\]
whereas \(\sqrt Y(\log Y)^2=O(X^3(\log X)^2)=o(X^4)\). For sufficiently large \(X\), after removing prime powers, the prime contribution is at least \(0.4Y/h^2\). Dividing by \(\log Y\), the number of primes in each reduced class in \([Y/2,Y]\) is at least
\[
\frac{0.4Y}{h^2\log Y}.
\]
There are at most \(Y/h^2\) candidate integers in that progression and interval. Hence a uniformly sampled candidate is prime with probability at least \(1/(4\log Y)\).

## 4. The required classes and the randomized search

Let \(\omega=1+h\), of order exactly \(h\) modulo \(M=h^2\), and let \(C=L+T\). The required classes are
\[
\omega^{w_{i,j}}\pmod M\quad(1\le i\le n,\ j\in\{0,1\}),
\qquad -\omega^C\pmod M.
\]
The \(2n\) weights are distinct and lie in \((0,W)\subset(0,h)\), so their powers are distinct in \(H=\langle\omega\rangle\). The special class lies in \(-H\), disjoint from \(H\) because \(h\) is odd. All classes are reduced.

For each class, sample independently and uniformly from the integers in \([Y/2,Y]\) in that class, and test candidates for primality using a deterministic polynomial-time primality test (e.g. AKS). Use at most
\[
K=\left\lceil16\log Y\log(8n)\right\rceil
\]
candidates per class. For a good \(h\), the probability of failing to find a prime in one class is at most
\[
\left(1-\frac1{4\log Y}\right)^K\le(8n)^{-4}.
\]
By the union bound, all \(2n+1\) classes succeed with probability greater than \(3/4\).

Combining this with the probability of a good \(h\), one round succeeds with probability at least \(9/16\), and hence at least \(3/8\), for all sufficiently large instances.

If all classes succeed, their prime representatives are automatically pairwise distinct because the residue classes are distinct. They are all coprime to \(M\). Since each is at least \(Y/2>4X^2>M\), their product \(D\) is larger than \(M\), so \(M/D\) is a reduced proper fraction.

## 5. Ineffective constants and exact fallback

The theorem's constants are ineffective, so the algorithm does not know the threshold beyond which the per-round success probability is at least \(3/8\).

Use the following fixed machine:
1. Run at most \(2n\) independent construction rounds.
2. If a round succeeds, output \(M/D\).
3. If all rounds fail, solve SUBSET SUM by exhaustive search and output the fixed TWO-EGYPTIAN YES instance \(1/2=1/3+1/6\), or the fixed NO instance \(3/7\), according to the exact answer.

For sufficiently large instances, the probability of reaching fallback is at most \((5/8)^{2n}\). Exhaustive search costs \(O(2^n\operatorname{poly}(N))\), so its expected contribution is
\[
O\left(2^n(5/8)^{2n}\operatorname{poly}(N)\right)
=O\left((25/32)^n\operatorname{poly}(N)\right).
\]
For instances below the unknown fixed threshold, \(X=4W\ge8B^n\) and \(B\ge16\), so \(n\) and \(A\) are bounded by absolute constants; these form a finite family, and exhaustive fallback has bounded cost. The algorithm does not need to know the threshold.

Every successful round is checked exactly, and fallback is exact. Thus the proposed reduction has zero error and expected polynomial running time. The finite-fallback argument should still be written in formal machine-level detail before publication.

## 6. Complexity consequence

If this Las Vegas expected-polynomial-time many-one reduction is fully validated, then a deterministic polynomial-time algorithm for TWO-EGYPTIAN would put SUBSET SUM in ZPP. Since SUBSET SUM is NP-complete and \(\mathrm{ZPP}\subseteq\mathrm{NP}\cap\mathrm{coNP}\), this implies \(\mathrm{NP}=\mathrm{coNP}\).

This does **not** prove \(\mathrm P=\mathrm{NP}\), and the reduction is not a standard deterministic Karp reduction. Describe the result as NP-hardness under a Las Vegas randomized reduction, not standard NP-completeness.

## 7. Remaining proof audit

- Verify the exact endpoint conventions and constants in Baier–Zhao Theorem 4.
- Formalize the proper-prime-power bound with explicit constants.
- Specify unbiased finite sampling from each progression.
- Formalize the finite-round fallback as an expected-time Turing machine.
- Reproduce the small exact experiments with committed code and primality certificates.
