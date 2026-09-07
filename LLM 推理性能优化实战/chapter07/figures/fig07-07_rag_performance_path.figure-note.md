# 图7-7 制作说明

- 来源段落：7.6 RAG。
- 图意：并行检索经 Merge、Rerank、Context Build 后进入 Prefill 和 Decode。
- 关键结论：检索既进入时间路径，也通过 prompt tokens 改变 LLM 工作量。
- 视觉约束：四个 Plane 分区；工作量影响使用虚线；保留质量提示。
