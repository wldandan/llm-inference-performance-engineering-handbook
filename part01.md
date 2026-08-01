# Part 1 Understanding LLM Inference System（理解推理系统）

## 本篇导读

做 LLM 推理性能优化，第一步不是打开某个框架参数，也不是先跑一组 benchmark。更稳的起点，是先知道自己面对的是一个什么系统。

一个在线 LLM 服务不只是模型权重加一次 forward。请求从客户端进入系统后，会经过入口层、队列、调度器、执行 worker、推理 runtime 和 GPU。用户看到的延迟、吞吐和稳定性，往往是这些组件共同作用的结果。只盯着模型计算，很容易把问题看窄：GPU 没跑满可能是调度问题，首包慢可能是队列或 Prefill 问题，吞吐高也可能掩盖尾部延迟。

Part 1 的目标，是给后续所有性能分析建立一张共同地图。后面讲 Benchmark、Profiling、Prefill、Decode、KV Cache、Batching、Speculative Decoding、多 GPU 和生产可观测性时，都要先回到这张地图上定位：问题发生在哪一层，应该观察什么，下一步才谈怎么优化。

## 本篇主线

本篇对应课程统一方法里的第一步：理解系统。

```text
理解系统
  -> 分析性能问题
  -> 优化系统
  -> 工程实践
```

在这一篇里，我们不急着给出优化结论，而是先回答四个基础问题：

1. LLM 推理系统由哪些组件组成？
2. 一个请求在系统里如何流动？
3. 用哪些指标描述系统表现？
4. 性能瓶颈通常来自哪些资源约束？

这四个问题分别由前四章承担。它们合在一起，构成后续性能工程的语言系统：架构用来定位组件，生命周期用来定位阶段，指标用来描述现象，性能模型用来提出假设。

## 本篇章节关系

| 章节 | 作用 |
|---|---|
| Chapter 1 LLM Inference Architecture | 建立系统架构视图，说明 Client、Gateway、Scheduler、Worker、Runtime 与 GPU 的职责边界。 |
| Chapter 2 Inference Lifecycle | 沿着一次请求的执行过程，解释 Queue、Prefill、Decode、Response、KV Cache 和 Streaming Response。 |
| Chapter 3 Performance Metrics | 定义 TTFT、TPOT / ITL、TPS、RPS、GPU Utilization、GPU Memory、P50 / P95 / P99 和 Cost per Token。 |
| Chapter 4 Global Performance Model | 把架构、生命周期和指标放到同一个模型里，理解 Compute、Memory、Scheduling 等瓶颈来源和指标之间的 Trade-off。 |

这四章不要混在一起写。第 1 章只讲系统长什么样，第 2 章讲请求怎么走，第 3 章讲如何度量，第 4 章才开始把瓶颈来源抽象成全局模型。这样拆开以后，后续进入 Profiling 和优化技术时，读者不会把“现象、阶段、指标、根因、优化手段”混成一团。

## 学完本篇你应该能做到什么

读完 Part 1，你应该能够：

- 画出一个在线 LLM 推理系统的基本架构。
- 把一次请求拆成入口、队列、Prefill、Decode、返回和缓存管理等阶段。
- 区分 TTFT、TPOT / ITL、TPS、RPS、尾延迟、GPU 利用率和显存占用各自回答的问题。
- 用 `Latency = Queue + Prefill + Decode` 这样的全局模型描述一次请求的主要时间来源。
- 面对一个性能现象时，先说清楚它落在哪个组件、哪个阶段、哪个指标上，而不是直接套优化技术。

## 进入下一篇之前的检查清单

- [ ] 能画出 Client -> Gateway -> Scheduler -> Worker -> Runtime -> GPU 的架构链路。
- [ ] 能说明 Prefill 和 Decode 在请求生命周期中的位置，但不急着展开优化细节。
- [ ] 能解释为什么单看 tokens/s 不足以判断在线服务体验。
- [ ] 能说明 Queue、Compute、Memory、Scheduling 至少四类瓶颈来源。
- [ ] 能把一个用户反馈转化成“组件 + 阶段 + 指标”的初步分析问题。

下一篇会进入 Performance Analysis。也就是说，从“知道系统长什么样”，进入“如何用 Benchmark、Profiling 和 Root Cause Analysis 证明问题到底在哪里”。
