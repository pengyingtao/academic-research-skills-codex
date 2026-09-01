# WP2 Annotation Guideline V1.1

> 本文件继承 `annotation_guideline_v1.md`，只记录 V1.1 新增或替换规则。未修改部分继续按 V1 执行。

## 1. Source-role 分离

### S/T/O — Technology Supply

- Science / Patent / Open Source 可映射 T01–T15；
- primary label 按最终 defensive objective；
- secondary label 仅在存在真实双重能力时使用。

### V — Vulnerability Demand

- CVE/CWE/KEV/EPSS 不直接获得 T01–T15 ground-truth label；
- 通过 `vdp_mapping_v1.yaml` 生成需求压力状态；
- 与技术族的关系是待估计/待验证的 hypothesis edge，不是人工正标签。

这条规则替换 V1 中任何可能把 CVE 作为普通技术记录进入分类器的理解。

## 2. 两阶段标注

### Stage A — Retrieval Label

只记录：

- 为什么被召回；
- 命中了哪些正向/上下文词；
- 是否进入人工/模型分类阶段。

Retrieval 命中不等于 in-scope。

### Stage B — Semantic Label

读取高优先级证据后判断：

- in_scope
- primary family
- secondary family
- false-positive type
- confidence

## 3. 新增 required_context 规则

### T01

`vulnerability` 单词本身不足。

高置信 T01 应能回答“具体软件/程序/二进制弱点是什么或如何被发现/定位/分析”。

### T02

`automated program repair` 本身不足。

必须存在 security vulnerability / CVE / CWE / security patch / vulnerability repair 等安全上下文。

### T04

`anomaly detection` 本身不足。

必须出现 network / traffic / intrusion / host / UEBA / security 等网络安全语境。

### T09

`agent` 本身不足。

必须出现 SOC / SIEM / blue-team / alert / security operations / analyst 等防御运营语境。

### T11

`forensics` 本身不足。

必须是 digital/computer/memory/disk/mobile/cyber forensic context。

## 4. Offensive / Dual-use 决策

新增 `use_orientation`：

- `DEFENSIVE`
- `DUAL_USE_DEFENSE_PRIMARY`
- `DUAL_USE_OFFENSE_PRIMARY`
- `OFFENSIVE`
- `UNCLEAR`

纳入规则：

- DEFENSIVE → 纳入；
- DUAL_USE_DEFENSE_PRIMARY → 纳入并标记 dual-use；
- DUAL_USE_OFFENSE_PRIMARY / OFFENSIVE → 从 AI-for-Cybersecurity supply corpus 排除；
- UNCLEAR → LOW confidence + 人工复核。

示例：自主 pentesting agent 同时声称 vulnerability detection 和 exploitation orchestration，若产品主要用于攻击性渗透流程，则排除，不因 `vulnerability detection` 命中 T01。

## 5. GitHub artifact_type

每个纳入/候选 repo 必须标记：

- `tool_framework`
- `production_platform`
- `paper_code`
- `dataset_benchmark`
- `awesome_list_catalog`
- `tutorial_course`
- `ctf_demo`
- `offensive_tool`
- `mixed_dual_use`

后续 O-source 技术状态不得简单把这些类型等权计数。

推荐：

- production_platform / tool_framework → 核心工程扩散信号；
- paper_code → 科学→工程转化信号；
- dataset_benchmark → 基础设施/评测信号；
- awesome_list → 生态发现辅助；
- tutorial/CTF → 教育/社区信号；
- offensive_tool → 不进入 AI-for-Cybersecurity supply state。

## 6. Patent 新边界

专利分类必须记录 `target_object`：

- `software_weakness`
- `network_attack_behavior`
- `asset_exposure`
- `identity_access`
- `malware`
- `incident_response`
- `other`

例如标题含 `network security vulnerability detection`，但摘要/claims 实际分析 abnormal traffic，则 `target_object=network_attack_behavior`，优先 T04，而不是 T01。

## 7. VDP 标注规则

V 源记录字段：

- cve_id
- snapshot_time
- cwe_group
- cvss_features_as_observed
- kev_status_as_observed
- epss_as_observed（若使用）
- affected_vendor/product
- pressure_group

不得填写 primary_technology_id 作为正标签。

可以填写：

`hypothesized_pressure_targets=[Txx...]`

但必须明确：该字段仅供后续建图/假设检验使用，不能作为 supervised target。

## 8. Point-in-time 注释

对可能随时间变化的字段增加：

- `observed_at`
- `valid_from`
- `source_modified_at`

特别是：

- citation count
- GitHub stars/forks/releases
- CVE modified data
- KEV inclusion
- EPSS

后续 F1/F2/F3 回测必须按 cutoff 重建状态。

## 9. 新增误差码

- OFFENSIVE_ONLY
- DUAL_USE_OFFENSE_PRIMARY
- SECURITY_OF_AI
- GENERIC_SOFTWARE_ENGINEERING
- GENERIC_ANOMALY
- GENERIC_FRAUD
- GENERIC_FORENSICS
- TITLE_KEYWORD_MISLEADING
- AGGREGATOR_NOT_TOOL
- FAMILY_CONFUSION
- TEMPORAL_METADATA_RISK

## 10. Gate 2A

V1.1 文件全部建立后，Gate 2A 状态改为 PASS。

下一阶段不是 WP3 全量数据，而是 WP2 Pilot Corpus：

- Papers ≈ 1000
- Patents ≈ 500
- GitHub ≈ 500
- Vulnerability-demand records ≈ 500

人工复核仍按至少 300 条规划，并对高歧义类别超额抽样。