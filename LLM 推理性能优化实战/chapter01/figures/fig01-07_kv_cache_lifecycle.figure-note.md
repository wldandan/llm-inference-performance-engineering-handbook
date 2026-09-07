# 图 1-7 制作说明：KV Cache 生命周期

- 来源段落：第 1.7 节。
- 阅读顺序：从 Prefill 创建，经 Decode 读写增长，到 Finish 资源交接。
- 关键结论：KV Cache 在 Prefill 写入，在 Decode 读写增长，结束时必须交接。
- 表达边界：不说明分页、量化或 Prefix Cache 的具体实现。
