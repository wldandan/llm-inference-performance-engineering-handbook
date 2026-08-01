# 第 1 章 Storyboard 索引

| 图号 | 标题 | 核心问题 | 状态 |
|---|---|---|---|
| 图1-1 | LLM 推理系统全局架构 | 一个在线 LLM 推理系统由哪些主要组件组成？ | wireframe |
| 图1-2 | Client 与 Gateway 边界 | 请求进入模型服务前，入口层负责什么？ | wireframe |
| 图1-3 | Scheduler 的核心职责 | Scheduler 如何决定请求共享 GPU 资源？ | wireframe |
| 图1-4 | Worker、Runtime 与 GPU 的分层关系 | 模型执行链路中三层职责如何区分？ | wireframe |
| 图1-5 | 推理服务的三类状态 | 调度为什么必须同时看请求、执行和资源状态？ | wireframe |
| 图1-6 | 部署形态演进 | 单实例、多实例、多模型和平台化服务有什么差别？ | wireframe |
| 图1-7 | 推理框架架构取向对比 | vLLM、SGLang、TensorRT-LLM、Llama.cpp 的取向如何不同？ | wireframe |
| 图1-8 | 架构视图到性能分析 | 架构定位如何连接到后续指标和工具？ | wireframe |
| 图1-9 | 本章最小 Demo 架构 | 本章 Demo 验证的最小服务链路是什么？ | wireframe |
| 图1-10 | 第 1 章与后续章节的边界 | 第 1 章只做架构，后续章节分别展开什么？ | wireframe |

## 视觉规范

- 16:9 SVG，`1280x720`。
- 白底、黑灰线框、简单箭头。
- 一图只回答一个问题。
- 不复制参考书图片，只抽取架构表达意图后重新绘制。
- 不在图中展开 Prefill、Decode、KV Cache、Benchmark 或 Profiling 细节。

