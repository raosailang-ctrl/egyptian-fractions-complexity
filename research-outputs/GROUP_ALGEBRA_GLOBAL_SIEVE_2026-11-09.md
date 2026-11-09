# 中心 K3 埃及分数族的修正版群代数生成函数

**日期：** 2026-11-09  
**性质：** 精确组合恒等式；修正局部因子在剩余素数幂为 1 时的重复计数。不是渐近上界或复杂度改进。

## 1. 参数化与局部选择

令
[
D=\prod_{i=1}^n\ell_i^{a_i},\qquad M=h^2,\qquad \gcd(D,M)=1.
]
任意分解对应
[
qrs=D,\qquad \gcd(r,s)=1,\qquad r+s\equiv0\pmod M.
]
写 (q=\prod_i\ell_i^{e_i})，(0\le e_i\le a_i)。由于 r,s 互素，剩余的完整素数幂 (\ell_i^{a_i-e_i}) 必须全部分给 r 或 s。

若 (e_i<a_i)，有两个不同方向：
[
\epsilon_i=0:\ \ell_i^{a_i-e_i}\mid s,\qquad
\epsilon_i=1:\ \ell_i^{a_i-e_i}\mid r.
]
若 (e_i=a_i)，剩余素数幂等于 1，两种“方向”是同一个选择，必须只计一次。这是此前未修正版本中的重复计数来源。

令 (c_i\in\mathbb F_2^m) 为 Legendre 特征列。局部 Jacobi 条件对应总 syndrome 为零。

## 2. 全局乘积同余

由 (qrs=D) 以及 (\gcd(qr,M)=1)，有
[
r+s\equiv0\pmod M
\iff qr^2\equiv-D\pmod M.
]
若 (e_i<a_i)，对应的局部乘法因子有两项：
[
\ell_i^{e_i}
\quad\text{或}\quad
\ell_i^{2a_i-e_i}.
]
若 (e_i=a_i)，只有一项 (\ell_i^{a_i})。

## 3. 修正版群代数定理

令 (G=(\mathbb Z/M\mathbb Z)^\times)。在整数群代数
[
\mathbb Z[\mathbb F_2^m\times G]
]
中定义
[
P_i=
\sum_{e=0}^{a_i-1}
\left(
[(e\bmod2)c_i,\ell_i^e]
+
[(e\bmod2)c_i,\ell_i^{2a_i-e}]
\right)
+
[a_i\bmod2)c_i,\ell_i^{a_i}].
]
所有第二坐标均按模 M 解释。令 (P=\prod_iP_i)。

则
[
\boxed{N(t)=\frac12[0,-D]P.}
\tag{1}
]

**证明。** 每个 (e_i<a_i) 的两项恰好对应剩余素数幂分配给 r 或 s 的两个不同方向；(e_i=a_i) 只有唯一方向选择。因此 P 的每个展开项与一个有序三元组 (q,r,s) 一一对应，不再重复。第一坐标为零恰好表示全部局部 Jacobi 条件成立；第二坐标为 (-D) 恰好表示 (qr^2\equiv-D\pmod M)，等价于 (r+s\equiv0\pmod M)。每个无序表示有两个不同的方向次序：若 r=s，则 gcd(r,s)=1 强迫 r=s=1，与 M>2 和 (M\mid r+s) 矛盾。因此目标系数为 (2N(t))。证毕。

## 4. 修正版 Fourier 展开

利用有限群特征正交关系，得到
[
2N(t)=\frac1{2^m|G|}
\sum_{u\in\mathbb F_2^m}
\sum_{\chi\in\widehat G}
\chi((-D)^{-1})
\prod_{i=1}^n F_i(u,\chi),
\tag{2}
]
其中
[
\begin{aligned}
F_i(u,\chi)
={}&\sum_{e=0}^{a_i-1}
(-1)^{u\cdot c_i(e\bmod2)}
\left(\chi(\ell_i)^e+
\chi(\ell_i)^{2a_i-e}\right)\\
&+
(-1)^{u\cdot c_i(a_i\bmod2)}
\chi(\ell_i)^{a_i}.
\end{aligned}
]
与旧公式相比，末端 (e=a_i) 只保留一个方向项。这一修正对群代数系数、Fourier 展开和任何数值计算都必须同步采用。

## 5. 直接的回归恒等式

令
[
T_i=2a_i+1.
]
这是第 i 个局部选择的数量：每个 (e<a_i) 有两个方向，(e=a_i) 有一个方向。因而总有序局部配置数是
[
\prod_i(2a_i+1),
]
而不是此前未修正版本所隐含的 (2\prod_i(a_i+1))。

将 P 的所有乘法群坐标和 syndrome 坐标求和后，必须得到这个总数。更重要的是，目标系数应当满足
[
[0,-D]P=2N(t),
]
其中 (N(t)) 可由独立的 gcd–互素因子参数化直接枚举验证。

## 6. 研究边界与下一步

已修正：
- 当 (e_i=a_i) 时方向变量不再重复计数；
- 群代数计数定理的双射论证；
- 对应的 Fourier 局部因子。

尚未完成：
- t=7、69 的稀疏群代数动态规划；
- 目标余数 (-D) 的频数分布和碰撞统计；
- 非平凡群特征项的有效界；
- 任何由群代数表达式推出的新渐近上界。

下一步先编写独立程序，对 t=7 和 t=69 的全部局部配置作精确计数；用 (\prod_i(2a_i+1)) 核验总配置数，并将目标系数与直接表示枚举所得的 (2N(t)) 比较。随后再考虑稀疏 DP 或 MITM 群代数卷积。

**重要：** 这是对先前群代数报告的数学修订。旧版公式在 (e_i=a_i) 处重复计数，不能继续作为正确的计数定理引用。
