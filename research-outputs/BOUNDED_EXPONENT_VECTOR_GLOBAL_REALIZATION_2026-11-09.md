# 有界指数向量参数化：将全局实现问题化为有限乘法同余

**日期：** 2026-11-09  
**性质：** 精确一一对应与计数恒等式；可替代此前较繁琐的局部方向记号。

## 1. 从局部选择到单一指数

令
[
D=\prod_{i=1}^n\ell_i^{a_i},\qquad M>2,\qquad \gcd(D,M)=1.
]
一个局部配置由 (0\le e_i\le a_i) 和方向 (epsilon_i\in\{0,1\}) 决定：
- (epsilon_i=0)：剩余完整素数幂进入 s；
- (epsilon_i=1)：剩余完整素数幂进入 r。
若 (e_i=a_i)，剩余块为1，只有一个方向选择。

配置对应
[
q=\prod_i\ell_i^{e_i},quad
r=\prod_i\ell_i^{(a_i-e_i)\epsilon_i},quad
s=\prod_i\ell_i^{(a_i-e_i)(1-epsilon_i)}.
]
定义新指数
[
\boxed{k_i=e_i+2(a_i-e_i)\epsilon_i.}
]
则 (0\le k_i\le2a_i)，并且：
- (k_i<a_i) 时，唯一原像为 (e_i=k_i,epsilon_i=0)；
- (k_i=a_i) 时，唯一原像为 (e_i=a_i)；
- (k_i>a_i) 时，唯一原像为 (e_i=2a_i-k_i,epsilon_i=1)。

因此这是局部选择集合与整数盒
[
\mathcal B=\prod_i\{0,1,\ldots,2a_i\}
]
之间的一一对应。总配置数为 (prod_i(2a_i+1))。

## 2. Jacobi syndrome 只依赖 k 的奇偶性

设 (p_1,\ldots,p_m) 是 h 的互异素因子，定义
[
A_{ji}=1\iff(\ell_i/p_j)=-1.
]
原 Jacobi 条件是 (A(e_i\bmod2)=0)。但
[
k_i\equiv e_i\pmod2
]
因为第二种方向的指数 (2a_i-e_i) 与 (e_i) 同奇偶。因此局部筛条件恰好化为
[
\boxed{Ak=0\quad\text{in }\mathbb F_2^m.}
\tag{1}
]

## 3. 全局乘法余数也只依赖 k 的乘积

原来定义的余数为 (g=qr^2\pmod M)。代入局部参数：
[
g=\prod_i\ell_i^{e_i+2(a_i-e_i)\epsilon_i}
=\boxed{\prod_i\ell_i^{k_i}\pmod M.}
\tag{2}
]
所以所有局部合法配置与 syndrome-zero 余数分布，可以直接写成：
[
\mu_0(g)=
\#\left\{
k\in\mathcal B:
Ak=0\ (\bmod2),\prod_i\ell_i^{k_i}\equiv g\ (\bmod M)
\right\}.
\tag{3}
]

这给出了一个比原群代数写法更简洁的精确表达。

## 4. 全局表示数的有界指数向量定理

**定理。** 在上述条件下，原无序两项单位分数分解数满足
[
\boxed{
N(t)=\frac12
\#\left\{
k\in\mathcal B:
Ak=0\ (\bmod2),\prod_i\ell_i^{k_i}\equiv-D\ (\bmod M)
\right\}.
}
\tag{4}
]

**证明。** 上述局部映射把每个 (kin\mathcal B) 唯一对应到一个有序局部配置 ((q,r,s))。条件 (Ak=0) 等价于所有 Jacobi 条件；乘积同余由 (2) 给出，且 (g=-D) 等价于 (r+s\equiv0\pmod M)。因此右侧计数有序三元组。交换 r,s 对应另一个不同配置：若 r=s，则互素性迫使 r=s=1，但 M>2 时 (M\nmid2)。故每个无序表示恰好计数两次。证毕。

## 5. 不动余数的全局实现判据

不动余数集合
[
H=\{g:g^2\equiv D^2\pmod M\}
]
中，Jacobi-compatible 只是必要条件。现在可以精确写出实际实现条件：

[
\boxed{
g\in H\cap\operatorname{supp}(\mu_0)
\iff
\exists k_i\in[0,2a_i]:
\quad Ak=0\pmod2,quad
\prod_i\ell_i^{k_i}\equiv g\pmod M.
}
\tag{5}
]

因此，对 t=69、137 等参数，未实现的 Jacobi-compatible 不动余数，正对应一个没有有界指数向量解的模乘法方程组。这把“局部—全局障碍”明确转化成一个有限的受限乘法子集积问题。

## 6. 结构性推论

1. 方向交换 (r\leftrightarrow s) 在新坐标下就是
   [
   k_i\longmapsto2a_i-k_i.
   ]
   对应乘法余数 (g\mapsto D^2g^{-1})，直接恢复此前的对合定理。
2. syndrome 只依赖 (k\bmod2)，而模乘法余数依赖完整的有界整数向量 k。因此可以先按核空间奇偶类分层，再在每层中求受限乘法积。
3. 每个奇偶类中的坐标取值数量由指数上界 (2a_i) 决定。这为带权 Gray-code、动态规划和 MITM 提供了统一输入格式。

## 7. 研究边界与下一步

这是精确参数化，不是新渐近上界，也没有消除指数搜索。下一步：
- 对每个 Jacobi-compatible 固定根 g，求解有界指数系统 (5)，尤其 t=69、137；
- 记录每个根的解向量数量，而不只记录是否可实现；
- 比较目标根 -D 与其他不动根的有界指数解数；
- 利用奇偶核空间先分层，再按剩余指数范围做 MITM。

不要把“Jacobi-compatible”当成充分条件，也不要从六个样本推断一般唯一性。

## 8. 可复现关联文件

- `research-outputs/GROUP_ALGEBRA_GLOBAL_SIEVE_2026-11-09.md`
- `research-outputs/ORIENTATION_SWAP_INVOLUTION_2026-11-09.md`
- `research-outputs/FIXED_RESIDUES_JACOBI_INTERSECTION_2026-11-09.md`
- 本报告：`research-outputs/BOUNDED_EXPONENT_VECTOR_GLOBAL_REALIZATION_2026-11-09.md`
