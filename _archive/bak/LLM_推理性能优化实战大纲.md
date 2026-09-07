# LLM 推理性能优化实战（基于 GX10）

## 课程定位

**课程名称：** LLM 推理性能优化实战------基于 GX10
的推理性能分析、Profiling 与优化实践

**课程目标**

完成本课程后，学员能够：

-   理解 LLM 推理完整生命周期（Prefill → Decode）
-   掌握 TTFT、ITL、TPS、GPU Utilization 等核心指标
-   使用 Profiling 工具定位性能瓶颈
-   理解 Compute Bound 与 Memory Bound 的本质区别
-   掌握主流推理优化技术及适用场景
-   独立完成 LLM 推理性能分析、优化与验证

------------------------------------------------------------------------

# 第一篇 推理基础

## 第1章 LLM 推理流程

### 内容

-   Transformer 推理流程
-   Token 生成过程
-   Prefill 与 Decode
-   GPU 生命周期
-   KV Cache 生命周期
-   Compute Bound vs Memory Bound

### Demo

运行 Qwen 模型，观察完整推理过程。

### 学习目标

建立完整的 LLM 推理生命周期认知。

------------------------------------------------------------------------

## 第2章 LLM 性能指标

### 内容

-   TTFT（Time To First Token）
-   ITL / TPOT（Inter-Token Latency）
-   Throughput（Tokens/s、Requests/s）
-   Latency（P50/P95/P99）
-   GPU Utilization
-   GPU Memory Usage
-   SM Occupancy
-   HBM Bandwidth

### Demo

使用 vLLM Benchmark 测试不同配置下的性能指标。

------------------------------------------------------------------------

# 第二篇 Profiling 与瓶颈分析

## 第3章 GPU Profiling

### 工具

-   nvidia-smi
-   nvtop
-   Nsight Systems
-   Nsight Compute
-   PyTorch Profiler

### Demo

观察 GPU 利用率、显存、Kernel Timeline、SM Occupancy。

------------------------------------------------------------------------

## 第4章 Prefill Profiling

### 内容

-   为什么 Prefill 是 Compute Bound
-   Prompt 长度对 TTFT 的影响
-   Attention 与 GEMM 的计算特点

### Demo

Prompt：512 / 1024 / 4096 / 8192 Token 对比实验。

------------------------------------------------------------------------

## 第5章 Decode Profiling

### 内容

-   为什么 Decode 是 Memory Bound
-   KV Cache 如何影响性能

### Demo

固定 Prompt，改变输出长度，对比 ITL 与 Tokens/s。

------------------------------------------------------------------------

# 第三篇 Compute Optimization

## 第6章 FlashAttention

-   FlashAttention 原理
-   FlashInfer
-   Kernel Fusion
-   Tensor Core

### Demo

开启 / 关闭 FlashAttention 对比 TTFT 与吞吐。

------------------------------------------------------------------------

## 第7章 CUDA Graph 与 Kernel Optimization

-   CUDA Graph
-   Persistent Kernel
-   Kernel Fusion

### Demo

分析 Kernel Launch 开销并进行优化。

------------------------------------------------------------------------

# 第四篇 Memory Optimization

## 第8章 KV Cache

-   KV Cache 生命周期
-   显存增长规律

### Demo

观察长上下文下的 KV Cache 增长。

------------------------------------------------------------------------

## 第9章 PagedAttention

-   分页管理
-   显存碎片优化

### Demo

开启 / 关闭 PagedAttention 对比显存利用率。

------------------------------------------------------------------------

## 第10章 Prefix Cache

### Demo

多个请求共享 Prompt，比较 TTFT。

------------------------------------------------------------------------

## 第11章 KV Quantization

-   FP16
-   FP8
-   INT8

### Demo

比较显存占用、吞吐和精度。

------------------------------------------------------------------------

# 第五篇 Scheduling Optimization

## 第12章 Dynamic Batching

Batch=1、2、4、8、16、32 对比实验。

------------------------------------------------------------------------

## 第13章 Continuous Batching

普通 Batch 与 Continuous Batch 对比。

------------------------------------------------------------------------

## 第14章 Chunked Prefill

长 Prompt 分块处理实验。

------------------------------------------------------------------------

# 第六篇 Decode Acceleration

## 第15章 Speculative Decoding

-   Draft & Verify
-   Speculative Decoding 原理

### Demo

普通 Decode 与 Speculative Decode 对比。

------------------------------------------------------------------------

## 第16章 Multi-Token Prediction

-   MTP
-   Medusa
-   EAGLE

### Demo

比较 Tokens/s 与 ITL。

------------------------------------------------------------------------

# 第七篇 Multi-GPU（可选）

-   Tensor Parallel
-   Pipeline Parallel
-   Expert Parallel
-   Context Parallel
-   通信优化（NCCL、NVLink、RDMA）

------------------------------------------------------------------------

# 第八篇 综合性能调优

## 第17章 构建 Benchmark

统一 Benchmark：

-   Prompt Length
-   Output Length
-   Batch Size
-   Concurrency

输出：

-   TTFT
-   ITL
-   TPS
-   GPU 利用率
-   GPU 显存

------------------------------------------------------------------------

## 第18章 综合调优实验

目标：

-   TTFT 降低 30%
-   TPS 提升 50%
-   GPU 利用率持续提升

流程：

> Profiling → 分析瓶颈 → 实施优化 → Benchmark 验证 → 输出实验报告

------------------------------------------------------------------------

# 每章 Demo 对应关系

  章节               Demo                关键指标
  ------------------ ------------------- ----------------
  推理流程           Prefill vs Decode   GPU Util、显存
  Profiling          Nsight Timeline     Kernel、SM
  Prefill            Prompt 长度实验     TTFT
  Decode             Output 长度实验     ITL
  FlashAttention     开关对比            TTFT、TPS
  KV Cache           长上下文实验        显存
  PagedAttention     开关对比            并发、显存
  Prefix Cache       重复 Prompt         TTFT
  Dynamic Batch      Batch 实验          吞吐、时延
  Continuous Batch   Batch 对比          GPU 利用率
  Speculative        开关对比            Tokens/s
  综合实验           Benchmark 调优      全部指标

------------------------------------------------------------------------

# 课程最终交付

-   LLM Benchmark 工具
-   GPU Profiling 环境
-   性能监控脚本
-   优化案例库
-   综合性能调优项目

## 核心方法论

> 建立性能模型 → 度量关键指标 → 定位瓶颈 → 选择优化策略 → 验证优化收益
