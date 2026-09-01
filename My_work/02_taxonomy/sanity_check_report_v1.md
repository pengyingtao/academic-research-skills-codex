# WP2 Sanity Check Report V1

## 1. 结论摘要

本轮不是正式 2500 条 Pilot Corpus，而是对论文、专利、GitHub 和 V 源进行结构性 sanity check。主要目的：找出 taxonomy V1 与 seed keywords V1 的系统误差。

当前结论：**Gate 2A 可在完成 V1.1 文件后通过。**

最重要的四个发现：

1. `vulnerability` 不能直接等价于 T01；网络异常/攻击检测类专利也大量使用 vulnerability 字样。
2. `automated program repair` 不能直接等价于 T02；大量 APR 是通用软件工程，不涉及 security vulnerability。
3. `AI agent + vulnerability detection` 可能是 autonomous pentesting/offensive exploitation，必须按主要目标排除。
4. CVE/CWE/KEV 不是技术供给记录，应完全退出 T01–T15 直接分类流程，改为 VDP demand-pressure mapping。

---

## 2. Paper sanity examples

### S01 — DeepCode AI Fix

记录：`DeepCode AI Fix: Fixing Security Vulnerabilities with Large Language Models`（2024）

判断：

- in_scope: YES
- primary: T02 Automated Remediation and Program Repair
- secondary: T01 Vulnerability Discovery/Analysis（若模型输入包含检测结果并开展 vulnerability reasoning）
- 原因：明确以 security vulnerabilities 的修复为目标，而非一般 bug fixing。

### S02 — VRpilot

记录：`A Case Study of LLM for Automated Vulnerability Repair: Assessing Impact of Reasoning and Patch Validation Feedback`（2024）

判断：

- in_scope: YES
- primary: T02
- 关键子类：T02.01 patch generation + T02.02 patch validation

该样本支持 T02 内部保留“生成”和“验证”两个子能力。

### S03 — Adversarial Bug Reports against LLM APR

记录：`Adversarial Bug Reports as a Security Risk in Language Model-Based Automated Program Repair`（2025）

判断：

- in_scope: NO（主样本库）
- false_positive_type: SECURITY_OF_AI / GENERIC_APR_CONTEXT
- 原因：研究重点是攻击 LLM-based APR 系统本身，而非利用 AI 提升一般网络安全防御能力。

说明：若后续论文专门讨论 AI 自动修复系统的安全边界，可作为背景文献，但不应计入 AI-for-Cybersecurity 技术供给状态。

### S04 — Generic Automated Program Repair

记录：一般 APR / mutation / fault localization 方法。

判断：

- 若没有 vulnerability/security/CVE/CWE/secure coding 等上下文：REJECT
- false_positive_type: GENERIC_SOFTWARE_ENGINEERING

因此 `automated program repair` 必须增加 security-required context。

### S05 — LLM for Cyber Threat Intelligence

记录：`The Use of Large Language Models (LLM) for Cyber Threat Intelligence (CTI) in Cybercrime Forums`（2024）

判断：

- in_scope: YES
- primary: T07 Cyber Threat Intelligence
- 子能力：情报抽取、总结、实体/变量识别

支持 T07 对 LLM information extraction / summarization / fusion 的覆盖。

---

## 3. Patent sanity examples

### P01 — US20240330151A1

标题：`Generative Artificial Intelligence for Source Code Security Vulnerability Inspection and Remediation`

判断：

- in_scope: YES
- primary: T02
- secondary: T01
- 原因：source-code security vulnerability inspection 后进一步 remediation，最终防御目标偏修复。

### P02 — CN119583221B

标题：`Network security vulnerability detection method and system based on artificial intelligence`

摘要核心：网络多层图、suspected network security vulnerabilities、动态指标评估、响应策略。

判断：

- 不能按标题自动 T01；
- 候选 primary: T04（network/intrusion/anomalous activity detection）
- 可能 secondary: T10（若 claims 的重点确实包含响应策略执行）
- false_positive_type: TITLE_KEYWORD_MISLEADING / FAMILY_CONFUSION

### P03 — CN121283772A

标题同样包含 `network security vulnerability detection`，但摘要突出 abnormal traffic、network modules、检测关联图和 detection strategy。

判断：

- 候选 primary: T04，而不是软件漏洞发现 T01；
- 必须检查 claims 对“漏洞”对象的真实定义。

**专利规则修订：** `vulnerability` 必须和 source code / binary / software flaw / CWE / program weakness 等对象词共同出现，才具有较高 T01 置信度。

---

## 4. GitHub sanity examples

### G01 — xalgorix/xalgorix

公开描述：`Autonomous AI pentesting agents — real-time reconnaissance, vulnerability detection, and exploitation orchestration.`

topics 包括 autonomous-pentesting、bug-bounty、ethical-hacking、penetration-testing、vulnerability-detection。

判断：

- retrieval：会被 `AI + vulnerability detection` 高度命中；
- in_scope: NO（AI-for-Cybersecurity technology supply）
- false_positive_type: OFFENSIVE_ONLY
- 原因：主要目标是 pentesting / reconnaissance / exploitation orchestration。

该样本证明仅使用正向关键词会显著污染 T01/T09。

### G02 — FunnyWolf/agentic-soc-platform

公开描述：`Agentic SOC Platform ... automated security operations platform (AI SOC)`；topics 包括 agentic-soc、blueteam、cybersecurity、llm、siem、soar。

判断：

- in_scope: YES
- primary: T09 AI SOC and Security Copilots/Agents
- secondary: T10 Incident Response / SOAR（需 README 进一步确认实际 response execution 能力）
- artifact_type: production_platform / tool_framework

### G03 — awesome-ai-security-tools 类型仓库

判断：

- 可用于生态发现和 candidate expansion；
- 不与真实工具的 commits/releases/stars 直接等权计入工程技术状态；
- artifact_type: awesome_list_catalog
- false_positive_type（若直接计数）: AGGREGATOR_NOT_TOOL

---

## 5. V-source sanity check

### 5.1 旧方案问题

原 Pilot 设计将 `cve_related: 500` 与 paper/patent/GitHub 放在同一个“technology label validation”流程中，容易产生概念错误：

> CVE 描述的是技术系统的缺陷和被攻击面，不是 AI 防御技术本身。

### 5.2 新方案

CVE/CWE/KEV/EPSS 改为两级 VDP：

1. **Specific pressure**：按 weakness family / affected product surface 聚合；
2. **Systemic exploitation pressure**：按 KEV、EPSS、CVSS exploitability、活跃利用等信号聚合。

这些压力再与 T01–T15 建立 `pressure_to_family` 关联，但不作为 ground-truth technology label。

### 5.3 Point-in-time 要求

V 源时间泄漏风险尤其高：

- CVE 后续 modified 字段；
- KEV 后加入时间；
- EPSS 每日变化；
- exploit/patch reference 后续新增。

历史回测必须保存当时可知状态，而不是使用 2026 年当前最终状态回填历史。

EPSS 官方方法本身采用 point-in-time daily architecture，这与本研究的 temporal-freeze 原则一致，可作为 V 层工程设计参照。

---

## 6. 当前主要误报类型

| Error Type | 风险关键词 | 主要来源 | 修订策略 |
|---|---|---|---|
| OFFENSIVE_ONLY | pentest, exploit, bug bounty, red team | GitHub | primary-purpose 排除 + offensive negative context |
| SECURITY_OF_AI | adversarial prompt/model/APR attack | Papers/GitHub | 与 AI-for-CyberSecurity 主范围分离 |
| GENERIC_SOFTWARE_ENGINEERING | automated program repair | Papers/Patents | T02 要求 security context |
| GENERIC_ANOMALY | anomaly detection | Papers/Patents | 要求 network/intrusion/traffic/security context |
| TITLE_KEYWORD_MISLEADING | network vulnerability | Patents | claims/abstract 判定对象 |
| AGGREGATOR_NOT_TOOL | awesome list/catalog | GitHub | artifact_type 分层，不作为真实工具等权计数 |
| FAMILY_CONFUSION | T01/T04/T12, T09/T10 | 全源 | 以最终 defensive objective 为 primary label |

---

## 7. Taxonomy V1 的结构判断

本轮未发现必须新增第 16 个一级技术族的强证据。

15 个一级 ID 暂时保留不变，但需要：

1. source-specific context constraints；
2. GitHub artifact_type；
3. offensive/dual-use 边界；
4. VDP 独立映射；
5. 对 T01/T04/T12、T02/T15、T09/T10 的判定规则加强。

因此 taxonomy 从 V1.0 升级 V1.1，但不改 T01–T15 ID。

---

## 8. Gate 2A 判断

**结论：CONDITIONAL PASS**

完成以下文件后转为 PASS：

- `taxonomy_v1_1.yaml`
- `seed_keywords_v1_1.yaml`
- `annotation_guideline_v1_1.md`
- `vdp_mapping_v1.yaml`

通过后执行约 2500 条 Pilot Corpus，而不是直接进入全量 WP3。