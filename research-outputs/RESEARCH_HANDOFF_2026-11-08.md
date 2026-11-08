# 2026-11-08 研究交接：中心 K3 分数族的整块约数刚性

## Current question
能否利用 `D(t)` 的八个线性因子、少量重叠素数和模 `M(t)=t^2(12t+1)^2` 的同余条件，超越通用约数函数估计，并排除部分普通整数两项分解？

## Completed
1. 独立证明：对每个 `t>=3`，任意 `d=prod_i L_i(t)^e_i, e_i in {0,1,2}`，若 `d == -D (mod M)`，则指数向量只有 `F(t)^2` 或 `G(t)^2` 两种；加入 `d<=D` 后只有 `G(t)^2`。这**不是**全体约数的唯一性。
2. 元素性证明：偶数 `e_5` 时 `t|q1(e)` 且 `|q1|<=234`；`12t+1` 整除 `P_e(-1/12)+D(-1/12)` 的既约分子。`q1=C=0` 只有2个标准向量。对剩下16个 `q1=0`，根值分子至多259，故 `t>=235` 自动排除。对 `3<=t<=234`，两道必要筛选只留332个 `(t,e)`，完整模 `M` 检验全部否决。
3. 上界常数严格改进：`N(t)<=tau(D^2)<=d3(D)`，固定 `d3` 最大阶上界给出 `log N(t) <= (8 log 3+o(1)) log t/loglog t`，强于之前 `16 log 2`。该常数改进来自经典工具而非新的除数函数定理。
4. 实现精确模 `M` 折半枚举：按互素素幂分开 `D^2=A B`，按 `a mod M` 建索引，枚举 `b|B` 时查询 `a == -D b^-1 mod M` 且 `a<=D/b`。完整计算 `1<=t<=1000`，只有 `t=1,2,7,69` 有多个分解，计数分别 `85,5,2,2`。这是**有限实验**，不能推导密度或无限唯一性。

## Evidence
- `BLOCK_DIVISOR_RIGIDITY_AND_SHARPER_COUNT_2026-11-08.md`：详细证明。
- `verify_block_divisor_rigidity.py`：纯标准库精确检验证书。输出 `JET_0_PRIME_FILTER PASS`、`FIRST_DERIVATIVE_ZERO_COUNT 18`、`ROOT_VALUE_ZERO_COUNT 64`、`DOUBLE_JET_ZERO_EXACTLY_CANONICAL 2`、`FINITE_NECESSARY_CANDIDATES 332`、`BLOCK_DIVISOR_RIGIDITY_FOR_ALL_t_GE_3 PASS`。
- `count_by_mitm.py`、`census_t1_1000.jsonl`、`mitm_1000_verification.txt`：精确折半计数及全部1000项结果。
- 之前 `research-outputs/PAIRWISE_FACTOR_RESULTANTS_2026-11-07.md` 证明非七个例外素数的线性因子质因数支持互不重叠。
- 经典数论出处：Pollack, *The maximal size of the k-fold divisor function for very large k*, JRMS 35(2020), 341–345（引言综述固定 `k` 最大阶）。

## Open problems
- **核心难题**：排除将线性因子内部质因数部分选入约数 `d` 的非标准表示。
- 无穷多个参数具有普通整数两项**完全唯一**分解，尚未证明。`t=7,69` 是本族反例，不能声称所有 `t>=3` 完全唯一。
- 需要把七个例外素数与其它不重叠的素数支持结合，研究恰有一个线性因子被部分拆分时的严格排除准则。
- 不存在已证的额外 gcd 增长统一幂下界；亏格2有理点完整分类及原创性文献核查均未完成。
- Chrome 附件自动化暂时搁置，不影响本次数学研究。

## Next step
1. 把非标准 `d` 的质因数指数与八个完整线性因子指数 `e_i` 的差异形式化；先处理仅一个因子需要部分拆分的情形。
2. 以 `t=7`、`t=69` 的已知非标准表示为反例测试，明确任何新判别条件不能错误排除真解。
3. 探索使用模 `t^2`、模 `(12t+1)^2` 的乘法群约束及有限重叠质因数，构建统一的部分拆分阻碍。
4. 若得到严格新界，再更新原有 `N(t)` 上界和可复现验证。

## Artifacts
- `research-outputs/BLOCK_DIVISOR_RIGIDITY_AND_SHARPER_COUNT_2026-11-08.md`
- `research-outputs/verify_block_divisor_rigidity.py`
- `research-outputs/count_by_mitm.py`
- `research-outputs/census_t1_1000.jsonl`
- `research-outputs/mitm_1000_verification.txt`
- `research-outputs/RESEARCH_HANDOFF_2026-11-08.md`