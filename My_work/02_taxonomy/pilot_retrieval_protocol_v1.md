# WP2 Pilot Retrieval Protocol V1

## 1. 目的

本协议用于 WP2 的小规模 Pilot 检索与 taxonomy sanity check。目标不是立即构建全量 STOV 数据，而是验证：

1. 15 个 AI-for-Cybersecurity 技术族能否在论文、专利、GitHub 三类技术供给源中稳定召回；
2. 高歧义关键词是否导致系统性误报；
3. CVE/CWE/KEV 是否应与 S/T/O 源使用不同映射机制；
4. 在进入约 2500 条 Pilot Corpus 前冻结 source-specific retrieval 与 screening 逻辑。

## 2. 两阶段检索原则

### Stage A — Candidate Retrieval

目标是高召回，不直接决定最终技术族。

候选条件：

- S/T/O：至少一个 AI 方法信号 + 至少一个 cybersecurity capability 信号；
- 或记录来自明确的 cyber-defense 专门语料库，此时可放宽 AI 词要求，由后续内容判定是否实际使用 AI；
- V：不使用 AI 词筛选。CVE/CWE/KEV 全部作为潜在需求压力证据，再按 weakness / exploitation / product surface 聚合。

### Stage B — Technology Classification

目标是高精度。

- 依据 abstract / claims / README 的主要防御目标分到 T01–T15；
- 允许 secondary label；
- offensive-only、Security-of-AI、纯通用 AI、纯通用软件工程记录在此阶段剔除；
- V 源不直接分 T01–T15，而通过 VDP 映射到需求压力通道。

## 3. 时间边界

Sanity check 可观察最新记录用于发现术语变化，但正式历史 Pilot 和后续回测必须保留 point-in-time 字段。

正式研究窗口：

- 2012Q1–2026Q2
- 2026Q3 以后记录不得进入历史训练集

## 4. OpenAlex / Papers

### 4.1 推荐获取方式

全量阶段优先 OpenAlex snapshot；API 仅用于小样本验证、补充元数据与检索式调试。

### 4.2 候选检索结构

概念式：

`(AI_TERMS) AND (FAMILY_SECURITY_TERMS)`

不建议只依赖 OpenAlex topic 标签。

### 4.3 高风险词的上下文约束

- `anomaly detection`：必须同时出现 network / intrusion / traffic / security / UEBA 等 cyber context；
- `automated program repair`：必须出现 vulnerability / security / CVE / CWE / secure code 等安全上下文，否则属于通用软件工程；
- `agent` / `multi-agent`：必须存在 SOC / SIEM / SOAR / incident / threat hunting / cyber defense 等运营上下文；
- `fraud detection`：必须明确 digital account / transaction / identity / cyber-enabled fraud，避免一般金融风控全部进入；
- `forensics`：必须是 digital/computer/memory/disk/mobile/cyber forensics。

### 4.4 Sanity sample 配额

第一轮：约 60–100 条。

优先抽取：T01、T02、T04、T07、T09、T15 等容易重叠/新兴技术族。

## 5. Patent

### 5.1 获取方式

- Sanity check：Google Patents / 可检索专利页面用于验证检索词和边界；
- Pilot / 全量：优先 PatentsView bulk / USPTO 公开批量数据；API 仅作补充。

### 5.2 证据优先级

Independent claims > abstract > CPC/IPC > title。

### 5.3 典型歧义

`network security vulnerability detection` 可能实际是在做异常流量/网络检测，而非软件漏洞发现。不得因为标题含 `vulnerability` 自动归 T01。

必须回答：

> 被发现的对象究竟是 source/binary/software weakness，还是 network anomalous/attack behavior？

前者偏 T01；后者偏 T04/T12。

### 5.4 Sanity sample 配额

第一轮：约 40–60 条，覆盖 T01/T02/T04/T09/T10/T12/T15。

## 6. GitHub

### 6.1 Candidate retrieval

使用 repository search 召回，再读取：

1. README
2. description
3. topics
4. release / package metadata
5. activity metadata

不得仅根据 repo name 标签。

### 6.2 GitHub artifact_type

新增字段：

- `tool_framework`
- `production_platform`
- `paper_code`
- `dataset_benchmark`
- `awesome_list_catalog`
- `tutorial_course`
- `ctf_demo`
- `offensive_tool`
- `mixed_dual_use`

O 源技术扩散建模时，各 artifact_type 后续采用不同权重；不把 awesome list 与真实工具活跃度等价。

### 6.3 排除/降权规则

- fork / archived / mirror：默认排除或去重；
- offensive pentest/exploit orchestration 为主要目标：从 AI-for-Cybersecurity O 源剔除；
- bug bounty / exploit generation / red-team-only：默认剔除，除非明确以防御评估或 remediation 为主要目标；
- awesome list：保留为生态发现辅助，不计入核心 engineering activity；
- course/tutorial/CTF：单独标注，不与生产工具等权。

### 6.4 Sanity sample 配额

第一轮：约 60–100 个 repositories。

优先对比：

- vulnerability detection vs autonomous pentesting
- SOC agent vs generic agent framework
- security code repair vs generic coding agent
- CTI agent vs OSINT/offensive intelligence agent

## 7. CVE / CWE / KEV / EPSS

### 7.1 关键原则

V 源是 `demand pressure`，不是 `technology supply`。

因此：

- 不要求记录含 AI 词；
- 不直接给 CVE 分配 T01–T15；
- 先构建 weakness / affected surface / exploitation activity 的压力向量；
- 再通过可审计 mapping 把压力传播到可能受影响的技术族。

### 7.2 建议数据字段

- CVE ID
- publication / modification time（保留 point-in-time）
- CWE
- CVSS base + vector components
- CPE / vendor / product
- KEV status / date
- EPSS score / percentile（作为 V 层外部 exploit-likelihood 特征，需保留历史快照）
- references / patch/advisory tags when available

### 7.3 不允许的做法

- 使用当前 KEV/EPSS 状态回填过去 backtest 时间点；
- 用 CVE 描述中的 `AI` 字样判断防御技术族；
- 将 CWE 类别与技术族一一硬编码成 ground truth。

## 8. Sanity Check 评价字段

每条样本至少记录：

- `candidate_query`
- `source_type`
- `source_id`
- `retrieved_by_terms`
- `in_scope`
- `primary_family`
- `secondary_family`
- `artifact_type`（GitHub）
- `false_positive_type`
- `confidence`
- `screening_reason`

误报类型：

- `OFFENSIVE_ONLY`
- `SECURITY_OF_AI`
- `GENERIC_AI`
- `GENERIC_SOFTWARE_ENGINEERING`
- `GENERIC_ANOMALY`
- `GENERIC_FRAUD`
- `GENERIC_FORENSICS`
- `TITLE_KEYWORD_MISLEADING`
- `AGGREGATOR_NOT_TOOL`
- `FAMILY_CONFUSION`

## 9. Gate 2A：进入 2500 条 Pilot Corpus 的条件

满足以下条件后才扩大采集：

1. source-specific rules 已形成版本化文件；
2. S/T/O sanity 样本中主要误报类型已识别；
3. CVE 已切换为 VDP mapping，不再直接使用 T01–T15 分类；
4. 高频家族的关键词边界有 required_context / negative_context；
5. taxonomy V1.1 保留旧 Txx ID，不因检索表现任意更改类别；
6. 所有历史数据规划均能实现 point-in-time freeze。

## 10. 下一步

1. 形成 `sanity_check_report_v1.md`；
2. 创建 `vdp_mapping_v1.yaml`；
3. 根据误差创建 taxonomy / keywords / guideline V1.1；
4. 通过 Gate 2A 后扩展到约 2500 条 Pilot Corpus。