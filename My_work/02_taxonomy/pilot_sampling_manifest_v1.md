# WP2 Pilot Sampling Manifest V1

## 1. 目标规模

总目标约 2500 条，用于 taxonomy 与 source-role 验证，不作为最终论文全量数据。

| Source | Target | 角色 |
|---|---:|---|
| OpenAlex / papers | 1000 | Science / knowledge production |
| Patents | 500 | Technology / formalization |
| GitHub | 500 | Open-source / engineering diffusion |
| CVE/CWE/KEV/EPSS | 500 | Vulnerability demand pressure |

## 2. 采样策略

### Science — 1000

采用分层召回：

- 15 个一级技术族均保证最小候选量；
- 对高频类 T03/T04/T05 做上限控制，避免挤压新兴类；
- 对 T01/T02/T07/T08/T09/T10/T14/T15 进行适度超额召回；
- 2012–2016、2017–2020、2021–2023、2024–2026Q2 分层保留，防止 corpus 只代表生成式 AI 时代。

建议初始配额：

- 每个 Txx 至少 30 个候选；
- 剩余数量按候选规模和时间覆盖分配；
- 多标签记录只计一次 source record。

### Patent — 500

- 重点覆盖 T01/T02/T04/T07/T09/T10/T12/T15；
- 保留 CPC/claims 足够完整的记录；
- 对标题含 `vulnerability` 的记录专门抽取边界样本，用于 T01/T04/T12 confusion analysis；
- 跨专利族去重策略在 WP3 冻结，本 Pilot 先保留 family identifier。

### GitHub — 500

目标不是“搜索结果前 500 个”，而是分层抽取：

- production_platform / tool_framework：核心；
- paper_code：单独层；
- dataset_benchmark：单独层；
- awesome_list/tutorial/CTF：小比例保留作误差与生态分析；
- offensive_tool：保留一小组负样本，不进入 supply 正样本。

建议至少 20% 为 hard negatives / boundary cases，包括 autonomous pentesting、red-team agents、generic coding agents、awesome lists。

### Vulnerability Demand — 500

不是“AI CVE”。按 VDP weakness / exploitation strata 抽样：

- W01 memory safety
- W02 injection/traversal/unsafe interpretation
- W03 authentication/authorization
- W04 crypto/credentials
- W05 configuration/dependency/supply chain
- W06 availability/resource exhaustion
- W07 concurrency/state/logic
- W99 other

同时分层：

- KEV vs non-KEV
- 高/中/低 CVSS exploitability
- 若可获取历史 EPSS：高/中/低 EPSS
- affected product/vendor diversity

## 3. 人工复核样本

最低 300 条：

- 随机 supply records：120
- LOW/MEDIUM confidence：80
- family boundary：50
- offensive/dual-use GitHub：25
- VDP mapping：25

如果某技术族样本少于 20 条，则该族所有样本均进入人工复核候选池。

## 4. Pilot 指标

### Supply screening

- in-scope Precision
- in-scope Recall（通过 hard-negative/expanded candidate pool 近似评估）
- Primary-family macro-F1
- per-family F1
- family confusion matrix

### GitHub

- artifact_type accuracy
- offensive/defensive orientation accuracy

### Vulnerability demand

VDP 不评价 Txx 分类 F1，评价：

- CWE group coverage
- mapping consistency
- missingness of CVSS/KEV/EPSS point-in-time fields
- affected-product mapping completeness

## 5. Gate 2B

WP2 进入完成状态需要：

1. Pilot corpus 实际形成；
2. 人工复核完成至少 300 条或达到等价证据量；
3. In-scope screening Precision 目标 ≥0.90；
4. Primary family macro-F1 目标 ≥0.80；
5. 高频类 F1 目标 ≥0.85；
6. VDP point-in-time 字段可实现且无结构性不可得问题；
7. taxonomy 版本冻结为用于 WP3 的正式版本。

任何阈值未达到时，继续 WP2 迭代，不进入 WP3。