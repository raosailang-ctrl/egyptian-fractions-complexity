# 中心化带符号指数定理：将目标余数 -D 化为乘积 -1

**日期：** 2026-11-09  
**性质：** 精确双射、一般等价判据；不是新的渐近上界。

## 1. 有界指数向量的中心化

已有精确参数化：
[
N(t)=\frac12\#\left\{k\in\mathbb Z^n:
0\le k_i\le2a_i,quad Ak=0\pmod2,quad
\prod_i\ell_i^{k_i}\equiv-D\pmod M
\right\}.
\]
令
[
x_i=k_i-a_i.
]
则 (-a_i\le x_i\le a_i)，且
[
\prod_i\ell_i^{k_i}
=\left(\prod_i\ell_i^{a_i}\right)
\left(\prod_i\ell_i^{x_i}\right)
=D\prod_i\ell_i^{x_i}.
]
由于 D 是模 M 的单位，目标同余等价于
[
\boxed{\prod_i\ell_i^{x_i}\equiv-1\pmod M.}
\tag{1}
]
又因 (k_i\equiv a_i+x_i\pmod2)，Jacobi 条件等价于
[
\boxed{Ax\equiv Aa\pmod2.}
\tag{2}
]

## 2. 中心化带符号指数定理

**定理。**
[
\boxed{
N(t)=\frac12\#\left\{
x\in\mathbb Z^n:
-a_i\le x_i\le a_i,quad
Ax\equiv Aa\pmod2,quad
\prod_i\ell_i^{x_i}\equiv-1\pmod M
\right\}.
}
\tag{3}
]

证明直接由双射 (k_i\leftrightarrow x_i=k_i-a_i) 得到。每个 x 唯一对应一个有序方向配置；目标乘积为 -1 时 x 与 -x 对应交换 r、s。若 x=-x，则 x=0，乘积为1，不可能等于 -1（M>2），故解数恰为偶数，每个无序表示计数两次。

## 3. 对固定余数集合的进一步解释

任意方向交换不动余数可写成
[
g=Dz,qquad z^2\equiv1\pmod M.
]
若它由某个局部配置实现，则存在带符号指数向量 x 满足
[
z\equiv\prod_i\ell_i^{x_i}\pmod M,quad
-a_i\le x_i\le a_i,quad
Ax\equiv Aa\pmod2.
]
因此固定余数的实际实现问题统一成为：在中心盒子 (prod_i[-a_i,a_i]) 内，寻找指定 2-扭元 z 的受限乘法表示，同时满足一个仿射 F_2 奇偶条件。

特别地，目标余数 (-D) 对应 (z=-1)。这比直接处理 k_i∈[0,2a_i] 更对称，也更便于使用正负指数配对。

## 4. 新的研究含义

- 群成员条件 (-1\in H) 只说明存在任意整数指数表示；
- 中心化定理要求指数同时落在对称盒 ([-a_i,a_i]) 内；
- 仿射条件 (Ax=Aa) 进一步限制奇偶类；
- 因此无解障碍可以拆成“群成员—有界指数—仿射奇偶”三个层次。

对于任意 Jacobi-compatible 固定根 (g=Dz)，只需把右侧 -1 替换为 z，即可得到其实际实现的精确判据。

## 5. 可复现关联文件

- `research-outputs/BOUNDED_EXPONENT_VECTOR_GLOBAL_REALIZATION_2026-11-09.md`
- `research-outputs/MULTIPLICATIVE_SUBGROUP_OBSTRUCTION_2026-11-09.md`
- 本报告：`research-outputs/CENTERED_SIGNED_EXPONENT_THEOREM_2026-11-09.md`

## 6. 下一步

以 t=69、137 为重点，求解中心盒子中的带符号指数系统：
[
-a_i\le x_i\le a_i,quad Ax=Aa\pmod2,quad
\prod_i\ell_i^{x_i}=z\pmod M.
]
分别对每个 Jacobi-compatible 2-扭元 z 统计解数。对目标 z=-1，解数应为 (2N(t)=4)（t=69、137 的已知样本均有 N=1 或2，需以独立枚举结果核对具体值）。不得把群成员作为充分条件。
