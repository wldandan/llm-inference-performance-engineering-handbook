# 《LLM 推理性能工程实战》v1.0 课程大纲

> 历史版本：当前权威大纲见 [`02_Course_Outline_v0.2.md`](02_Course_Outline_v0.2.md)。本文件只用于追溯早期结构决策。

> 副标题：从模型原理、性能分析到 Serving 与 Agent 优化

## 课程定位

面向后端工程师、Agent 工程师、AI 应用工程师和 MLOps / 平台工程师，目标是让学员能够运行 LLM 服务、理解推理机制、建立性能基线、定位瓶颈，并完成面向 RAG、Agent 和生产 Serving 的性能优化。

课程分为两条路径：

- **Core Track**：后端和 Agent 工程师必须掌握的内容。
- **Advanced Track**：平台和基础设施工程师深入学习的内容。

标签说明：`[Core]` 核心必修；`[Bridge]` 基础必修、深度选修；`[Advanced]` 进阶选修。

## 学习主线

```text
启动服务 → 理解推理 → 测量性能 → 定位瓶颈 → 优化单 GPU
→ 优化 Serving / RAG / Agent → 规模化部署 → 综合项目
```

## Part 1：LLM 推理系统基础

| 章节 | 标题 | 定位 | 核心问题 |
|---|---|---|---|
| Ch1 | 第一个 LLM 服务 | Core | 如何启动、调用并测量一个 LLM 服务？ |
| Ch2 | Inference Lifecycle | Core | 一次请求如何从进入服务到返回结果？ |
| Ch3 | LLM Inference Architecture | Core | Client、Gateway、Scheduler、Worker 如何协作？ |
| Ch4 | Transformer 推理机制 | Core | Attention、Prefill、Decode 和 Sampling 如何工作？ |
| Ch5 | GPU 性能心智模型 | Bridge | GPU 的计算、显存和带宽如何影响推理？ |
| Ch6 | LLM 性能指标 | Core | 如何定义 TTFT、TPOT、TPS、P99 和成本？ |
| Ch7 | Global Performance Model | Core | 性能瓶颈来自 Queue、Prefill、Decode 还是其他环节？ |

## Part 2：性能测量与根因分析

| 章节 | 标题 | 定位 | 核心问题 |
|---|---|---|---|
| Ch8 | Benchmark Design | Core | 如何建立可信、可重复的 Baseline？ |
| Ch9 | Profiling Toolchain | Core + Advanced | 不同工具分别能回答什么性能问题？ |
| Ch10 | Root Cause Analysis | Core | 如何从性能现象追溯到真正根因？ |
| Ch11 | Performance Diagnosis Lab | Core | 如何完成一次从现象到证据的诊断？ |

## Part 3：Prefill 优化

| 章节 | 标题 | 定位 | 核心问题 |
|---|---|---|---|
| Ch12 | Prefill 工作机制 | Core | Prompt 如何被处理并生成 KV Cache？ |
| Ch13 | Prefill 性能分析 | Core + Advanced | 为什么 Prefill 常常是计算受限？ |
| Ch14 | Prefill 优化方法 | Core + Advanced | FlashAttention、FlashInfer 和上下文优化何时有效？ |
| Ch15 | Prefill 实战验证 | Core | 如何用实验降低长 Prompt 对 TTFT 的影响？ |

## Part 4：Decode 优化

| 章节 | 标题 | 定位 | 核心问题 |
|---|---|---|---|
| Ch16 | Decode 工作机制与 KV Cache | Core | LLM 如何逐 token 生成结果？ |
| Ch17 | Decode 性能分析 | Core + Advanced | 为什么 Decode 容易受显存带宽和 Kernel 开销影响？ |
| Ch18 | Decode 优化方法 | Core + Advanced | 如何使用 Batching、Cache、量化和投机解码？ |
| Ch19 | Decode 实战验证 | Core | 如何验证 TPOT、吞吐和显存是否改善？ |

## Part 5：Serving、RAG 与 Agent 性能工程

| 章节 | 标题 | 定位 | 核心问题 |
|---|---|---|---|
| Ch20 | Serving 工作机制 | Core | API、Queue、Scheduler、Worker 如何组成服务？ |
| Ch21 | Serving 调度与性能分析 | Core | 为什么队列、批处理和调度会影响尾延迟？ |
| Ch22 | Serving 优化方法 | Core + Advanced | 如何处理限流、准入、优先级、缓存和资源池？ |
| Ch23 | RAG 性能工程 | Core | 检索、重排和上下文如何影响延迟与成本？ |
| Ch24 | Agent 性能工程 | Core | 多步推理和工具调用为什么会放大延迟？ |
| Ch25 | Serving 与 Agent 综合实战 | Core | 如何优化一条完整的 RAG / Agent 服务链路？ |

## Part 6：规模化与分布式推理

| 章节 | 标题 | 定位 | 核心问题 |
|---|---|---|---|
| Ch26 | 容量模型、显存与成本 | Core | 单实例能承载多少请求，成本如何计算？ |
| Ch27 | 多副本、Scale-out 与 Autoscaling | Core | 如何提升容量并保持 SLO？ |
| Ch28 | Multi-GPU Inference | Advanced | Tensor / Pipeline Parallel 和 NCCL 如何工作？ |
| Ch29 | MoE、Expert Parallel 与 PD Disaggregation | Advanced | 如何处理 MoE 和分离式分布式推理？ |

## Part 7：综合项目

| 章节 | 标题 | 定位 | 核心问题 |
|---|---|---|---|
| Ch30 | End-to-End Performance Engineering Project | Core + Advanced | 如何完成一套可测量、可解释、可优化的 LLM 服务？ |

## 学习路径

### Core Track

重点完成 Ch1–Ch27，Ch28–Ch29 了解基本概念即可。学员最终应能启动服务、完成 Benchmark、定位瓶颈、优化单 GPU 推理，并优化 RAG / Agent 服务。

### Advanced Track

深入 Ch5、Ch9、Ch13、Ch17、Ch18、Ch28 和 Ch29，重点学习 GPU Runtime、多 GPU、NCCL、MoE、Expert Parallel、PD Disaggregation 和分布式容量规划。

## Demo 交付要求

每个核心实践章节都应提供可运行 Demo，包含：

1. 环境与版本；
2. Baseline 配置；
3. 性能脚本；
4. 指标采集；
5. 优化配置；
6. 相同流量重跑；
7. 优化前后对比；
8. 适用条件、限制和 Trade-off。

Demo 环境分为三档：

- Level 1：CPU / 无 GPU，验证机制和数据分析；
- Level 2：单 GPU，完成 Core 性能优化；
- Level 3：多 GPU / 多机，完成 Advanced 实验。

## Final Project

### Core 路线

构建一个可观测的 RAG / Agent 服务，完成 API、Streaming、Benchmark、缓存或量化、限流、性能报告和成本分析。

### Advanced 路线

构建一个可扩展的推理平台，完成多副本、自动扩缩容、多 GPU、Cache-aware Routing、SLO / Goodput 和性能回归。
