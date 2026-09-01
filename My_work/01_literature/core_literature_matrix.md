# WP1 核心文献矩阵（首轮检索 V0.1）

> 本文件记录 WP1 第一、二轮高相关方法文献。当前为首轮样本，不代表最终系统检索完成。

| ID | 年份 | 文献/方法 | 主要方法 | 数据/校准 | 回测/验证 | 情景推演 | 与 ECDS-TF 的关系 | 相似风险 |
|---|---:|---|---|---|---|---|---|---|
| L01 | 2009 | Shin & Park, *Brownian agent-based technology forecasting* | Brownian agent-based technology forecasting | 韩国软件产业数据 | 案例仿真 | 有 | 直接证明 Agent-based technology forecasting 已存在；需避免宣称“首次智能体技术预测” | 中 |
| L02 | 2009 | *Agent-based modeling of the diffusion of environmental innovations – An empirical approach* | 经验型 ABM | 问卷经验数据校准，独立数据验证 | 有 | 有 | 证明“经验数据校准 ABM + 未来场景”已有先例 | 中 |
| L03 | 2012 | Chen, Wakeland & Yu, *A two-stage technology foresight model with system dynamics simulation...* | Delphi + System Dynamics | 专家识别关键技术；SD 参数需历史数据校准 | 仿真实验 | 有 | 直接证明 SD 用于 technology foresight 已成熟；论文还明确指出历史数据校准和复杂建模是限制 | 高（针对“推演”概念） |
| L04 | 2014 | *Technology foresight for medical device development through hybrid simulation: The ProHTA Project* | System Dynamics + ABM hybrid simulation | 医疗技术案例数据 | 案例验证 | 有 | 证明混合宏观/微观 simulation 已用于技术预见 | 中 |
| L05 | 2016 | Chen, Yu & Wakeland, *Generating technology development paths to the desired future through system dynamics modeling and simulation* | System Dynamics | 关键技术/扩散参数 | 模型实验 | 有 | 证明通过 simulation 生成“通向期望未来的技术路径”已有明确研究 | 高（针对“路线推演”） |
| L06 | 2016 | Xiao & Han, *Forecasting new product diffusion with agent-based models* | ABM + 参数估计 + HIN | 317 条耐用消费品扩散时间序列；估计非结构参数 | 与传统扩散模型比较 | 有 | 证明 ABM 可作为预测工具且可由真实数据估参 | 中 |
| L07 | 2017 | *Automating agent-based modeling: Data-driven generation and application of innovation diffusion models* | 数据驱动自动生成 ABM | 从经验扩散数据自动筛选/拟合模型 | 通过经验模式筛选 | 有干预实验 | 证明“数据驱动/证据校准 ABM”不是空白；ECDS-TF 必须超越这一贡献 | 高（针对 evidence calibration） |
| L08 | 2021 | Rand & Stummer, *Agent-based modeling of new product market diffusion: an overview of strengths and criticisms* | ABM 方法综述 | 讨论参数化、验证、随意性、计算成本等问题 | 方法综述 | 支持 | 为 ECDS-TF 论证“校准与验证难题”提供方法基础 | 低 |
| L09 | 2021 | Stummer et al., *Beaming market simulation to the future by combining agent-based modeling with scenario analysis* | ABM + Scenario Analysis | 创新/市场扩散 | 情景实验 | 强 | 证明 ABM + scenario 已成熟，不能把“智能体情景推演”本身当首创 | 中 |
| L10 | 2025 | Zhang et al., *Discovering technology opportunities of latecomers based on RGNN and patent data* | RGNN / patent network | 单一专利源，33,347 patent families | 用后续专利申请验证预测机会 | 无 | 证明 GNN + technology opportunity + 时间后验验证已存在 | 高（针对图预测） |
| L11 | 2025 | Chen et al., *Study on Technology Opportunity Discovery Method in Medical Field Based on Dynamic Graph Neural Network* | DynGNN-TOD | 专利动态技术语义网络，滑动时间窗 | AUC、Accuracy@10 与 baseline 比较 | 无 | 证明动态图神经网络直接用于 TOD 已存在 | 高（针对动态图创新） |
| L12 | 2026 | Du et al., *Technology Opportunity Identification Based on Dynamic Graph Neural Networks* | DGNN | 动态技术关系数据 | 对比实验 | 无 | 进一步确认 2026 年 DGNN-TOD 已成为现实研究线 | 高 |
| L13 | 2026 | Wu et al., *Identifying firm-specific technology opportunities: Heterogeneous graph neural network-based link prediction* | 异构图 + Multi-Attention Graph Link Prediction | 专利结构与语义信息 | 案例/预测验证 | 无 | 证明异构图 + 技术机会链路预测已存在 | 高 |
| L14 | 2026 | Liu et al., *Future-oriented technology opportunities identification via extending patent citation network with LSTM and GCN* | LSTM + GCN | 专利引用网络 + 语义时间轨迹 | 未来导向机会预测 | 无 | 证明时间序列 + 图联合预测技术机会已存在 | 高 |
| L15 | 2026 | Wang & Zhu, *Technology foresight in China’s industrial robotics with MLWS-TF* | Machine Learning + Weak Signals | 数据驱动技术预见 | 模型验证 | 无 | 证明“完全数据驱动 + 弱信号”技术预见已出现 | 高（针对 data-driven/weak signal） |
| L16 | 2026 | Tang et al., *Early Identification of Emerging Research Topics through Weak Signal Analysis of Multi-Source Data* | BERTopic + 多源弱信号 | 专利、临床、新闻、论文四源数据 | 新兴主题识别 | 无 | 证明多源数据 + 弱信号早期识别已存在；STOV 多源本身不能作为唯一创新 | 高 |
| L17 | 2017 | Kim & Lee, *Novelty-focused weak signal detection in futuristic data* | Text mining + Local Outlier Factor | futuristic data | 弱信号识别 | 无 | 弱信号 novelty 指标已有成熟基础 | 中 |
| L18 | 2025 | Choi et al., *Academic Simulacra: Forecasting Research Ideas through Multi-Agent LLM Simulations* | 多智能体 LLM scholar simulation | 作者 2024 前出版历史；针对 2024 论文思想预测 | 与真实论文语义比较、随机 baseline | Agent simulation | 证明 multi-agent LLM 已用于科研方向/idea forecasting；MAF-TF 只能作为扩展而非首创核心 | 高（针对 LLM Agent） |

---

## 首轮结论

### 已明确不是空白的部分

1. **System Dynamics / simulation 用于 technology foresight**：已有长期研究线。
2. **Agent-based technology forecasting / innovation diffusion forecasting**：至少自 2009 年已有直接研究。
3. **经验数据/数据驱动 ABM 校准**：已有经验校准、参数估计和自动生成模型研究。
4. **动态图/GNN/异构图用于 Technology Opportunity Discovery**：2025–2026 年已明显成熟。
5. **多源数据 + 弱信号识别**：2026 年已有直接多源研究。
6. **LLM 多智能体科研方向预测**：2025 年已有直接先例。

### 当前仍可能成立的组合型研究缺口（待继续系统验证）

1. 将 **Science + Patent + Open-source + Vulnerability demand** 作为技术状态证据共同建模，而不是仅多源主题识别；
2. 从多源历史证据中学习 **technology state transition + cross-source lead-lag + technology interaction**；
3. 将 learned dynamics 用于 **可干预的 Monte Carlo scenario simulation**，而非仅做一次性预测；
4. 使用严格 **rolling historical backtesting / temporal cutoff** 验证推演能否重建真实技术演化；
5. 将 **predictive accuracy + probability calibration + uncertainty + counterfactual scenarios** 放进同一技术预见框架；
6. 将 LLM Agent 限定为情景压力测试，与可回测计算推演形成双轨，而不是用 LLM 直接替代量化模型。

> 以上六点仍是“候选 gap”，必须继续检索后才能写入论文作为正式创新。
