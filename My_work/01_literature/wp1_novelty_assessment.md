# WP1 方法新颖性评估（中期 V0.2）

> 论文题目：《面向技术预见的证据校准动态推演方法研究——以AI赋能网络安全技术为例》
>
> 状态：`INTERIM / IN_PROGRESS`
>
> 本文件只记录当前系统检索支持到的中期判断。任何“首次”“首创”“尚无研究”等表述，除非后续 50–80 篇核心文献编码完成并进行反例检索，否则不得写入论文最终贡献。

---

## 1. 当前结论摘要

截至本轮检索，ECDS-TF 原先设想中的多数单项组件均已有直接或邻近先例：

- simulation / System Dynamics technology foresight：已有；
- Agent-based technology forecasting：已有；
- empirical/data-calibrated ABM：已有；
- dynamic / heterogeneous GNN for technology opportunity discovery：已有；
- Science–Technology lead-lag：已有，而且 2026 年已有 knowledge lag + temporal graph attention + multi-step prediction；
- publications + patents + GitHub multi-source emerging-technology identification：已有；
- GitHub-based technology landscape forecasting：已有；
- ex-post/historical validation：已有；
- probabilistic technology forecasting：已有；
- LLM multi-agent research/forecast simulation：已有；
- learned graph dynamics + intervention/counterfactual simulation：在其他复杂系统领域已有。

因此，ECDS-TF 不能依赖任何一个单独组件的“首次使用”建立新颖性。

---

## 2. 必须放弃的创新主张

后续论文不得使用以下未经限定的表述：

1. 首次用 simulation/SD 做技术预见；
2. 首次用 ABM 做技术预测；
3. 首次用数据校准 ABM；
4. 首次用动态图/异构图做技术机会发现；
5. 首次建模 science–technology lead-lag；
6. 首次融合论文、专利、GitHub 做技术预见；
7. 首次使用 GitHub 预测未来技术景观；
8. 首次进行历史回测技术预见；
9. 首次做概率技术预测；
10. 首次使用 LLM 多智能体做未来研究方向预测；
11. 首次提出图学习动力学 + counterfactual intervention 的通用方法。

---

## 3. 当前仍有潜力的贡献中心

### 3.1 Vulnerability Demand Pull（当前优先级最高）

拟将 CVE/CWE/KEV 从一般“漏洞数据源”重新定义为 AI for Cybersecurity 技术发展的 **问题/需求压力通道**：

\[
V_{k,t} \rightarrow S/T/O_{k,t+h}
\]

其中：

- \(V\)：漏洞暴露、弱点类别、可利用性/威胁压力；
- \(S\)：科学研究响应；
- \(T\)：专利/技术化响应；
- \(O\)：开源工具、工程实现和修复生态响应。

当前定向检索主要发现 CVE 严重度预测、漏洞披露、风险管理与漏洞数量预测，尚未发现高度直接的“CVE/CWE/KEV demand-pull → technology foresight state transition”方法论文。

**中期判断：高潜力，但必须继续做直接反例检索。**

关键风险：

- CVE 数量同时受到披露制度、CNA 扩张、检测工具能力变化影响，不等于真实安全需求；
- 必须引入 CVSS、KEV、CWE、受影响产品、披露制度等控制或分解变量；
- 需要证明 vulnerability signal 对未来 Research/Patent/GitHub 的增量预测价值，而不是相关性叙事。

---

### 3.2 STOV Role-aware Technology State

不是把论文、专利、GitHub、CVE 文本简单拼接聚类，而是定义四个机制通道：

| 通道 | 机制解释 |
|---|---|
| Science | 科学知识产生、方法突破、研究前沿 |
| Technology/Patent | 技术化、产权化、产业化意图 |
| Open Source | 工程实现、开发者采用、复用和扩散 |
| Vulnerability | 问题暴露、风险压力、修复/防御需求 |

统一形成：

\[
X_{k,t}=[S_{k,t},T_{k,t},O_{k,t},V_{k,t}]
\]

研究单位是 **Technology × Quarter**，不是 Document/Topic 本身。

**中期判断：中高潜力。** 前三源融合已出现，因此贡献必须依赖“角色化状态 + 动态机制 + 第四源 vulnerability demand”，不能只强调多源。

---

### 3.3 Learned Dynamics → Intervenable Foresight

拟方法：

```text
Historical STOV states
→ learn technology interactions / state transitions
→ explicit scenario/shock operators
→ Monte Carlo forward trajectories
```

区别于：

- GNN/TOD：常停留在 future link/rank prediction；
- SD/ABM：可干预但动力学通常依赖人工机制或较低维参数；
- ECDS-TF：希望让推演机制从历史多源状态与关系中学习，同时保留干预接口。

但跨领域已经存在 ABM-informed neural networks、causal spatiotemporal GNN + counterfactual simulation 等方法。

**中期判断：中高潜力、跨领域方法风险高。** 后续应避免把算法描述成通用 learned simulator 首创，而强调 technology-foresight-specific state/action design。

---

### 3.4 Historical Reconstruction Protocol

历史 backtesting 不是空白，因此拟贡献调整为严格统一协议：

1. 多个 rolling origins；
2. 同时预测 Growth / Emergence / Convergence；
3. cutoff 后所有 citation、GitHub、CVE、taxonomy 信息完全隔离；
4. baseline 和 simulation 共享相同 data freeze；
5. normalization、topic/entity mapping 也必须按 cutoff 重建；
6. 明确 temporal leakage audit；
7. 将 ex-post reconstruction 作为“模型可用性证据”，而不是证明未来必然正确。

**中期判断：中等新颖性，强方法严谨性贡献。**

---

### 3.5 Calibration + Uncertainty + Scenario Sensitivity

概率预测本身历史悠久，因此拟保留的是统一评价设计：

- point/rank accuracy；
- Brier Score / ECE；
- interval coverage；
- scenario sensitivity；
- robustness under alternative state definitions；
- multiple historical origins。

**中期判断：中等。** 更适合作为研究质量与可信度贡献，而不是核心算法创新。

---

### 3.6 Quantitative Simulation + Agentic Stress Test

LLM agent 不承担历史主要性能评估。

建议最终双轨：

**Track A — ECDS-TF**
- 可历史回测；
- 给出基准技术发展概率；
- 可校准、不确定性可量化。

**Track B — MAF-TF**
- 只用于 2027–2030 prospective scenarios；
- 分析组织采用、监管、责任、极端事件等难参数化因素；
- 重点解释算法/Agent 分歧。

当前 LLM forecasting 文献已经显示，提示模型“只使用过去信息”并不能可靠阻止 temporal contamination。

**中期判断：中等新颖性，但实验设计合理性较强。**

---

## 4. 当前贡献优先级

| 优先级 | 候选贡献 | 新颖性潜力 | 主要风险 |
|---|---|---|---|
| 1 | Vulnerability Demand Pull | 高 | CVE ≠ 真实需求；必须做严格信号分解和增量预测验证 |
| 2 | STOV role-aware state + dynamic mechanism | 中高 | 论文+专利+GitHub 已有直接融合研究 |
| 3 | learned dynamics → intervenable technology simulation | 中高 | 跨领域已有相似算法结构 |
| 4 | unified historical reconstruction protocol | 中 | backtesting 本身已有 |
| 5 | calibration + uncertainty + scenario sensitivity | 中 | 通用 forecasting 已成熟 |
| 6 | quantitative model + agentic stress test | 中 | agentic foresight 发展很快 |
| 降级 | Lead-Lag | 低（独立贡献） | 2024/2026 直接先例 |
| 降级 | GitHub early signal | 低（独立贡献） | 2026 多源和 GitHub 预测均有直接先例 |

---

## 5. 当前拟修订后的方法核心

ECDS-TF 后续应围绕下式设计：

\[
X_{k,t+1}=F_{\theta}(X_{k,t},H_{k,t},D_{k,t},I_t)+\epsilon_{k,t}
\]

其中：

- \(X_{k,t}\)：STOV role-aware technology state；
- \(H_{k,t}\)：技术之间的动态图关系表示；
- \(D_{k,t}\)：需求/漏洞压力及其结构性分解；
- \(I_t\)：显式 scenario intervention/shock；
- \(\epsilon\)：随机扰动与不可观测因素。

Lead-Lag 进入 \(F_\theta\) 的动态特征，但不作为独立原创主张。

---

## 6. WP1 下一步直接任务

### Task 1 — Vulnerability Demand 专项反例检索

目标：确认是否已有 CVE/CWE/KEV 被用于：

- cybersecurity technology forecasting；
- technology opportunity discovery；
- defense R&D demand forecasting；
- innovation response / research response；
- patent/GitHub growth prediction。

### Task 2 — Technology foresight 内部 learned dynamics + intervention

目标：区分：

- 一般复杂系统 learned simulator；
- 真正 technology foresight / innovation foresight 中的 learned dynamics + scenario intervention。

### Task 3 — Probability calibration in technology forecasting

目标：检查是否已有 Brier/ECE/conformal/coverage 等正式 calibration 评价进入技术预见。

### Task 4 — Hybrid quantitative + LLM scenario design

目标：查找是否存在“量化模型提供概率 + LLM agent 仅做 stress test”的同构架构。

### Task 5 — 文献池扩展

当前矩阵已编码 39 个高相关方法/邻域条目；继续扩展到 50–80 篇，并区分：

- Core direct evidence；
- Adjacent methodological evidence；
- Context/implementation evidence。

---

## 7. 中期判定

**当前不建议放弃题目，但必须缩窄创新叙事。**

最有希望的论文贡献不再是“我用了 GNN / Lead-Lag / GitHub / Agent”，而是：

> **在 AI for Cybersecurity 技术预见中，将科学知识、专利、开源工程和漏洞压力解释为不同演化机制，验证漏洞压力的需求牵引作用，从多源历史状态学习技术动力学，经严格历史重演后用于可干预、带不确定性的动态推演，并用智能体对不可参数化情景做压力测试。**

该陈述仍为研究假设，WP1 未完成前不得写成最终“首创”结论。
