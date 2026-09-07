# Part 1 LLM 推理系统基础

## 本篇导读

性能优化的起点不是调参数，而是建立一张足够准确的系统地图：请求从哪里进入，模型在算什么，时间花在哪里，系统又受哪些资源约束。

本篇采用“先运行、再解释、后建模”的顺序。第 1 章先启动一个 OpenAI-compatible 服务，让读者看到流式响应和客户端指标；第 2 章把一次请求整理成完整的 Inference Lifecycle；第 3、4 章分别解释服务架构与 Transformer 推理机制；第 5 章补充 GPU 性能心智模型；第 6、7 章建立指标体系和全局性能模型。

这套顺序面向后端工程师和 Agent 工程师设计。读者不需要先掌握 CUDA、GPU 微架构或分布式通信，就能完成第一次服务调用。硬件内容仍然保留，但第 5 章只讲分析性能必需的概念，更深的 CUDA、NCCL 和多 GPU 内容放在 Advanced Track。

## 本篇主线

```text
启动服务
  -> 观察请求生命周期
  -> 理解服务架构与模型计算
  -> 建立 GPU 性能直觉
  -> 定义指标
  -> 建立全局性能模型
```

本篇回答七个基础问题：

1. 如何启动、调用并观察一个 LLM 服务？
2. 一次请求如何从进入系统走到流式返回结束？
3. Client、Gateway、Scheduler、Worker 和 Runtime 如何协作？
4. Attention、Prefill、Decode 与 Sampling 分别做什么？
5. 计算量、显存容量与显存带宽如何约束推理？
6. 如何定义 TTFT、TPOT / ITL、TPS、P99 与 Cost per Token？
7. 如何判断瓶颈更可能来自 Queue、Prefill、Decode 或其他环节？

## 本篇章节关系

| 章节 | 路径 | 作用 |
|---|---|---|
| Chapter 1 第一个 LLM 服务 | Core | 启动 vLLM 服务，发出一次流式请求，把客户端现象映射到请求链路。 |
| Chapter 2 Inference Lifecycle | Core | 正式拆解 Queue、Prefill、First Token、Decode、Response 与资源回收。 |
| Chapter 3 LLM Inference Architecture | Core | 说明 Client、Gateway、Scheduler、Worker、Runtime 与 GPU 的职责边界。 |
| Chapter 4 Transformer 推理机制 | Core | 建立 Attention、Prefill、Decode、Sampling 和 KV Cache 的模型计算基础。 |
| Chapter 5 GPU 性能心智模型 | Bridge | 解释算力、显存、带宽、Kernel 与并行度如何影响推理，不要求先学高级 CUDA。 |
| Chapter 6 LLM 性能指标 | Core | 定义延迟、吞吐、尾延迟、资源利用率和成本指标，并说明测量边界。 |
| Chapter 7 Global Performance Model | Core | 把阶段、组件、指标和资源约束放进同一张性能地图。 |

七章之间有明确边界。第 1 章负责让系统跑起来；第 2 章描述请求如何流动；第 3 章解释组件如何协作；第 4 章解释模型为何以 Prefill 和 Decode 两种形态执行；第 5 章提供必要的硬件直觉；第 6 章定义测量语言；第 7 章才把现象收敛成可验证的瓶颈假设。

## 学完本篇你应该能做到什么

读完 Part 1，你应该能够：

- 独立启动一个 OpenAI-compatible LLM 服务并完成流式调用。
- 把一次请求拆成入口、排队、Prefill、Decode、返回和资源回收等阶段。
- 画出在线推理服务的基本架构，并说明主要组件的职责。
- 解释 Transformer 推理中 Attention、KV Cache、Prefill 和 Decode 的关系。
- 用计算量、显存容量、显存带宽和 Kernel 开销解释常见性能现象。
- 区分 TTFT、TPOT / ITL、TPS、RPS、P95 / P99 和 Cost per Token。
- 对普通串行请求使用阶段分解，对 RAG / Agent 使用依赖图与 Critical Path 建立性能假设。

## 进入下一篇之前的检查清单

- [ ] 能在本地或 GPU 服务器上启动课程提供的最小服务。
- [ ] 能画出 Request -> Queue -> Prefill -> Decode -> Response 的生命周期。
- [ ] 能区分请求阶段、系统组件、性能指标与优化手段。
- [ ] 能说明 Prefill 和 Decode 的计算形态为什么不同。
- [ ] 能解释为什么单看 tokens/s 不足以判断在线服务体验。
- [ ] 能把一个用户反馈转成“阶段 + 组件 + 指标 + 待验证假设”。
- [ ] 能画出 RAG 或 Agent 的依赖图，并区分关键路径与节点时间总和。

下一篇进入性能测量与根因分析：先建立可重复的 Baseline，再用 Profiling 证据判断瓶颈到底在哪里。
