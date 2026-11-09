# Jacobi 筛的带权 MacWilliams 计数公式：中心 K3 埃及分数族

**日期：** 2026-11-09  
**性质：** 精确计数恒等式与13个参数的独立验证；不涉及表示数唯一性。

## 1. 问题

令
[
D=\prod_{i=1}^n\ell_i^{a_i},\qquad
h=\prod_{j=1}^m p_j^{b_j},\qquad M=h^2,
]
其中 (ell_i) 是 D 的互异素因子，(p_j) 是 h 的互异素因子。定义二进制矩阵
[
A_{ji}=\begin{cases}
1,&(\ell_i/p_j)=-1,\\
0,&(\ell_i/p_j)=1.
end{cases}
]
对约数 (q=\prod_i\ell_i^{e_i})，局部 Jacobi 条件 ((q/p_j)=1) 对所有 j 成立，当且仅当其指数奇偶向量 (v_i=e_i\bmod2) 满足 (Av=0)。

已有的粗略估计通常写成 (	au(D)/2^r)，但这只有在所用的独立二进制坐标确实可以等权自由选择时才可直接使用。对于一般非平方自由 D，同一奇偶向量对应的 q 数量并不恒定。

## 2. 带权核空间公式

令
[
\alpha_i=\lfloor a_i/2\rfloor+1,qquad
\beta_i=\lceil a_i/2\rceil.
]
当 (v_i=0) 时，指数 (e_i\in\{0,2,4,\ldots\}) 有 (alpha_i) 种选择；当 (v_i=1) 时，指数 (e_i\in\{1,3,5,\ldots\}) 有 (eta_i) 种选择。因此通过所有 Jacobi 条件的约数数量精确等于
[
\boxed{
Q_{\rm pass}=\sum_{v\in\ker A}
\prod_{i:v_i=0}\alpha_i
\prod_{i:v_i=1}\beta_i.}
\tag{1}
]

## 3. 带权 MacWilliams 变换

令 (r=\operatorname{rank}(A))。有限域字符正交关系给出
[
\mathbf1_{Av=0}=2^{-m}\sum_{u\in\mathbb F_2^m}
(-1)^{u^TAv}.
]
代入 (1)，交换求和与乘积：
[
Q_{\rm pass}
=2^{-m}\sum_u\prod_i
\left(\alpha_i+(-1)^{(A^Tu)_i}\beta_i\right).
]
映射 (u\mapsto A^Tu) 的像是 row(A)，每个像有 (2^{m-r}) 个原像。因此
[
\boxed{
Q_{\rm pass}
=2^{-r}\sum_{y\in\operatorname{Row}(A)}
\prod_{i=1}^n
\left(\alpha_i+(-1)^{y_i}\beta_i\right).}
\tag{2}
]
这是对非等权坐标的精确带权线性码枚举公式。

## 4. 化简：奇指数坐标与偶指数坐标

令
[
O=\{i:a_i\text{ 为奇数}\},\qquad
E=\{i:a_i\text{ 为偶数}\}.
]
若 (i\in O)，则 (alpha_i=\beta_i=(a_i+1)/2)，所以式 (2) 中只要 (y_i=1)，对应乘积就为零。故只有支撑完全落在 E 上的行空间向量有贡献。若 (i\in E)，则
[
\alpha_i+\beta_i=a_i+1,\qquad
\alpha_i-\beta_i=1.
]
于是得到更简洁的精确公式：
[
\boxed{
Q_{\rm pass}
=\frac{\prod_{i\in O}(a_i+1)}{2^r}
\sum_{\substack{y\in\operatorname{Row}(A)\\
\operatorname{supp}(y)\subseteq E}}
\prod_{\substack{i\in E\\y_i=0}}(a_i+1).
}
\tag{3}
]

令 (A_O) 表示只保留 A 中 O 类坐标列的子矩阵，秩为 (r_O)。则
[
\dim\{y\in\operatorname{Row}(A):\operatorname{supp}(y)\subseteq E\}
=r-r_O.
]
因此式 (3) 的求和项最多只有 (2^{r-r_O}) 项，而不是遍历整个核空间 (2^{n-r})，也不是遍历整个行空间 (2^r)。

**重要特例：** 若所有 (a_i) 都是奇数，则 E 为空，求和只含 y=0，故
[
Q_{\rm pass}=\tau(D)/2^r.
]
若 D 平方自由，这也就是经典的等权情况。

## 5. 13 个参数的精确验证

程序 `weighted_jacobi_code_count.py` 用两条独立路径计算：
- 直接枚举所有 (q\mid D)，检查全部 Legendre 条件；
- 用带权行空间公式 (2) 及化简公式 (3) 计算。

两种结果对全部13个参数完全一致。

| t | n | rank(A) | 奇指数素因子数 | 偶指数素因子数 | 行空间大小 | 支撑限于 E 的行向量数 | tau(D) | 精确通过数 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 7 | 2 | 4 | 3 | 4 | 1 | 864 | 216 |
| 7 | 9 | 3 | 8 | 1 | 8 | 1 | 4608 | 576 |
| 17 | 8 | 2 | 7 | 1 | 4 | 1 | 1408 | 352 |
| 69 | 13 | 3 | 11 | 2 | 8 | 1 | 172032 | 21504 |
| 137 | 11 | 3 | 11 | 0 | 8 | 1 | 6144 | 768 |
| 185 | 10 | 2 | 10 | 0 | 4 | 1 | 3072 | 768 |
| 609 | 11 | 3 | 10 | 1 | 8 | 1 | 14336 | 1792 |
| 1105 | 11 | 5 | 8 | 3 | 32 | 4 | 48384 | 1920 |
| 1285 | 11 | 4 | 9 | 2 | 16 | 4 | 17920 | 1536 |
| 1457 | 9 | 3 | 9 | 0 | 8 | 1 | 2048 | 256 |
| 5957 | 11 | 5 | 10 | 1 | 32 | 2 | 7168 | 256 |
| 6215 | 10 | 3 | 8 | 2 | 8 | 1 | 2304 | 288 |
| 6657 | 12 | 6 | 8 | 4 | 64 | 4 | 48384 | 1056 |

在 t=1105、1285、5957、6657，支撑限于 E 的非零行向量确实产生额外带权项。这解释了为什么只用完整矩阵秩去套用 (	au(D)/2^r) 会错；精确公式 (3) 则完整处理了这些重复素数幂权重。

## 6. 对当前项目的意义

本结果精确刻画了“局部 Jacobi 筛到底留下多少 q”，但它尚未计入全局互素因子分配 (R=rs) 与 (r^2\equiv-R\pmod M)。因此它是局部候选数的精确公式，不是最终表示数 (N(t)) 的公式。

它提供了一个更好的研究接口：
1. 用式 (3) 精确计算局部候选规模；
2. 找到实际贡献的行空间子码 (W=\operatorname{Row}(A)\cap\mathbb F_2^E)；
3. 按这些带权奇偶类组织平方根传输与 MITM；
4. 研究哪些核类必然无法包含全局互素因子分配。

这比单纯比较 (	au(D)/2^r) 更精确，但尚未给出全局表示数的新渐近定理。

## 7. 可复现文件

- `research-outputs/weighted_jacobi_code_count.py`
- `research-outputs/WEIGHTED_JACOBI_CODE_ENUMERATOR_2026-11-09.md`

运行：
```bash
python research-outputs/weighted_jacobi_code_count.py
```
需要 SymPy。
