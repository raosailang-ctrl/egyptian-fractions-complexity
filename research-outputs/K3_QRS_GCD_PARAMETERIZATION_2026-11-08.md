# K3 中心埃及分数族的 gcd–互素因子参数化与新渐近上界

**日期：** 2026-11-08  
**研究对象：** 中心共振模板 (a,b,c)=(1/6,4,2)。  
**结论性质：** 一般整数分解的精确双射；利用模平方根数量得到的新渐近上界；对 3<=t<=1000 的精确实例复核。  
**限制：** 不证明全部普通整数分解唯一；不宣称算法为多项式时间。

## 摘要

此前普通两项单位分数分解已对应到约数 d|D²，满足 d<=D 与 d≡-D (mod M)。本轮进一步把每个分解精确改写为

\[
D=qrs,\qquad (r,s)=1,\qquad r+s=kM,
\]

其中 q,k,r,s 为正整数。对应分母恰为

\[
\boxed{\{u,v\}=\{qkr,qks\}},\qquad \boxed{\gcd(u,v)=qk}.
\]

由此得到新的模平方根筛选。固定 q|D 后，r 必须满足

\[
r^2\equiv-D/q\pmod M.
\]

因为 D=FG 且 F+G=1260M，故 D<=630²M²，进而 r<=630M。模 M 的单位平方根至多 4·2^{ω(M)} 个，每个剩余类在 [1,630M] 内至多有630个代表。因此

\[
\boxed{N(t)\le2520\,\tau(D(t))\,2^{\omega(M(t))}.}
\]

又因 M=[t(12t+1)]²、gcd(t,12t+1)=1，ω(M)=ω(t)+ω(12t+1)≤(2+o(1))log t/loglog t。结合 Wigert 的 τ(D) 最大阶和 deg D=8，得到

\[
\boxed{\log N(t)\le(10\log2+o(1))\frac{\log t}{\log\log t}.}
\]

新常数 10log2≈6.93147，比上一轮 8log3≈8.78890 低约21.1%。这是本轮真正利用同余条件得到的上界改进；τ 与 ω 的最大阶仍是经典数论工具。

## 1. 中心构造和约数双射

令

\[
\begin{aligned}
L_1&=1+3t,&L_2&=1+14t,&L_3&=1+60t,&L_4&=1+36t,\\
L_5&=4t-1,&L_6&=1+84t,&L_7&=1+15t,&L_8&=1+18t,\\
F&=L_1L_2L_3L_4,&G&=L_5L_6L_7L_8,\\
D&=FG,&h&=t(12t+1),&M&=h^2.
\end{aligned}
\]

既有恒等式为

\[
F+G=1260M,\qquad D\equiv-1\pmod h,\qquad \gcd(D,M)=1.
\]

对 M/D=1/u+1/v，取 u<=v，定义 d=Mu-D、e=Mv-D，则

\[
de=D^2,\quad d\le e,\quad d\equiv e\equiv-D\pmod M.
\tag{1}
\]

因此

\[
N(t)=\#\{d\mid D^2:d\le D,\ d\equiv-D\pmod M\}.
\tag{2}
\]

## 2. 精确参数化定理

**定理 2.1（gcd–互素因子双射）。** 设 M,D 为互素正整数且 M>2。所有正整数无序分解 M/D=1/u+1/v，与满足

\[
qrs=D,\quad q,r,s>0,\quad \gcd(r,s)=1,\quad M\mid r+s
\tag{3}
\]

的三元组 (q,{r,s}) 一一对应。若 k=(r+s)/M，则

\[
\boxed{\{u,v\}=\{qkr,qks\}},\qquad \boxed{\gcd(u,v)=qk}.
\tag{4}
\]

**证明。** 由 (1) 令 q=gcd(d,e)。对每个素数 p，若 v_p(D)=a、v_p(d)=b，则 v_p(e)=2a-b，故 v_p(q)=min(b,2a-b)<=a，因而 q|D。并且 d/q、e/q 的每个素数指数中，一个为0，另一个为偶数，所以存在正整数 r,s 使 d=qr²、e=qs²、gcd(r,s)=1、qrs=D。

因 gcd(q,M)=1，且 gcd(r,M)=1，由 d≡-D=-qrs (mod M) 得 qr²≡-qrs (mod M)，约去 qr 得 r+s≡0 (mod M)。令 k=(r+s)/M，则

\[
u=(D+d)/M=qr(r+s)/M=qkr,
\]
\[
v=(D+e)/M=qs(r+s)/M=qks.
\]

反过来，若 (3) 成立，令 u=qkr、v=qks，则

\[
1/u+1/v=(r+s)/(qkrs)=M/(qrs)=M/D.
\]

两构造互逆，证毕。

此外 gcd(k,rs)=1：若素数同时整除 k 与 r，则由 r+s=kM 可知它也整除 s，与 gcd(r,s)=1 矛盾。

## 3. 直接推论

### 3.1 精确组合上界

固定 q|D，令 R=D/q。因 gcd(r,s)=1 且 rs=R，每个完整素数幂必须整体分配给 r 或 s。若 R>1，无序分配数为 2^{ω(R)-1}；R=1 时 r=s=1，但 r+s=2 不被 M>2 整除。因此

\[
N(M,D)\le\sum_{q\mid D,\ q<D}2^{\omega(D/q)-1}.
\]

又

\[
\sum_{q\mid D}2^{\omega(D/q)}
=\prod_{p^a\parallel D}(1+2a)=\tau(D^2),
\]

故

\[
\boxed{N(M,D)\le\frac{\tau(D^2)-1}{2}.}
\tag{5}
\]

### 3.2 模平方根筛与新渐近上界

固定 q|D，令 R=D/q。由 rs=R、r+s≡0 (mod M) 得

\[
r^2\equiv-R\pmod M.
\tag{6}
\]

因 gcd(R,M)=1，右侧是单位。对奇素数幂，单位平方根同余至多有2根；对2的幂至多4根。由 CRT，模 M 的根数至多 4·2^{ω(M)}。

另一方面，

\[
D=FG\le((F+G)/2)^2=(630M)^2,
\]

而 r<=sqrt(R)<=sqrt(D)，故 1<=r<=630M。每个非零模 M 剩余类在该区间内至多有630个正整数代表。每个 q 因而至多对应 2520·2^{ω(M)} 个 r，且 s=R/r 唯一确定。q 的选择数为 τ(D)，于是

\[
\boxed{N(t)\le2520\,\tau(D(t))\,2^{\omega(M(t))}.}
\tag{7}
\]

经典最大阶估计为

\[
\log\tau(n)\le(\log2+o(1))\frac{\log n}{\log\log n},\qquad
\omega(n)\le(1+o(1))\frac{\log n}{\log\log n}.
\]

D(t)=8230118400t^8+O(t^7)，故 log τ(D(t))≤(8log2+o(1))logt/loglogt。又 M=h²、gcd(t,12t+1)=1，故

\[
\omega(M)=\omega(t)+\omega(12t+1)
\le(2+o(1))\frac{\log t}{\log\log t}.
\]

代入 (7) 得

\[
\boxed{\log N(t)\le(10\log2+o(1))\frac{\log t}{\log\log t}.}
\tag{8}
\]

此上界比 8log3 的系数低约21.1%。它确实利用了平方根同余条件；但经典最大阶工具本身并非本项目原创。

## 4. 标准表示与真实非标准样本

对标准分解 d=G²、e=F²，令 g=gcd(F,G)，则 q0=g²、r0=G/g、s0=F/g、k0=1260/g。标准分母 gcd 为 q0k0=1260g。

| t | 类型 | q | r | s | k | gcd(u,v)=qk |
|---:|---|---:|---:|---:|---:|---:|
| 7 | 标准 | 324 | 11,893,677 | 12,888,073 | 70 | 22,680 |
| 7 | 非标准 | 16,814,886 | 81 | 36,464,494 | 103 | 1,731,933,258 |
| 69 | 标准 | 19,600 | 14,663,540,485 | 14,784,049,124 | 9 | 176,400 |
| 69 | 非标准 | 3,470,764 | 430,908,401 | 2,841,046,000 | 1 | 3,470,764 |

每行均满足 qrs=D、gcd(r,s)=1、r+s=kM，并恢复原分母。t=7 的高 gcd 来自较大的 q 与 k；t=69 则主要来自 q。

## 5. 精确复核

验证程序复核了 3<=t<=1000 的全部1000组实际表示，逐项检查 qrs=D、gcd(r,s)=1、r+s=kM、gcd(u,v)=qk、r²≡-D/q (mod M)，并验证 (5)、(7) 的有限实例上界。非唯一参数仍为 (7,2)、(69,2)。这只是有限计算，不是无限唯一性证明。

## 6. 局部 Jacobi 筛的下一步入口

由 (6)，对每个奇素数 p|h，q 必须满足

\[
(q/p)=(-D/p).
\]

将 Legendre 符号编码到 F_2，可构造以 p|h 为行、指数为1的素数 ell|D 为列的特征矩阵。若矩阵满行秩 s=ω(h)，则恰有 τ(D)/2^s 个 q 通过这些局部条件。t=7、69 已有独立基的精确证书，见 LOCAL_JACOBI_SIEVE_2026-11-08.md。该局部条件仍非充分条件。

## 7. 研究边界与下一步

已完成：q,r,s 精确双射；gcd(u,v)=qk；组合上界 (5)；模平方根上界 (8)；t=7、69 的真实非标准样本分解。

未解决：全部普通整数分解唯一性、非标准 q 的一般分类、局部特征矩阵在变化 t 下的秩、Siegel 逃逸阈值的有效估计。

下一步：对变化的 t，构造 F_2 Legendre 特征矩阵，研究是否能在正密度或显式无限子列上证明满行秩；分离八因子 resultant 所指出的七个重叠素数 {2,3,5,7,11,19,23}；将 q 的局部 Jacobi 筛与 r²≡-D/q (mod M) 结合，并用 t=7、69 的非标准解作反例保护。

## 参考文献

- S. Wigert, “Sur l’ordre de grandeur du nombre des diviseurs d’un entier,” Arkiv för Matematik, Astronomi och Fysik 3 (1907), no.18, 1–9；现代概述：P. Pollack, The maximal size of the k-fold divisor function for very large k, JRMS 35 (2020), no.4, 341–345, https://pollack.uga.edu/largedk3.pdf。
- Hardy–Ramanujan 最大阶 ω(n) 的讲义证明：https://eclass-b.uoa.gr/modules/document/file.php/MATH717/04.%20%CE%92%CE%BF%CE%B7%CE%B8%CE%AE%CE%BC%CE%B1%CF%84%CE%B1/Analytic-number-theory-Hildebrand.pdf。

原创性说明：q,r,s 参数化是经典两项分解方程的结构化重写；可能的新贡献是它与本 K3 中心族 M=h² 结合后得到的显式 10log2 上界。尚未完成系统文献优先权审查。
