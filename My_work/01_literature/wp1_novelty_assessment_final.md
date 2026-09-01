# WP1 最终方法新颖性评估

> 论文题目：《面向技术预见的证据校准动态推演方法研究——以AI赋能网络安全技术为例》
>
> WP1 Verdict：**MODIFY**
>
> 含义：题目和研究问题具有继续推进价值，但原始方法贡献声明必须收紧；修改 WP0 后可进入 WP2。

## 一、最终结论

经过 simulation/SD/ABM、data-driven foresight、multi-source weak signals、science–technology lead-lag、GitHub/open-source、dynamic/heterogeneous graph、historical validation、probabilistic forecasting、LLM agent forecasting、temporal leakage、vulnerability-demand mechanism 和 counterfactual learned dynamics 等方向的多轮定向检索，当前没有发现与“收紧后的 ECDS-TF 整体框架”完全同构的方法论文。

但大量原计划中的单独组件已有直接先例，因此研究不能用“首次引入 X”式叙述建立贡献。

## 二、明确放弃的创新主张

以下内容不得作为论文首创主张：

1. 首次使用 System Dynamics / simulation 做技术预见；
2. 首次使用 ABM 做技术预测；
3. 首次以真实数据校准 ABM；
4. 首次融合论文、专利和 GitHub；
5. 首次把 GitHub 作为技术领先信号；
6. 首次建模 Science–Technology lead-lag；
7. 首次用 dynamic/heterogeneous GNN 做技术机会预测；
8. 首次做 probabilistic technology forecasting；
9. 首次做 historical backtesting / rolling forecasting；
10. 首次用 LLM multi-agent 做 emerging technology forecasting；
11. 首次发现 vulnerability disclosure / cyber risk 会牵引 security R&D；
12. 首次用 temporal graph 做 counterfactual/intervention。

## 三、建议保留的核心贡献

### Contribution 1 — Role-aware STOV Technology State

将四类证据赋予不同技术演化角色，而不是简单多源拼接：

- `S — Science`：知识生产与研究能力；
- `T — Technology/Patent`：技术化、产权化和组织投入；
- `O — Open Source`：工程实现、开发者扩散和工具可用性；
- `V — Vulnerability Demand Pressure`：现实安全问题、利用压力和修复需求。

状态定义：

\[
X_{k,t}=[S_{k,t},T_{k,t},O_{k,t},VDP_{k,t}]
\]

当前未检出高度同构的 AI-for-Cybersecurity 技术预见状态模型。

### Contribution 2 — Exploitation-weighted Vulnerability Demand Pressure (VDP)

不再把 CVE count 当作普通数量指标，而构造安全需求压力：

\[
VDP_{k,t}=f(CVE,KEV,Severity,Exploitability,Exposure,RemediationGap)
\]

研究贡献不是“提出需求牵引理论”，而是：

> 将已有漏洞披露/安全风险→研发响应机制形式化为可被历史检验的技术预见状态变量，并测试其增量预测和情景干预价值。

### Contribution 3 — Evidence-Calibrated Intervenable Technology Dynamics

从历史 STOV 状态和技术关系学习动态：

\[
X_{t+1}=F_\theta(X_t,G_t,Z_t)+\epsilon_t
\]

然后把 learned dynamics 转换为 forward simulator，允许施加：

- AI capability shock；
- vulnerability/threat shock；
- OSS diffusion shock；
- regulation/constraint shock。

创新主张必须限定为“技术预见问题中的特化整合”，而不能宣称 learned graph simulator 本身首次出现。

### Contribution 4 — Unified Historical Reconstruction Protocol

用同一 temporal-freeze 框架验证三类任务：

1. Technology Growth；
2. Emerging Technology；
3. Technology Convergence。

至少采用：

- F1：2012–2018 → 2019–2021；
- F2：2012–2020 → 2021–2023；
- F3：2012–2022 → 2023–2025；
- rolling-origin supplementary evaluation。

关键贡献是统一验证范式，而不是“第一次回测”。

### Contribution 5 — Reliability-oriented Evaluation

在同一方法中联合评价：

- point forecast accuracy；
- ranking quality；
- probability calibration；
- interval coverage；
- scenario sensitivity / stability。

当前终检没有发现技术预见领域高度同构的统一评价协议，但最终论文应使用“据检索所见/较少研究同时……”等谨慎措辞，而避免绝对首创。

### Contribution 6 — Computational Simulation + Multi-Agent Stress Test

LLM agent 不再承担主要预测角色。

正式名称调整为：

## MAST — Multi-Agent Scenario Stress Test

角色：

- ECDS-TF：产生可回测概率基准路径；
- MAST：寻找制度、监管、组织采用、责任风险、人才、商业化和极端事件等未参数化失效模式。

这形成“quantitative baseline path + agentic adversarial scenario critique”的双轨方法。

## 四、算法结构建议

### Layer 1 — Evidence State Construction

形成 Technology × Quarter：

\[
X_{k,t}=[S,T,O,VDP]
\]

### Layer 2 — Relational Encoder

Temporal/Heterogeneous Graph 只作为关系学习模块，负责：

- technology interactions；
- convergence；
- neighborhood effects；
- cross-source lag representation。

图模型不再是论文创新主角。

### Layer 3 — State Transition

学习：

\[
P(X_{t+1}|X_t,G_t,Z_t)
\]

### Layer 4 — Probabilistic Rollout

利用 Monte Carlo / probabilistic transition 生成：

\[
X_{t+1},X_{t+2},...,X_{2030}
\]

### Layer 5 — Intervention

在 rollout 中改变 shock variables，比较 counterfactual trajectories。

### Layer 6 — Historical Reconstruction

所有模块必须首先通过历史时间隔离验证，再允许进行 2030 forecast。

## 五、Baseline 修订

正式 baseline 保留：

- Persistence / Linear Trend；
- ARIMA / Prophet / Bass；
- XGBoost / LSTM；
- GCN / R-GCN；
- TGAT / TGN；
- ABM-R；
- ABM-C。

新增一个重要参考：

### AgentProphet-style benchmark

由于 AgentProphet 与原 MAF-TF 高度接近，后续 Task B（Emerging Technology）应考虑增加：

- `AgentProphet-Style (anonymized/history-only)` 作为补充对照；
- 若无法严格复现其模型/提示配置，应作为外部方法参考而非直接性能比较；
- 任何 LLM 历史回测必须做 contamination/leakage disclosure。

## 六、对题目的判断

当前题目可以保留：

> 《面向技术预见的证据校准动态推演方法研究——以AI赋能网络安全技术为例》

理由：

- “证据校准动态推演”仍能概括最终方法核心；
- 题目没有宣称动态图、ABM、Lead-Lag 或 Agent 是首创；
- AI for Cybersecurity 提供了 VDP 这一具有领域机制意义的需求通道。

## 七、WP1 最终判定

### Verdict：MODIFY

不是 `STOP`：当前未发现与收紧后整体框架完全同构的技术预见方法。

不是原样 `GO`：原 WP0 中 Lead-Lag、MAF-TF、Vulnerability Demand 等贡献定位需更新。

### 下一步

1. 回写 WP0 `research_protocol.md`；
2. 回写 WP0 `research_questions.md`；
3. 回写 WP0 `experiment_matrix.md`；
4. 将 MAF-TF 全部替换/解释为 MAST；
5. 增加 VDP 定义和对应消融；
6. 增加 AgentProphet-style supplementary baseline 设计；
7. 完成 WP0 V2 后，WP1 状态改为 DONE，进入 WP2。
