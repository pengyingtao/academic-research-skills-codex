# WP1 Method Gap Matrix（定向查重 V0.2）

> 本矩阵依据 WP1 多轮高精度检索形成。结论仍为中期判断，最终 gap 需在核心文献池扩展至 50–80 篇、完成系统编码后复核。

| 方法族 | 多源数据 | 数据/证据校准 | 动态状态 | 图关系 | Lead-Lag | 历史回测 | 情景干预 | 不确定性 | Agent | 当前判断 |
|---|---|---|---|---|---|---|---|---|---|---|
| Delphi / Scenario | △ | ×/△ | △ | × | × | 少数 ex-post | ✓ | ✓（定性） | 人类角色 | 擅长 plausible futures；已有事后准确性研究，但难形成连续可重复 ground truth |
| System Dynamics Foresight | △/✓ | ✓ | ✓ | ×/△ | 通常× | △ | ✓ | ✓（Monte Carlo/概率可扩展） | × | bibliometrics/patent + SD + scenario + calibration 早已有先例，不能把“证据+推演”笼统作为创新 |
| ABM Innovation/Technology Diffusion | △ | ✓ | ✓ | ✓（社会/影响网络） | 通常× | ✓（部分） | ✓ | ✓ | ✓ | calibrated ABM、预测和 scenario intervention 都已有；ABM-C 只能做 baseline |
| Bibliometric / Data-driven Foresight | ✓ | ✓ | ✓（时间序列） | △ | ✓（S&T） | ✓ | 通常× | △ | × | 多源、Lead-Lag、弱信号、历史预测验证都已有明确先例 |
| Patent GNN / RGNN | 通常单源 | ✓ | △ | ✓ | ×/△ | ✓ | × | △ | × | 技术机会链路预测成熟 |
| Dynamic GNN / Temporal Graph TOD | 通常单源/双源 | ✓ | ✓ | ✓ | ✓（最新工作） | ✓（多步/滑动） | × | △ | × | 2024–2026 已出现 S&T lag + temporal graph/attention；图与 Lead-Lag 均非独立创新 |
| Heterogeneous GNN TOD | 多实体，常单数据域 | ✓ | △/✓ | ✓ | △ | ✓/△ | × | △ | × | 异构关系与语义结构已有成熟先例 |
| Multi-source Weak Signal / Topic Identification | ✓ | ✓ | ✓（主题演化） | △ | △ | △ | × | △ | × | 论文+专利+GitHub 已有直接研究；GitHub 被明确解释为早期工程信号 |
| GitHub-based Technology Forecasting | 开源为主 | ✓ | ✓ | ✓ | 可构造 | ✓/△ | × | △ | × | 2026 已有 GitHub 技术景观 + GCN link prediction；OSS 作为技术数据源已进入正式预测研究 |
| Probabilistic Technology Forecasting | △ | △ | ✓ | 通常× | × | △ | ✓（部分 simulation） | ✓ | × | semi-Markov/probabilistic forecasts 至少 1990s 已有；概率化本身不是创新 |
| LLM Multi-Agent Forecasting/Foresight | ✓（可输入多证据） | △/✓ | ✓ | Agent interaction | △ | 有但高污染风险 | ✓ | △ | ✓ | 预测 Agent 研究已形成谱系；temporal leakage 是核心测量问题 |
| Cross-domain Learned Dynamics + Intervention | 领域数据 | ✓ | ✓ | ✓ | 可学习 | ✓ | ✓ | ✓/△ | 可含 ABM | 非 technology foresight，但 ABM-informed NN、causal spatiotemporal GNN 已支持 counterfactual intervention；算法通用组合不能声称首创 |
| **ECDS-TF（拟）** | **✓ STOV** | **✓** | **✓** | **✓** | **✓（组件）** | **✓ rolling** | **✓** | **✓** | **扩展 MAF-TF** | 创新只能落在领域特化机制与统一验证/推演范式，不能落在单个组件首次使用 |

---

## 已被检索否定的高风险创新表述

后续论文禁止直接使用以下表述：

1. “首次将 System Dynamics / Simulation 用于技术预见”；
2. “首次使用 Agent-Based Modeling 进行技术预测”；
3. “首次使用真实数据校准 ABM 做技术/创新扩散预测”；
4. “首次使用动态图或异构图神经网络做技术机会预测”；
5. “首次显式建模 science–technology lead-lag”；
6. “首次将论文、专利和 GitHub 融合用于新兴技术识别”；
7. “首次使用 GitHub 预测技术景观”；
8. “首次通过历史 cutoff/backtesting 验证新兴技术预测”；
9. “首次进行概率化技术预测”；
10. “首次使用 LLM 多智能体预测科研/技术方向”；
11. “首次把 learned graph dynamics 用于 intervention/counterfactual simulation”（跨领域已有先例）。

---

# 当前真正值得保留的 Gap

## Gap A — STOV 的“角色化状态建模”，而非多源拼接

当前已有论文 + 专利 + GitHub 多源主题识别。因此 ECDS-TF 不能把“三源/四源融合”本身作为贡献。

拟保留的差异是将四源映射为不同机制通道：

- **Science**：知识产生与科学前沿；
- **Technology/Patent**：技术化、产权化与产业信号；
- **Open Source**：工程实现、开发者扩散与实际复用；
- **Vulnerability**：安全需求、问题暴露与防御压力。

模型对象是 `Technology × Quarter State`，而不是把所有文档混在一个 topic corpus 里计算综合指标。

**当前风险：中。** 前三源已有直接融合研究；Vulnerability 角色化进入技术预见尚需专项确认。

---

## Gap B — Vulnerability Demand Pull

当前对 CVE/CWE 的文献主要集中在漏洞预测、严重度、披露机制、风险管理；定向检索暂未发现把 CVE/CWE/KEV 作为“技术需求牵引变量”，与论文/专利/GitHub 一起用于防御技术演化预测或技术预见状态转移的高度直接方法论文。

拟检验：

\[
VulnerabilityPressure_{k,t} \rightarrow Research/OSS/PatentGrowth_{k,t+h}
\]

重点不只是使用 CVE，而是验证其是否构成某些 AI for Cybersecurity 防御技术的领先或同步需求信号。

**当前风险：低—中；当前最值得继续深挖。** “未检索到”不等于不存在。

---

## Gap C — Forecast → Intervenable Technology Simulation

技术预见内部的 GNN/TOD 通常执行：

`historical graph → future edge/topic/rank prediction`

SD/ABM 则通常执行：

`assumed/calibrated mechanisms → scenario intervention → future trajectories`

ECDS-TF 拟连接两者：

`STOV historical states → learned relations/dynamics → explicit intervention/shock → Monte Carlo trajectories`

但 ABM-informed neural networks、causal spatiotemporal GNN 在其他领域已经支持 learned dynamics + counterfactual intervention。

因此贡献应表述为：

> 在技术预见问题中构造可从多源技术情报学习、又可被场景干预的状态转移推演，而不是宣称发明了 learned simulator。

**当前风险：中高（跨领域方法相似）；领域化贡献仍可能成立。**

---

## Gap D — 统一的 Historical Reconstruction Protocol

历史验证不是空白：

- expert foresight 有五年后 ex-post realization comparison；
- emerging-tech ML 已有 past→future cutoff 验证；
- 新近技术预测已有 rolling-origin 尝试。

ECDS-TF 如要保留验证贡献，必须把它收紧成“统一协议”：

1. 固定 temporal cutoff；
2. 多个 rolling origins；
3. Growth / Emergence / Convergence 三任务同一数据冻结；
4. 所有 taxonomy、归一化、citation、GitHub/CVE metadata 均按当时可用信息重建；
5. simulation 与 predictive baseline 用同一测试窗口；
6. 明确 leakage audit。

**当前风险：中。** 创新在 rigor 和统一性，不在“首次 backtest”。

---

## Gap E — Accuracy + Calibration + Uncertainty + Scenario Sensitivity 的统一评价

概率技术预测历史很长，Conformal Prediction 等不确定性校准方法在通用 forecasting 也成熟。

当前仍需验证：技术预见领域是否已有一个框架同时报告：

- Growth error；
- Emerging ranking；
- Convergence link prediction；
- Brier/ECE 等概率校准；
- coverage / prediction intervals；
- shock/scenario sensitivity；
- historical rolling backtest。

**当前风险：中。** 更像评价协议贡献，而非算法原创。

---

## Gap F — Quantitative Forecast + Agentic Stress Test 的角色分工

LLM forecasting agents 已存在，且 2025–2026 研究明确显示：仅通过提示“回到过去”无法可靠防止 post-cutoff knowledge leakage。

因此 ECDS-TF 不应让 MAF-TF 参与主要历史排行榜。

建议角色固定为：

- ECDS-TF：可回测、可校准的基准概率；
- ABM-R / ABM-C：机制型正式 baseline；
- MAF-TF：只在真实未来 2027–2030 做组织、监管、采用、极端事件压力测试。

**当前风险：低—中。** 尚未检出完全同构的双轨技术预见设计，但需继续搜索 hybrid forecasting-agent + simulation work。

---

# 当前优先级重新排序

| 优先级 | 候选贡献 | 当前新颖性潜力 | 风险 |
|---|---|---:|---:|
| 1 | CVE/CWE/KEV 作为 Vulnerability Demand Pull 进入多源技术状态与动态推演 | **高** | 需证明映射有效，不应把 CVE 数量简单等同需求 |
| 2 | 多源 learned dynamics → 可干预 Monte Carlo 技术推演 | **中高** | 跨领域已有相似 learned simulator |
| 3 | STOV 四通道机制化状态建模 | **中高** | 论文+专利+GitHub 已被占位 |
| 4 | 严格统一历史重演/temporal leakage audit | **中** | 单项 backtesting 已存在 |
| 5 | Accuracy + calibration + uncertainty + scenario sensitivity 统一评估 | **中** | 通用概率预测方法成熟 |
| 6 | ECDS + LLM Agent stress test 双轨 | **中** | Agentic foresight 快速发展 |
| 已降级 | Lead-Lag | **低（作为独立创新）** | 2024/2026 已有高度直接工作 |
| 已降级 | GitHub early signal | **低（作为独立创新）** | 2026 已有直接多源/景观预测 |

---

# 下一轮 WP1 专项检索

1. `CVE/CWE/KEV + demand pull + cybersecurity innovation`：验证 Gap B；
2. `cybersecurity technology forecasting + vulnerability data`：寻找直接反例；
3. `learned simulator + technology foresight + intervention/counterfactual`：验证 Gap C 是否已有领域内工作；
4. `probability calibration + technology forecasting/foresight`：验证 Gap E；
5. `hybrid quantitative foresight + LLM agents/scenario stress testing`：验证 Gap F；
6. 扩展核心文献池至 50–80 篇并按统一编码表整理。

---

## 当前中期结论

ECDS-TF 的论文叙事应从“把很多新技术拼起来”转向一个更严格的问题：

> **能否将可追溯的科学、专利、开源与漏洞压力证据转化为面向技术实体的状态变量，从历史中学习其演化机制，并在严格历史重演验证后，把这些机制用于可干预、带不确定性的未来技术推演？**

如果后续检索证明 Vulnerability Demand Pull 和该统一推演/验证范式尚缺直接同构研究，这将是比 Lead-Lag、GNN、GitHub、多源融合本身更可辩护的贡献中心。
