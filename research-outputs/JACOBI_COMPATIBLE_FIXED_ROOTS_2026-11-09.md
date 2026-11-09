# 不动平方根与 Jacobi 条件的直接交汇定理

**日期：** 2026-11-09  
**性质：** 一般定理（h 为奇数）及六组参数的精确验证。

## 1. 关键恒等式

每个 syndrome-zero 局部配置对应
[
g\equiv qr^2\pmod M.
]
由于 (p\mid h) 且 (gcd(r,M)=1)，
[
\boxed{(g/p)=(q/p).}
]
因此余数 g 满足所有 Jacobi 条件，当且仅当其对应的 q 满足所有局部筛条件。这使 Jacobi syndrome 可以直接从乘法余数恢复。

## 2. 不动平方根的局部结构

令 (M=h^2)，且 h 为奇数。对每个 (p^a\parallel h)，不动点方程
[
g^2\equiv D^2\pmod {p^{2a}}
]
等价于
[
(gD^{-1})^2\equiv1\pmod {p^{2a}}.
]
因为 p 为奇素数，模 (p^{2a}) 的方程 (x^2=1) 恰有两个解 (x=\pm1)。所以
[
g\equiv\pm D\pmod {p^{2a}}.
]
CRT 表明全部不动余数由每个 p 独立选择一个符号构成，总数恰为
[
|H_t|=2^{\omega(h)}.
]

对一个符号选择 (arepsilon_p\in\{+1,-1\})，Jacobi 条件为
[
1=(g/p)=(\varepsilon_pD/p)
=(\varepsilon_p/p)(D/p).
]

于是：
- 若 (p\equiv1\pmod4)，则 ((-1/p)=1)。两个符号的 Legendre 值相同：当 ((D/p)=1) 时两者都允许；当 ((D/p)=-1) 时两者都不允许。
- 若 (p\equiv3\pmod4)，则 ((-1/p)=-1)。两个符号中恰有一个允许。

得到精确计数定理：
[
\boxed{
\#\{g\in H_t:(g/p)=1\ \forall p\mid h\}
=
\begin{cases}
2^{\#\{p\mid h:p\equiv1\ (4)\}},
& (D/p)=1\text{ 对所有 }p\mid h,\ p\equiv1\ (4),\\
0,&\text{否则}.
\end{cases}}
\tag{1}
]
这里 p 按互异素数计数，不按指数计数。

这只是所有 Jacobi-compatible fixed roots 的数量；其中哪些实际出现在局部配置余数分布的支撑中，是更强的问题，不能混为一谈。

## 3. 六组参数的验证

| t | h 的素因子 | 全部不动根数 | Jacobi-compatible 不动根数 | 实际支撑中的不动根数 |
|---:|---|---:|---:|---:|
| 3 | 3,37 | 4 | 2 | 2 |
| 7 | 5,7,17 | 8 | 4 | 2 |
| 17 | 5,17,41 | 8 | 8 | 2 |
| 69 | 3,23,829 | 8 | 2 | 1 |
| 137 | 5,7,47,137 | 16 | 4 | 1 |
| 185 | 5,37,2221 | 8 | 8 | 2 |

例如 t=69：
- p=3、23 均为 3 mod 4，各自强制唯一符号；
- p=829 为 1 mod 4，且 (D/829)=1，因此有两个符号；
- 所以 Jacobi-compatible fixed roots 恰有2个，但只有1个被实际局部配置实现。

这说明“满足固定点方程和 Jacobi 条件”仍只是必要条件，不是可实现性充分条件。

## 4. 对研究的意义

此前需要先生成整个 syndrome-zero 余数分布，再与固定点集合求交。现在对合固定点的 Jacobi 合法性可以直接按 h 的素因子分类，无需枚举全部 (2^{\omega(h)}) 个 CRT 根。

更重要的是，公式 (1) 把交集大小化为 h 的素因子模4类别和 D 的 Legendre 符号条件。这是一个一般性、可证明的结构结果。

但它还没有给出实际支撑交集的精确公式，也没有给出 N(t) 的新上界。

## 5. 可复现文件

- `research-outputs/jacobi_compatible_fixed_roots.py`
- 本报告：`research-outputs/JACOBI_COMPATIBLE_FIXED_ROOTS_2026-11-09.md`

运行：
```bash
python research-outputs/jacobi_compatible_fixed_roots.py
```
需要 SymPy。
