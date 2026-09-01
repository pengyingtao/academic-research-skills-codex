# WP1 新颖性评估 V0.4

> 论文题目：《面向技术预见的证据校准动态推演方法研究——以AI赋能网络安全技术为例》
>
> 状态：WP1 仍在进行中。本评估建立在当前 55 条高相关/方法邻域文献池基础上，用于决定后续方法贡献如何收敛；不是最终系统综述结论。

## 一、当前总体判断

ECDS-TF 已不能以“某个单一方法组件首次用于技术预见”为创新主线。以下组件均已在技术预见或相邻领域存在直接先例：

- System Dynamics / Simulation；
- Agent-Based Modeling；
- 数据校准 ABM；
- 论文+专利+GitHub 多源融合；
- Science–Technology Lead-Lag；
- GCN/R-GCN/DGNN/TGNN 技术机会预测；
- 概率技术预测；
- 历史 cutoff / rolling forecast；
- LLM multi-agent emerging-technology forecasting；
- temporal graph counterfactual intervention（跨领域）。

因此，本研究若要保持方法创新价值，必须依赖“机制特化 + 组合架构 + 严格验证范式”，而非组件堆叠。

## 二、本轮新增高风险边界

### 1. Vulnerability demand-pull 不是空白

现有研究已表明：

- 漏洞信息披露能够提高软件厂商补丁 R&D 概率；
- 漏洞严重度、关注度和提前披露会影响修复研发速度；
- 企业面临的 cybersecurity risk 会改变专利和创新策略；
- bug bounty / coordinated disclosure 可通过激励机制改变厂商安全研发与发布时间。

因此禁止使用：

> “首次提出漏洞需求驱动安全创新。”

仍可能成立的细化贡献为：

> **将 CVE/CWE/KEV 处理为 exploitation-weighted vulnerability-demand state，并检验其在多源技术状态转移、技术增长与技术融合预测中的边际预测价值。**

这里的研究问题从“有没有需求牵引”变成：

1. 如何量化需求压力；
2. 需求压力是否领先于 AI 防御技术的论文/专利/GitHub 增长；
3. 它是否改善历史预测；
4. 它是否能作为情景 shock 进入 2030 forward simulation。

### 2. AgentProphet 显著压缩 MAF-TF 空间

2026 年 AgentProphet 已将：

- 多源技术证据；
- role-specialized LLM agents；
- history-only feature records；
- source-aware confidence calibration；
- critic-guided refinement；
- rolling forecasting；
- emerging-technology ranking

组合在同一框架中。

因此原 `MAF-TF` 不应继续定位为独立预测创新。

建议正式调整为：

## MAST — Multi-Agent Scenario Stress Test

功能边界：

- 输入 ECDS-TF 的量化预测路径；
- 负责寻找模型未参数化的制度、法规、组织、责任、商业化和极端事件风险；
- 生成 failure modes / counterarguments / scenario explanations；
- 不进入主要 historical leaderboard；
- 不单独宣称 emerging-technology forecast accuracy。

这一调整能够避免和 AgentProphet 正面重复，并强化“双轨方法”的角色分工。

## 三、当前创新点分级

| 候选贡献 | 当前状态 | 判断 |
|---|---|---|
| Simulation for technology foresight | 已存在 | 放弃 |
| Calibrated ABM | 已存在 | baseline |
| Multi-source foresight | 已存在 | 组件 |
| Paper–Patent–GitHub fusion | 已存在 | 组件 |
| Lead-Lag | 已存在 | 组件 |
| Dynamic/heterogeneous graph | 已存在 | 组件 |
| Probabilistic forecasting | 已存在 | 组件 |
| Historical backtesting | 已存在 | 验证组件 |
| LLM multi-agent technology forecasting | 已存在 | 不作为创新 |
| Vulnerability → patch/security R&D demand | 已有机制/实证 | 理论依据，不是首创 |
| STOV role-aware technology state | 尚未发现高度同构 | **重点保留** |
| Exploitation-weighted vulnerability-demand state | 尚未发现用于技术预见的高度同构实现 | **重点保留** |
| Learned technology dynamics → explicit scenario intervention | 技术预见内尚未发现高度同构；跨领域存在 | **重点保留但谨慎表述** |
| Growth + Emergence + Convergence 多任务 historical reconstruction | 暂未发现高度同构统一框架 | **重点保留** |
| Accuracy + ranking + calibration + interval + scenario sensitivity 统一验证 | 暂未发现高度同构 | **重点保留** |
| Quantitative simulation + MAST stress test | 暂未发现相同角色分工 | **扩展贡献** |

## 四、建议修改后的方法主张

不再使用：

> “提出一种全新的基于多源时序异构图的技术预见算法。”

建议改为：

> **本文提出一种面向技术预见的证据校准动态推演框架。该框架将科学研究、专利技术化、开源工程扩散与漏洞需求压力表示为角色化技术状态，在严格历史时间隔离条件下学习状态转移与跨技术相互作用，并将学习到的动力学转换为可干预的概率前向推演；其有效性通过多窗口历史重演、技术增长/新兴/融合多任务预测、概率校准和情景敏感性联合验证。**

该表述的优点是：

1. 不错误宣称任何单个组件首次出现；
2. 把创新重心放到“技术预见问题如何被形式化”；
3. 强调 empirical validation 而不是算法复杂度；
4. 保留 2030 what-if 技术推演能力。

## 五、Vulnerability 通道的推荐正式定义

建议把原始 CVE count 改为更有理论含义的：

## Vulnerability Demand Pressure (VDP)

暂定：

\[
VDP_{k,t}=f(CVE_{k,t},KEV_{k,t},Severity_{k,t},Exploitability_{k,t},Exposure_{k,t},RemediationGap_{k,t})
\]

其中：

- CVE：漏洞披露规模；
- KEV：已确认实际利用；
- Severity：CVSS/影响；
- Exploitability：EPSS/LEV 或可用代理；
- Exposure：受影响产品/生态广度；
- RemediationGap：披露、利用与修复速度差。

理论解释：

> VDP 不代表“漏洞数量”，而代表某技术领域对防御研发、自动化分析和修复能力的现实需求压力。

后续必须通过消融和 lead-lag 检验决定 VDP 是否真正具有预测增益。

## 六、对 ECDS-TF 算法设计的影响

建议把算法从“图模型主导”改成“动态状态模型主导”。

### Layer 1 — Role-aware Evidence State

\[
X_{k,t}=[S_{k,t},T_{k,t},O_{k,t},VDP_{k,t}]
\]

### Layer 2 — Learned Relational Dynamics

图模型负责估计：

- technology interaction；
- cross-source timing；
- convergence probability；
- neighborhood influence。

### Layer 3 — Evidence-Calibrated State Transition

\[
X_{t+1}=F_\theta(X_t,G_t,Z_t)+\epsilon_t
\]

### Layer 4 — Intervenable Forward Simulation

允许改变：

- AI capability shock；
- vulnerability/threat shock；
- OSS diffusion shock；
- regulatory/constraint shock。

### Layer 5 — Historical Reconstruction & Calibration

必须同时验证：

- MAE/RMSE/sMAPE；
- Precision/Recall/NDCG；
- AUC/F1/Hits@K；
- Brier/ECE（若输出概率）；
- interval coverage；
- scenario sensitivity / stability。

## 七、WP1 尚未结束的原因

虽然当前文献池已达到 55 条，超过最低数量阈值，但还需完成：

1. 统计类别配额是否满足：simulation/SD/ABM ≥10，graph/TOD ≥10，computational foresight ≥20；
2. 针对 VDP 定义继续查 exploitability/patch-demand/innovation linkage；
3. 查找技术预见领域是否已有正式 probability calibration 指标（Brier/ECE/coverage）；
4. 查找是否已有 technology foresight 的 learned simulator + explicit intervention；
5. 去重并形成最终 50–80 篇核心矩阵；
6. 输出最终 `wp1_novelty_assessment.md` 并决定是否回写 WP0 修改研究协议。

## 八、当前决策

**WP1 状态：IN_PROGRESS**。

当前不进入 WP2。下一轮重点是“类别配额核验 + 剩余三个 gap 终检”，然后给出 GO / MODIFY / STOP 决策：

- `GO`：现有题目与框架可以进入 taxonomy/data；
- `MODIFY`：题目保留，但方法结构/贡献声明需修改；
- `STOP`：发现高度同构研究，需要重新选方法问题。
