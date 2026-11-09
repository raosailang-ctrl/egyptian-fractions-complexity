# 乘法子群成员障碍与有限阿贝尔群线性化

**日期：** 2026-11-09  
**性质：** 一般必要条件与精确等价改写；不宣称充分性可由子群成员单独保证。

## 1. 有界指数向量问题

已知
[
D=\prod_{i=1}^n\ell_i^{a_i},\quad M=h^2,\quad \gcd(D,M)=1.
]
全局表示数满足
[
N(t)=\frac12\#\left\{k\in\mathbb Z^n:
0\le k_i\le2a_i,quad
Ak=0\pmod2,quad
\prod_i\ell_i^{k_i}\equiv-D\pmod M
\right\}.
\tag{1}
]

## 2. 乘法子群成员必要条件

令
[
G=(\mathbb Z/M\mathbb Z)^\times,\qquad
H=\langle\ell_1,\ldots,\ell_n\rangle\le G.
]
因为 (D=\prod_i\ell_i^{a_i}\in H)，有
[
-D\in H\iff -1\in H.
]
式 (1) 的乘积左侧必然属于 H。因此得到：

**定理（子群成员障碍）。**
[
\boxed{-1\notin H\Longrightarrow N(t)=0.}
\]
这是一个可在任何指数枚举之前执行的必要条件。它不是充分条件：即使 (-1\in H)，也未必存在满足 (Ak=0\pmod2) 和 (0\le k_i\le2a_i) 的指数向量。

## 3. 有限阿贝尔群坐标中的线性同余系统

有限阿贝尔群 H 可写成不变因子分解
[
H\cong\mathbb Z/d_1\mathbb Z\oplus\cdots\oplus\mathbb Z/d_s\mathbb Z,
\qquad d_1\mid d_2\mid\cdots\mid d_s.
]
固定一个这样的同构，令 (v_i\in\prod_j\mathbb Z/d_j\mathbb Z) 为 (ell_i) 的坐标，令 (b) 为 (-D) 的坐标。则
[
\prod_i\ell_i^{k_i}=-D
]
等价于
[
\boxed{\sum_i k_i v_i\equiv b
\pmod{(d_1,\ldots,d_s)}.}
\tag{2}
]
因此原问题精确等价于一个混合模数有界线性系统：
[
\boxed{
Ak\equiv0\pmod2,qquad
Vk\equiv b\pmod{(d_1,\ldots,d_s)},qquad
0\le k_i\le2a_i.
}
\tag{3}
]
这可用整数 Smith normal form、模线性代数和有界整数规划工具研究。

## 4. 两层障碍

现在可以把全局实现拆成两个不同层次：

1. **群成员障碍：** (-1\in H) 是否成立？若不成立，立即得到 (N(t)=0)。
2. **有界格点障碍：** 即使 (-1\in H)，线性同余系统 (3) 是否存在落在指定盒子内、且满足 Jacobi 奇偶条件的整数点？

第二层才是目前 t=69、137 等案例中需要解释的精细障碍。不能把群成员条件误认为充分条件。

## 5. 与对合的兼容性

方向交换在指数坐标中为
[
k_i\mapsto2a_i-k_i.
]
乘积坐标随之变为
[
\prod_i\ell_i^{2a_i-k_i}
=D^2\left(\prod_i\ell_i^{k_i}\right)^{-1}.
]
当目标为 (-D) 时，它仍映到 (-D)。因此目标方程的解向量除可能的中心点 (k_i=a_i) 外均成对出现。中心点对应乘积 D 而非 (-D)，由于 (M>2)、(gcd(D,M)=1)，它不可能是目标解。

这再次说明目标指数向量解数为偶数，与 (2N(t)) 一致。

## 6. 下一步

1. 对 t=3,7,17,69,137,185 构造 H，计算 (-1\in H) 的成员证书或非成员证书。
2. 求 H 的不变因子分解，并将每个 (ell_i) 与 (-D) 表示成群坐标。
3. 将 (3) 转成整数矩阵同余系统，用 Smith normal form 先判断无界整数解，再检查盒约束和 Jacobi 奇偶条件。
4. 对 t=69、137 的 Jacobi-compatible fixed roots，比较子群成员、无界同余可解性与有界可解性，精确定位障碍发生在哪一层。

**边界：** 这是精确的代数重写与必要条件。尚未计算样本中的子群不变因子，也未得到新的 N(t) 上界或唯一性定理。
