# Part 1 从一个请求理解 LLM 推理系统（Understanding One LLM Request）

## 本篇导读

性能优化不能从参数表开始。工程师首先要确认服务确实能运行，再把一次请求拆成可观察的生命周期，理解模型在执行什么、Serving 系统由谁负责，最后统一性能指标。缺少这张地图，后面看到 TTFT 上升、吞吐下降或 GPU 利用率变化时，很容易把现象误判成原因。

本篇坚持“先遇到问题，再引入技术”。第 1 章用同步请求完成最小生成闭环；当长回答暴露出等待期间没有反馈、首个内容到达不可见的问题后，第 2 章再引入流式响应，并在同一个 vLLM 服务上补齐服务端证据。第 3、4 章分别解释模型生成机制与 Serving 组件；第 5 章建立整门课程共用的性能语言。

读者不需要先掌握 CUDA、GPU 微架构或分布式通信。Core 只在解释 Prefill、Decode 和资源指标时引入必要的硬件直觉；GPU/CUDA、NCCL、多 GPU、MoE 和 PD Disaggregation 留在 Advanced。

## 本篇主线

```text
启动真实 vLLM 服务
  -> 用同步请求完成最小生成闭环
  -> 发现等待期间没有反馈、内部过程不可见
  -> 引入流式事件和服务端证据，还原请求生命周期
  -> 理解 Transformer 如何生成 token
  -> 理解 Serving 组件如何承接请求
  -> 用统一指标描述体验、产能、可靠性与成本
```

这不是六条彼此独立的知识点，而是同一个 Reference System 的逐层展开。第 1 章只证明“链路通了”；第 2 章回答“请求经历了什么”；第 3 章回答“模型算了什么”；第 4 章回答“谁组织这些计算”；第 5 章回答“怎样准确描述结果”。第 3～5 章可以复用前面采集的真实报告，但必须尊重证据边界；离线工具只用于核对机制、架构合同和公式，不能替代真实服务数据。

## 本篇章节关系

| 章节 | 定位 | 本章完成什么 | 明确不做什么 |
|---|---|---|---|
| Chapter 1 第一个 LLM 服务 | Core | 启动 vLLM，用同步请求验证完整生成链路 | 不引入流式协议，不分析服务内部阶段 |
| Chapter 2 真实请求生命周期 | Core | 为解决同步调用的观察缺口，引入流式事件，并采集 vLLM 请求级指标和 Prometheus 增量 | 不用聚合指标伪造单请求时间线，不做压测 |
| Chapter 3 Transformer 生成机制 | Core | 解释 Tokenizer、Attention、Prefill、Sampling、Decode 与 KV Cache | 不评价速度，不教授优化算法 |
| Chapter 4 LLM Serving 架构 | Core | 解释 Gateway、Router、Admission、Scheduler、Worker、Runtime 和 GPU 的职责 | 不把架构契约检查当成运行态验证 |
| Chapter 5 性能指标与延迟预算 | Core | 定义 TTFT、TPOT/ITL、成功输出/请求速率、分位数、SLO-aware Goodput 与成本口径 | 不设计正式 Benchmark，不做根因分析 |

五章的边界刻意收紧。特别是 Ch1 与 Ch2：Ch1 的产物是“第一次同步调用记录”，只证明服务能够返回完整答案；Ch2 的产物是“带证据等级的生命周期报告”，用更细的客户端事件和服务端数据回答同步调用无法回答的问题。后者必须明确哪些字段来自客户端、哪些来自 vLLM、哪些只是根据缺失边界做出的推断。

## 学完本篇你应该能做到什么

读完 Part 1，你应该能够：

- 独立启动 OpenAI-compatible vLLM 服务，先完成同步调用，再说明为什么需要流式调用；
- 区分 token、流式 chunk、请求级指标和服务端聚合指标；
- 画出 Request Received、Queue、Prefill、Decode、Streaming 和终态清理；
- 对每个生命周期结论标注“直接观测、计算得到、推断或当前不可得”；
- 解释 Transformer 的自回归生成过程，以及 KV Cache 在 Prefill/Decode 间的作用；
- 画出 LLM Serving 的核心组件与责任交接关系；
- 为 TTFT、TPOT/ITL、成功输出/请求速率、P95/P99、Goodput 和成本写出测量合同；
- 拒绝用单请求结果、GPU Utilization 或聚合直方图增量直接证明根因。

## 进入下一篇之前的检查清单

- [ ] Ch1 的同步请求可以复现，且没有被描述成 Benchmark。
- [ ] Ch2 能对真实 vLLM 请求生成生命周期证据报告。
- [ ] 能解释为什么客户端首个 chunk 不等于服务端首 token。
- [ ] 能解释为什么 Prometheus 增量在并发流量下不能归属于某一请求。
- [ ] 能区分 Transformer 机制、Serving 组件和性能指标三种视图。
- [ ] 能为一个指标写清测量点、公式、统计窗口和分母。
- [ ] 知道当前只建立 Baseline 所需语言，还没有完成性能归因。

下一篇进入“测量、观测与根因分析”：先定义生产代表性的 Workload 与 SLO，再建立可重复 Baseline，最后用分层证据验证瓶颈假设。
