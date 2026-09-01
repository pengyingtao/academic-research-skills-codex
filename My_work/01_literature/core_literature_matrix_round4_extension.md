# WP1 核心文献矩阵扩展（第四轮定向查重）

> 本文件作为 `core_literature_matrix.md` 的第四轮扩展，编号延续 L40–L55。与主矩阵合计后，WP1 当前高相关/方法邻域文献池达到 55 条。后续 WP1 收尾时再合并去重为最终矩阵。

| ID | 年份 | 文献/方法 | 主要方法 | 数据/校准 | 回测/验证 | 情景推演 | 与 ECDS-TF 的关系 | 相似风险 |
|---|---:|---|---|---|---|---|---|---|
| L40 | 2023 | Xiong et al., *An empirical analysis of vulnerability information disclosure impact on patch R&D of software vendors* | 回归 + Cox 风险模型 | CNNVD 漏洞披露数据 + 软件厂商数据 | 实证检验漏洞披露对补丁 R&D 概率/速度影响 | 无 | 直接证明“漏洞信息会牵引补丁研发”已有实证先例；ECDS-TF 不可声称首次发现 vulnerability demand-pull | **极高（针对 demand-pull 概念）** |
| L41 | 2023 | Lattanzio & Ma, *Cybersecurity risk and corporate innovation* | 文本化 cyber-risk exposure + 企业创新计量 | 企业 10-K、专利、R&D 等 | 实证因果/关联分析 | 无 | 证明网络安全风险会改变企业专利、知识产权与研发策略；“安全压力影响创新”不是空白 | 高 |
| L42 | 2026 | Gal-Or, Hydari & Telang, *Merchants of vulnerabilities: How bug bounty programs benefit software vendors* | 博弈论模型 | 厂商、白帽/黑帽发现竞争与披露/修复机制 | 理论机制分析 | 有策略情景 | 表明漏洞发现、披露激励与厂商安全研发/发布时间之间可被机制化建模；可为 V 通道提供微观机制基础 | 中高 |
| L43 | 2025 | Piao, Li & Woods, *Measuring the Vulnerability Disclosure Policies of AI Vendors* | 混合方法 + 大规模政策/事件/论文比较 | 264 AI vendors、1,130 AI incidents、359 academic publications | 跨源时序比较 | 无 | 发现 AI 厂商漏洞披露政策演化滞后于学术研究与现实事件，支持“安全事件—研究—治理”存在可测异步关系 | 高（场景直接相关） |
| L44 | 2025 | NIST CSWP 41, *Likely Exploited Vulnerabilities: A Proposed Metric for Vulnerability Exploitation Probability* | exploit likelihood metric / security measurement | CVE、KEV、EPSS 等 | 需要产业测量进一步验证 | 无 | 说明 CVE 总量并不等于有效需求信号；Vulnerability 通道应区分 disclosed vulnerability 与 exploitation-weighted pressure | 高（数据定义） |
| L45 | 1992 | *Probabilistic technological forecasts using precursor events* | 最大熵 + precursor-event time-lag probability distribution | 航空航天/汽车技术前兆事件 | 案例验证 | 概率预测 | 早已存在“前兆事件→技术出现时间”的概率预测；概率分布和 lead-time 不是新概念 | 高（针对概率预测） |
| L46 | 2007 | Banuls & Salmeron, *A Scenario-Based Assessment Model—SBAM* | Scenario generation + assessment model | 技术环境不确定性 | 方法案例 | 有 | 说明 scenario assessment 早已尝试将情景生成与技术政策评估连接；情景评价本身不是创新 | 中 |
| L47 | 2016 | Lee, Kim & Lee, *Towards robust technology roadmapping: How to diagnose the vulnerability of organisational plans* | Future analysis + ANP + scenario robustness | 组织技术路线图案例 | 情景下计划脆弱性诊断 | 有 | 技术路线图已有显式 uncertainty / robustness 分析；ECDS-TF 的不确定性贡献要落在概率校准和动态推演验证 | 中高 |
| L48 | 2021 | Golkar et al., *Model-based approaches for technology planning and roadmapping: Technology forecasting and game-theoretic modeling* | 技术预测 + 博弈论规划 | 技术性能/时间/风险不确定性 | 模型案例 | 有多个规划选项/情景 | 已将 forecasting 与可行动 planning 连接；ECDS-TF 应强调 learned dynamics + empirical backtest + intervention simulation 的差异 | 高 |
| L49 | 2021 | Luo, *Forecasting COVID-19 pandemic: Unknown unknowns and predictive monitoring* | predictive monitoring / uncertainty-aware forecasting paradigm | 疫情预测案例 | 持续监测而非单点预测 | 支持情景适应 | 强调极端不确定性下 accuracy-only forecasting 的局限，为 ECDS-TF 的“预测+持续更新/情景敏感度”提供理论依据 | 低（理论支持） |
| L50 | 2026 | Chen, Wang & Guo, *AgentProphet: Source-Aware Multi-Agent Emerging Technology Forecasting for Upstream Decision-Making in AI-Based IoT Systems* | 多源证据 + role-specialized LLM agents + source-aware confidence calibration + critic refinement | 论文、专利、政策、报告；history-only feature records | rolling forecasting；NDCG/E-Gain/E-MAP；与 GRU/DirectLLM/DLinear/ARIMA 比较 | 非动态情景模拟 | 与原 MAF-TF 高度接近，证明“多源+多智能体+history-only+confidence calibration”的 emerging-tech forecasting 已存在；LLM 支线必须降为 stress-test 辅助 | **极高** |
| L51 | 2026 | Haugk & Leyh, *Agentic Foresight: Potenziale autonomer KI-Agenten für die strategische Vorausschau in Unternehmen* | Scout–Validator–Synthesis 多智能体架构 | 非结构化数据持续扫描 | 概念/架构验证 | 持续 foresight | 证明 autonomous agents + continuous strategic foresight 已成为明确研究线；不能把 agentic foresight 本身作为贡献 | 高 |
| L52 | 2026 | *The Use of Generative AI in Foresight: A Model Comparison for Scenario Development* | GenAI-assisted scenario development | 课堂 foresight 实验，多模型比较 | 18 名学生/6 团队比较 | 直接用于 scenario development | 生成式 AI 辅助 foresight scenario 已有直接应用；Agent 价值应定位于补充解释/压力测试而非“首次AI推演” | 中高 |
| L53 | 2026 | *Causal inference-integrated temporal graph convolutional networks for dynamic prediction and optimization of enterprise total factor productivity* | causal inference + temporal GCN + heterogeneous treatment effect + counterfactual scenario simulation | 企业面板数据 | out-of-sample prediction + intervention verification | 有 | 非技术预见，但高度接近“动态图学习→主动干预→情景轨迹”；算法组合层面不存在通用空白 | **高（跨领域方法）** |
| L54 | 2025 | *Generating Counterfactual Temporal Motifs: Unraveling the Mysteries of Temporal Graph Neural Networks* | TGNN + counterfactual what-if perturbation | 时间图事件 | interventional probability estimation | 反事实解释 | 说明 temporal graph 的 what-if intervention 已有成熟方法邻域；ECDS-TF 需避免泛化宣称“首次对时序图做反事实干预” | 高（跨领域方法） |
| L55 | 2010 | Vecchiato & Roveda, *Strategic foresight in corporate organizations: handling the effect and response uncertainty of technology and social drivers of change* | strategic foresight uncertainty framework | 企业 strategic foresight | 案例/概念验证 | 有 | 说明技术/社会驱动因素的不确定性与组织响应早已是 foresight 核心议题；支持将不确定性处理作为必要设计而非新颖组件 | 低 |

---

## 第四轮关键结论

### 1. Vulnerability demand-pull 必须重新表述

本轮已经检出直接实证：漏洞信息披露会显著提高软件厂商补丁研发概率，并且漏洞关注度、严重度、提前披露等因素会加快补丁研发。因此，后续不能使用：

> “首次提出漏洞需求牵引安全技术创新。”

更可辩护的命题应收紧为：

> **首次/较少见地（最终是否可用“首次”仍待完整检索确认）将 CVE/CWE/KEV 构造成 exploitation-weighted vulnerability-demand state，并把它作为多源技术状态转移与 2030 技术预见中的可检验外生/内生压力通道。**

即创新候选不在“存在需求牵引”，而在“如何把该机制正式进入可回测技术预见模型”。

### 2. 概率预测与 uncertainty 也不是空白

1990s 已有 semi-Markov、maximum-entropy precursor-event probabilistic technology forecasts；technology roadmapping 也长期研究 uncertainty 和 robustness。因此：

- `probabilistic forecasting` 本身不能作为创新；
- `Monte Carlo` 本身不能作为创新；
- `uncertainty-aware foresight` 本身不能作为创新。

ECDS-TF 更合理的贡献是：

> 在同一历史可验证框架中联合评价 point/rank accuracy、probability calibration、interval coverage 与 scenario sensitivity。

### 3. AgentProphet 对 MAF-TF 构成直接高相似风险

AgentProphet 已具备：

- papers + patents + policy + reports；
- source-aware evidence；
- role-specialized multi-agent reasoning；
- confidence-calibrated critic refinement；
- history-only feature records；
- rolling forecasting；
- emerging technology ranking。

因此建议从本轮开始把原 **MAF-TF（Multi-Agent Foresight for Technology Forecasting）** 重命名/降级为：

## MAST — Multi-Agent Scenario Stress Test

其职责限定为：

- 读取 ECDS-TF 已产生的未来概率路径；
- 注入法规、组织采用、责任风险、人才、商业化、极端事件等难参数化因素；
- 生成反例、失败模式和情景解释；
- 不参与核心历史性能排行榜；
- 不声称独立完成 emerging-technology forecasting。

### 4. 当前最有希望的方法核心继续收敛

截至本轮，最值得保留的整体命题为：

> **构建角色化 STOV 技术状态，在严格 temporal freeze 下从多源历史证据学习技术状态动力学，将 learned dynamics 转换为可施加安全需求/AI能力/开源扩散等 shock 的概率 forward simulation，并通过多窗口 historical reconstruction、概率校准和场景敏感性共同验证其技术预见有效性。**

其中任何单独组件均非首创，创新性只能由“问题特化 + 机制组合 + 验证范式”共同支撑。
