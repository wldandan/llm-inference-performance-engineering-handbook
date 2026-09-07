# 图 2-5 制作说明：Prefill 与首 token 的边界

- 来源段落：第 2.5 节。
- 阅读顺序：先读服务端 Prefill 路径，再沿虚线进入客户端首包观测点。
- 关键结论：首 token 已生成，不代表客户端已经收到首包。
- 表达边界：不展开 Attention 公式、优化 Kernel 或 Benchmark 数据。
