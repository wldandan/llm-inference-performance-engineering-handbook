# Part 3 Prefill Optimization（Prefill 优化）

## 本篇导读

Part 1 建立了推理系统地图，Part 2 建立了 Benchmark、Profiling、Root Cause 和 Diagnosis 的证据链。第三篇开始进入真正的优化模块，但仍然遵守同一条原则：先理解机制，再分析瓶颈，然后选择优化，最后验证收益。

Prefill 是 LLM 推理中处理完整输入 prompt 的阶段。它通常决定用户看到首个 token 之前要等待多久，因此和 TTFT 关系最直接。长 prompt、RAG 上下文、Agent 工具结果、代码仓库片段和多轮对话历史都会放大 Prefill 压力。Prefill 慢，不一定是模型“整体慢”，也不一定能靠调大并发解决。它可能来自 attention 数据访问、GEMM 计算、kernel launch、KV Cache 创建、batch token 预算或输入长度分布。

本篇的目标，是把 Prefill 从一个模糊的“首包前计算”拆成可分析、可优化、可验证的工程对象。

## 本篇主线

本篇对应课程统一方法中的完整闭环：

```text
理解系统
  -> 理解瓶颈
  -> 定位瓶颈
  -> 优化方案
  -> 验证收益
```

四章关系如下：

1. 第 9 章先讲 Prefill 工作机制：输入如何进入模型，Attention、GEMM 和 KV Cache 创建各自在哪里。
2. 第 10 章讲 Prefill 性能分析：为什么它更容易 compute-bound，如何用 Roofline、Tensor Core 和 Timeline 看证据。
3. 第 11 章讲 Prefill 优化方法：FlashAttention、FlashInfer、CUDA Graph、Kernel Fusion 和 Persistent Kernel 分别解决什么问题。
4. 第 12 章讲 Prefill 实战验证：用 prompt 长度实验、TTFT Benchmark 和 Performance Report 验证收益边界。

这四章必须连起来写。第 9 章不急着优化，第 10 章不直接调参，第 11 章不只列技术名，第 12 章不只展示结果截图。

## 本篇章节关系

| 章节 | 作用 |
|---|---|
| Chapter 9 Prefill 工作机制 | 建立 Prefill 执行流程、Attention Pipeline、GEMM 和 KV Cache 创建的机制视图。 |
| Chapter 10 Prefill 性能分析 | 解释 Compute Bound、Roofline、Tensor Core、Kernel Timeline 和 Profiling 证据。 |
| Chapter 11 Prefill 优化方法 | 按技术专题讲 FlashAttention、FlashInfer、CUDA Graph、Kernel Fusion、Persistent Kernel 的适用条件和 Trade-off。 |
| Chapter 12 Prefill 实战验证 | 用 prompt 长度实验和 TTFT Benchmark 完成 Baseline -> Profiling -> Optimization -> Verification -> Report。 |

## 学完本篇你应该能做到什么

读完 Part 3，你应该能够：

- 画出 Prefill 从 token 输入到 KV Cache 写入的执行路径。
- 判断 Prefill 问题更像计算瓶颈、kernel launch 开销、attention 数据访问问题还是调度问题。
- 根据 Profiling 证据选择合适的 Prefill 优化技术，而不是看到 TTFT 高就盲目打开所有开关。
- 设计 prompt 长度实验，验证优化对 TTFT、TPS、GPU Utilization 和显存的影响。
- 写出一份 Prefill Performance Report，说明收益、边界、Trade-off 和上线前检查项。

## 进入下一篇之前的检查清单

- [ ] 能说明 Prefill 与 Decode 的职责边界。
- [ ] 能解释为什么长 prompt 会显著影响 TTFT。
- [ ] 能把 Prefill 的主要计算拆成 Attention、GEMM、KV Cache 创建和运行时调度开销。
- [ ] 能用 Benchmark 和 Profiling 证据判断一项 Prefill 优化是否适用。
- [ ] 能说明某项优化的收益在哪些 prompt 长度、模型结构、硬件和框架版本下成立。

下一篇会进入 Decode Optimization。Prefill 关注首个 token 之前的大块输入处理；Decode 关注首个 token 之后的逐 token 生成节奏。两者瓶颈不同，优化方法也不同。
