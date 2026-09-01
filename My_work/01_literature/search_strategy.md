# WP1 方法新颖性系统检索策略

## 1. 研究目的

本阶段用于验证论文拟提出的 Evidence-Calibrated Dynamic Simulation for Technology Foresight（ECDS-TF）是否具有真实、可辩护的方法创新性。

重点不是证明“没有人做过推演”，而是识别现有研究分别解决了哪些问题、尚未解决哪些问题，并判断以下模块是否已经存在高度相似组合：

1. 多源科技情报融合；
2. 数据驱动/证据校准的动态推演；
3. 时序异构图学习；
4. 跨源 Lead-Lag 学习；
5. 历史时间切片回测；
6. 概率校准与不确定性；
7. Monte Carlo / scenario simulation；
8. ABM 与 LLM Agent 辅助 foresight。

---

## 2. 核心检索问题

### SQ1
技术预见中 simulation、system dynamics、ABM 的参数通常如何确定？是否依赖 Delphi/专家判断，还是存在大规模历史数据自动校准？

### SQ2
是否已有将论文、专利、开源项目、漏洞/需求信号共同用于技术预见的统一多源框架？

### SQ3
动态图/时序异构图已被用于哪些 technology opportunity discovery、technology convergence、emerging technology prediction 任务？

### SQ4
现有计算式技术预见是否进行严格历史回测和 temporal holdout？

### SQ5
现有 foresight simulation 是否同时输出概率分布、不确定性区间，并允许反事实情景干预？

### SQ6
LLM/多智能体在 foresight 中主要承担预测器、情景生成器、角色模拟器还是压力测试器？其 future leakage 与复现问题如何处理？

---

## 3. 检索主题簇

### Cluster A — Simulation Foresight

- "technology foresight" AND simulation
- "technology forecasting" AND simulation
- "interactive foresight simulation"
- "scenario simulation" AND technology
- "dynamic simulation" AND foresight

### Cluster B — System Dynamics / Agent-Based Modeling

- "system dynamics" AND "technology foresight"
- "system dynamics" AND "technology forecasting"
- "agent-based model" AND "technology foresight"
- "agent-based simulation" AND innovation diffusion
- "exploratory modeling" AND technology transition

### Cluster C — Data-driven / Computational Foresight

- "data-driven technology foresight"
- "computational foresight"
- "evidence-based foresight"
- "quantitative foresight" AND technology
- "machine learning" AND "technology foresight"

### Cluster D — Graph / Temporal Graph

- "graph neural network" AND "technology opportunity"
- "heterogeneous graph" AND technology forecasting
- "temporal graph" AND technology forecasting
- "dynamic graph" AND technology convergence
- patent graph neural network technology opportunity

### Cluster E — Multi-source / Weak Signals / Lead-Lag

- "multi-source" AND technology foresight
- "weak signal" AND technology foresight
- "science technology linkage" AND forecasting
- paper patent linkage technology forecasting
- open source patent paper technology forecasting
- lead lag technology forecasting

### Cluster F — LLM / Agentic Foresight

- LLM agent foresight
- multi-agent future simulation
- LLM agent-based modeling foresight
- generative agents scenario planning
- research idea forecasting multi-agent

---

## 4. 数据库与来源优先级

### Tier 1：高优先级学术来源

- Web of Science / Scopus（如可访问）
- ScienceDirect
- SpringerLink
- Wiley
- IEEE Xplore
- ACM Digital Library
- Nature Portfolio
- Taylor & Francis

### Tier 2：开放学术检索

- Google Scholar（人工检索入口）
- Semantic Scholar
- OpenAlex
- Crossref
- arXiv（仅作前沿补充，不与同行评审论文等权）

### Tier 3：机构/方法资料

- OECD Strategic Foresight
- EU JRC Foresight
- UNDP Foresight
- NIST / DARPA / MITRE（用于 AI+Cybersecurity 技术语境，不替代方法论文）

---

## 5. 时间范围

- 经典基础文献：不限年份；
- 方法新颖性重点：2015–2026；
- LLM/Agentic Foresight：重点 2023–2026；
- 对 2025–2026 新方法进行单独标注，避免把已有最新研究误判为研究空白。

---

## 6. 纳入标准

文献满足至少一项：

1. 明确提出或应用技术预见/技术预测方法；
2. 使用 System Dynamics、ABM、simulation、scenario simulation 做未来技术/创新系统研究；
3. 使用多源科技情报做技术机会识别/技术演化预测；
4. 使用图学习、动态图或异构图做技术预测；
5. 讨论计算式 foresight 的验证、校准、不确定性或回测；
6. 使用 LLM/Agent 进行 futures/foresight/scenario/research forecasting。

优先纳入可获得 DOI、正式出处、摘要/全文方法信息的研究。

---

## 7. 排除标准

1. 仅讨论一般经济预测而无技术预见关系；
2. 仅使用“foresight”作为普通英文词，而非研究方法；
3. 纯网络安全攻击仿真、无技术演化/预见目标；
4. 纯 GNN 算法论文、无技术机会/技术预测应用；
5. 纯场景叙事、没有方法描述且无法支持方法比较；
6. 重复预印本与正式论文同时出现时优先保留正式版本。

---

## 8. 文献编码字段

每篇核心文献至少记录：

- Citation ID
- Title
- Authors
- Year
- Venue
- DOI/URL
- Foresight target
- Method family
- Data sources
- Multi-source? (Y/N)
- Simulation? (Y/N)
- System dynamics? (Y/N)
- ABM? (Y/N)
- Graph/temporal graph? (Y/N)
- Parameter calibration source
- Lead-Lag modeling? (Y/N)
- Historical backtest? (Y/N)
- Scenario intervention? (Y/N)
- Uncertainty output? (Y/N)
- Agent/LLM? (Y/N)
- Main findings
- Main limitations
- Relation to ECDS-TF
- Similarity risk: Low / Medium / High

---

## 9. 初始 Method Gap Matrix 维度

| 方法族 | 多源数据 | 数据校准 | 动态状态 | 图关系 | Lead-Lag | 历史回测 | 情景干预 | 不确定性 | Agent |
|---|---|---|---|---|---|---|---|---|---|
| Delphi | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 |
| System Dynamics | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 |
| ABM | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 |
| Bibliometric/Data-driven | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 |
| GNN/Temporal Graph | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 |
| LLM/Agentic Foresight | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 | 待检索 |
| ECDS-TF（拟） | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 扩展 |

> ECDS-TF 行是拟研究设计，不表示已经证明其独创性。只有 WP1 完成后才能确认哪些组合属于真实 gap。

---

## 10. WP1 完成判据

- 核心文献池达到 50–80 篇；
- 能够对每个拟创新模块找到直接比较对象；
- 至少识别 3 个可辩护且非措辞型的研究缺口；
- 对“Evidence Calibration + Dynamic Simulation + Multi-source + Backtesting”是否存在高度相似工作做出明确结论；
- 若存在高相似方法，返回 WP0 修改模型名称、问题或贡献边界。
