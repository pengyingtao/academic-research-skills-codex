# WP2 Gate 2B 扩容执行日志

**日期：** 2026-09-01  
**WP2：** IN_PROGRESS  
**Gate 2B：** IN_PROGRESS

## 1. O/V 扩容

在 140 GitHub + 140 VDP 正式历史子批次通过后，已启动扩容批次：

- GitHub main target：450；
- VDP target：500；
- compact manual review queue target：300。

GitHub 继续执行：

- `created_at <= 2026-06-30`；
- AI search anchor + cyber capability term；
- semantic hard AI gate；
- stars/forks 等当前累计量不用于历史回测特征。

VDP 采样器已修改为 W01–W07 quota-balanced historical sampling，并在多个 <=120-day NVD publication windows 中轮转补齐，以修复前一批 W01/W02 过度代表、W04/W05 欠代表的问题。

当前 O/V expansion workflow 已启动并通过预采集单元测试，正在执行 GitHub 扩展采集。

## 2. OpenAlex 凭据检测

已创建并实际运行：

`.github/workflows/wp2-openalex-pilot.yml`

检测结果：

`BLOCKED_CREDENTIAL`

原因：仓库 Secret `OPENALEX_API_KEY` 未配置。

已落库状态文件：

`My_work/03_data/pilot/output/openalex_pilot_status.json`

OpenAlex API collector 已 READY；有 key 时可直接运行约 1000 条 Science Pilot。

另有 `collect_openalex_snapshot.py` 支持本地 snapshot，但 OpenAlex 完整 public snapshot 体量约数百 GB compressed，且 works shard 不是按本研究主题预分区，因此不适合在 GitHub Actions 中为 1000 条 Pilot 扫描整个 snapshot。

## 3. Patent Bulk 路径实跑与状态纠正

### 3.1 临时假设

基于 PatentsView 历史代码示例，曾尝试直接访问 legacy S3 bulk：

- `https://s3.amazonaws.com/data.patentsview.org/download/g_patent_abstract.tsv.zip`
- `https://s3.amazonaws.com/data.patentsview.org/download/g_patent.tsv.zip`

并建立：

- `My_work/03_data/pilot/collect_patents_public_bulk.py`
- `My_work/03_data/pilot/patent_bulk_input_contract.md`
- `.github/workflows/wp2-patent-public-bulk.yml`

### 3.2 实际执行结果

Patent workflow 已真实运行，Actions run：`33523265236`。

失败发生在首个 bulk 下载步骤：

`g_patent_abstract.tsv.zip -> HTTP 403 Forbidden`

因此必须撤销“legacy public S3 当前可直接访问”的临时判断。

### 3.3 当前官方状态

2026 年 USPTO 已将 PatentsView 数据下载迁移到 USPTO Open Data Portal（ODP）的 Bulk Data Directory；从 2026-06-18 起，ODP 的访问、搜索和数据下载要求 USPTO.gov 账户登录。

因此 Patent 正式状态调整为：

`BLOCKED_AUTHENTICATED_ODP_ACCESS`

而不是 `PUBLIC_BULK_PIPELINE_READY`。

现有 `collect_patents_public_bulk.py` 保留作为 legacy/可替换下载端点的流式筛选实现，但在找到当前可认证 ODP 下载输入或用户提供官方 bulk 文件前，其输出不得计入 Gate 2B。

### 3.4 后续允许路径

1. 使用已登录 USPTO ODP 下载的官方 PatentsView bulk 文件，再运行 `collect_patents_bulk.py`；
2. 若后续获得可程序化认证的 ODP bulk/API 方式，再将认证接入 workflow；
3. 第三方 mirror 最多只能用于 WP2 临时 taxonomy sanity check，不得替代 WP3 正式官方 patent 数据，除非重新进行 provenance 风险评估并修改协议。

## 4. 当前 Gate 2B 状态

已完成/通过：

- Taxonomy V1.1；
- source-role separation；
- formal GitHub cutoff；
- formal NVD historical windows；
- point-in-time VDP materialization；
- 280 条正式 O/V 子批次；
- compact annotation queue 生成器；
- OpenAlex credential-aware workflow；
- Patent bulk parser/normalizer 和真实访问失败验证。

仍需：

- O/V 扩容结果完成并落库；
- Patent 官方 bulk 约500条（当前阻塞于 authenticated ODP access）；
- OpenAlex ~1000 条 Science Pilot（当前缺 API key）；
- >=300 gold labels；
- Precision >=0.90；
- primary-family macro-F1 >=0.80；
- 高频类 F1 >=0.85。

WP3 仍保持 TODO，不提前启动。
