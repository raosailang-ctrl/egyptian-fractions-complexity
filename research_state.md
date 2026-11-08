Current question:
研究中心 K3 埃及分数族的 q,r,s 参数化，利用局部 Jacobi 特征筛排除非标准整数分解。

Completed:
- 读取 research_state.md、最新提交及前期数学证明。
- 建立普通整数分解与 qrs=D、gcd(r,s)=1、r+s=kM 的精确双射。
- 得到分母 {qkr,qks} 及 gcd(u,v)=qk。
- 推导模平方根条件 r² ≡ -D/q (mod M)。
- 得到 N(t) ≤ 2520 τ(D) 2^ω(M)。
- 改进渐近上界至 10 log 2，较此前 8 log 3 降低约21.1%。
- 得到 N(M,D) ≤ (τ(D²)-1)/2。
- 完成 t=3 至1000的1000组实际表示参数化验证。
- 对 t=7、69 完成标准与非标准分解的 q,r,s 分解。
- 建立条件性 F2 Jacobi 特征筛引理。
- 在 t=7、69 精确验证1/8的局部筛选比例。
- 生成研究报告、验证程序、交接文件和 ZIP。
- 更新 GitHub。

Evidence:
- QRS 主报告：b0bab6564c73daa1b8eeda8d7c5c185e1cd34356。
- QRS 验证：e755c811816231d56d3144e3e638e8b941fc72f9。
- Jacobi 报告：df659af1b005ea5b273cf9ba28b3dae65df6ff1b。
- Jacobi 验证：4be161ba5f87127d58d4bf4113c72eed55abf0b2。
- 最新状态：0bc061f6e89d48589d57f8878442f8141af7fd10。
- qrs 验证1000组全部通过。
- Jacobi 两个实例均精确得到1/8。
- ZIP完整性检查通过。

Open problems:
- 普通整数分解完全唯一性尚未证明。
- t=7、69存在真实非标准分解。
- 局部 Jacobi 筛仍是必要条件，不是充分条件。
- 尚未证明一般 t 下特征矩阵满行秩。
- 新渐近上界尚未证明为最优。
- 文献原创性仍需系统审查。

Next step:
研究变化 t 下的 F2 Legendre 特征矩阵，利用八个线性因子及七个重叠素数建立满秩条件；结合 q 的局部筛和模平方根条件，研究非标准分解的排除。

Artifacts:
- research-outputs/K3_QRS_GCD_PARAMETERIZATION_2026-11-08.md
- research-outputs/verify_qrs_parametrization.py
- research-outputs/QRS_RESEARCH_HANDOFF_2026-11-08.md
- research-outputs/LOCAL_JACOBI_SIEVE_2026-11-08.md
- research-outputs/verify_local_jacobi_sieve.py
- K3_QRS_GCD_PARAMETERIZATION_2026-11-08.zip
