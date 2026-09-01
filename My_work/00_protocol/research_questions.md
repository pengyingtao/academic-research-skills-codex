# Research Questions V2

> WP1 结论：`MODIFY`。本文件据新颖性检索结果修订，正式将 VDP、统一历史重演和可干预动态推演纳入研究问题；Lead-Lag、动态图、多智能体不再单独作为创新问题。

## RQ1 — Role-aware STOV 技术状态

> **RQ1：AI赋能网络安全技术在科学研究、专利技术化、开源工程扩散和漏洞需求压力四类证据中呈现怎样的动态演化结构？四类证据在不同技术族中具有怎样的领先、滞后和耦合关系？**

### 子问题

- RQ1.1：Science、Patent、Open Source 和 Vulnerability Demand 的时间结构是否显著不同？
- RQ1.2：不同技术族是否表现出稳定或异质的跨源 lag？
- RQ1.3：GitHub/Open Source 是否在部分技术族中提供早于专利或产业化的工程扩散信号？
- RQ1.4：技术融合出现前是否存在可检测的跨源关系变化？

### 对应证据

- OpenAlex
- Patent
- GitHub
- CVE/CWE/KEV/EPSS/LEV

### 研究意义

该 RQ 不以“首次发现 Lead-Lag”为贡献，而用于建立 ECDS-TF 的可解释状态表示和动态结构基础。

---

## RQ2 — Vulnerability Demand Pressure（VDP）

> **RQ2：将漏洞披露、实际利用、严重度、暴露范围和修复缺口联合构造为 Vulnerability Demand Pressure 后，VDP 是否能够解释并预测 AI 网络安全防御技术的研究、工程化和技术化响应？**

### 子问题

- RQ2.1：VDP 与论文、GitHub、专利增长之间是否存在稳定的 lead-lag？
- RQ2.2：KEV/Exploitability 权重是否比 raw CVE count 更有效？
- RQ2.3：VDP 是否能提升 Technology Growth Forecasting？
- RQ2.4：VDP 是否能提升 Emerging Technology Detection？
- RQ2.5：VDP 是否对 Technology Convergence Forecasting 有增量解释力？

### 待检验命题

- H2a：`VDP > raw CVE count` 的历史预测性能；
- H2b：高 exploitation pressure 后，相关防御技术的开源/研究信号会显著增强；
- H2c：VDP 的预测价值具有技术族异质性。

### 方法边界

已有研究已经证明 vulnerability disclosure / cyber risk 会影响 patch R&D 和创新策略，因此本研究不主张发现了新的 demand-pull 理论，而检验该机制作为技术预见状态变量的价值。

---

## RQ3 — Evidence-Calibrated Dynamic Simulation

> **RQ3：从历史 STOV 状态与技术关系中学习的动态状态转移模型，能否在历史时间隔离条件下准确重建未来的技术增长、新兴和融合，并优于传统统计、机器学习、图模型和 ABM baseline？**

### 子问题

- RQ3.1：Evidence Calibration 相较规则型 ABM 是否提高预测性能？
- RQ3.2：关系图编码是否提供稳定增益？
- RQ3.3：cross-source timing/lag representation 是否仍具有边际增益？
- RQ3.4：概率 rollout 是否比 deterministic rollout 更适合长时间窗预见？

### 核心比较路径

\[
ABM-R \rightarrow ABM-C \rightarrow ECDS-v0 \rightarrow ECDS-v1 \rightarrow ECDS-TF
\]

### 方法贡献

贡献不在“首次使用 GNN/ABM/Lead-Lag”，而在角色化状态、证据校准状态动力学和可验证技术预见推演的整体实现。

---

## RQ4 — Unified Historical Reconstruction & Reliability

> **RQ4：在严格 temporal freeze 下，ECDS-TF 能否同时对技术增长、新兴技术和技术融合进行稳定的多窗口历史重演，并产生可靠校准的概率与不确定性区间？**

### 子问题

- RQ4.1：F1/F2/F3 中性能是否稳定？
- RQ4.2：rolling-origin 下结论是否稳健？
- RQ4.3：预测概率是否校准？
- RQ4.4：预测区间 coverage 是否达到预定水平？
- RQ4.5：不同数据源消融是否改变模型可靠性，而不仅是平均准确率？

### 指标

- Growth：MAE / RMSE / sMAPE
- Emerging：Precision@K / Recall@K / NDCG@K / AUPRC
- Convergence：AUC / F1 / Hits@K
- Calibration：Brier Score / ECE / reliability diagram
- Interval：coverage / width / sharpness

### 方法意义

已有技术预见存在 historical validation 和 probabilistic forecasting；本研究重点检验的是多任务、多折时间隔离、概率校准与情景敏感性是否可统一成一个可靠性验证协议。

---

## RQ5 — Intervenable Foresight toward 2030

> **RQ5：在通过历史验证后，ECDS-TF 对不同外部冲击的干预响应是否能够产生可解释、稳定且具有决策价值的 2027–2030 AI 网络安全技术演化路径？**

### 情景

- S0 Baseline
- S1 AI Capability Acceleration
- S2 Threat / Vulnerability Shock
- S3 OSS Acceleration
- S4 Constraint / Regulation

### 子问题

- RQ5.1：哪些技术对 AI capability shock 最敏感？
- RQ5.2：哪些技术受 VDP shock 强烈驱动？
- RQ5.3：哪些技术在 OSS acceleration 下更早进入高增长？
- RQ5.4：哪些技术路径对 regulation/constraint 高度脆弱？
- RQ5.5：不同情景下技术融合结构如何变化？

---

## RQ6 — MAST：Multi-Agent Scenario Stress Test

> **RQ6：当 LLM 多智能体不承担核心数值预测，而作为情景压力测试器时，是否能够系统发现 ECDS-TF 未参数化的制度、组织、责任、商业化和极端事件失效模式？**

### 角色建议

- Science/Research Analyst
- Industry/Adoption Analyst
- Open-source Ecosystem Analyst
- Cyber Defender / Threat Analyst
- Regulation & Governance Analyst
- Adversarial Synthesizer

### 输出

- failure modes
- missing variables
- scenario counterarguments
- adoption barriers
- regulatory/liability risks
- tail-event hypotheses

### 边界

MAST 不进入核心 historical leaderboard；不声称独立实现 emerging technology forecasting。

---

# RQ 与论文贡献映射

| RQ | 核心贡献 |
|---|---|
| RQ1 | Role-aware STOV Technology State |
| RQ2 | Exploitation-weighted VDP |
| RQ3 | Evidence-Calibrated Intervenable Dynamics |
| RQ4 | Unified Historical Reconstruction & Reliability |
| RQ5 | 2030 Intervention-based Technology Foresight |
| RQ6 | Quantitative Simulation + Agentic Stress Test |

# 当前冻结状态

- RQ1–RQ6：WP0 V2 暂时冻结；
- WP2 taxonomy 可在此基础上启动；
- 若 Pilot 数据证明 VDP 无法可靠映射到 Technology Entity，可在执行日志中记录并降级 RQ2，而不强行保留该贡献。
