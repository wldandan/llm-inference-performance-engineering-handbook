# LLM Performance Engineering：面向推理系统的性能优化实战

> **核心理念：理解推理系统 → 分析性能问题 → 优化系统 → 工程实践**

本文档只回答：

> **这门课程讲什么？**

课程设计理念和统一性能分析方法见 `01_Course_Design.md`；章节编写方式见 `03_Course_Template.md`。

---

## Part 1 Understanding LLM Inference System（理解推理系统）

> 建立统一的推理系统认知。

### Chapter 1 LLM Inference Architecture

**回答问题：** LLM 推理系统长什么样？

#### 内容

- LLM 推理系统整体架构
- Client / Gateway / Scheduler / Worker
- Runtime 与 GPU
- vLLM、SGLang、TensorRT-LLM 架构对比

---

### Chapter 2 Inference Lifecycle

**回答问题：** 一个请求如何完成推理？

#### 内容

- Request 生命周期
- Queue
- Prefill
- Decode
- Response
- KV Cache 生命周期
- Streaming Response

---

### Chapter 3 Performance Metrics

**回答问题：** 如何评价一个推理系统？

#### 内容

- TTFT
- TPOT / ITL
- TPS
- RPS
- GPU Utilization
- GPU Memory
- P50 / P95 / P99
- Cost per Token

---

### Chapter 4 Global Performance Model

**回答问题：** 性能瓶颈来自哪里？

#### 内容

- `Latency = Queue + Prefill + Decode`
- Compute Bottleneck
- Memory Bottleneck
- Scheduling Bottleneck
- 指标之间的关系与 Trade-off

---

## Part 2 Performance Analysis（性能分析）

> 建立统一的性能分析方法。

### Chapter 5 Benchmark Design

**回答问题：** 如何建立可信、可重复的性能 Baseline？

#### 内容

- Benchmark 原则
- Baseline 建立
- Warmup
- Repeat
- Prompt / Output / Concurrency 设计

---

### Chapter 6 Profiling Toolchain

**回答问题：** 如何采集推理系统不同层次的性能数据？

#### 内容

- Nsight Systems
- Nsight Compute
- PyTorch Profiler
- nvidia-smi
- vLLM Profiling

---

### Chapter 7 Root Cause Analysis

**回答问题：** 如何从性能现象追溯到真正瓶颈？

#### 内容

- Timeline 分析
- GPU Utilization 分析
- Memory Bandwidth 分析
- CPU Bottleneck
- Scheduler Bottleneck

---

### Chapter 8 Performance Diagnosis

**回答问题：** 如何形成统一、可执行的性能诊断流程？

#### 输出

统一 Performance Checklist：

- TTFT Checklist
- TPOT Checklist
- TPS Checklist
- GPU Util Checklist
- Memory Checklist

---

## Part 3 Prefill Optimization（Prefill 优化）

> 回答：为什么 Prefill 慢，以及如何降低 Prefill 对 TTFT 的影响？

### Chapter 9 Prefill 工作机制

#### 内容

- Prefill 执行流程
- Attention Pipeline
- GEMM
- KV Cache 创建

---

### Chapter 10 Prefill 性能分析

#### 内容

- Compute Bound
- Roofline
- Tensor Core
- Kernel Timeline
- Profiling

---

### Chapter 11 Prefill 优化方法

#### 内容

- FlashAttention
- FlashInfer
- CUDA Graph
- Kernel Fusion
- Persistent Kernel

每项技术统一讲解：

- 适用场景
- 原理
- Profiling 特征
- Benchmark
- Trade-off

---

### Chapter 12 Prefill 实战验证

#### 内容

- Prompt 长度实验
- TTFT Benchmark
- Performance Report
- Best Practice

---

## Part 4 Decode Optimization（Decode 优化）

> 回答：为什么 Decode 慢，以及如何改善 TPOT 和生成效率？

### Chapter 13 Decode 工作机制

#### 内容

- Decode Flow
- Sampling
- KV Cache Read
- Token Generation

---

### Chapter 14 Decode 性能分析

#### 内容

- Memory Bound
- HBM Bandwidth
- Decode Timeline
- KV Cache Growth

---

### Chapter 15 Decode 优化方法

#### Memory Optimization

- KV Cache
- PagedAttention
- KV Quantization
- Prefix Cache

#### Generation Optimization

- Speculative Decoding
- MTP
- Medusa
- EAGLE

---

### Chapter 16 Decode 实战验证

#### 内容

- Long Context 实验
- TPOT Benchmark
- Best Practice

---

## Part 5 Serving Optimization（Serving 优化）

> 回答：为什么 GPU 没有跑满，以及如何提高调度效率和系统吞吐？

### Chapter 17 Serving 工作机制

#### 内容

- Queue
- Scheduler
- Worker
- Runtime

---

### Chapter 18 Serving 性能分析

#### 内容

- Queue Delay
- GPU Idle
- Batch Efficiency
- Worker 利用率

---

### Chapter 19 Serving 优化方法

#### 内容

- Dynamic Batching
- Continuous Batching
- Chunked Prefill
- Admission Control

---

### Chapter 20 Serving 实战验证

#### 内容

- TPS Benchmark
- GPU Util Benchmark
- Queue Delay 分析
- Best Practice

---

## Part 6 Scalability Optimization（规模化优化）

> 回答：如何提升并发、扩展容量并降低成本？

### Chapter 21 Scalability 工作机制

#### 内容

- Capacity Model
- Memory Pool
- Multi-GPU

---

### Chapter 22 Scalability 性能分析

#### 内容

- Fragmentation
- Capacity Profiling
- KV Pool

---

### Chapter 23 Scalability 优化方法

#### Scale-up

- Quantization
- Tensor Parallel
- Pipeline Parallel
- Expert Parallel

#### Scale-out

- Replica
- Load Balance
- Autoscaling

---

### Chapter 24 Scalability 实战验证

#### 内容

- Capacity Benchmark
- 并发实验
- 成本分析
- Best Practice

---

## Part 7 Production Performance Engineering（生产实践）

> 回答：企业如何持续进行性能优化，而不是只完成一次性调优？

### Chapter 25 Benchmark Automation

#### 内容

- 自动化 Benchmark
- 数据采集

---

### Chapter 26 Performance Regression

#### 内容

- Regression
- CI 集成
- 自动告警

---

### Chapter 27 Observability

#### 内容

- Dashboard
- Grafana
- Prometheus
- 可观测性

---

### Chapter 28 Performance Review

#### 内容

- Performance Checklist
- Optimization Matrix
- Performance Report

---

### Chapter 29 Final Project

完成完整企业案例：

```text
Benchmark
    ↓
Profiling
    ↓
Root Cause
    ↓
Optimization
    ↓
Verification
    ↓
Performance Report
```
