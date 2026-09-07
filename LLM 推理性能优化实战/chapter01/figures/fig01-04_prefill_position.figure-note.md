# 图 1-4 制作说明：Prefill 在生命周期中的位置

- 来源段落：第 1.4 节。
- 阅读顺序：从首次调度进入 Prefill，再分流到 KV Cache 和首 token logits。
- 关键结论：Prefill 处理完整输入，并写入 Decode 后续复用的 KV Cache。
- 表达边界：不加入 Attention 公式、Kernel 或优化实现。
