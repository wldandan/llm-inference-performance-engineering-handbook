# Part 6 Scalability Optimization（规模化优化）

## 本篇导读

前 3 篇已经建立了系统地图、性能分析证据链，以及 Prefill 阶段的完整优化闭环。从这一篇开始，课程继续沿着同一套方法推进：先明确模块在推理系统中的位置，再分析瓶颈，选择优化方法，最后用 Benchmark 和 Performance Report 验证收益。

Scalability Optimization（规模化优化） 的核心问题是：回答：如何提升并发、扩展容量并降低成本？ 本篇不会把技术点写成孤立清单，也不会跳过证据直接给参数建议。每章都要继承前面三篇的经验：Part 1 负责定位系统位置，Part 2 负责证明问题在哪里，Part 3 提供“机制 -> 分析 -> 优化 -> 验证”的写作形态。

## 本篇主线

```text
理解系统
  -> 理解瓶颈
  -> 定位瓶颈
  -> 优化方案
  -> 验证收益
```

本篇把这条主线落到 Scalability 场景。读者不只要知道有哪些技术，还要知道这些技术解决什么问题、证据是什么、收益边界在哪里。

## 本篇章节关系

| 章节 | 核心问题 |
|---|---|
| Chapter 22 Scalability 工作机制 | 推理系统容量由哪些资源决定？ |
| Chapter 23 Scalability 性能分析 | 如何分析容量、碎片和 KV Pool 问题？ |
| Chapter 24 Scalability 优化方法 | 如何扩展容量并降低单位 token 成本？（【调整】Expert Parallel 扩展为 MoE 推理优化专项：All-to-All 通信开销、专家负载均衡/路由倾斜、按激活参数而非总参数的显存与成本模型——2026 年主流开源模型 DeepSeek V3.2 / Llama 4 Maverick / Kimi K2 均为 MoE 架构；【新增】Scale-out 呼应 Chapter 20 的 PD 分离：独立 Prefill/Decode 资源池可分别弹性伸缩） |
| Chapter 25 Scalability 实战验证 | 如何证明扩容方案真的提升容量并控制成本？ |

## 学完本篇你应该能做到什么

- 说明 Scalability 在完整 LLM 推理系统中的位置。
- 使用 Benchmark、Profiling、Root Cause 和 Diagnosis 方法定位 Scalability 相关瓶颈。
- 根据 Profiling 证据选择候选优化，而不是凭经验打开所有开关。
- 设计实验验证收益，并说明对 TTFT、TPOT、TPS、GPU Utilization、Memory 和 Cost 的影响。
- 写出带有边界和 Trade-off 的 Performance Report。

## 进入下一篇之前的检查清单

- [ ] 能画出本篇模块和 Request / Prefill / Decode / Serving / Scalability 的关系。
- [ ] 能说明本篇常见瓶颈的指标特征。
- [ ] 能给出至少一个可验证 root cause 假设。
- [ ] 能设计一个不混入后续篇章结论的 Demo。
- [ ] 能说明本篇和 Production Performance Engineering 的衔接。
