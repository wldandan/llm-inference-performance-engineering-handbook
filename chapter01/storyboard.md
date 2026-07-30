# 第一章 Storyboard 索引

| 图号 | 标题 | 核心问题 | 状态 |
|---|---|---|---|
| 图1-1 | 一次 LLM 在线推理请求生命周期 | 一次请求发生了什么？ | wireframe |
| 图1-2 | LLM Serving 整体架构 | 请求经过哪些模块？ | wireframe |
| 图1-3 | Decoder-only Transformer 推理过程 | 模型如何生成 token？ | wireframe |
| 图1-4 | Prefill 执行过程 | Prefill 做什么？ | wireframe |
| 图1-5 | Decode 执行过程 | Decode 做什么？ | wireframe |
| 图1-6 | KV Cache 生命周期与增长 | KV Cache 如何变化？ | wireframe |
| 图1-7 | GPU Memory & Compute Lifecycle | GPU 如何工作？ | wireframe |
| 图1-8 | Compute Bound vs Memory Bound | 为什么会慢？ | wireframe |
| 图1-9 | Profiling Workflow | 如何观察？ | wireframe |
| 图1-10 | Performance Diagnosis Tree | 如何定位？ | wireframe |

## Wireframe 说明

当前 10 张图均为 SVG wireframe，用于确定章节插图位置、阅读路径和核心信息，不是最终出版图。

统一规则：

- 16:9 横版 SVG。
- 白底。
- 黑灰线段。
- 空心框。
- 简单箭头。
- 少量文字。
- 底部保留 Key Takeaway。
- 不使用彩色填充。

## 下一步

正式制图前，应逐张补充详细 storyboard。建议优先处理：

1. 图1-1：一次 LLM 在线推理请求生命周期。
2. 图1-4：Prefill 执行过程。
3. 图1-5：Decode 执行过程。
