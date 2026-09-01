# WP1 文献类别配额核验

> 核验日期：2026-09-01
> 当前文献池：55 条（主矩阵 L01–L39 + 第四轮扩展 L40–L55）

## 一、验收配额

WP1 预设最低门槛：

- 核心/高相关文献：50–80 条；
- computational/simulation foresight：≥20；
- SD/ABM foresight：≥10；
- graph/temporal graph/TOD：≥10。

## 二、当前分类计数

### A. Simulation / SD / ABM / Scenario Mechanism

明确计入：L01–L09、L30、L31、L46、L48。

**保守计数：13 条。**

结论：`13 ≥ 10`，通过。

### B. Graph / Temporal Graph / Technology Opportunity / Learned Dynamics

明确计入：L10–L14、L19–L20、L22、L32–L33、L53–L54。

**保守计数：12 条。**

结论：`12 ≥ 10`，通过。

### C. Computational / Data-driven / Simulation Foresight

明确计入：L01–L16、L19–L22、L26–L33、L45–L50、L53–L54 等。

按最严格口径剔除纯理论综述、数据源文档和仅作背景支持的条目后，仍超过 20 条。

**保守计数：≥30 条。**

结论：通过。

### D. LLM / Agentic Foresight / Temporal Leakage

L18、L34–L38、L50–L52。

**计数：9 条。**

该类别不是 WP1 强制配额，但已足够支持 MAF-TF → MAST 的方法调整。

### E. Cybersecurity Vulnerability / Demand / Innovation Mechanism

L40–L44 以及若干前轮安全领域材料。

**核心机制文献：≥5 条。**

该类别数量尚少，但已经出现关键直接反例：漏洞披露能够影响 patch R&D，因此“漏洞需求牵引”不能作为首创理论；后续 WP2/WP3 仍应继续补充领域实证文献。

## 三、配额结论

| 验收项 | 门槛 | 当前 | 结果 |
|---|---:|---:|---|
| 核心/高相关文献 | ≥50 | 55 | PASS |
| Simulation/SD/ABM | ≥10 | 13 | PASS |
| Graph/TOD | ≥10 | 12 | PASS |
| Computational/Simulation Foresight | ≥20 | ≥30 | PASS |

WP1 的**数量和类别最低门槛已经满足**。

## 四、终检补充结论

针对以下精确组合进行了最后定向检索：

- `technology foresight + Brier score`；
- `technology forecasting + expected calibration error`；
- `technology foresight + conformal prediction`；
- `emerging technology forecasting + probability calibration`；
- `technology foresight + learned simulator`；
- `technology forecasting + learned dynamics + scenario intervention`；
- `technology foresight + graph + counterfactual simulation`。

当前检索结果显示：

1. 技术预见已有 probabilistic forecasts、semi-Markov、maximum entropy precursor methods、scenario robustness；
2. 但未检出直接使用 Brier/ECE/conformal coverage 作为核心技术预见校准协议的高度同构论文；
3. learned graph dynamics + counterfactual/intervention 在其他领域已有成熟先例；
4. 技术预见内部已有 SD/ABM 可干预推演，但未检出把多源 learned state dynamics、严格 historical backtest 和概率校准统一起来的直接同构工作；
5. “未检出”只能支持研究 gap，不等于证明世界范围内不存在相关研究。

## 五、WP1 验收建议

数量与分类：**PASS**。

新颖性结论：**MODIFY**。

原因：原方案中的多个独立创新主张已被文献占用，但收紧后的整体框架仍存在可研究空间。
