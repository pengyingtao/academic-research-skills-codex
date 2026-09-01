# Research Protocol V2

## 1. 研究题目

> 《面向技术预见的证据校准动态推演方法研究——以AI赋能网络安全技术为例》

英文暂定：

> Evidence-Calibrated Dynamic Simulation for Technology Foresight: A Study of AI-Enabled Cybersecurity Technologies

## 2. WP1 后的方法定位修订

WP1 多轮方法新颖性检索结论为 `MODIFY`：题目保留，但原方案中若干单独方法组件已有明确先例，不能继续作为首创贡献。

本研究的正式定位调整为：

> **以角色化多源技术状态为基础，从历史证据学习技术动力学，将其转换为可干预的概率动态推演，并通过严格历史重演、概率校准和情景敏感性验证其作为技术预见方法的有效性。**

应用场景继续限定为 AI for Cybersecurity，而非 Security of AI。

## 3. 不再作为创新主张的组件

以下内容仅作为方法组成或 baseline，不宣称首次：

- System Dynamics / Simulation；
- Agent-Based Modeling；
- 数据校准 ABM；
- 多源数据融合；
- Papers–Patents–GitHub；
- Lead-Lag；
- Dynamic/Heterogeneous GNN；
- Probabilistic Technology Forecasting；
- Historical Backtesting；
- LLM Multi-Agent Technology Forecasting；
- Vulnerability disclosure / cyber risk → security R&D demand；
- Temporal graph counterfactual intervention。

## 4. 核心方法：ECDS-TF

主方法继续命名：

- **ECDS-TF：Evidence-Calibrated Dynamic Simulation for Technology Foresight**

### 4.1 Layer 1 — Role-aware STOV Technology State

四源被赋予不同演化角色：

- `S — Science`：科学知识生产与研究能力；
- `T — Technology/Patent`：技术化、产权化与组织研发投入；
- `O — Open Source`：工程实现、开发者扩散与工具可用性；
- `V — Vulnerability Demand Pressure`：现实安全问题、漏洞利用与修复需求压力。

技术季度状态：

\[
X_{k,t}=[S_{k,t},T_{k,t},O_{k,t},VDP_{k,t}]
\]

### 4.2 Vulnerability Demand Pressure（VDP）

不直接使用 CVE count 作为“需求”。正式定义候选：

\[
VDP_{k,t}=f(CVE_{k,t},KEV_{k,t},Severity_{k,t},Exploitability_{k,t},Exposure_{k,t},RemediationGap_{k,t})
\]

其中：

- CVE：漏洞披露规模；
- KEV：已确认实际利用；
- Severity：CVSS/影响；
- Exploitability：EPSS/LEV 或可获得代理；
- Exposure：受影响产品、平台或生态广度；
- RemediationGap：披露、利用、修复之间的时间差。

VDP 的贡献不是提出“漏洞会推动安全研发”的新理论，而是将已知机制形式化为可被历史验证的技术预见状态变量。

### 4.3 Layer 2 — Relational Encoder

Temporal/Heterogeneous Graph 的作用调整为关系编码器，而非创新主角。

负责学习：

- technology interaction；
- convergence relationships；
- neighborhood influence；
- cross-source timing / lag representation。

### 4.4 Layer 3 — Evidence-Calibrated State Transition

核心状态模型：

\[
X_{t+1}=F_\theta(X_t,G_t,Z_t)+\epsilon_t
\]

其中：

- \(X_t\)：技术状态；
- \(G_t\)：技术关系图；
- \(Z_t\)：外部环境/情景变量；
- \(\epsilon_t\)：随机不确定性。

### 4.5 Layer 4 — Intervenable Forward Simulation

学习到的 dynamics 必须可以显式施加情景 shock：

- AI capability shock；
- vulnerability/threat shock；
- OSS diffusion shock；
- regulation/constraint shock。

最终通过概率 rollout / Monte Carlo 产生 2027–2030 轨迹分布。

## 5. 数据范围

### 5.1 时间范围

- 历史起点：2012Q1
- 历史观测终点：2026Q2
- 时间粒度：Quarter
- 前瞻窗口：2026Q3–2030Q4

### 5.2 数据源

- Science：OpenAlex
- Technology：PatentsView / USPTO 等公开专利数据
- Open Source：GitHub
- Vulnerability：NVD CVE/CWE、CISA KEV、EPSS/LEV 等可获取利用概率信号

### 5.3 预测单位

统一 Technology Entity × Quarter。

## 6. 核心预测任务

### Task A — Technology Growth Forecasting

预测未来 4/8/12 季度技术增长。

指标：MAE、RMSE、sMAPE。

### Task B — Emerging Technology Detection

识别未来快速成长技术。

指标：Precision@K、Recall@K、NDCG@K、AUPRC。

### Task C — Technology Convergence Forecasting

预测技术融合关系。

指标：AUC、F1、Hits@K。

成熟度不作为主要监督标签，仅作为最终综合解释指标。

## 7. 历史重演协议

| Fold | Train | Forecast |
|---|---|---|
| F1 | 2012–2018 | 2019–2021 |
| F2 | 2012–2020 | 2021–2023 |
| F3 | 2012–2022 | 2023–2025 |

并增加 rolling-origin supplementary evaluation。

本研究不声称“首次历史回测”，而强调 Growth + Emergence + Convergence 在同一 temporal-freeze 协议下进行多任务重演。

## 8. Temporal Leakage Rules

任何预测折叠必须满足：

1. 未来论文引用不得回填；
2. 未来 GitHub stars/commits/releases 不得回填；
3. CVE modified/KEV 后验状态按预测时点截断；
4. normalization/statistics 仅用训练窗口估计；
5. taxonomy refinement 不使用未来概念反标历史；
6. embeddings/LLM 的知识截止风险必须记录；
7. LLM agent 不进入主要历史性能排行榜；
8. 若使用 AgentProphet-style 对照，采用匿名化/history-only 输入并披露 contamination risk。

## 9. Baseline 体系 V2

### Naive
- Persistence
- Linear Trend

### Statistical
- ARIMA
- Prophet
- Bass/S-curve（适用时）

### ML
- XGBoost
- LSTM

### Graph
- GCN
- R-GCN

### Temporal Graph
- TGAT
- TGN

### Agent Simulation
- ABM-R：Rule-based ABM
- ABM-C：Evidence-Calibrated ABM

### Proposed
- ECDS-v0：Evidence-Calibrated State Transition
- ECDS-v1：+ cross-source timing/lag
- ECDS-TF：+ relational temporal/heterogeneous graph encoder + probabilistic intervention rollout

### Supplementary Agentic Benchmark
- AgentProphet-style anonymized/history-only benchmark（Task B，若可严格复现）

### Future Scenario Stress Test
- **MAST：Multi-Agent Scenario Stress Test**

原 MAF-TF 名称停止作为正式方案使用。

MAST 不承担主要预测任务，仅负责发现未参数化的：

- regulation；
- organizational adoption；
- liability；
- commercialization；
- talent constraints；
- extreme events。

## 10. 消融实验 V2

至少包含：

- ECDS-TF Full
- w/o Science
- w/o Patent
- w/o GitHub
- w/o VDP
- VDP using raw CVE count only
- VDP w/o KEV/Exploitability
- w/o Lead-Lag representation
- w/o Graph Encoder
- w/o Evidence Calibration
- deterministic rollout vs probabilistic rollout

重点检验：

> VDP 是否比简单漏洞数量提供真正增量预测价值。

## 11. Reliability-oriented Evaluation

除传统性能指标外，若模型输出概率/区间，必须增加：

- Brier Score；
- Expected Calibration Error（ECE，适用时）；
- reliability diagram；
- prediction interval coverage；
- interval width / sharpness；
- scenario sensitivity；
- scenario stability。

本研究不宣称这些指标首次用于 forecasting，而是检验其在统一技术预见验证协议中的价值。

## 12. 2030 情景推演

- S0 Baseline
- S1 AI Acceleration
- S2 Threat / Vulnerability Shock
- S3 OSS Acceleration
- S4 Constraint / Regulation

每个情景 Monte Carlo N≥1000。

输出：

- growth probability；
- emergence probability；
- convergence probability；
- uncertainty intervals；
- scenario-dependent trajectory shifts。

## 13. WP1 后正式贡献候选

### C1 — Role-aware STOV Technology State

多源不是简单融合，而是不同技术演化机制状态。

### C2 — Exploitation-weighted VDP

将漏洞披露、实际利用、严重度和修复缺口形成可历史检验的技术需求压力变量。

### C3 — Evidence-Calibrated Intervenable Technology Dynamics

将历史学习到的技术 dynamics 转换为可施加情景 shock 的概率 forward simulation。

### C4 — Unified Historical Reconstruction

在同一 temporal freeze 下验证 Growth / Emergence / Convergence。

### C5 — Reliability-oriented Foresight Validation

联合评价 accuracy、ranking、calibration、coverage 与 scenario sensitivity。

### C6 — ECDS-TF + MAST 双轨

量化模型负责基准概率轨迹，agentic stress test 负责不可充分参数化因素的挑战与解释。

## 14. 当前状态

- WP0 V1：已完成；
- WP1：方法新颖性检索完成，Verdict=`MODIFY`；
- 本文件：WP0 V2 修订版；
- 下一步：同步更新 Research Questions 和 Experiment Matrix，随后关闭 WP1 并进入 WP2。
