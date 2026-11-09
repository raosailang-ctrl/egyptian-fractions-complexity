# 六个参数的乘法子群成员检验：-1 是否属于生成子群 H

**日期：** 2026-11-09  
**性质：** 通过有限阿贝尔群坐标和整数格指数判据完成的精确成员检验。

## 1. 方法

令 (H=\langle\ell_1,\ldots,\ell_n\rangle\le(\mathbb Z/M\mathbb Z)^\times)。由于 (h) 为奇数，(M=h^2) 的单位群按 CRT 分解为各奇素数幂单位群的直积；每个 ((\mathbb Z/p^{2a}\mathbb Z)^\times) 都是循环群，阶为
[
d_p=\varphi(p^{2a})=p^{2a-1}(p-1).
]
选择一个原根 (u_p)，将每个 (ell_i) 及目标 (-D) 写成离散对数：
[
\ell_i\equiv u_p^{v_{pi}},\qquad -D\equiv u_p^{b_p}\pmod {p^{2a}}.
]
则 (-D\in H) 当且仅当整数线性系统
[
\sum_i x_i v_{pi}-d_p y_p=b_p
]
对所有 p 同时有整数解。

将生成元矩阵与关系列组成整数矩阵
[
B=[V\mid-\operatorname{diag}(d_p)].
]
因为 B 有 m 行且满行秩，目标向量 b 属于其整数列格，当且仅当
[
\gcd\{\text{所有 }m\times m\text{ 子式 of }B\}
=
\gcd\{\text{所有 }m\times m\text{ 子式 of }[B\mid b]\}.
]
这是一个精确的格成员判据，可由 Smith normal form 的不变因子理解。程序直接计算最大阶子式的 gcd，避免依赖不透明的群成员搜索。

## 2. 结果

| t | h 的素因子 | 各局部循环群阶 | 格指数 gcd | 加入目标后的 gcd | 结论 |
|---:|---|---|---:|---:|:---:|
| 3 | 3,37 | 6, 1332 | 1 | 1 | (-1\in H) |
| 7 | 5,7,17 | 20, 42, 272 | 1 | 1 | (-1\in H) |
| 17 | 5,17,41 | 20, 272, 1640 | 2 | 2 | (-1\in H) |
| 69 | 3,23,829 | 6, 506, 686412 | 1 | 1 | (-1\in H) |
| 137 | 5,7,47,137 | 20, 42, 2162, 18632 | 2 | 2 | (-1\in H) |
| 185 | 5,37,2221 | 20, 1332, 4930620 | 2 | 2 | (-1\in H) |

所有六个参数都满足 (-1\in H)。因此，简单的子群成员障碍在这六个例子中没有排除任何参数。

## 3. 解释

这是一个有用的否定结果：虽然 (-1\in H) 是存在全局表示的必要条件，但在这些参数中它过于宽松，不能解释 t=69、137 的有界指数实现障碍。

下一步必须区分：
1. 无界整数指数是否存在；
2. 指数是否能落入 (0\le k_i\le2a_i)；
3. 是否同时满足 (Ak=0\pmod2)。

特别要注意，群成员检验只允许任意整数生成元指数 x_i；它并不自动给出有界非负指数 k_i，也不保证 Jacobi syndrome。

## 4. 可复现文件

- `research-outputs/multiplicative_subgroup_membership.py`
- 本报告：`research-outputs/MULTIPLICATIVE_SUBGROUP_MEMBERSHIP_2026-11-09.md`

运行：
```bash
python research-outputs/multiplicative_subgroup_membership.py
```
需要 SymPy。
