# Research Questions

## 研究题目

> 《面向技术预见的证据校准动态推演方法研究——以AI赋能网络安全技术为例》

## RQ1：跨源技术演化规律

### 问题

AI赋能网络安全技术在科学研究、专利、开源生态和漏洞需求之间存在怎样的演化、领先—滞后和技术融合规律？

### 子问题

- RQ1a：不同 Technology Family 的 Science→Technology→Open Source 转化时滞是否显著不同？
- RQ1b：Vulnerability demand 是否对部分防御技术形成可检测的 demand-pull 效应？
- RQ1c：GitHub 是否在论文与专利之间构成可观察的工程化领先信号？
- RQ1d：技术融合是否可由跨源共现、语义接近度和动态图邻接变化提前识别？

### 待检验命题

- H1a：不同 STOV 数据源之间存在稳定但技术类别相关的 Lead-Lag 结构。
- H1b：加入 GitHub 和 CVE/CWE 后，可以观察到仅依赖论文/专利时不可见的早期技术信号。

### 证据

- Quarterly STOV time series
- Cross-correlation / Granger-style lead-lag diagnostics（只作为统计证据，不自动解释为因果）
- Dynamic graph relation evolution

---

## RQ2：证据校准是否降低主观参数依赖

### 问题

多源历史科技情报能否有效校准技术状态转移、扩散与需求响应参数，从而减少传统动态推演对专家主观参数设定的依赖？

### 对比

- ABM-R：规则/经验参数
- ABM-C：历史证据校准参数
- ECDS-v0：数据驱动状态转移

### 待检验命题

- H2a：ABM-C 在历史回测中优于 ABM-R。
- H2b：不同时间折叠中，证据校准参数具有可接受的稳定性。
- H2c：数据校准能够降低推演结果对单个专家规则设定的敏感性。

### 评价

- Growth forecast error
- Emerging technology ranking performance
- Parameter stability
- Sensitivity analysis

---

## RQ3：ECDS-TF 是否提升预测性能

### 问题

ECDS-TF 是否能够比传统统计模型、机器学习、静态图模型、动态图模型和传统 ABM 更准确地预测技术成长、新兴技术和技术融合？

### 待检验命题

- H3a：ECDS-TF 在 Task A 上总体优于传统趋势与机器学习基线。
- H3b：ECDS-TF 在 Task B 的 Precision@K / NDCG@K 上优于不含图结构与 Lead-Lag 的模型。
- H3c：ECDS-TF 在 Task C 上优于静态图模型。

### Baseline

Persistence、Linear Trend、ARIMA、XGBoost、LSTM、GCN、R-GCN、TGAT/TGN、ABM-R、ABM-C。

### 统计比较

- Across-fold mean/std
- Paired bootstrap or other appropriate paired comparison
- Effect size / confidence interval
- Multiple-comparison control where necessary

---

## RQ4：历史可验证性

### 问题

ECDS-TF 能否在历史时间切片中重建已经发生的 AI 网络安全技术演化，而不是仅产生不可证伪的未来叙事？

### 核心设计

- F1：2012–2018 → 2019–2021
- F2：2012–2020 → 2021–2023
- F3：2012–2022 → 2023–2025

### 待检验命题

- H4a：模型在多个历史窗口中保持方向一致的预测优势。
- H4b：概率输出具有可接受校准性，不只追求排序准确率。
- H4c：模型能够重建部分真实发生的技术增长与融合转折点。

### 评价

- MAE/RMSE/sMAPE
- Precision@K/Recall@K/NDCG@K/AUPRC
- AUC/F1/Hits@K
- Brier Score / ECE（如概率预测定义允许）

---

## RQ5：2030 多情景技术预见

### 问题

不同外部冲击情景下，2027—2030 年 AI赋能网络安全技术的成长、融合与演化路径有何差异？

### 情景

- S0 Baseline
- S1 AI Acceleration
- S2 Threat Shock
- S3 OSS Acceleration
- S4 Constraint

### 输出

- P(Emergence)
- P(HighGrowth)
- P(Convergence)
- 95% simulation interval
- Technology roadmap
- Tipping point distribution

### MAF-TF 扩展分析

LLM 多智能体仅用于 prospective stress test，不进入正式历史性能排名。

重点分析：

- ECDS-TF 与 MAF-TF 的技术排序一致性；
- Agent 提出的组织、监管、责任、采用成本、人才、算力等无法完全参数化因素；
- 算法与智能体预测分歧的原因。

---

# RQ 与论文贡献映射

| RQ | 主要贡献 |
|---|---|
| RQ1 | STOV 跨源技术演化理论与实证 |
| RQ2 | Evidence Calibration 方法价值 |
| RQ3 | ECDS-TF 算法性能 |
| RQ4 | 可验证技术推演方法论 |
| RQ5 | 2030 AI for Cybersecurity 技术预见 |

# 冻结规则

RQ V1 在 WP1 完成前保持稳定。若 WP1 新颖性检索证明某一问题已有充分解决，可修改 RQ，但必须在协议中记录版本变化、原因和影响，禁止在看到最终实验结果后为迎合结果重写研究问题。
