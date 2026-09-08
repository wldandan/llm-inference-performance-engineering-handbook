# Part 1 交付报告

## 交付结论

Part 1《LLM 推理系统基础》已按 v1.0 大纲完成 Chapter 1–7 的正文、Demo、Review、Storyboard 和插图整理，可以作为文字教程与离线实践包交付。

当前唯一未闭环项是：在课程目标 GPU 环境实际启动 vLLM、加载模型并完成流式请求。仓库内的启动命令、客户端逻辑和干运行已通过检查，但这项真实环境验证不能由离线测试替代。

## 章节清单

| 章节 | 核心产出 | Demo 测试 | 插图 |
|---|---|---:|---:|
| Chapter 1 第一个 LLM 服务 | 启动、流式调用、客户端观察 | 7 | 4 |
| Chapter 2 Inference Lifecycle | 请求状态与阶段时间报告 | 9 | 10 |
| Chapter 3 LLM Inference Architecture | 架构角色与连线契约校验 | 13 | 10 |
| Chapter 4 Transformer 推理机制 | Shapes、Sampling、Prefill / Decode Trace | 8 | 8 |
| Chapter 5 GPU 性能心智模型 | Compute / Capacity / Bandwidth / Launch 预算 | 9 | 8 |
| Chapter 6 LLM 性能指标 | 延迟、吞吐、Goodput、成本与测量合同 | 8 | 9 |
| Chapter 7 Global Performance Model | DAG Critical Path 与 RAG / Agent 路径 | 8 | 9 |
| 合计 | 7 章 | 62 | 58 |

Chapter 4 另有 25 项模型机制 Workshop 测试。章节插图之外还有 31 项结构、视觉契约、集中代码目录和校验器测试；本轮合计执行 118 项测试。

## 交付物组成

每章至少包含：

- `chapterXX.md`：可独立阅读的教程正文；
- `code/chapterNN/`：不依赖 GPU 的最小可运行练习或真实服务客户端；
- `review.md`：结构、技术边界、缺口与后续优先级；
- `storyboard.md`：插图职责、Wireframe 和视觉规范；
- `figures/`：SVG 正稿和一一对应的 `figure-note.md`；
- `test_figures.py`：图片集合、图号、链接和视觉契约检查。

## 验证记录

- `python3 scripts/validate_part.py --part 1`：通过，实际覆盖 Chapter 1–7。
- 七章 Demo：62 项测试通过。
- Chapter 4 模型机制 Workshop：25 项测试通过。
- 章节结构、插图契约、集中代码目录与校验器：31 项测试通过。
- 58 张 SVG：XML 解析通过，并全部重新渲染为 1280×720 PNG。
- 58 张 SVG 均有同名 `figure-note.md`。
- Part 1 正文与 Demo README 的本地 Markdown 链接：0 个缺失。
- vLLM、Ray Serve、KServe、Triton、TensorRT-LLM、NVIDIA Dynamo 与 llama.cpp 的课程引用入口已于 2026-09-07 复核。
- Git 差异格式检查：通过。

## 已知边界

1. Chapter 1 的真实 vLLM 服务需要 NVIDIA GPU 环境；当前只完成客户端测试和启动命令干运行。
2. Chapter 2–7 的报告使用合成或离线输入，用于验证概念和算法，不代表具体模型、硬件或框架的 Benchmark。
3. Chapter 7 的 Critical Path 解释单请求/单任务依赖关系；跨请求争抢、动态 Batch 和 GPU Kernel 证据留给 Part 2。
4. RAG 与 Agent 在 Part 1 只建立端到端性能路径，专项优化分别进入后续章节。

## 下一步

Part 2 从 Chapter 8 Benchmark Design 开始：把 Part 1 已定义的 Outcome、Workload、Boundary 和 Guardrail 固化成可复现实验合同，再进入 Chapter 9 Profiling Toolchain。
