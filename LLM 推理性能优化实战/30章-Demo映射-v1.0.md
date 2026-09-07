# 《LLM 推理性能工程实战》30 章 - Demo 映射（v1.0）

> 本表是课程交付清单。状态“已有代码”表示仓库中已有脚本或测试；“待建设”表示需要后续实现或迁移。实际性能数字必须在指定硬件上运行后填写。

| 章节 | Demo / Workshop | 目标指标 | 环境 | 状态 |
|---|---|---|---|---|
| Ch1 | 第一个 LLM 服务 | 请求成功率、TTFT、流式首包 | Level 1/2 | 已有代码，单测通过；GPU 实跑待验收 |
| Ch2 | 请求生命周期追踪 | Queue、Prefill、Decode 时间 | Level 1/2 | 已有代码，9 项单测通过 |
| Ch3 | 服务架构拆解 | 请求路径、响应路径、组件边界 | Level 1 | 已有代码，13 项单测通过 |
| Ch4 | Transformer 与 KV Cache 演示 | Cache 正确性、生成时间 | Level 1/2 | 已有代码，可迁移 |
| Ch5 | GPU 性能心智模型 | GPU Util、带宽、Kernel 时间 | Level 2 | 待建设 |
| Ch6 | 指标采集客户端 | TTFT、TPOT、TPS、P99 | Level 1/2 | 已有公共工具 |
| Ch7 | 全局性能模型实验 | Queue / Prefill / Decode 占比 | Level 1/2 | 待建设 |
| Ch8 | Benchmark 基线 | 重复性、分位数、吞吐 | Level 2 | 已有公共工具 |
| Ch9 | Profiling 工具链 | Timeline、GPU、CPU 证据 | Level 2 | 部分已有 |
| Ch10 | 根因分析案例 | 现象 → 证据 → 根因 | Level 1/2 | 待建设 |
| Ch11 | 性能诊断 Lab | 诊断报告完整性 | Level 1/2 | 待建设 |
| Ch12 | Prefill 工作机制 | Prompt / KV Cache 形状 | Level 1/2 | 待建设 |
| Ch13 | Prefill 性能分析 | TTFT、Compute Util | Level 2 | 待建设 |
| Ch14 | FlashAttention / FlashInfer | TTFT、Attention Kernel | Level 2 | 待建设 |
| Ch15 | Prefill 综合实验 | 长 Prompt TTFT、成本 | Level 2 | 待建设 |
| Ch16 | Decode 与 KV Cache | TPOT、KV Cache 增长 | Level 1/2 | 已有代码，可迁移 |
| Ch17 | Decode 性能分析 | HBM、TPOT、Kernel Gap | Level 2 | 部分已有 |
| Ch18 | Decode 优化组合 | TPS、TPOT、显存 | Level 2 | 多个样板可组合 |
| Ch19 | Decode 综合实验 | 优化收益与边界 | Level 2 | 待建设 |
| Ch20 | Serving 工作机制 | Queue、Streaming、取消 | Level 1/2 | 待建设 |
| Ch21 | 调度与性能分析 | Queue Delay、P99 | Level 2 | 部分已有 |
| Ch22 | Serving 优化方法 | 准入、优先级、限流 | Level 2 | 待建设 |
| Ch23 | RAG 性能工程 | 检索延迟、TTFT、成本 | Level 1/2 | 待建设 |
| Ch24 | Agent 性能工程 | E2E、步骤耗时、Token | Level 1/2 | 待建设 |
| Ch25 | Serving / Agent 综合实战 | Goodput、SLO、成本 | Level 2 | 待建设 |
| Ch26 | 容量、显存与成本 | 最大并发、OOM、单位成本 | Level 2 | 待建设 |
| Ch27 | 多副本与 Autoscaling | TPS、P99、扩容生效时间 | Level 2/3 | 待建设 |
| Ch28 | Multi-GPU Inference | Scaling Efficiency、通信 | Level 3 | 待建设 |
| Ch29 | MoE / EP / PD 分离 | All-to-All、Goodput | Level 3 | 选修待建设 |
| Ch30 | End-to-End Project | 综合性能报告 | Level 2/3 | 待建设 |

## Core 首批 Demo

1. Ch4：模型内部与 KV Cache；
2. Ch6 / Ch8：指标采集与 Benchmark；
3. Ch16 / Ch18：Decode、Batching 与 KV Cache；
4. Ch14 / Ch15：Prefill 与 TTFT；
5. Ch23：RAG 上下文与 Prefix Cache；
6. Ch24：Agent 多步调用与并行工具；
7. Ch25：Serving / Agent 综合优化。

## Advanced Demo

- Ch5 / Ch9：GPU Runtime 与 Profiling；
- Ch17 / Ch18：CUDA Graph、Kernel Fusion；
- Ch28：Tensor Parallel、Pipeline Parallel、NCCL；
- Ch29：MoE、Expert Parallel、PD Disaggregation。

## 每个 Demo 的验收标准

- 能在 README 中完成环境安装和启动；
- Baseline 与 optimized 使用相同请求集；
- 有 warmup 和多次重复；
- 至少记录平均值与 P50 / P95 / P99；
- 同时记录质量、延迟、吞吐、显存和成本中适用的指标；
- 说明收益成立的条件和不适用的场景；
- 有自动化测试覆盖纯函数和输入校验。
