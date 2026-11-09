# 中心 K3 埃及分数族的全局群代数生成函数：统一局部筛与互素因子分配

**日期：2026-11-09**  
**性质：** 精确组合恒等式与有限群代数表达；不是复杂度改进定理，不证明唯一性。

## 1. 目标

此前的研究分成三个步骤：
1. 用 Jacobi 符号条件筛选 q|D；
2. 用 F_2 核空间组织 q 的奇偶指数，并传输平方根集合；
3. 对 R=D/q 枚举互素因子分配 R=rs，检查 r+s ≡0 (mod M)。

本轮把这些条件合并成一个乘法群上的生成函数。它直接计数所有满足局部条件和全局同余条件的有序分配。

## 2. 从全局同余得到单一乘积条件

写
[
D=\prod_{i=1}^n\ell_i^{a_i},\qquad
q=\prod_i\ell_i^{e_i},\qquad 0\le e_i\le a_i.
]
由于 gcd(D,M)=1，每个 ell_i 都是模 M 的单位。

因 gcd(r,s)=1，剩余因子 R=D/q 的每个完整素数幂 ell_i^{a_i-e_i} 必须整体进入 r 或 s。用 epsilon_i\in\{0,1\} 记录方向：
- epsilon_i=1：ell_i^{a_i-e_i} 分配给 r；
- epsilon_i=0：该素数幂分配给 s。

于是
[
r=\prod_i\ell_i^{(a_i-e_i)\epsilon_i},\qquad
s=\prod_i\ell_i^{(a_i-e_i)(1-\epsilon_i)}.
]
显然 qrs=D 且 gcd(r,s)=1。

原参数化要求 r+s ≡0 (mod M)。因为 D=qrs 且 qr 是模 M 的单位，
[
r+s\equiv0\pmod M
\iff r^2+rs\equiv0\pmod M
\iff qr^2+D\equiv0\pmod M.
]
因此全局条件等价于一个乘积同余：
[
\boxed{q r^2\equiv-D\pmod M.}\tag{1}
]

代入局部素数幂分配后：
[
qr^2=\prod_i\ell_i^{e_i+2(a_i-e_i)\epsilon_i}.
\tag{2}
]

## 3. Jacobi 条件是一个 F_2 syndrome

令 A 的第 i 列为向量 c_i\in\mathbb F_2^m，其第 j 个坐标为
[
(c_i)_j=1\iff(\ell_i/p_j)=-1,
]
其中 p_j 遍历 h 的互异素因子。

约数 q 通过全部局部 Jacobi 条件，当且仅当
[
\sum_i(e_i\bmod2)c_i=0\quad\text{in }\mathbb F_2^m.
\tag{3}
]

因此每个素数幂因子的选择 (e_i,epsilon_i) 同时贡献：
- 一个 F_2 syndrome：((e_i\bmod2)c_i)；
- 一个模 M 的乘法群元素：
[
g_i(e_i,epsilon_i)
=\ell_i^{e_i+2(a_i-e_i)epsilon_i}\pmod M.
]

## 4. 群代数生成函数定理

令 G=(\mathbb Z/M\mathbb Z)^\times。考虑整数系数群代数
[
\mathbb Z[\mathbb F_2^m\times G].
]
对每个 i 定义局部因子
[
P_i=
\sum_{e=0}^{a_i}\sum_{\epsilon=0}^1
\left[(e\bmod2)c_i,,
\ell_i^{e+2(a_i-e)\epsilon}\bmod M\right].
]
令
[
P=\prod_{i=1}^nP_i.
]
记 ([0,-D]) 在 P 中的系数为 (C(0,-D))。

**定理（全局群代数计数恒等式）。**
[
\boxed{N(t)=\frac12\,[0,-D]\prod_{i=1}^nP_i.}\tag{4}
]

这里 (N(t)) 是原问题中无序正整数两项单位分数分解的数量。

**证明。**
P 的每一个展开项唯一对应一组指数 e_i 和方向 epsilon_i，因此唯一对应一个有序三元组 (q,r,s)，满足 qrs=D、gcd(r,s)=1。其群代数第一坐标为零，当且仅当所有 Jacobi 条件成立；第二坐标为 -D，当且仅当 (1) 成立。由 (1)，这又等价于 r+s ≡0 (mod M)。因此目标系数恰好计数全部有序表示。

每个无序表示对应交换 r、s 得到的两个有序方向选择。两者不同：若 r=s，则 gcd(r,s)=1 强迫 r=s=1，但 M>2 时不可能有 r+s≡0 (mod M)。所以有序计数恰为 2N(t)，证毕。

## 5. 这个表达式揭示的局部—全局鸿沟

局部筛只看 syndrome 坐标为零；全局可实现性还要求乘法群坐标恰好等于 -D。

所以“通过 Jacobi 筛”的数量是把 P 的所有 residue 坐标加总后，取 syndrome=0 的总系数；而真正的整数表示数只取其中一个特定 residue (-D) 的系数，再除以2。

这给出一个精确的解释：
- Jacobi 筛回答：有多少素数指数选择满足局部二次剩余条件？
- 全局群代数系数回答：这些选择中，有多少同时把乘积送到指定的模 M 余数？

此前观察到的巨大筛选落差，正是同一个 syndrome 层内，乘法群坐标分布不均匀造成的。

## 6. 可能的进一步工具：群特征 Fourier 展开

对有限阿贝尔群 G，目标余数的指示函数可以用所有群特征 chi 展开：
[
\mathbf1_{g=-D}
=\frac1{|G|}\sum_{\chi\in\widehat G}
\chi(gD^{-1}).
]
同样，syndrome=0 可用 F_2 线性特征展开。于是目标系数可写为局部因子的乘积和：
[
2N(t)=\frac1{2^m|G|}
\sum_{u\in\mathbb F_2^m}
\sum_{\chi\in\widehat G}
\chi(D^{-1})
\prod_i
\left(
\sum_{e=0}^{a_i}\sum_{\epsilon=0}^1
(-1)^{u\cdot c_i(e\bmod2)}
\chi(\ell_i)^{e+2(a_i-e)\epsilon}
\right).
\tag{5}
]
式 (5) 是精确恒等式，不是渐近估计。若能控制非平凡群特征项，才有希望得到比单纯 Jacobi 筛更强的全局表示数上界。

## 7. 研究边界与下一步

已经得到：
1. 将全局同余 r+s ≡0 (mod M) 精确改写为 qr² ≡ -D (mod M)；
2. 每个素数幂的指数和方向选择都被编码为一个局部群代数因子；
3. (N(t)) 是群代数中一个指定系数的一半；
4. 通过局部筛的约数总数是 syndrome=0 层的总质量，而表示数是该层中单一乘法余数的质量。

尚未得到：
- 非平凡群特征和的有效上界；
- (N(t)) 的新统一渐近上界；
- 普通两项分解唯一性；
- 多项式时间算法。

**下一步：** 先在 t=7 和 t=69 上显式计算局部乘法余数分布，测量 syndrome=0 层的质量在 G 中有多集中；再研究能否用子群、商群或特征和将目标系数上界化。若群 G 太大，先取由 ell_i 生成的子群 H=<ell_1,...,ell_n>，因为所有可达乘积都在 H 中，避免无谓地遍历整个单位群。

## 8. 相关项目文件

- `research-outputs/WEIGHTED_JACOBI_CODE_ENUMERATOR_2026-11-09.md`
- `research-outputs/GRAY_KERNEL_ROOT_TRANSPORT_2026-11-09.md`
- 本报告：`research-outputs/GROUP_ALGEBRA_GLOBAL_SIEVE_2026-11-09.md`
