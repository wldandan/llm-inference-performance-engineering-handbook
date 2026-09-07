# 图 3-2 制作说明：Client 与 Gateway 边界

- 来源段落：第 3.2 节。
- 阅读顺序：先左右对照职责，再读取跨越协议边界的请求与流式响应。
- 关键结论：Gateway 管入口契约，不决定下一轮 token batch。
- 表达边界：不加入 Router、Engine Scheduler 或模型执行细节。
