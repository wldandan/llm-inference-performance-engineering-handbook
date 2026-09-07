# Part 5 Serving Optimization（Serving 优化）

## 本篇导读

前 3 篇已经建立了系统地图、性能分析证据链，以及 Prefill 阶段的完整优化闭环。从这一篇开始，课程继续沿着同一套方法推进：先明确模块在推理系统中的位置，再分析瓶颈，选择优化方法，最后用 Benchmark 和 Performance Report 验证收益。

Serving Optimization（Serving 优化） 的核心问题是：回答：为什么 GPU 没有跑满，以及如何提高调度效率和系统吞吐？ 本篇不会把技术点写成孤立清单，也不会跳过证据直接给参数建议。每章都要继承前面三篇的经验：Part 1 负责定位系统位置，Part 2 负责证明问题在哪里，Part 3 提供“机制 -> 分析 -> 优化 -> 验证”的写作形态。

## 本篇主线

```text
理解系统
  -> 理解瓶颈
  -> 定位瓶颈
  -> 优化方案
  -> 验证收益
```

本篇把这条主线落到 Serving 场景。读者不只要知道有哪些技术，还要知道这些技术解决什么问题、证据是什么、收益边界在哪里。

## 本篇章节关系

| 章节 | 核心问题 |
|---|---|
| Chapter 18 Serving 工作机制 | Serving 层如何把请求变成高效执行？（【新增】API 层 / 客户端协议：OpenAI 兼容接口如何衔接 Chapter 1 的生命周期） |
| Chapter 19 Serving 性能分析 | 为什么 Serving 层会让 GPU 没跑满？ |
| Chapter 20 Serving 优化方法 | 如何提升调度效率和系统吞吐？（【新增】Prefill-Decode 分离 PD Disaggregation：利用 Prefill 计算密集、Decode 显存带宽密集的根本差异，拆到独立 GPU 池，已是 2026 年生产级主流架构） |
| Chapter 21 Serving 实战验证 | 如何证明 Serving 优化真的提高吞吐并控制队列？ |

## 学完本篇你应该能做到什么

- 说明 Serving 在完整 LLM 推理系统中的位置。
- 使用 Benchmark、Profiling、Root Cause 和 Diagnosis 方法定位 Serving 相关瓶颈。
- 根据 Profiling 证据选择候选优化，而不是凭经验打开所有开关。
- 设计实验验证收益，并说明对 TTFT、TPOT、TPS、GPU Utilization、Memory 和 Cost 的影响。
- 写出带有边界和 Trade-off 的 Performance Report。

## 进入下一篇之前的检查清单

- [ ] 能画出本篇模块和 Request / Prefill / Decode / Serving / Scalability 的关系。
- [ ] 能说明本篇常见瓶颈的指标特征。
- [ ] 能给出至少一个可验证 root cause 假设。
- [ ] 能设计一个不混入后续篇章结论的 Demo。
- [ ] 能说明本篇和 Scalability Optimization 的衔接。
