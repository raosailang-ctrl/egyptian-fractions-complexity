# 方向交换对合与 syndrome-zero 余数分布的精确对称性

**日期：** 2026-11-09  
**性质：** 一般代数恒等式与奇偶性定理；六组参数的有限验证。

## 1. 局部配置与余数

固定 (D=\prod_i\ell_i^{a_i})、(M>2)、(gcd(D,M)=1)。局部配置对应
[
qrs=D,\qquad \gcd(r,s)=1,
]
其中每个剩余完整素数幂被分配给 r 或 s。定义余数
[
g(q,r,s)=qr^2\pmod M.
]
Jacobi syndrome 只依赖 q，因此交换 r 与 s 不改变 syndrome。

## 2. 方向交换对合定理

交换 r 与 s 后，余数变为 (g'=qs^2)。由 qrs=D，
[
gg'=q^2r^2s^2=D^2.
]
因此
[
\boxed{\iota(g)=D^2g^{-1}\pmod M}
]
且 (iota^2) 为恒等映射。于是 syndrome-zero 分布满足
[
\boxed{\mu_0(g)=\mu_0(D^2g^{-1}).}
\tag{1}
]

证明中的关键细节：在全部局部配置中，交换固定配置必须有 r=s；结合 gcd(r,s)=1 得 r=s=1、q=D。这是唯一固定配置，余数为 D。但是它只有在 q=D 本身通过 Jacobi 筛时，才属于 syndrome-zero 层。不能无条件声称它一定在该层中。

## 3. 固定余数的奇偶性

对合的不动余数满足
[
g^2\equiv D^2\pmod M.
]
在 syndrome-zero 层中，每个不动余数对应的配置都被交换对合固定或成对配对。唯一可能的固定配置是 (q,r,s)=(D,1,1)。

因此，对任意满足 (g^2\equiv D^2\pmod M) 的余数：
[
\boxed{
\mu_0(g)\equiv
\begin{cases}
1\pmod2,&g\equiv D\pmod M\text{ 且 }D\text{ 通过 Jacobi 筛},\\
0\pmod2,&\text{其他情形}.
\end{cases}}
\tag{2}
]
目标余数 (-D) 与 D 不同，因为 M>2 且 gcd(D,M)=1。因此 (mu_0(-D)) 必为偶数，与 (mu_0(-D)=2N(t)) 一致。

注意，模合数 M 下 (g^2=D^2) 可能有多于两个解，不能假设不动余数只有 (\pm D)。

## 4. 六组参数的不动点实验

对每个参数，完整求解 (g^2\equiv D^2\pmod M)，再与 syndrome-zero 余数支撑比较：

| t | 不动余数总数 | 支撑中不动余数数 | 目标 (-D) 质量 |
|---:|---:|---:|---:|
| 3 | 4 | 2 | 2 |
| 7 | 8 | 2 | 4 |
| 17 | 8 | 2 | 2 |
| 69 | 8 | 1 | 4 |
| 137 | 16 | 1 | 2 |
| 185 | 8 | 2 | 2 |

全部六组的目标余数均为不动余数。实际出现在 syndrome-zero 支撑中的不动余数数量远少于模方程的全部根数，说明 Jacobi 条件还会排除大量不动点。

更细的结果：
- t=3：支撑中的不动余数为 445（质量2）、10507（质量4）；D 本身未通过 Jacobi 筛。
- t=7：为 90371（质量4）、134471（质量4）；D 本身未通过 Jacobi 筛。
- t=17：为 787611（质量2）、11357614（质量1）；D 通过 Jacobi 筛，故后一原子包含唯一固定配置。
- t=69：只有 12927427（质量4）；D 未通过 Jacobi 筛。
- t=137：只有 50932491（质量2）；D 未通过 Jacobi 筛。
- t=185：为 92860011（质量2）、168733623214（质量1）；D 通过 Jacobi 筛，故后一原子包含唯一固定配置。

## 5. 解释与边界

这项结果给出了三个精确事实：
1. 余数分布关于 (g\mapsto D^2g^{-1}) 完全对称；
2. 目标 (-D) 必是对合不动点，且其质量必为偶数；
3. 其他不动余数是否有奇数质量，取决于唯一固定配置 q=D 是否通过 Jacobi 筛。

它解释了目标原子的偶数性，但不能解释目标为何在某些参数中成为最大原子，也没有给出 (N(t)) 的新上界或唯一性结论。

## 6. 可复现文件

- `research-outputs/syndrome_zero_residue_distribution.py`（包含对合对称及奇偶断言）
- 本报告：`research-outputs/ORIENTATION_SWAP_INVOLUTION_2026-11-09.md`

运行六组参数并检查对称性：
```bash
python research-outputs/syndrome_zero_residue_distribution.py --values 3 7 17 69 137 185
```
