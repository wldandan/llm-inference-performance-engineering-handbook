# Chapter 6 Demo：离线指标报告

这个 Demo 读取一组 JSONL 请求记录，计算客户端口径的：

- TTFT、E2E、TPOT 和 ITL 分布；
- Output TPS、RPS 与满足 TTFT / E2E SLO 的 Goodput；
- 每百万输出 token 成本与每个成功请求成本。

运行：

```bash
python3 metrics_report.py
```

保存报告：

```bash
python3 metrics_report.py sample.jsonl --output metrics-report.json
```

输入中的 `token_times_ms` 是客户端观察到的 token 时间点。真实流式接口有时按 chunk 返回，不能把 chunk 时间直接冒充严格 token 时间；接入真实服务时，应先固定 tokenizer 计数、流式聚合和时钟口径。

报告固定使用 nearest-rank 分位数，并记录共享墙钟窗口和成本分母。样例是合成数据，只用于验证公式，不是 Benchmark。
