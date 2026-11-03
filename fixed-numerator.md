# Fixed numerator: finite-group dynamic programming and known criteria

Fix a positive integer \(a\). Let \(T_a\) be the language of denominators \(b>a\), \(\gcd(a,b)=1\), for which \(a/b\) is a sum of two distinct unit fractions.

By the factor criterion, this is equivalent to existence of
\[
r\mid b^2,\quad r\ne b,\quad r\equiv-b\pmod a.
\]

## 1. Dynamic programming given the factorization of b

Suppose
\[
b=\prod_{i=1}^{s}p_i^{\alpha_i}.
\]
Every divisor of \(b^2\) has the form
\[
r=\prod_i p_i^{e_i},\qquad 0\le e_i\le2\alpha_i.
\]
All \(p_i\) are units modulo \(a\).

Use states \(DP_i(g,\delta)\), where:
- \(g\in(\mathbb Z/a\mathbb Z)^*\) is the product residue after the first \(i\) prime powers;
- \(\delta=1\) means at least one chosen exponent differs from the central exponent \(\alpha_j\).

Initialize \(DP_0(1,0)=1\). For each prime power, transition over \(e=0,\ldots,2\alpha_i\):
\[
g'=gp_i^e\pmod a,\qquad
\delta'=\delta\lor(e\ne\alpha_i).
\]
A proper divisor with target residue exists exactly when
\[
DP_s(-b\bmod a,1)=1.
\]
The flag excludes the unique central exponent vector \((\alpha_1,\ldots,\alpha_s)\), which represents \(r=b\).

The number of group operations is
\[
O\left(\varphi(a)\sum_i(2\alpha_i+1)\right)=O_a(\log b).
\]
For variable \(a\), this is pseudo-polynomial in \(a\), not polynomial in \(\log a\).

## 2. Membership in NP ∩ coNP for fixed a

- **YES certificate:** a divisor \(r\mid b^2\) with \(r\ne b\) and \(r\equiv-b\pmod a\). Its bit length is at most \(2\log_2b+O(1)\).
- **NO certificate:** a complete prime factorization of \(b\). The verifier checks each listed prime using a deterministic polynomial-time primality test, checks the product, and runs the finite-state DP. If no noncentral exponent vector reaches \(-b\pmod a\), the instance is NO.

The factorization certificate has polynomial bit length. Therefore, for each fixed \(a\),
\[
\boxed{T_a\in NP\cap coNP.}
\]
This does not prove \(T_a\in P\), because finding the factorization of \(b\) is not known to have a deterministic polynomial-time algorithm in general.

## 3. Known special numerators in the literature

Chen and Koo (2013), Theorems 9–10, prove the following:

- If every prime factor of \(b\) is congruent to \(\pm1\pmod a\), then \(a/b\) has a proper two-term expansion if and only if \(b\) has a prime factor congruent to \(-1\pmod a\).
- In particular, for reduced fractions:
\[
\frac3b\text{ has a two-term expansion}\iff b\text{ has a prime factor }\equiv2\pmod3,
\]
\[
\frac4b\text{ has a two-term expansion}\iff b\text{ has a prime factor }\equiv3\pmod4,
\]
\[
\frac6b\text{ has a two-term expansion}\iff b\text{ has a prime factor }\equiv5\pmod6.
\]

These special-numerator criteria are established literature, not new results of this project. The general fixed-a NP∩coNP observation is an algorithmic consequence of the factor criterion and finite-group DP; its novelty should be checked against the literature before publication.

Reference: Chen and Koo, “Two-term Egyptian fractions,” *Notes on Number Theory and Discrete Mathematics* 19(2), 2013, pp. 15–25, especially Theorems 4 and 9–10.
