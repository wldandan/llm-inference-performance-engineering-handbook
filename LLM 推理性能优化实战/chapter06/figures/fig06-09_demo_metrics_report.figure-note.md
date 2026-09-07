# 图 6-9 制作说明：Demo 输出指标报告

- 来源段落：第 6 章“6.8 Demo：从请求记录生成指标报告”。
- 阅读顺序：三类输入进入 `metrics_report.py`，输出延迟、产能、成本和测量合同。
- 关键结论：Demo 把公式和口径写入报告，不把合成记录包装成实测。
- 边界：必须保留 `synthetic_client_metrics` 与 `NOT A BENCHMARK`。
