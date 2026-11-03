# Mathematical foundations

## 1. Two-term Egyptian fractions: factor criterion

Let \(0<a<b\), \(\gcd(a,b)=1\). Then
\[
\frac ab=\frac1u+\frac1v,\qquad u,v\in\mathbb Z_{>0},\ u\ne v,
\]
if and only if there is a positive integer \(r\) such that
\[
r\mid b^2,\qquad r\ne b,\qquad r\equiv-b\pmod a.
\]

### Proof

From \(auv=b(u+v)\),
\[
(au-b)(av-b)=b^2.
\]
Set \(r=au-b\), \(s=av-b\). Since each unit fraction is strictly smaller than \(a/b\), both are positive. Thus \(rs=b^2\) and \(r\equiv-b\pmod a\). If \(r=b\), then \(s=b\), hence \(u=v\), contrary to the hypothesis.

Conversely, given such an \(r\), set \(s=b^2/r\). Since \(r\equiv-b\pmod a\) and \(\gcd(a,b)=1\),
\[
s\equiv b^2(-b)^{-1}\equiv-b\pmod a.
\]
Thus \(u=(r+b)/a\) and \(v=(s+b)/a\) are positive integers. The identity \(rs=b^2\) gives \(auv=b(u+v)\), hence the desired fraction identity. Since \(r\ne b\), also \(s\ne r\), so \(u\ne v\).

## 2. Equivalent coprime-divisor-pair criterion

The preceding condition is equivalent to
\[
\boxed{\exists d_1,d_2\mid b:\quad \gcd(d_1,d_2)=1,\quad a\mid(d_1+d_2).}
\]
For \(a>2\), such a pair is automatically nontrivial and gives distinct unit fractions.

To see the equivalence, write \(g=\gcd(r,b)\), \(d_1=b/g\), \(d_2=r/g\). From \(r\mid b^2\), one obtains \(d_1,d_2\mid b\) and \(\gcd(d_1,d_2)=1\). Also \(r=bd_2/d_1\). The congruence \(r\equiv-b\pmod a\), after multiplying by \(d_1\) and cancelling \(b\), is exactly \(d_1+d_2\equiv0\pmod a\). The converse follows by setting \(r=bd_2/d_1\).

This is Chen–Koo (2013), Theorem 4, and is a particularly useful form for the reduction below.

## 3. TWO-EGYPTIAN is in NP

A YES certificate can be \(r\), with \(r\le b^2\), or a pair \((d_1,d_2)\) of divisors of \(b\). Each has polynomial bit length. Verify divisibility, gcd, and the required congruence in polynomial time.

## 4. Ternary-exponent encoding (earlier formulation)

For positive SUBSET SUM input \(a_1,\ldots,a_n,T\), put \(A=\sum_i a_i\), \(B=8(A+1)\), \(L=\sum_{i=1}^nB^i\), and \(w_{i,0}=B^i\), \(w_{i,1}=B^i+a_i\). The bounded-exponent equation with exponents in \(\{0,1,2\}\) can encode SUBSET SUM. The signed formulation below is cleaner for the divisor-pair criterion and is the current preferred proof.

## 5. Preferred signed SUBSET SUM encoding

Assume \(1\le T\le A\). Define
\[
B=8(A+1),\qquad L=\sum_{i=1}^nB^i,
\]
\[
w_{i,0}=B^i,\qquad w_{i,1}=B^i+a_i,
\qquad W=\sum_{i,j}w_{i,j}=2L+A,
\]
and set
\[
C=L+T.
\]
Then
\[
\boxed{\exists x_{i,j}\in\{-1,0,1\}:\quad
\sum_{i,j}x_{i,j}w_{i,j}=C}
\]
if and only if the SUBSET SUM instance has a subset summing to \(T\).

### Proof

Expanding the signed equation gives
\[
\sum_i c_iB^i+\delta=0,
\]
where
\[
c_i=x_{i,0}+x_{i,1}-1\in\{-3,-2,-1,0,1\},
\qquad \delta=\sum_i x_{i,1}a_i-T.
\]
Since \(x_{i,1}\in\{-1,0,1\}\), we have \(|\delta|\le A+T\le2A\).

If \(k\) is the largest index with \(c_k\ne0\), then
\[
B^k\le |c_k|B^k\le3\sum_{i<k}B^i+2A<B^k,
\]
a contradiction. The final strict inequality follows from \(B=8(A+1)\):
\[
3\sum_{i<k}B^i+2A
<\left(\frac3{B-1}+\frac{2A}{B}\right)B^k<B^k.
\]
Thus every \(c_i=0\), so \(x_{i,0}+x_{i,1}=1\). The only possibilities are \((x_{i,0},x_{i,1})=(1,0)\) or \((0,1)\). Hence \(x_{i,1}\in\{0,1\}\), and \(\delta=0\) says exactly that the selected \(a_i\)'s sum to \(T\). The converse is obtained by setting \((x_{i,0},x_{i,1})=(0,1)\) for selected indices and \((1,0)\) otherwise.

The weights are pairwise distinct: for each \(i\),
\[
B^i < B^i+a_i\le B^i+A < B^{i+1},
\]
so the two weights for index \(i\) lie strictly between the corresponding blocks for adjacent indices.

## 6. Odd-square cyclic subgroup

For any odd integer \(h>1\), set
\[
M=h^2,\qquad \omega=1+h.
\]
The binomial theorem gives
\[
(1+h)^k\equiv1+kh\pmod{h^2}.
\]
Thus \(\omega^h\equiv1\pmod{h^2}\), while no \(0<k<h\) gives 1. Hence
\[
\operatorname{ord}_{h^2}(\omega)=h.
\]
Every element of \(H=\langle\omega\rangle\) is 1 modulo \(h\), whereas \(-1\not\equiv1\pmod h\). Therefore
\[
H\cap(-H)=\varnothing.
\]

## 7. Algebraic reduction using coprime divisor pairs

Take \(h>2W\) odd, set \(M=h^2\), \(\omega=1+h\), and \(C=L+T\). Suppose there are pairwise distinct primes \(P_{i,j},R\), all coprime to \(M\), satisfying
\[
P_{i,j}\equiv\omega^{w_{i,j}}\pmod M,
\qquad R\equiv-\omega^C\pmod M.
\]
Let
\[
D=R\prod_{i,j}P_{i,j}.
\]
Then \(M<D\) if the primes are chosen above \(M\), and \(\gcd(M,D)=1\).

By the coprime-divisor-pair criterion, \(M/D\) has a proper two-term Egyptian fraction exactly when there are coprime divisors \(d_1,d_2\mid D\) with \(M\mid d_1+d_2\).

Because every \(P_{i,j}\) lies in \(H\), while \(R\) lies in \(-H\), exactly one of \(d_1,d_2\) must contain \(R\): if neither did, their ratio would lie in \(H\) and could not equal \(-1\); both cannot contain \(R\) because they are coprime. Swap them if necessary so that \(R\mid d_1\).

Let \(I\) be the indices whose primes are assigned to \(d_1\), and \(J\) those assigned to \(d_2\). The sets are disjoint. Then
\[
\frac{d_1}{d_2}\equiv-\omega^{C+\sum_{I}w_{i,j}-\sum_{J}w_{i,j}}\pmod M.
\]
The condition \(d_1+d_2\equiv0\pmod M\) is equivalent to \(d_1/d_2\equiv-1\), hence
\[
\sum_Jw_{i,j}-\sum_Iw_{i,j}\equiv C\pmod h.
\]
Put \(x_{i,j}=1\) on \(J\), \(-1\) on \(I\), and 0 otherwise. Then \(x_{i,j}\in\{-1,0,1\}\), and
\[
\left|\sum_{i,j}x_{i,j}w_{i,j}\right|\le W.
\]
Since \(C=L+T\) satisfies \(0<C<W\), and \(h>2W\), the congruence forces the integer equality
\[
\sum_{i,j}x_{i,j}w_{i,j}=C.
\]
By Section 5 this is equivalent to SUBSET SUM.

Conversely, a signed solution from Section 5 assigns exactly one prime from each pair \((P_{i,0},P_{i,1})\) to \(d_2\), with the other prime unused, and takes \(d_1=R\). Then \(d_1/d_2\equiv-1\pmod M\), so \(M\mid d_1+d_2\). Thus
\[
\boxed{\text{SUBSET SUM YES}\iff M/D\text{ is a sum of two distinct unit fractions}.}
\]

This algebraic reduction is proved **conditional on constructing the specified primes**. The randomized prime-search route is recorded separately.
