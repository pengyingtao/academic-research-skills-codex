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

## 3. Patent 公共 Bulk 路径

进一步核验 PatentsView 官方代码示例后确认公开 S3 bulk 文件仍可直接访问：

- `https://s3.amazonaws.com/data.patentsview.org/download/g_patent_abstract.tsv.zip`
- `https://s3.amazonaws.com/data.patentsview.org/download/g_patent.tsv.zip`

因此 Patent 从“必须等待 API key”调整为：

`PUBLIC_BULK_PIPELINE_READY`

已新增：

- `My_work/03_data/pilot/collect_patents_public_bulk.py`
- `My_work/03_data/pilot/patent_bulk_input_contract.md`
- `.github/workflows/wp2-patent-public-bulk.yml`

正式采样逻辑：

1. 下载 PatentsView public abstract/patent bulk ZIP；
2. 流式扫描 abstracts；
3. 同时要求 AI signal + T01–T15 capability signal；
4. 每 family 使用 deterministic low-hash pool，避免文件顺序采样偏差；
5. 回连 g_patent 标题与日期；
6. 过滤 `patent_date <= 2026-06-30`；
7. 输出目标约 500 条 patent candidates；
8. 再进入 semantic screening 和后续 claims/CPC enrichment。

Patent public-bulk workflow 已提交，等待 GitHub Actions 调度/执行状态确认。

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
- Patent public bulk collector/workflow。

仍需：

- O/V 扩容结果完成并落库；
- Patent public bulk 500 条执行验证；
- OpenAlex ~1000 条 Science Pilot（当前缺 API key）；
- >=300 gold labels；
- Precision >=0.90；
- primary-family macro-F1 >=0.80；
- 高频类 F1 >=0.85。

WP3 仍保持 TODO，不提前启动。
