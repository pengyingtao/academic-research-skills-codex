# WP1 Method Gap Matrix（首轮 V0.1）

> 本矩阵依据 WP1 首轮与第二轮高精度检索形成，所有 gap 结论均为暂定，需在文献池扩展至 50–80 篇后复核。

| 方法族 | 多源数据 | 数据/证据校准 | 动态状态 | 图关系 | Lead-Lag | 历史回测 | 情景干预 | 不确定性 | Agent | 当前判断 |
|---|---|---|---|---|---|---|---|---|---|---|
| Delphi / Scenario | △ | ×/△ | △ | × | × | 通常× | ✓ | △ | 人类角色 | 擅长探索 plausible futures，但量化回测和数据校准弱 |
| System Dynamics Foresight | △ | △/✓ | ✓ | ×/△ | 通常× | △ | ✓ | △ | × | 技术路径推演已成熟，历史数据校准已有先例，但多源情报和图关系不足 |
| ABM Innovation/Technology Diffusion | △ | ✓ | ✓ | ✓（社会/影响网络） | 通常× | ✓（部分研究） | ✓ | ✓（Monte Carlo 可做） | ✓ | 数据校准、预测和情景干预均已有研究，不能把 calibrated ABM 本身作为创新 |
| Bibliometric / Data-driven Foresight | ✓（部分） | ✓ | ✓（时间序列） | △ | △ | ✓ | 通常× | △ | × | 多源弱信号和数据驱动预见已出现，但通常不具可干预动态机制 |
| Patent GNN / RGNN | 通常单源 | ✓ | △ | ✓ | × | ✓（后续专利验证） | × | △ | × | 技术机会链路预测成熟，主要受限于专利单源与非情景推演 |
| Dynamic GNN / Temporal Graph TOD | 通常单源 | ✓ | ✓ | ✓ | △ | ✓（滑动窗口） | × | △ | × | 2025–2026 已直接用于技术机会发现，ECDS-TF 不能声称首次动态图技术预见 |
| Heterogeneous GNN TOD | 通常单源多实体 | ✓ | △/✓ | ✓ | × | ✓/△ | × | △ | × | 异构实体关系与语义结构已有直接先例 |
| Multi-source Weak Signal | ✓ | ✓ | ✓（主题演化） | △ | △ | △ | × | △ | × | 2026 已有专利+临床+新闻+论文多源弱信号识别，多源本身不是创新 |
| LLM Multi-Agent Forecasting/Foresight | ✓（可输入多证据） | △/✓ | ✓ | Agent interaction | △ | △/✓ | ✓ | △ | ✓ | 2025–2026 快速出现；存在 future leakage 与复现问题，适合作扩展而非主历史 baseline |
| **ECDS-TF（拟）** | **✓ STOV** | **✓** | **✓** | **✓** | **✓** | **✓ rolling** | **✓** | **✓** | **扩展 MAF-TF** | 创新只能落在组合架构与验证范式，不能落在任一单独组件“首次使用” |

---

## 首轮相似性风险评估

### 高风险创新表述——应禁止

以下表述已被当前文献直接否定，不应出现在后续论文中：

1. “首次将 System Dynamics/Simulation 用于技术预见”；
2. “首次使用 Agent-Based Modeling 进行技术预测”；
3. “首次使用真实数据校准 ABM 做创新/技术扩散预测”；
4. “首次使用动态图神经网络做技术机会发现”；
5. “首次使用异构图神经网络做技术机会预测”；
6. “首次将多源数据与弱信号结合做技术预见”；
7. “首次使用 LLM 多智能体预测科研或技术方向”。

---

## 当前最有潜力的研究缺口

### Gap A — 多源技术状态而非多源主题

现有多源研究更多聚焦主题识别/弱信号聚合。ECDS-TF 拟将 Science、Patent、Open Source、Vulnerability Demand 分别解释为不同技术演化机制，构造 Technology × Quarter 状态，而不是把不同文档简单混合聚类。

**待验证问题：** 是否已有论文+专利+开源+需求/漏洞的统一动态状态模型？

### Gap B — Cross-source Lead-Lag

拟显式学习 Paper→GitHub、GitHub→Patent、Vulnerability→Research/Engineering 等领先—滞后关系。

**待验证问题：** 现有 science-technology linkage / paper-patent linkage 文献是否已经进行了可用于预测的动态 lead-lag 建模？

### Gap C — Predictive Model → Intervenable Simulation

现有 GNN/TOD 多为一次性机会预测；现有 SD/ABM 可做情景推演但通常不具多源时序图学习。

ECDS-TF 拟把从历史证据学习到的 dynamics 转化为可干预状态转移，在不同 shock 下做 Monte Carlo forward simulation。

**待验证问题：** 是否已有“图学习动态 + scenario intervention”的技术预见框架？

### Gap D — Historical Reconstruction of Foresight

拟采用严格 temporal cutoff 与 rolling-origin backtesting，验证如果模型停留在过去某一时间点，能否重建后来真实出现的技术增长、Emergence 和 Convergence。

**待验证问题：** simulation foresight 文献中历史回测究竟普遍还是少数？是否存在多任务历史重演验证？

### Gap E — Accuracy + Calibration + Uncertainty + Counterfactual

拟同时评价：

- predictive accuracy；
- ranking quality；
- probability calibration；
- uncertainty intervals；
- counterfactual scenario sensitivity。

**待验证问题：** 是否已有技术预见模型将上述评价统一使用？

### Gap F — Quantitative Simulation + Agentic Stress Test

LLM Agent 不承担主要历史预测，而用于检验量化推演没有参数化的制度、组织、采用与极端事件风险。

**待验证问题：** 是否已有明确的“可回测计算推演 + LLM Agent scenario stress test”双轨技术预见框架？

---

## WP1 下一轮检索重点

1. paper–patent science/technology linkage + time lag；
2. open-source/GitHub 作为创新领先指标；
3. demand-pull / vulnerability signals 与安全技术研发动态；
4. historical backtesting in foresight/simulation；
5. probabilistic/calibrated technology forecasting；
6. graph-based simulation / learned dynamics + scenario intervention；
7. LLM agent forecast calibration、future leakage、time-aware evaluation。

---

## 当前结论

ECDS-TF 的可辩护创新方向已经从“新组件”转向“**新组合与新验证范式**”。

最值得保留的核心命题是：

> 将多源技术情报映射为可解释技术状态，通过历史数据学习跨源时滞和技术相互作用，将 learned dynamics 转化为可干预的概率动态推演，并使用严格历史回测验证其作为技术预见方法的有效性。

该命题仍需后续系统检索确认是否存在高度同构方法。
