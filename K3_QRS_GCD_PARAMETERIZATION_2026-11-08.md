# K3 中心埃及分数族的 gcd–coprime-factor 参数化与新渐近上界

**日期：** 2026-11-08  
**研究对象：** 中心共振模板 `(a,b,c)=(1/6,4,2)`。  
**结论性质：** 一般整数分解的精确双射；利用模平方根数量得到的新渐近上界；对 `3<=t<=1000` 的精确实例复核。  
**重要限制：** 不证明全部普通整数分解唯一；不宣称算法为多项式时间。

## 摘要

前期已将普通两项单位分数分解对应到约数 `d|D^2`，满足 `d<=D` 与 `d≡-D (mod M)`。本轮进一步把每个分解精确改写为

\[
D=qrs,\qquad (r,s)=1,\qquad r+s=kM,
\]

其中 `q,k,r,s` 均为正整数。对应分母恰为

\[
\boxed{\{u,v\}=\{qkr,qks\}},\qquad \gcd(u,v)=qk.
\]

这给出一个清楚的结构解释：`q` 是两个变换后因子 `d,e` 的公共核心，`r,s` 是互素的剩余因子，`k` 是它们的和相对于模数 `M` 的倍数。特别地，额外分解的高 gcd 正好表现为 `qk` 的增大。

更重要的是，参数化导出新的模平方根筛选。固定 `q|D` 后，`r` 必须满足

\[
r^2\equiv -D/q\pmod M.
\]

由于 `D=FG` 且 `F+G=1260M`，有 `D<=630^2M^2`，从而 `r<=630M`。模 `M` 的单位平方根至多 `4·2^{ω(M)}` 个，每个剩余类在 `[1,630M]` 内至多有630个代表。因此

\[
\boxed{N(t)\le2520\,\tau(D(t))\,2^{\omega(M(t))}.}
\]

又因 `M=[t(12t+1)]^2` 且 `gcd(t,12t+1)=1`，有

\[
\omega(M)=\omega(t)+\omega(12t+1)
\le(2+o(1))\frac{\log t}{\log\log t}.
\]

结合 Wigert 的 `τ(D)` 最大阶和 `deg D=8`，得到

\[
\boxed{\log N(t)\le(10\log2+o(1))\frac{\log t}{\log\log t}.}
\]

这比上一轮 `8 log 3` 的常数更小：`10 log 2≈6.93147`，`8 log 3≈8.78890`，约降低21.1%。这是本轮真正利用同余条件得到的上界改进；所用的 `τ` 与 `ω` 最大阶仍是经典数论工具。

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

前期恒等式为

\[
F+G=1260M,\qquad D\equiv-1\pmod h,\qquad \gcd(D,M)=1.
\]

考虑

\[
\frac MD=\frac1u+\frac1v,
\]
并取 `u<=v`。定义

\[
d=Mu-D,\qquad e=Mv-D.
\]

则

\[
de=D^2,\quad d\le e,\quad d\equiv e\equiv-D\pmod M.
\tag{1}
\]

反之，满足 `d|D²`、`d<=D`、`d≡-D (mod M)` 的约数唯一恢复一组无序正整数分母。因此普通分解数量是

\[
N(t)=\#\{d\mid D^2:d\le D,\ d\equiv-D\pmod M\}.
\tag{2}
\]

## 2. 新的精确参数化定理

**定理 2.1（gcd–互素因子双射）。** 设 `M,D` 为互素正整数且 `M>2`。所有正整数无序分解

\[
M/D=1/u+1/v
\]

与所有满足

\[
qrs=D,\quad q,r,s\in\mathbb Z_{>0},\quad \gcd(r,s)=1,\quad M\mid r+s
\tag{3}
\]

的三元组 `(q,{r,s})` 一一对应。若 `k=(r+s)/M`，对应分母为

\[
\boxed{\{u,v\}=\{qkr,qks\}},\qquad \boxed{\gcd(u,v)=qk}.
\tag{4}
\]

**证明。** 从 (1) 出发，令 `q=gcd(d,e)`。对每个素数 `p`，若 `v_p(D)=a`、`v_p(d)=b`，则 `v_p(e)=2a-b`。因此

\[
v_p(q)=\min(b,2a-b)\le a,
\]

所以 `q|D`。而 `d/q` 与 `e/q` 的每个素数指数中，一个为0，另一个为偶数；故存在正整数 `r,s` 使

\[
d=qr^2,\qquad e=qs^2,\qquad \gcd(r,s)=1,\qquad qrs=D.
\]

又 `q|D` 且 `gcd(D,M)=1`，所以 `q` 在模 `M` 下可逆。由 `d≡-D` 和 `D=qrs` 得

\[
qr^2\equiv-qrs\pmod M.
\]

除以 `q`，再利用 `gcd(r,M)=1`，得到 `r+s≡0 (mod M)`。令 `k=(r+s)/M`，则

\[
\begin{aligned}
u&=(D+d)/M=q r(r+s)/M=qkr,\\
v&=(D+e)/M=q s(r+s)/M=qks.
\end{aligned}
\]

因 `(r,s)=1`，即得 `gcd(u,v)=qk`。

反过来，给定 (3)，令 `k=(r+s)/M`、`u=qkr`、`v=qks`，则

\[
\frac1u+\frac1v=\frac{r+s}{qkrs}=\frac{M}{qrs}=\frac MD.
\]

构造互逆，唯一性成立。证毕。

**附带性质。** 由 `r+s=kM` 与 `(r,s)=1` 可得

\[
\boxed{\gcd(k,rs)=1.}
\tag{5}
\]

例如若某素数同时整除 `k` 与 `r`，则它整除 `r+s=kM`，进而整除 `s`，矛盾。这个条件对筛选 `k` 很有用。

## 3. 两个直接推论

### 3.1 一个精确的纯组合上界

固定 `q|D`，令 `R=D/q`。条件 `rs=R`、`(r,s)=1` 意味着每个完整素数幂 `p^a||R` 必须整体分配给 `r` 或 `s`，不能拆到两边。因此有序分配数为 `2^{ω(R)}`。若 `R>1`，交换 `r,s` 无固定点，故无序分配数为 `2^{ω(R)-1}`。

`R=1` 时只能 `r=s=1`，但 `r+s=2` 不可能被 `M>2` 整除。因此

\[
N(M,D)\le\sum_{q\mid D,\ q<D}2^{\omega(D/q)-1}.
\]

对每个 `p^a||D`，局部生成函数是 `1+2a`，故

\[
\sum_{q\mid D}2^{\omega(D/q)}=\prod_{p^a\parallel D}(1+2a)=\tau(D^2).
\]

于是

\[
\boxed{N(M,D)\le\frac{\tau(D^2)-1}{2}.}
\tag{6}
\]

这比旧的 `N<=τ(D²)` 改善一个近似因子2，但不改变渐近指数常数。

### 3.2 模平方根筛选与新渐近上界

由定理2.1，固定 `q|D`，令 `R=D/q`。因 `rs=R` 且 `r+s≡0 (mod M)`，有

\[
r^2\equiv-rs\equiv-R\pmod M.
\tag{7}
\]

又 `gcd(R,M)=1`，所以 (7) 是单位模数上的平方根同余。

**平方根数量。** 对奇素数幂 `p^a`，一个单位平方根同余至多有2个根；对2的幂至多有4个根。由中国剩余定理，模 `M` 的根数至多

\[
4\cdot2^{\omega(M)}.
\tag{8}
\]

**每个根类的代表数。** 因

\[
D=FG\le\left(\frac{F+G}{2}\right)^2=(630M)^2,
\]

而 `r<=sqrt(R)<=sqrt(D)`，所以 `1<=r<=630M`。每个非零模 `M` 剩余类在该区间内恰至多有630个正整数代表。结合 (8)，每个 `q` 至多对应

\[
2520\cdot2^{\omega(M)}
\]
个 `r`，而 `s=R/r` 唯一确定。`q` 的选择数为 `τ(D)`，因此

\[
\boxed{N(t)\le2520\,\tau(D(t))\,2^{\omega(M(t))}.}
\tag{9}
\]

**渐近推论。** 经典最大阶估计给出

\[
\log\tau(n)\le(\log2+o(1))\frac{\log n}{\log\log n},
\]

以及

\[
\omega(n)\le(1+o(1))\frac{\log n}{\log\log n}.
\]

这里 `D(t)=8230118400t^8+O(t^7)`，故

\[
\log\tau(D(t))\le(8\log2+o(1))\frac{\log t}{\log\log t}.
\]

又 `M=h²`，所以 `ω(M)=ω(h)`；并且 `gcd(t,12t+1)=1`，从而

\[
\omega(M)=\omega(t)+\omega(12t+1)
\le(2+o(1))\frac{\log t}{\log\log t}.
\]

代入 (9)：

\[
\boxed{\log N(t)\le(10\log2+o(1))\frac{\log t}{\log\log t}.}
\tag{10}
\]

数值比较：

- 上一轮三重除数上界：`8 log 3 ≈ 8.788898`；
- 本轮模平方根上界：`10 log 2 ≈ 6.931472`；
- 常数降低约 `21.1%`。

这次上界真正使用了 `r²≡-D/q (mod M)` 的同余结构，而不是只对 `D²` 的约数总数作估计。经典最大阶工具本身仍非本项目原创。

## 4. 标准表示与非标准样本的 q,r,s 结构

对标准分解 `d=G²,e=F²`，令 `g=gcd(F,G)`，则

\[
q_0=g^2,\quad r_0=G/g,\quad s_0=F/g,\quad k_0=1260/g.
\]

因为 `g|1260`，`k_0` 为整数，且 `r_0+s_0=k_0M`。标准分母 gcd 为 `q_0k_0=1260g`。

本轮对前1000个参数的精确 MITM 计数中，非唯一参数仍只有 `t=1,2,7,69`。特别检查 `t=7,69`：

| t | 类型 | q | r | s | k | gcd(u,v)=qk |
|---:|---|---:|---:|---:|---:|---:|
| 7 | 标准 | 324 | 11,893,677 | 12,888,073 | 70 | 22,680 |
| 7 | 非标准 | 16,814,886 | 81 | 36,464,494 | 103 | 1,731,933,258 |
| 69 | 标准 | 19,600 | 14,663,540,485 | 14,784,049,124 | 9 | 176,400 |
| 69 | 非标准 | 3,470,764 | 430,908,401 | 2,841,046,000 | 1 | 3,470,764 |

每行均满足 `qrs=D`、`gcd(r,s)=1`、`r+s=kM`，并精确恢复原来的两个分母。它们展示了高 gcd 的两种不同来源：`t=7` 的非标准表示同时具有较大的 `q` 和 `k`；`t=69` 则由很大的 `q` 单独产生。

## 5. 有限精确验证

独立验证程序使用前期 MITM 计数器枚举 `3<=t<=1000` 的所有有效约数 `d`，并对每个表示计算

\[
q=\gcd(d,D^2/d),\quad r=\sqrt{d/q},\quad s=\sqrt{(D^2/d)/q}.
\]

逐项检查：

1. `qrs=D`；
2. `gcd(r,s)=1`；
3. `r+s` 被 `M` 整除；
4. `u=qkr`、`v=qks`；
5. `gcd(u,v)=qk`；
6. `r²≡-D/q (mod M)`；
7. `N<= (τ(D²)-1)/2` 与 `N<=2520 τ(D)2^{ω(M)}`。

`3<=t<=1000` 共复核1000组实际表示，非唯一参数为 `(7,2)` 与 `(69,2)`，与此前完整1000参数普查一致。该有限复核验证的是计算与参数化一致，不是无限唯一性证明。

## 6. 研究边界与下一步

本轮完成：

- 普通两项分解的 gcd–互素因子精确双射；
- 高 gcd 的结构公式 `gcd(u,v)=qk`；
- `N<= (τ(D²)-1)/2` 的组合上界；
- 利用模平方根数量得到 `10 log 2` 的新渐近上界；
- `t=7,69` 两个真实非标准解的 q,r,s 完整分解。

仍未解决：

- 是否存在无限多个 `t` 使全部普通分解唯一；
- 如何排除 q,r,s 参数化中的非标准互素因子分配；
- 如何把模平方根必要条件进一步变成显著更强的 q 计数；
- Siegel gcd 逃逸阈值仍非有效；
- 国际文献优先权仍需独立审查。

**下一步建议：** 固定 `q|D`，研究 `r²≡-D/q (mod M)` 的根类中，哪些代表还能同时满足 `r|D/q` 与 `s=(D/q)/r` 且 `r+s=kM`。重点利用八个线性因子两两 resultant 的重叠素数集合 `{2,3,5,7,11,19,23}`，把 `q` 分解成重叠素数部分与八个互素部分，再建立对 q 的局部平方剩余筛。必须用 `t=7`、`t=69` 的真实非标准样本测试每条新限制，不能错误排除已知解。

## 7. 参考文献

- S. Wigert, “Sur l’ordre de grandeur du nombre des diviseurs d’un entier,” *Arkiv för Matematik, Astronomi och Fysik* 3 (1907), no. 18, 1–9；现代概述见 Paul Pollack, “The maximal size of the k-fold divisor function for very large k,” *Journal of the Ramanujan Mathematical Society* 35 (2020), no. 4, 341–345, https://pollack.uga.edu/largedk3.pdf。
- Hardy–Ramanujan maximal order of `ω(n)` 的讲义证明见 https://eclass-b.uoa.gr/modules/document/file.php/MATH717/04.%20%CE%92%CE%BF%CE%B7%CE%B8%CE%AE%CE%BC%CE%B1%CF%84%CE%B1/Analytic-number-theory-Hildebrand.pdf。
- 项目既有精确约数双射与中心恒等式：`research-outputs/SUBPOLYNOMIAL_ORDINARY_DECOMPOSITION_BOUND_2026-11-07.md`。
- 项目既有八因子 resultant 证书：`research-outputs/PAIRWISE_FACTOR_RESULTANTS_2026-11-07.md`。

**原创性说明：** q,r,s 参数化是对经典两项分解方程的结构化重写；新的贡献候选是它与该 K3 中心族 `M=h²` 的结合，得到显式 `10 log 2` 上界。尚未完成系统文献检索，不宣称文献优先权。
