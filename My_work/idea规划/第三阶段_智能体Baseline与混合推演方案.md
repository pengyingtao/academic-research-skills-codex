# 第三阶段：智能体 Baseline 与混合推演方案

## 一、研究主题背景

论文暂定题目：

> 《面向技术预见的证据校准动态推演方法研究——以AI赋能网络安全技术为例》

在前两阶段基础上，本阶段重点完善“动态推演”部分的实验设计，引入智能体方法，并明确不同类型智能体在论文中的角色。

核心判断：

> 有必要加入智能体方法，但必须区分传统 Agent-Based Modeling（ABM）与 LLM/生成式多智能体。传统 ABM 应作为正式 baseline；LLM 多智能体更适合作为扩展 baseline 或情景压力测试工具，而不宜直接作为核心性能 baseline。

---

## 二、智能体方法的三类划分

### 1. 传统 Agent-Based Modeling（ABM）

适合作为正式 baseline。

ABM 的优势是可以显式刻画技术、组织、开源社区、需求和政策环境等主体之间的动态互动，符合“推演”这一研究目标。

建议设置以下 Agent：

- Technology Agent
- Research Agent
- Firm Agent
- Open-source Community Agent
- Cybersecurity Demand Agent

每个 Technology Agent 可以维护如下状态：

\[
State_i(t)=[Maturity,Growth,Knowledge,OSS,Demand]
\]

示例增长规则：

\[
P_i^{growth}=\sigma(\alpha S_i+\beta T_i+\gamma O_i+\delta V_i)
\]

其中：

- \(S_i\)：科学研究信号
- \(T_i\)：专利/技术化信号
- \(O_i\)：开源工程化信号
- \(V_i\)：漏洞需求/网络安全压力信号

示例规则：

```text
IF scientific_growth ↑
AND open_source_activity ↑
THEN technology maturity ↑

IF CVE demand ↑
AND research capability ↑
THEN defensive technology investment ↑

IF technology A and B repeatedly co-occur
THEN convergence probability ↑
```

最终通过 Monte Carlo Simulation 进行多次演化：

\[
N=1000
\]

并获得技术成长、融合和成熟的概率分布。

---

## 三、正式 ABM Baseline 设计

建议设置两个版本。

### 1. ABM-R：Rule-based ABM

特点：

- 采用文献规则、专家规则或经验规则；
- 不从 STOV 历史数据中自动学习全部参数；
- 代表传统推演范式。

用途：

> 检验传统“规则设定型”智能体推演的预测性能。

### 2. ABM-C：Calibrated ABM

特点：

- Agent结构与 ABM-R 类似；
- 参数由历史 STOV 数据校准；
- 从论文、专利、GitHub、CVE/CWE数据中估计增长率、扩散率、需求响应和技术融合参数。

用途：

> 检验“仅仅增加数据校准”是否已经足以显著提升技术推演效果。

这可以直接支持主论文的核心论证：

> ECDS-TF 的优势究竟来自 Evidence Calibration，还是来自更复杂的时序异构图关系学习与动态状态转移机制。

---

## 四、强化学习 Agent 的定位

强化学习 Agent 在网络安全中的典型用途包括：

- 自动渗透测试
- 攻击路径选择
- 自动防御策略
- Cyber Range 决策
- 自主攻击/防御训练

但 RL Agent 解决的问题主要是：

> 在既定环境中，选择什么行动以最大化 Reward？

而本论文的核心问题是：

> 技术生态系统未来如何演化？

二者的目标函数并不一致。

因此：

- RL Agent 可以进入文献综述；
- 不建议作为核心 baseline；
- 如后续需要，可在面向“自主攻防能力演进”特定子问题时作为补充实验。

---

## 五、LLM / 生成式多智能体方法

近年的新趋势是：

> LLM + Agent-Based Simulation

相较传统 ABM，LLM Agent 不再完全依赖手写规则，而可以根据上下文进行复杂行为判断。

建议构建一个扩展模型：

## MAF-TF

**Multi-Agent Foresight for Technology Forecasting**

中文可称：

> 多智能体技术预见模型

建议设置五类 Agent：

### 1. Scientist Agent

关注：

- 论文增长
- 科学突破
- 研究热点
- 学科融合

### 2. Industry Agent

关注：

- 商业价值
- 专利数量
- 企业进入
- 产品化潜力

### 3. Open-Source Agent

关注：

- GitHub项目增长
- Commit活跃度
- 开发者生态
- 工程实现速度

### 4. Cyber Defender Agent

关注：

- CVE增长
- CWE结构
- 威胁压力
- 防御需求

### 5. Technology Analyst Agent

负责：

- 汇总其他 Agent 判断
- 识别分歧
- 给出技术成长与成熟概率预测

例如，对某项技术输入截至时间 \(t\) 的观测证据：

```text
Technology: AI Automated Patching

Papers:
2018: 14
2019: 23
2020: 38
...

Patents:
...

GitHub:
...

CVE demand:
...
```

要求各 Agent 独立给出：

> 基于截至2020年的证据，预测2021—2023年该技术进入高增长阶段的概率。

多智能体结果可以聚合为：

\[
P_{MAF}=\sum_i w_iP_i
\]

---

## 六、LLM Agent 最大风险：Future Leakage

LLM 多智能体不适合作为普通历史回测 baseline 的核心原因是：

> 模型可能已经通过训练数据知道未来发生了什么。

例如：

使用2012—2018数据预测2019—2021，

但今天的大模型训练语料很可能已经包含2019—2021真实历史。

这样所谓“预测”可能变成“回忆未来”，破坏实验有效性。

因此必须进行严格控制。

---

## 七、LLM Agent 的三种使用方案

### 方案A：使用历史知识截止模型

要求：

\[
KnowledgeCutoff < PredictionStart
\]

例如预测2024年的研究方向，模型知识截止时间必须早于2024。

优点：

- 理论上最干净。

缺点：

- 很难为2019、2020等历史时间点找到合适的大模型；
- 模型版本和可复现性受限。

### 方案B：匿名化技术信息

不直接输入技术名称，例如：

> Technology A-17

只输入归一化特征：

```text
Science growth = 1.32
Patent growth = 1.11
OSS growth = 1.74
Demand growth = 1.26
Network centrality = ...
```

优点：

- 降低模型调用世界知识“偷看答案”的概率。

缺点：

- 无法完全消除未来知识泄漏；
- 削弱 LLM Agent 基于语义进行推理的优势。

### 方案C：只在2030未来情景中使用

这是本研究最推荐方案。

历史 Backtesting 阶段：

- 不将 LLM Agent 作为正式性能 baseline；
- 使用 Statistical、ML、GNN、Temporal Graph、ABM 等方法严格验证 ECDS-TF。

2027—2030 Prospective Foresight 阶段：

加入 LLM Multi-Agent Foresight，用于：

- 情景解释
- 风险发现
- 反事实讨论
- 制度和组织因素分析
- 技术路径压力测试

---

## 八、双轨推演框架

建议最终形成两个平行轨道。

## Track A：Computational Simulation

主方法：

### ECDS-TF

流程：

```text
STOV历史数据
↓
Temporal Heterogeneous Graph
↓
Evidence Calibration
↓
Dynamic State Transition
↓
Monte Carlo Simulation
↓
2030 Technology Foresight
```

作用：

> 给出可量化、可回测、可验证的技术演化概率。

---

## Track B：Agentic Simulation

扩展方法：

### MAF-TF

结构：

```text
Scientist Agent
Industry Agent
OSS Agent
Cyber Defender Agent
Technology Analyst Agent
↓
Multi-Agent Interaction
↓
2030 Agent Forecast
```

作用：

> 对制度、组织行为、技术采用障碍、潜在突发因素进行解释和压力测试。

---

## 九、Forecast Convergence Analysis

最终不应只比较“谁预测得更高”，而应研究不同预见机制是否形成共识。

可以计算：

\[
Agreement(ECDS,Agents)
\]

指标包括：

- Spearman \(\rho\)
- Kendall \(\tau\)
- Jaccard@K
- Rank Correlation

例如：

ECDS-TF：

> AI Automated Patching = 0.81

LLM Agents：

> AI Automated Patching = 0.43

此时重点研究：

> 为什么算法与智能体产生分歧？

可能原因包括：

- 算法观察到论文、GitHub、专利高速增长；
- Agent认为责任风险、错误补丁、企业采用成本和监管约束会抑制真实部署。

由此得到：

> Quantitative Forecast + Qualitative Reasoning

即：

- ECDS-TF 回答 **What is likely?**
- Agentic Simulation 回答 **Why might it fail?**

---

## 十、最终 Baseline 体系

建议论文实验设置为：

| 类别 | 方法 | 角色 |
|---|---|---|
| Naive | Persistence / Linear Trend | 最低基线 |
| Statistical | ARIMA / Prophet / Bass | 传统趋势预测 |
| ML | XGBoost / LSTM | 数据驱动预测 |
| Topic | BERTopic Trend | 主题演化 |
| Graph | GCN / R-GCN | 静态异构关系学习 |
| Temporal Graph | TGAT / TGN | 动态关系预测 |
| Agent Simulation | **ABM-R** | 传统规则型推演 |
| Calibrated Agent Simulation | **ABM-C** | 数据校准型推演 |
| Proposed | **ECDS-TF** | 主方法 |
| Exploratory | **MAF-TF** | LLM多智能体未来情景推演 |

正式 baseline 中应优先包含：

- ABM-R
- ABM-C

MAF-TF 建议作为扩展实验，而非主性能 baseline。

---

## 十一、推荐消融演进路径

建议把论文方法演进设计成：

\[
ABM-R
\]

传统规则 Agent

↓

\[
ABM-C
\]

+ Evidence Calibration

↓

\[
ECDS-NoGraph
\]

+ Dynamic State Learning

↓

\[
ECDS-TF
\]

+ Temporal Heterogeneous Graph

↓

\[
ECDS-TF + Agentic\ Scenario
\]

+ LLM Agent解释与压力测试

这个路径能够回答：

> 技术预见究竟应该依赖规则推演、数据预测，还是智能体推演？

---

## 十二、预期方法论结论

本研究不预设最终实验结果，但理论上可以检验如下命题：

> 数据驱动模型更适合估计技术演化基准概率；传统ABM更适合机制解释；LLM智能体更适合探索难以参数化的制度、组织与行为不确定性。

如果实验支持这一判断，则可以进一步提出：

> **高可信技术预见更适合采用“证据校准计算推演 + 智能体情景压力测试”的混合范式。**

这将使论文的创新点从单一预测算法升级为：

1. Evidence-Calibrated Simulation
2. Temporal Heterogeneous Graph Forecasting
3. Agent-Based Mechanism Simulation
4. LLM Multi-Agent Scenario Stress Testing
5. Forecast Convergence / Disagreement Analysis

---

## 十三、下一步实施建议

下一阶段建议依次开展：

1. 系统检索 ABM + Technology Foresight 文献；
2. 系统检索 LLM Agent + Foresight / Future Simulation 文献；
3. 建立 ABM-R 和 ABM-C 的可计算规则体系；
4. 明确 Agent 状态、行为、交互和转移函数；
5. 建立历史回测协议；
6. 设计 MAF-TF Prompt、角色、信息隔离和未来知识泄漏控制协议；
7. 将上述 baseline 正式纳入 ECDS-TF 的实验设计。

最终建议保持：

> **ECDS-TF 为论文主模型；ABM-R 与 ABM-C 为正式智能体 baseline；MAF-TF 为2030未来情景推演和解释性扩展。**
