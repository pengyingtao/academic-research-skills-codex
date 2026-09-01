# Experiment Matrix

## 1. 实验目标

建立从数据、任务、Baseline、主模型、回测、消融到2030情景推演的一致实验矩阵，使不同方法在相同数据切分、标签定义与评价指标下可公平比较。

## 2. 数据窗口

- 历史观测：2012Q1–2026Q2
- 时间粒度：Quarter
- 最终推演：2026Q3–2030Q4

## 3. 预测任务

| Task | 目标 | Horizon | 主指标 |
|---|---|---|---|
| A Growth | 技术增长预测 | 4/8/12季度 | MAE, RMSE, sMAPE |
| B Emerging | 新兴技术识别/排序 | 4/8/12季度 | Precision@K, Recall@K, NDCG@K, AUPRC |
| C Convergence | 技术融合预测 | 4/8/12季度 | AUC, F1, Hits@K |

## 4. 回测折叠

| Fold | Train End | Forecast Window | 用途 |
|---|---|---|---|
| F1 | 2018Q4 | 2019Q1–2021Q4 | 早期历史回测 |
| F2 | 2020Q4 | 2021Q1–2023Q4 | 中期历史回测 |
| F3 | 2022Q4 | 2023Q1–2025Q4 | 近期历史回测 |

说明：具体训练起点统一为2012Q1；后续可追加 rolling-origin folds。

## 5. 方法矩阵

| ID | 类别 | 方法 | Task A | Task B | Task C | 是否正式Baseline |
|---|---|---|---:|---:|---:|---:|
| B00 | Naive | Persistence | ✓ | ✓ | 视定义 | ✓ |
| B01 | Naive | Linear Trend | ✓ | ✓ | × | ✓ |
| B02 | Statistical | ARIMA | ✓ | ✓ | × | ✓ |
| B03 | Statistical | Prophet | ✓ | ✓ | × | 可选 |
| B04 | Diffusion | Bass/S-curve | ✓ | ✓ | × | 条件适用 |
| B05 | ML | XGBoost | ✓ | ✓ | 可扩展 | ✓ |
| B06 | Sequence | LSTM | ✓ | ✓ | 可扩展 | ✓ |
| B07 | Graph | GCN | 可扩展 | ✓ | ✓ | ✓ |
| B08 | Heterogeneous Graph | R-GCN | 可扩展 | ✓ | ✓ | ✓ |
| B09 | Temporal Graph | TGAT | ✓ | ✓ | ✓ | ✓ |
| B10 | Temporal Graph | TGN | ✓ | ✓ | ✓ | ✓ |
| B11 | Agent Simulation | ABM-R | ✓ | ✓ | ✓ | ✓ |
| B12 | Calibrated Agent Simulation | ABM-C | ✓ | ✓ | ✓ | ✓ |
| P00 | Proposed | ECDS-v0 | ✓ | ✓ | 可扩展 | 否 |
| P01 | Proposed | ECDS-v1 | ✓ | ✓ | 可扩展 | 否 |
| P02 | Proposed | ECDS-TF | ✓ | ✓ | ✓ | 主模型 |
| X01 | Exploratory | MAF-TF | 未来情景 | 未来情景 | 未来情景 | 否 |

## 6. 主模型递进设计

### P00 ECDS-v0

Evidence-Calibrated State Transition，不含图与Lead-Lag。

目标：验证“从历史数据校准动态状态转移”是否本身有效。

### P01 ECDS-v1

ECDS-v0 + 跨源 Lead-Lag。

目标：验证 STOV 不同数据源的时滞信息是否带来增益。

### P02 ECDS-TF

ECDS-v1 + Temporal Heterogeneous Graph。

目标：验证技术之间及多类实体之间动态关系是否进一步提高增长、涌现与融合预测能力。

## 7. 消融矩阵

| Ablation | Science | Patent | GitHub | Vulnerability | Lead-Lag | Graph | Calibration |
|---|---:|---:|---:|---:|---:|---:|---:|
| Full | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| w/o Science | × | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| w/o Patent | ✓ | × | ✓ | ✓ | ✓ | ✓ | ✓ |
| w/o GitHub | ✓ | ✓ | × | ✓ | ✓ | ✓ | ✓ |
| w/o Vulnerability | ✓ | ✓ | ✓ | × | ✓ | ✓ | ✓ |
| w/o Lead-Lag | ✓ | ✓ | ✓ | ✓ | × | ✓ | ✓ |
| w/o Graph | ✓ | ✓ | ✓ | ✓ | ✓ | × | ✓ |
| w/o Calibration | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | × |

## 8. 数据表示

统一最小表：Technology × Quarter。

主要字段族：

### Science
- paper_count
- paper_growth
- citation_growth
- novelty
- interdisciplinary_score

### Patent
- patent_count
- patent_growth
- cpc_diversity
- assignee_diversity
- patent_citation_growth

### Open Source
- repo_count
- repo_growth
- stars_growth
- commit_growth
- contributor_growth
- release_growth

### Vulnerability
- cve_count
- cve_growth
- cvss_mean
- high_critical_ratio
- kev_count
- cwe_diversity

### Graph/Structural
- centrality
- community
- convergence_score
- neighborhood_growth
- source_diffusion_entropy

## 9. 标签定义待办

以下标签必须在 WP1/WP2 后正式冻结：

1. Growth target 的归一化与极端值处理；
2. Emerging Technology 的阈值/排名定义；
3. Convergence edge 的生成标准；
4. 技术类别最小数据支持量；
5. 冷启动 Technology 的处理方式。

禁止根据最终测试集结果反复调整阈值；阈值选择必须在训练/验证窗口完成并记录。

## 10. 模型选择与超参数规则

1. 所有模型共享相同 temporal split；
2. 超参数仅使用训练集或训练集内部验证窗口选择；
3. 不使用未来窗口做 early stopping；
4. 报告随机种子；
5. 随机模型至少重复 5 次，资源允许时 10 次；
6. 报告 mean ± std；
7. 记录依赖版本、硬件和运行时间。

## 11. 统计比较

计划采用：

- Across-fold paired comparison
- Bootstrap confidence interval
- Effect size
- 必要时多重比较校正

最终检验方法根据数据分布和独立性条件确定，不预先强制使用不适合的参数检验。

## 12. ABM Baseline 规则

### ABM-R

参数来源：文献、规则或公开专家知识；完整记录规则表和参数来源。

### ABM-C

保持尽可能相同的 Agent 结构，仅将核心增长、扩散、需求响应和融合参数改由历史 STOV 数据校准。

ABM-R vs ABM-C 用于独立识别 Evidence Calibration 的贡献。

## 13. MAF-TF 规则

MAF-TF 不进入 F1/F2/F3 正式性能排行榜，主要原因是 LLM 训练语料可能包含历史预测窗口之后的信息，存在 Future Leakage。

仅用于 2027–2030 prospective foresight：

- Scientist Agent
- Industry Agent
- Open-source Agent
- Cyber Defender Agent
- Technology Analyst Agent

比较 ECDS-TF 与 MAF-TF 排名和观点一致性：Spearman rho、Kendall tau、Jaccard@K 等。

## 14. 2030 情景矩阵

| Scenario | 核心冲击 | 主要调整参数 |
|---|---|---|
| S0 Baseline | 当前趋势延续 | 基准 |
| S1 AI Acceleration | AI模型/Agent能力加速 | AI capability / transition rate ↑ |
| S2 Threat Shock | 漏洞与攻击压力增加 | vulnerability demand ↑ |
| S3 OSS Acceleration | 开源生态加速 | OSS diffusion ↑ |
| S4 Constraint | 监管/成本/治理约束 | adoption / diffusion ↓ |

每个情景目标 Monte Carlo N=1000；输出概率分布、95%区间和技术排序，而非单点结论。

## 15. 实验成功判据

WP0 阶段不预设“主模型必须显著获胜”。成功标准是：

1. 所有方法在同一数据口径下可复现；
2. temporal leakage 得到严格控制；
3. 至少三轮历史回测完成；
4. 能区分 Calibration、Lead-Lag、Graph、多源数据各自的边际贡献；
5. 若 ECDS-TF 未优于强基线，结果仍如实报告并重新评估方法假设。

## 16. 当前状态

Version: experiment_matrix_v1

Status: WP0 FROZEN FOR WP1

允许在 WP1 文献检索和 WP2 Pilot Taxonomy 后进行有理由的协议修订，但必须保留版本记录，禁止结果导向修改。
