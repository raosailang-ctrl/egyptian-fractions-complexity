# The minimum-term decision problem and NP membership

Define MIN-EGYPT as follows. Input: a reduced rational \(a/b\), \(0<a<b\), and an integer \(k\). Question: does \(a/b\) have an Egyptian-fraction expansion with at most \(k\) distinct unit fractions?

A recent short-Egyptian-fraction theorem gives an absolute constant \(C\) such that every sufficiently large denominator \(b\) admits an expansion with at most \(C\log\log b\) terms. See the OpenAI preprint (2026) and the human-written Bloom–van Doorn exposition (2026); neither should be confused with a peer-reviewed complexity classification.

The short-length theorem, together with the following elementary denominator bound, implies that MIN-EGYPT belongs to NP.

## Denominator bound for any m-term expansion

Suppose
\[
\frac ab=\sum_{i=1}^m\frac1{d_i},\qquad 2\le d_1<\cdots<d_m.
\]
Let \(P_j=\prod_{i=1}^j d_i\) and
\[
R_j=\frac ab-\sum_{i=1}^j\frac1{d_i}.
\]
For \(j<m\), the residual is positive and has denominator dividing \(bP_j\), hence
\[
R_j\ge\frac1{bP_j}.
\]
Since every remaining denominator is at least \(d_{j+1}\),
\[
R_j\le\frac{m-j}{d_{j+1}}.
\]
Therefore
\[
d_{j+1}\le(m-j)bP_j\le mbP_j,
\]
and
\[
P_{j+1}\le mbP_j^2.
\]
Induction from \(P_0=1\) gives
\[
P_j\le(mb)^{2^j-1}.
\]
In particular,
\[
\log_2 d_i\le(2^m-1)\log_2(mb).
\]

If \(m\le C\log_2\log_2 b\), then \(2^m\le(\log_2 b)^C\), so every denominator in such an expansion has polynomially many bits in the input length.

## NP certificate

For a YES instance, if \(k\ge C\log\log b\), use the short expansion guaranteed by the theorem; if \(k<C\log\log b\), any witness with at most \(k\) terms already has \(m=O(\log\log b)\). Thus every YES instance has a polynomial-bit certificate consisting of its denominators. Verify positivity, pairwise distinctness, and the exact rational identity by integer arithmetic.

Consequently, conditional on the cited short-expansion theorem,
\[
\boxed{\mathrm{MIN\text{-}EGYPT}\in\mathrm{NP}.}
\]
The Las Vegas reduction to TWO-EGYPTIAN is also a reduction to MIN-EGYPT with the threshold fixed at \(k=2\). This gives randomized NP-hardness for MIN-EGYPT under the same reduction convention, but not standard deterministic NP-hardness.
