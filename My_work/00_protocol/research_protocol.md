# Research Protocol

## 1. 研究题目

> 《面向技术预见的证据校准动态推演方法研究——以AI赋能网络安全技术为例》

英文暂定：

> Evidence-Calibrated Dynamic Simulation for Technology Foresight: A Study of AI-Enabled Cybersecurity Technologies

## 2. 研究定位

本研究定位为方法创新型技术预见研究。核心目标不是简单描述 AI+网络安全热点，而是提出并验证一种“证据校准动态推演”方法，用多源历史科技情报学习技术演化参数，并通过历史回测、基线比较、消融实验和多情景 Monte Carlo 推演对方法进行验证。

应用场景限定为 AI for Cybersecurity，而非 Security of AI。

## 3. 核心方法

主方法暂定命名：

- ECDS-TF：Evidence-Calibrated Dynamic Simulation for Technology Foresight

核心组成：

1. STOV 多源科技情报框架：Science、Technology、Open Source、Vulnerability；
2. 跨源技术实体对齐；
3. 技术季度状态向量；
4. Lead-Lag 跨源领先—滞后学习；
5. Temporal Heterogeneous Graph；
6. Evidence Calibration；
7. Dynamic State Transition；
8. Monte Carlo Scenario Simulation；
9. 历史回测与不确定性评估。

## 4. 数据范围

### 4.1 时间范围

- 历史数据起点：2012Q1
- 历史观测终点：2026Q2
- 时间粒度：季度
- 最终未来推演：2026Q3–2030Q4

2026Q3 及之后数据不得作为当前冻结版本的历史训练信息。

### 4.2 数据源

- Science：OpenAlex
- Technology：PatentsView/公开专利数据
- Open Source：GitHub
- Vulnerability：NVD CVE/CWE/KEV

### 4.3 预测对象

预测对象为统一 Technology Entity，不以单篇论文、单个专利或单个仓库作为主要预测单位。

## 5. 主要预测任务

### Task A：Technology Growth Forecasting

预测技术未来 4、8、12 个季度增长状态。

主指标：MAE、RMSE、sMAPE。

### Task B：Emerging Technology Detection

识别未来进入快速成长阶段的技术。

主指标：Precision@K、Recall@K、NDCG@K、AUPRC。

### Task C：Technology Convergence Forecasting

预测未来技术之间的融合关系。

主指标：AUC、F1、Hits@K。

### 暂不作为主要监督任务

技术成熟度暂不作为主要监督标签。成熟度仅作为后期综合指数或2030推演结果之一，避免因主观 maturity ground truth 导致自定义标签循环论证。

## 6. 历史回测

核心折叠：

| Fold | Train | Forecast |
|---|---|---|
| F1 | 2012–2018 | 2019–2021 |
| F2 | 2012–2020 | 2021–2023 |
| F3 | 2012–2022 | 2023–2025 |

后续根据数据量增加 rolling-origin evaluation。

## 7. Temporal Leakage 规则

对任何历史预测折叠：

1. 预测起点后的论文引用数不得进入训练特征；
2. 预测起点后的 GitHub stars/commits/releases 不得进入训练特征；
3. 预测起点后的 CVE modified 信息不得回填；
4. 标准化参数必须仅由训练窗口估计；
5. taxonomy refinement 不得利用未来技术名称或未来聚类结果反向修改历史标签；
6. embedding 模型、LLM 或外部知识用于回测时必须记录其可能的时间泄漏风险；
7. LLM 多智能体不进入正式历史性能排名。

## 8. Baseline 体系

### Naive
- Persistence
- Linear Trend

### Statistical
- ARIMA
- Prophet（可选）
- Bass/S-curve（适用于相应任务时）

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
- ECDS-v0
- ECDS-v1
- ECDS-TF

### Exploratory
- MAF-TF：LLM Multi-Agent Foresight，仅用于未来情景压力测试。

## 9. 消融实验

至少包含：

- ECDS-TF Full
- w/o Science
- w/o Patent
- w/o GitHub
- w/o Vulnerability
- w/o Lead-Lag
- w/o Graph
- w/o Calibration

## 10. 2030情景推演

- S0 Baseline
- S1 AI Acceleration
- S2 Threat Shock
- S3 OSS Acceleration
- S4 Constraint

每个情景目标 Monte Carlo N=1000，输出概率分布与95%区间，而非单一点预测。

## 11. 预期主要贡献

1. STOV 多源技术演化证据框架；
2. ECDS-TF 证据校准动态推演方法；
3. 面向技术预见的历史回测验证框架；
4. AI for Cybersecurity 2027–2030 多情景技术演化预见；
5. 计算式推演与智能体情景压力测试的混合预见范式。

## 12. 当前状态

WP0：启动并冻结 V1。

下一门槛：完成 WP1 文献与方法新颖性验证后，才能正式确认 ECDS-TF 的创新性表述。
