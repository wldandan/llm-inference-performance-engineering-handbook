# 图 2-6 制作说明：Decode step 与 KV Cache 增长

- 来源段落：第 2.6 节。
- 阅读顺序：上方看多轮 Decode step，下方按列观察 KV Cache 追加。
- 关键结论：一条请求跨越多轮执行，Decode 区间也可能包含执行间隙。
- 表达边界：不提供 KV Cache 容量公式、分页或量化实现。
