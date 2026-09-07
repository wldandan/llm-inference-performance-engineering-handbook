# 图 2-4 制作说明：Queue 与首次调度的边界

- 来源段落：第 2.3 与 2.4 节。
- 阅读顺序：从 queued 事件进入 Waiting Queue，到首次 scheduled 事件退出。
- 关键结论：Queue 由 queued 与首次 scheduled 两个事件闭合。
- 表达边界：不评价队列策略，也不把全部客户端等待算作 Queue。
