# WP2 Annotation Guideline V1

> 目标：将论文、专利、GitHub、CVE/漏洞相关记录映射到统一 AI-for-Cybersecurity Technology Entity，验证 taxonomy_v1 是否足以支撑 STOV 技术状态构建。

## 1. 标注单位

每条记录的基本标注字段：

- `source_type`
- `source_id`
- `title/name`
- `text_evidence`
- `primary_technology_id`
- `secondary_technology_ids`
- `ai_method_tags`
- `cybersecurity_function_tags`
- `in_scope`
- `confidence`
- `reason`
- `needs_review`

## 2. 范围规则

### 纳入

当记录的主要目标是利用 AI/ML/LLM/Agent 提升网络安全防御能力时纳入，包括：

- 发现/分析/修复漏洞；
- 检测恶意代码、入侵、异常、钓鱼、Botnet；
- 提取/融合威胁情报；
- threat hunting / investigation；
- SOC / incident response / SOAR；
- digital forensics；
- attack surface / exposure / risk analytics；
- identity/access defense；
- deception/adaptive defense；
- secure software engineering。

### 排除

- 主要研究目标是 Security of AI，例如 prompt injection、model poisoning、model stealing 等，而非一般 cyber defense；
- AI 用于主动攻击、恶意 exploit 生成，且无防御/安全测试/修复目的；
- 仅讨论 AI 或 cybersecurity，但没有明确技术能力交集；
- 纯政策/伦理讨论且不产生防御技术能力；
- CVE 记录本身不能自动映射为某个 AI 防御技术。

## 3. Primary Label 原则

Primary label 按“最终防御目的”确定，而不是按模型名称确定。

示例：

- 用 GNN 检测网络异常 → T04，而不是单独建立 GNN 类；
- 用 LLM 自动修补 CVE → T02；
- 用 LLM 分析 CVE 并排序，但不生成修补 → T01 或 T12，按主要贡献判断；
- SOC agent 自动调查并执行 containment → primary T09 或 T10，若重点是 autonomous SOC workflow 则 T09，重点是 response execution 则 T10。

## 4. 多标签规则

允许 secondary labels，但仅当存在实质双重能力。

例如：

- LLM agent 先 threat hunt 再 incident response：Primary=T08，Secondary=T10；
- vulnerability detection + patch generation：若文章核心是 end-to-end repair，Primary=T02，Secondary=T01；
- threat intelligence KG + threat actor attribution：Primary=T07，无需额外技术族。

禁止为了提高覆盖率而过度多标签。

## 5. 四类数据源的证据优先级

### OpenAlex / Paper

优先：

1. Abstract
2. Title
3. Keywords/Topics
4. Full text（若合法可得）

不要仅依靠 OpenAlex topic 自动标签。

### Patent

优先：

1. Abstract
2. Independent claims
3. CPC/IPC context
4. Title

专利中的营销性/宽泛标题不得覆盖 claims 中的真实技术目的。

### GitHub

优先：

1. README
2. Topics
3. Repository description
4. Dependencies / package metadata
5. Releases / examples

Repository 名称不能单独作为标签依据。

### CVE / CWE / KEV

其主要作用不是直接生成 Technology label，而是构建 VDP。

只有当 CVE 与某项防御技术通过以下关系相连时，才建立关联：

- defense tool explicitly detects/repairs/prioritizes it；
- paper/patent/repository explicitly references relevant CVE/CWE；
- technology family can be justified through affected software/security problem mapping。

## 6. Confidence 规则

- `HIGH`：摘要/README/claims 明确说明 AI 方法与 cyber defense 目标；
- `MEDIUM`：目标明确但具体技术族存在邻近类别歧义；
- `LOW`：仅关键词或短描述支持，需要人工复核；
- `REJECT`：不在研究范围。

所有 LOW 必须进入人工复核样本。

## 7. 易混淆边界

### T01 vs T12

- T01：发现/定位/分析具体 vulnerability；
- T12：从资产/漏洞集合角度进行 risk/exposure prioritization。

### T01 vs T02

- T01：find/understand vulnerability；
- T02：fix/remediate vulnerability。

### T08 vs T09

- T08：threat hunting/investigation 是核心任务；
- T09：SOC copilot/agent 是跨任务运营主体。

### T09 vs T10

- T09：分析、triage、调查和 SOC workflow；
- T10：response execution / orchestration / containment / recovery。

### T03 vs T15

- T03：识别/分析恶意代码；
- T15：在软件开发/供应链阶段提高代码安全。

### AI-for-Cybersecurity vs Security-of-AI

例如：

- 用 AI 检测传统恶意软件 → 纳入；
- 检测 prompt injection → 默认排除（Security of AI）；
- 研究 LLM 作为 SOC agent 检测企业网络攻击 → 纳入。

## 8. Pilot 标注流程

### Phase A — Seed retrieval

从四源各抽取候选：

- OpenAlex 1000
- Patent 500
- GitHub 500
- CVE-linked / vulnerability-related 500

目标总量约 2500。

### Phase B — 自动初标

使用：

- seed keyword rules
- embedding similarity
- taxonomy descriptions

生成 candidate labels 和 confidence。

### Phase C — 人工验证

至少人工复核 300 条：

- 150 条随机样本；
- 100 条低置信度/边界样本；
- 50 条多标签样本。

### Phase D — 误差分析

记录：

- false inclusion
- false exclusion
- family confusion
- source-specific error
- taxonomy missing category

## 9. Pilot 验收指标

建议最低目标：

- In-scope screening Precision ≥ 0.90
- Primary family macro-F1 ≥ 0.80
- 高频技术族 F1 ≥ 0.85
- 低频技术族允许较低，但必须报告样本量
- 若双人标注，Cohen's Kappa ≥ 0.75 为目标

这些阈值是工程门槛，不是论文最终结果预设；Pilot 可根据样本分布调整，并在执行日志记录。

## 10. Taxonomy 修改纪律

Taxonomy v1 可以在 Pilot 后修改，但必须：

1. 记录版本号；
2. 说明新增/合并/拆分类别原因；
3. 保留旧 ID 映射；
4. 在历史 backtest 阶段冻结 taxonomy，禁止利用未来结果反向调整历史分类；
5. 不因为某类别预测表现差而删除该类别。

## 11. WP2 下一步

1. 设计四源 Pilot retrieval query；
2. 抽取小规模样本先做 50–100 条 sanity check；
3. 根据误差修改 seed keywords；
4. 再扩展到约 2500 条 Pilot Corpus；
5. 输出 `taxonomy_validation_report_v1.md`；
6. 通过 Gate 1 后才进入 WP3 全量采集。
