# Part 2 Performance Analysis（性能分析）

## 本篇导读

理解系统以后，下一步不是立刻调参数，而是建立可信的分析证据。LLM 推理性能问题经常同时牵涉请求形态、队列、Prefill、Decode、GPU、CPU、网络和调度策略。如果没有可重复的 Benchmark 和分层 Profiling，团队很容易把偶然现象当成优化方向。

Part 2 的目标，是把“感觉慢”转化为可以验证的工程问题。我们先设计可信 Baseline，再学习不同层次的 Profiling 工具，然后把 Timeline、GPU Utilization、Memory Bandwidth、CPU 和 Scheduler 现象连成根因链路，最后形成统一的 Performance Checklist。

## 本篇主线

本篇对应课程统一方法中的第二步和第三步：理解瓶颈，定位瓶颈。

```text
理解系统
  -> 理解瓶颈
  -> 定位瓶颈
  -> 优化方案
  -> 验证收益
```

Part 1 已经回答系统由哪些组件和阶段组成。Part 2 继续回答四个问题：

1. 如何建立可信、可重复的性能 Baseline？
2. 如何采集推理系统不同层次的性能数据？
3. 如何从性能现象追溯到真正瓶颈？
4. 如何把诊断过程沉淀成可执行 Checklist？

这四个问题合在一起，构成后续所有优化章节的证据基础。没有 Baseline，优化收益无法比较；没有 Profiling，瓶颈只是猜测；没有 Root Cause，优化方案可能打错位置；没有 Checklist，团队每次排障都会重新摸索。

## 本篇章节关系

| 章节 | 作用 |
|---|---|
| Chapter 6 Benchmark Design | 建立可信 Baseline，说明 Warmup、Repeat、Prompt / Output / Concurrency 如何影响结论。 |
| Chapter 7 Profiling Toolchain | 说明 Nsight Systems、Nsight Compute、PyTorch Profiler、nvidia-smi 和 vLLM Profiling 分别能回答什么问题。 |
| Chapter 8 Root Cause Analysis | 从 Timeline、GPU Utilization、Memory Bandwidth、CPU 和 Scheduler 现象追溯根因。 |
| Chapter 9 Performance Diagnosis | 把前面的方法整理成 TTFT、TPOT、TPS、GPU Util 和 Memory 的统一诊断 Checklist。 |

这四章不能写成工具清单。第 6 章先保证实验输入可靠，第 7 章讲数据从哪里来，第 8 章讲如何把数据连成因果链，第 9 章才把方法压缩成现场可用的诊断流程。

## 学完本篇你应该能做到什么

读完 Part 2，你应该能够：

- 为一个 LLM 服务设计可信 Baseline，而不是只跑一次压测命令。
- 说明 Warmup、Repeat、Prompt 长度、Output 长度和 Concurrency 为什么会改变 Benchmark 结论。
- 根据问题层级选择 Profiling 工具，而不是所有问题都打开最重的 GPU profiler。
- 从 Timeline、GPU 利用率、显存、CPU 和 Scheduler 状态中提出可验证的 Root Cause 假设。
- 使用统一 Checklist 把 TTFT、TPOT、TPS、GPU Utilization 和 Memory 问题拆成下一步检查项。

## 进入下一篇之前的检查清单

- [ ] 能描述一个 Benchmark 的 Baseline、Workload、指标和重复性边界。
- [ ] 能解释为什么 Warmup 和 Repeat 是 Benchmark 的必要条件。
- [ ] 能区分系统级观测、框架级 Profiling 和 kernel 级 Profiling。
- [ ] 能把一个性能现象写成“现象 -> 证据 -> 假设 -> 验证动作”。
- [ ] 能用统一 Checklist 判断一个问题更像 Queue、Prefill、Decode、CPU、Scheduler 还是 Memory 瓶颈。

下一篇会进入 Prefill Optimization。也就是说，从“证明瓶颈在哪里”，进入“针对 Prefill 阶段选择优化方案并验证收益”。
