# WP1 核心文献矩阵（定向查重 V0.2）

> 本文件记录 WP1 高相关方法文献。当前已完成 simulation/ABM、动态图、Lead-Lag、GitHub/开源、历史验证、不确定性与 LLM temporal leakage 的定向检索；仍需继续扩展文献池至 50–80 篇后再形成最终新颖性结论。

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
| L13 | 2026 | Wu et al., *Identifying firm-specific technology opportunities: Heterogeneous graph neural network-based link prediction* | 异构图 + Multi-Attention Graph Link Prediction | 专利结构与语义信息 | 案例/预测验证 | 无 | 证明异构实体关系与语义结构已有直接先例 | 高 |
| L14 | 2026 | Liu et al., *Future-oriented technology opportunities identification via extending patent citation network with LSTM and GCN* | LSTM + GCN | 专利引用网络 + 语义时间轨迹 | 未来导向机会预测 | 无 | 证明时间序列 + 图联合预测技术机会已存在 | 高 |
| L15 | 2026 | Wang & Zhu, *Technology foresight in China’s industrial robotics with MLWS-TF* | Machine Learning + Weak Signals | 数据驱动技术预见 | 模型验证 | 无 | 证明“完全数据驱动 + 弱信号”技术预见已出现 | 高（针对 data-driven/weak signal） |
| L16 | 2026 | Tang et al., *Early Identification of Emerging Research Topics through Weak Signal Analysis of Multi-Source Data* | BERTopic + 多源弱信号 | 专利、临床、新闻、论文四源数据 | 新兴主题识别 | 无 | 证明多源数据 + 弱信号早期识别已存在；STOV 多源本身不能作为唯一创新 | 高 |
| L17 | 2017 | Kim & Lee, *Novelty-focused weak signal detection in futuristic data* | Text mining + Local Outlier Factor | futuristic data | 弱信号识别 | 无 | 弱信号 novelty 指标已有成熟基础 | 中 |
| L18 | 2025 | Choi et al., *Academic Simulacra: Forecasting Research Ideas through Multi-Agent LLM Simulations* | 多智能体 LLM scholar simulation | 作者历史发表记录；预测后续 research ideas | 与真实论文语义比较 | Agent simulation | 证明 multi-agent LLM 已用于科研方向/idea forecasting；MAF-TF 只能作为扩展而非首创核心 | 高（针对 LLM Agent） |
| L19 | 2024 | Ba et al., *Discovering technological opportunities by identifying dynamic structure-coupling patterns and lead-lag distance between science and technology* | S&T network coupling + Time-Lag Cross-Correlation | 论文/专利科学—技术知识网络 | 能源节约案例验证 | 无 | 直接证明 Science–Technology lead-lag 已用于技术机会发现；ECDS-TF 不可声称首次 Lead-Lag | **很高** |
| L20 | 2026 | Yu et al., *Asynchrony as information: Predicting technology transfer opportunities through science–technology knowledge lag* | LLM语义对齐 + TLCC + temporal co-occurrence graph + dual-stream attention | WoS论文 + Incopat专利；S&T knowledge lag 作为图属性 | 1/3/5-step ahead；F1 相对最佳基线提升 | 无 | 已把“知识滞后 + 图注意力 + 多步预测”组合起来；迫使 ECDS-TF 将 Lead-Lag 降为组件而非核心首创 | **极高** |
| L21 | 2026 | Wang & Wu, *A Multi-Source Data Fusion Framework for Emerging Technology Topic Identification: Integrating Publications, Patents, and GitHub Open-Source Data* | BERTopic + 多源指标 + 熵权 | 论文 + 专利 + GitHub | 消融实验 | 无 | 直接证明 Papers–Patents–GitHub 多源融合已出现，且研究明确将 GitHub 解释为早期工程信号 | **极高** |
| L22 | 2026 | *Navigating the AI technology landscape from GitHub data* | GitHub repository network + attributed clustering + GCN link prediction | 2879 个 AI GitHub repositories，library coupling | 预测 AI technology landscape changes | 无 | GitHub 单独用于技术景观预测已成立；Open Source 不能仅作为“新数据源”贡献 | 高 |
| L23 | 2024 | Brown et al., *Measuring Software Innovation with Open Source Software Development Data* | OSS innovation indicators | 约 28,000 packages、200,000 releases | 一年滞后依赖增长预测 | 无 | 支持 GitHub/OSS 作为创新活动可量化数据，并存在 lagged predictive signal | 中 |
| L24 | 2023 | Kang et al., *Papers with code or without code? Impact of GitHub repository usability on the diffusion of machine learning research* | paper–GitHub linkage + econometric causal analysis | Papers with Code + MAG + GitHub API | 月度时间分析 | 无 | 说明论文与开源代码存在可测的时序耦合；GitHub 不只是结果变量，也影响后续科研扩散 | 中 |
| L25 | 2026 | Tang et al., *Paper with code diffusion on GitHub: Disruption or consolidation?* | GitHub diffusion metrics + citation network + interpretable ML | 29,900 CS papers with GitHub links（2009–2024） | 统计/ML验证 | 无 | 进一步证明“论文—代码扩散”可系统建模，但研究目标不是技术预见 | 中 |
| L26 | 2019 | Apreda et al., *Expert forecast and realized outcomes in technology foresight* | Ex-post foresight validation | 医疗设备技术预见与五年后实际结果 | 直接比较 false positive/negative | 无 | 证明 foresight ex-post validation 有明确先例，同时文献强调长期预见通常难直接验证 | 高（针对“首次历史验证”） |
| L27 | 2020 | *Forecasting emerging technologies using data augmentation and deep learning* | Deep Learning emerging-tech prediction | 历史技术数据 | 用 2000–2016 训练预测 2017，并用 2017 实际结果验证 | 无 | 明确历史 cutoff 验证先例；ECDS-TF 不能声称首次 backtesting | 高 |
| L28 | 2026 | Zhang & Pu, *From Micro-Signals to Macro-Trends... BCI Innovations*（SSRN） | DNN + GRU + hierarchical trend forecast | 技术微观信号 | 五个 rolling-origin historical windows | 无 | rolling-origin technology forecasting 已有近期直接尝试；作为补充而非最终证据 | 中高 |
| L29 | 2003 | Martino, *A review of selected recent advances in technological forecasting* | 技术预测方法综述 | 多类技术预测 | 综述 | probabilistic simulation | 早已讨论 probabilistic technology forecasts；“概率预见”本身不是新概念 | 中 |
| L30 | 1991 | Cho et al., *A Delphi technology forecasting approach using a semi-Markov concept* | Semi-Markov probabilistic technology development + simulation | Delphi sequential development estimates | 模型模拟 | 有 | 技术发展状态的概率转移/模拟早已有先例；ECDS-TF 的状态转移需强调数据和图关系的不同 | 高 |
| L31 | 2006 | Daim et al., *Forecasting emerging technologies: Use of bibliometrics and patent analysis* | Bibliometrics + patent + scenario + growth curves + SD | 论文/专利 + 历史数据校准 | 多案例验证 | 有 | 很早已有“多方法 + 数据校准 + SD + scenario”的混合框架，组合创新必须更具体 | **极高** |
| L32 | 2025 | *Towards agent-based-model informed neural networks* | ABM-informed restricted GNN + learned dynamics | 经验轨迹/ABM结构 | out-of-sample + interventions | 支持 counterfactual | 虽非技术预见，但说明“结构化机制模型 + GNN learned dynamics + intervention”在其他领域已存在；ECDS-TF 的算法新颖性需落在 foresight/STOV 特化与验证协议 | 高（跨领域方法风险） |
| L33 | 2026 | *SCGRN: Spatiotemporal causal graph reasoning network for regional economic development modeling* | causal discovery + spatial graph + temporal model | 21年区域面板 | out-of-sample | counterfactual policy simulation | 非技术预见，但直接表明“时空图学习 + counterfactual intervention”不是通用方法空白 | 高（跨领域方法风险） |
| L34 | 2025 | Gao et al., *Can Prompts Rewind Time for LLMs?* | prompted knowledge cutoff evaluation | LLM temporal tasks | temporal contamination evaluation | 无 | 说明单靠提示词不能可靠建立历史知识截止；MAF-TF 回测必须谨慎 | 高（实验设计） |
| L35 | 2026 | Liu et al., *ExAnte: A Benchmark for Ex-Ante Inference in Large Language Models* | ex-ante benchmark + leakage rate | 股票、QA、Wikipedia、scientific publication generation | cutoff leakage evaluation | 无 | 进一步确认 LLM 在显式时间截止下仍可能利用未来信息 | 高（实验设计） |
| L36 | 2026 | Zhang et al., *All Leaks Count, Some Count More* | claim-level temporal contamination + Shapley-DCLR + TimeSPEC | 多类预测任务 | leakage audit | 无 | 支持 MAF-TF 若用于历史回测需 claim-level 时间验证，而匿名化/提示词并不足够 | 高（实验设计） |
| L37 | 2026 | Zhang & Stadie, *Temporal Leakage in LLM Backtesting* | leakage measurement / matched controls | LLM forecasting backtests | leakage-adjusted scores | 无 | 指出被动 backtest 很难区分 recency 与 leakage，需要 defensible reference；强化“LLM agent 只做未来压力测试”的当前决策 | 高（实验设计） |
| L38 | 2026 | Xu et al., *LLM-based Agents for Forecasting and Prediction: Methods, Training, Evaluation, and Applications* | forecasting-agent survey | 多领域 | 综述 calibration、contamination、live evaluation | 多种 | 说明 LLM forecasting agents 已形成方法谱系，且测量/校准/污染是核心瓶颈 | 中高 |
| L39 | 2026 | Veen, *Anticipatory Methods for the Emergence of Radically New Technologies: Navigating Uncertainty* | foresight methods under uncertainty | 多案例方法比较 | 方法比较 | scenario | 支持“高不确定性下单一预测模型不足、应组合方法”的理论依据 | 中 |

---

## 第二轮定向查重后的结论

### 已明确不是空白的部分

1. **System Dynamics / simulation 用于 technology foresight**：长期存在。
2. **Agent-based technology forecasting / innovation diffusion forecasting**：至少自 2009 年已有直接研究。
3. **经验数据/数据驱动 ABM 校准**：已有经验校准、参数估计和自动生成模型研究。
4. **动态图/GNN/异构图用于 Technology Opportunity Discovery**：2025–2026 年已明显成熟。
5. **Science–Technology Lead-Lag**：2024 年已有直接技术机会发现；2026 年已出现 knowledge lag + temporal graph/attention + multi-step prediction。
6. **论文 + 专利 + GitHub 多源技术识别**：2026 年已有直接框架；GitHub 也已被单独用于 AI 技术景观预测。
7. **历史 cutoff / ex-post validation / rolling-origin**：已有不同程度先例，不能声称首次历史回测技术预见。
8. **概率技术预测**：至少 1990s–2000s 已有 probabilistic/semi-Markov 传统。
9. **LLM 多智能体科研/预测**：已经出现，并存在严重 temporal leakage 风险。
10. **learned graph dynamics + counterfactual intervention**：虽在技术预见中尚未发现高度同构框架，但在复杂系统、宏观经济等邻域已出现，算法层面不能把这一组合泛化地宣称首创。

### 当前剩余、仍值得继续验证的候选 gap

1. **STOV 角色化技术状态模型**：不是简单把多源文本混合聚类，而是把 Science、Patent、Open Source、Vulnerability 分别作为知识生产、产权化/技术化、工程扩散和安全需求压力的可解释状态通道。
2. **Vulnerability demand channel**：当前定向检索尚未发现把 CVE/CWE/KEV 作为“需求牵引变量”进入技术预见状态转移/情景推演的直接方法论文；但“未检出”不是“证明不存在”，需继续专项检索。
3. **从 forecast 到 intervenable foresight 的统一实现**：技术预见内部尚未发现同时拥有多源时序图学习、learned state dynamics、显式 shock/intervention、Monte Carlo forward simulation 的高度同构工作；但跨领域方法存在明显相似先例。
4. **统一验证协议**：已有单项 historical validation、rolling-origin、probabilistic forecasts，但仍需验证是否有技术预见论文在同一框架里同时做 Growth/Emergence/Convergence、多折历史重演、概率校准、情景敏感性。
5. **计算式预测 + Agentic stress test 的角色分工**：尚未检出明确采用“可回测量化模型负责基准概率、LLM agents 只负责不可参数化因素压力测试”的技术预见框架。

> 当前最重要的方法学调整：Lead-Lag、GitHub、多源、概率化、历史回测都应从“创新点”降级为 ECDS-TF 的组成模块。真正需要争取的是 **STOV 特化机制 + vulnerability demand + 可干预推演 + 严格统一验证范式** 的整体贡献。
