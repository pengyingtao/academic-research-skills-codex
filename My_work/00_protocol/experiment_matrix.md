# Experiment Matrix V2

> WP1 Verdict：`MODIFY`。本矩阵据最终新颖性评估修订。

## 1. 实验总目标

验证 ECDS-TF 是否能在严格 temporal freeze 下：

1. 预测 Technology Growth；
2. 识别 Emerging Technologies；
3. 预测 Technology Convergence；
4. 输出校准概率与可靠不确定性；
5. 将 learned dynamics 转换为可干预 2030 forward simulation；
6. 证明 VDP 相较 raw CVE count 的增量价值；
7. 使用 MAST 做未来情景压力测试，而非历史预测主模型。

---

## 2. 数据状态

统一季度状态：

\[
X_{k,t}=[S_{k,t},T_{k,t},O_{k,t},VDP_{k,t}]
\]

### VDP 候选字段

- CVE count
- CWE composition
- CVSS / severity
- KEV count/share
- EPSS / LEV / exploitability proxy
- affected product / ecosystem exposure
- disclosure-to-exploit lag
- disclosure/exploit-to-remediation lag

---

## 3. 预测任务

| Task | Target | Horizon | Core Metrics |
|---|---|---|---|
| A Growth | technology growth/value change | 4/8/12 quarters | MAE, RMSE, sMAPE |
| B Emerging | future high-growth/emergence label/rank | 4/8/12 quarters | Precision@K, Recall@K, NDCG@K, AUPRC |
| C Convergence | future technology pair relation/link | 4/8/12 quarters | AUC, F1, Hits@K |

---

## 4. Historical Reconstruction Folds

| Fold | Train | Forecast | Purpose |
|---|---|---|---|
| F1 | 2012–2018 | 2019–2021 | earlier-cycle reconstruction |
| F2 | 2012–2020 | 2021–2023 | mid-cycle reconstruction |
| F3 | 2012–2022 | 2023–2025 | frontier-era reconstruction |

Supplementary：rolling-origin evaluation。

### Temporal Freeze Audit

每 fold 记录：

- data snapshot cutoff；
- citation cutoff；
- GitHub activity cutoff；
- CVE/KEV status cutoff；
- normalization fit range；
- taxonomy version；
- embedding/LLM contamination note。

---

## 5. Baseline Matrix V2

| Family | Model | Task A | Task B | Task C | Scenario | Role |
|---|---|---:|---:|---:|---:|---|
| Naive | Persistence | ✓ | △ | × | × | minimum baseline |
| Naive | Linear Trend | ✓ | △ | × | × | trend baseline |
| Statistical | ARIMA | ✓ | △ | × | × | time-series baseline |
| Statistical | Prophet | ✓ | △ | × | × | trend/seasonality |
| Diffusion | Bass / S-curve | ✓ | △ | × | △ | diffusion baseline |
| ML | XGBoost | ✓ | ✓ | △ | × | tabular predictive baseline |
| DL | LSTM | ✓ | ✓ | △ | × | temporal baseline |
| Graph | GCN | △ | ✓ | ✓ | × | static relation baseline |
| Graph | R-GCN | △ | ✓ | ✓ | × | heterogeneous relation baseline |
| Temporal Graph | TGAT | △ | ✓ | ✓ | × | temporal graph baseline |
| Temporal Graph | TGN | △ | ✓ | ✓ | × | temporal graph baseline |
| Agent | ABM-R | ✓ | ✓ | △ | ✓ | rule-based simulation baseline |
| Agent | ABM-C | ✓ | ✓ | △ | ✓ | calibrated simulation baseline |
| Proposed | ECDS-v0 | ✓ | ✓ | △ | ✓ | calibrated state transition |
| Proposed | ECDS-v1 | ✓ | ✓ | △ | ✓ | + timing/lag representation |
| Proposed | ECDS-TF | ✓ | ✓ | ✓ | ✓ | full framework |
| Supplementary | AgentProphet-style history-only/anonymized | ×/△ | ✓ | × | × | recent agentic forecasting comparator |
| Stress Test | MAST | × | × | × | ✓ | future scenario critique only |

---

## 6. ECDS 渐进实现

### ECDS-v0

无图版本：

\[
X_{t+1}=F_\theta(X_t,Z_t)+\epsilon_t
\]

目的：验证 evidence-calibrated state transition 本身是否有效。

### ECDS-v1

加入 cross-source timing / lag 表示。

目的：检验异步信息是否有边际增益，而不将 Lead-Lag 本身作为创新主张。

### ECDS-TF

加入 relational temporal/heterogeneous graph encoder：

\[
H_t=GraphEncoder(G_{1:t})
\]

\[
X_{t+1}=F_\theta(X_t,H_t,Z_t)+\epsilon_t
\]

随后执行 probabilistic rollout 和 intervention。

---

## 7. VDP 专项实验

### VDP-0

`raw CVE count`

### VDP-1

`CVE + Severity`

### VDP-2

`CVE + Severity + KEV/Exploitability`

### VDP-Full

`CVE + KEV + Severity + Exploitability + Exposure + RemediationGap`

### 比较问题

1. VDP-Full 是否显著优于 raw CVE？
2. 哪些技术族从 VDP 获益最大？
3. VDP 是否提供提前 1–8 个季度的防御技术增长信号？
4. VDP 是否提高 calibration，而不仅提高平均 accuracy？

---

## 8. 消融矩阵

| Ablation | Purpose |
|---|---|
| w/o Science | 科学知识通道价值 |
| w/o Patent | 技术化通道价值 |
| w/o GitHub | 工程扩散通道价值 |
| w/o VDP | 安全需求压力价值 |
| VDP→raw CVE | exploitation-weighted demand 是否必要 |
| VDP w/o KEV/EPSS/LEV | 实际利用权重价值 |
| w/o Lag Representation | 异步信息价值 |
| w/o Graph Encoder | 关系学习价值 |
| w/o Calibration | 数据估参价值 |
| Deterministic rollout | 概率推演价值 |
| w/o intervention layer | “forecast”与“foresight simulation”的差异 |

---

## 9. Reliability Evaluation

### Point / Ranking

- MAE
- RMSE
- sMAPE
- Precision@K
- Recall@K
- NDCG@K
- AUPRC
- AUC
- F1
- Hits@K

### Probability Calibration

- Brier Score
- ECE（适用时）
- reliability diagram

### Interval Reliability

- empirical coverage
- mean interval width
- sharpness

### Scenario Reliability

- sensitivity to shock magnitude
- rank stability
- trajectory stability
- seed sensitivity / Monte Carlo convergence

---

## 10. AgentProphet-style 补充对照

仅针对 Task B。

### 原则

- 优先采用匿名技术 ID；
- 输入 history-only numeric/source-profile records；
- 不提供未来名称和未来事件；
- 明确披露 LLM 训练语料带来的潜在 contamination；
- 若无法严格复现 AgentProphet 公开设置，则只做 supplementary comparison，不进入主结论统计显著性比较。

---

## 11. 2030 Intervention Matrix

| Scenario | Intervention | Main Question |
|---|---|---|
| S0 Baseline | no structural shock | current dynamics continuation |
| S1 AI Acceleration | increase AI capability/productivity parameters | 哪些防御技术最受AI能力跃迁驱动？ |
| S2 Threat/VDP Shock | raise exploitability/KEV/remediation pressure | 哪些技术被安全需求快速牵引？ |
| S3 OSS Acceleration | increase OSS diffusion/adoption | 开源是否压缩科学到工程化时滞？ |
| S4 Constraint | regulation/liability/compute/adoption friction | 哪些技术路线最脆弱？ |

每情景：Monte Carlo N≥1000。

---

## 12. MAST — Multi-Agent Scenario Stress Test

### 输入

- ECDS-TF scenario trajectories；
- uncertainty intervals；
- technology rankings；
- explicit scenario assumptions。

### Agent Roles

- Research Analyst
- Industry Adoption Analyst
- OSS Ecosystem Analyst
- Cyber Threat/Defense Analyst
- Regulation/Governance Analyst
- Adversarial Synthesizer

### 输出

- missing assumptions
- failure modes
- counterexamples
- tail risks
- adoption barriers
- scenario narratives

MAST 不输出用于主排行榜的历史准确率。

---

## 13. Decision Gates

### Gate 1 — Pilot Taxonomy

若跨源 Technology Entity 映射质量不足，则停止大规模采集。

### Gate 2 — Predictive Signal

若简单 baseline 均无法得到稳定信号，暂停复杂 ECDS-TF 开发并重新审视目标标签。

### Gate 3 — VDP Value

若 VDP-Full 对 raw CVE 无稳定增益：

- 将 VDP 从核心贡献降级为领域特征；
- 不通过调参强行制造贡献。

### Gate 4 — Graph Value

若 graph encoder 无稳定增益，ECDS-TF 可退化为非图动态状态模型。

### Gate 5 — Historical Reliability

若历史重演失败，则不发布确定性 2030 技术排名，只保留探索性 scenario findings。

---

## 14. 当前状态

- WP0 V2：本矩阵已更新；
- WP1：等待执行日志正式关闭；
- 下一阶段：WP2 taxonomy + Pilot Corpus。
