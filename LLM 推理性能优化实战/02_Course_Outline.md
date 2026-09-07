# LLM Performance Engineering：面向推理系统的性能优化实战（历史大纲）

> v1.0 权威大纲已迁移至 [`02_Course_Outline_v1.0.md`](02_Course_Outline_v1.0.md)。本文件暂作历史版本保留，后续正文重构以 v1.0 大纲为准。

> **核心理念：理解推理系统 → 分析性能问题 → 优化系统 → 工程实践**

本文档只回答：

> **这门课程讲什么？**

课程设计理念和统一性能分析方法见 `01_Course_Design.md`；章节编写方式见 `03_Course_Template.md`；每章配套的动手实验见 `workshops/`（与历史遗留的 `../_archive/lesson/` 课堂讲稿是两种不同格式，区分见项目根目录 `README.md`）。

> **2026-09-02 业界刷新**：三路并行调研（已有课程对标 MIT/Stanford/Berkeley/DeepLearning.AI、2025-2026 最新技术进展、vLLM/SGLang/TensorRT-LLM 等工业界一手实践）后，Part 1 新增「GPU 架构基础」一章，此后全部章节顺延 +1，**全课程由 29 章变为 30 章**。调研依据见 `.spike/llm-inference-optimization-course/NOTES.md`（本仓库外的调研暂存目录）。
>
> **2026-09-03 Part 1 内部排序调整**：Inference Lifecycle 和 LLM Inference Architecture 互换到 GPU 架构基础前面。原因：GPU 架构基础作为全书开篇过于"干"、缺代入感；而 Lifecycle 只需要 Gateway/Queue/Scheduler 这类字面意思即可理解的词，不像 GPU 硬件术语那样需要先修知识，适合放在最前面用一个具体场景（Llama-3.1-8B-Instruct 聊天服务）切入。新顺序：**Chapter 1 Inference Lifecycle → Chapter 2 LLM Inference Architecture → Chapter 3 GPU 架构基础 → Chapter 4 Performance Metrics → Chapter 5 Global Performance Model**。此前用于解决"开篇太干"问题的"先睹为快"非正式导读已退休——Chapter 1 本身现在就承担这个作用。下文所有 Chapter 编号均为最终编号。

## 适用范围与边界

本课程覆盖**纯文本、decoder-only LLM 的在线推理服务性能工程**，聚焦"系统已经训练好、要把它跑快、跑稳、跑省"这一段。以下两类内容**有意不在本课程展开**，不应理解为遗漏：

- **模型压缩训练侧内容**（量化训练、蒸馏、剪枝、NAS）—— 属于「课程03 · AI Infra 关键技术与实践」的职责范围，本课程仅在 Scalability 部分从**推理侧**触及权重量化。
- **多模态 / VLM 推理** —— 课程名即「LLM」，聚焦文本自回归生成。

---

## Part 1 Understanding LLM Inference System（理解推理系统）

> 建立统一的推理系统认知。开篇即 Chapter 1 Inference Lifecycle，用一个 Llama-3.1-8B-Instruct 聊天场景的具体请求把整个流程走一遍，Gateway / Queue / Scheduler 等词先按字面意思理解，正式定义留给 Chapter 2 和 Chapter 3。

### Chapter 1 Inference Lifecycle【2026-09-03 从 Chapter 3 移到 Chapter 1】

**回答问题：** 一个请求如何完成推理？

#### 内容

- Request 生命周期
- Queue
- Prefill
- Decode
- Response
- KV Cache 生命周期
- Streaming Response

作为全书开篇，本章不要求读者先懂 Gateway、Scheduler 等词的精确定义——跟着一个具体请求走一遍即可建立直觉，精确的组件职责边界留给 Chapter 2。

---

### Chapter 2 LLM Inference Architecture【编号不变，2026-09-03 起排在 Lifecycle 之后】

**回答问题：** LLM 推理系统长什么样？

#### 内容

- LLM 推理系统整体架构
- Client / Gateway / Scheduler / Worker
- Runtime 与 GPU
- vLLM、SGLang、TensorRT-LLM 架构对比

本章把 Chapter 1 里按字面意思使用的 Gateway、Queue、Scheduler 等词，拆解成更精确的架构分层（例如 Scheduler 细分为 Router、Admission / Queue、Engine Scheduler）。

---

### Chapter 3 GPU 架构基础【2026-09-02 新增为 Chapter 1；2026-09-03 移到 Chapter 3】

**回答问题：** GPU 硬件内部是怎么组织算力和显存的？

#### 内容

- SM（Streaming Multiprocessor）与 Warp 调度
- 显存层级：HBM / L2 Cache / Shared Memory / Register
- Tensor Core 与低精度计算单元
- Occupancy 与并行度

本章是后续所有性能分析的硬件前提：Chapter 11（Prefill 性能分析）的 Tensor Core、Chapter 15（Decode 性能分析）的 HBM Bandwidth、Chapter 7（Profiling Toolchain）里 Nsight Compute 输出的 SM Occupancy 等指标，都要求读者先具备本章的硬件认知；此前全课程从未专门教过，只在后续章节里默认读者已懂。最初设计为 Part 1 开篇（Chapter 1），但硬件规格作为全书第一印象偏干、缺代入感，2026-09-03 调整为排在 Lifecycle 和 Architecture 之后。

---

### Chapter 4 Performance Metrics

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

### Chapter 5 Global Performance Model

**回答问题：** 性能瓶颈来自哪里？

#### 内容

- `Latency = Queue + Prefill + Decode`
- Compute Bottleneck
- Memory Bottleneck
- Scheduling Bottleneck
- 指标之间的关系与 Trade-off

---

## Part 2 Performance Analysis（性能分析）

> 建立统一的性能分析方法。（本 Part 内容未改动，仅章节编号因 Part 1 新增顺延；调研确认本 Part 指标口径与 Fireworks / Baseten / Together 等平台实际对外报告的口径一致）

### Chapter 6 Benchmark Design

**回答问题：** 如何建立可信、可重复的性能 Baseline？

#### 内容

- Benchmark 原则
- Baseline 建立
- Warmup
- Repeat
- Prompt / Output / Concurrency 设计

---

### Chapter 7 Profiling Toolchain

**回答问题：** 如何采集推理系统不同层次的性能数据？

#### 内容

- Nsight Systems
- Nsight Compute
- PyTorch Profiler
- nvidia-smi
- vLLM Profiling

---

### Chapter 8 Root Cause Analysis

**回答问题：** 如何从性能现象追溯到真正瓶颈？

#### 内容

- Timeline 分析
- GPU Utilization 分析
- Memory Bandwidth 分析
- CPU Bottleneck
- Scheduler Bottleneck

---

### Chapter 9 Performance Diagnosis

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

> 回答：为什么 Prefill 慢，以及如何降低 Prefill 对 TTFT 的影响？（调研确认深度与 Stanford CS229S 相当）

### Chapter 10 Prefill 工作机制

#### 内容

- Prefill 执行流程
- Attention Pipeline
- GEMM
- KV Cache 创建

---

### Chapter 11 Prefill 性能分析

#### 内容

- Compute Bound
- Roofline
- Tensor Core
- Kernel Timeline
- Profiling

---

### Chapter 12 Prefill 优化方法【调整】

#### 内容

- FlashAttention
- FlashInfer

每项技术统一讲解：适用场景 / 原理 / Profiling 特征 / Benchmark / Trade-off。

> **【移出】** CUDA Graph / Kernel Fusion / Persistent Kernel 已移至 Chapter 16（Decode 优化方法）。理由：这三项针对的是"小 kernel 高频调用的启动开销"，Decode 逐 token 生成、每步 batch 小但 kernel 多，这一问题更突出；Prefill 是大批量计算密集型，启动开销占比小，不是主要矛盾。vLLM 官方设计文档实测 CUDA Graph 重放可消除 Decode 每步约 28% 的启动+同步开销。

---

### Chapter 13 Prefill 实战验证

#### 内容

- Prompt 长度实验
- TTFT Benchmark
- Performance Report
- Best Practice

---

## Part 4 Decode Optimization（Decode 优化）

> 回答：为什么 Decode 慢，以及如何改善 TPOT 和生成效率？（调研确认投机解码深度与 Stanford CS229S 作业相当或更系统）

### Chapter 14 Decode 工作机制

#### 内容

- Decode Flow
- Sampling
- KV Cache Read
- Token Generation

---

### Chapter 15 Decode 性能分析【调整】

#### 内容

- Memory Bound
- HBM Bandwidth
- Decode Timeline
- KV Cache Growth
- **【新增】CPU Dispatch / Kernel Launch Overhead** —— 与 Chapter 16 新增的 Kernel-Level Optimization 小节对应的根因条目；此前移动优化手段时漏了分析章节的根因条目，此处补上，保持"先分析后根因、后优化"的结构完整。

---

### Chapter 16 Decode 优化方法【调整】

#### Memory Optimization

- KV Cache
- PagedAttention
- KV Quantization
- Prefix Cache（单节点前缀复用）
- **【新增】跨副本缓存感知路由（Cache-Aware Routing）** —— 多副本场景下按前缀树命中率而非轮询调度请求（如 SGLang RadixAttention 路由），前缀密集负载下吞吐可提升约 5 倍；与单节点 Prefix Cache 互补：单节点解决"要不要算"，路由解决"该发去哪台机器算"。引用：SGLang 文档 / TrueFoundry、LearnOpenCV

#### Kernel-Level Optimization【调整：从 Chapter 12 移入】

- CUDA Graph / Kernel Fusion / Persistent Kernel

#### Generation Optimization

- Speculative Decoding
- MTP
- Medusa
- EAGLE

---

### Chapter 17 Decode 实战验证

#### 内容

- Long Context 实验
- TPOT Benchmark
- Best Practice

---

## Part 5 Serving Optimization（Serving 优化）

> 回答：为什么 GPU 没有跑满，以及如何提高调度效率和系统吞吐？

### Chapter 18 Serving 工作机制【调整】

#### 内容

- **【新增】API 层 / 客户端协议** —— OpenAI 兼容接口、请求如何从客户端协议进入 Queue（衔接 Chapter 1 的生命周期）。引用：DeepLearning.AI《Fast & Efficient LLM Inference with vLLM》(2026-06)
- Queue
- Scheduler
- Worker
- Runtime

---

### Chapter 19 Serving 性能分析

#### 内容

- Queue Delay
- GPU Idle
- Batch Efficiency
- Worker 利用率

---

### Chapter 20 Serving 优化方法【调整】

#### 内容

- Dynamic Batching
- Continuous Batching
- Chunked Prefill
- Admission Control
- **【新增】Prefill-Decode 分离（PD Disaggregation）** —— 利用 Prefill 计算密集、Decode 显存带宽密集的根本差异，将两阶段拆到独立 GPU 池，通过 KV Cache 传输衔接。已是 2026 年生产级主流架构（Meta / LinkedIn / Mistral / HuggingFace 的 vLLM 部署、NVIDIA Dynamo、AMD MORI-IO RDMA KV 连接器实测 2.5x goodput 提升）。与 Chapter 24 的 Scale-out 呼应：单机内是调度问题，跨机是资源池切分问题。引用：jarvislabs.ai blog、arXiv 2508.01989、vLLM Blog (2026-04-07)

---

### Chapter 21 Serving 实战验证

#### 内容

- TPS Benchmark
- GPU Util Benchmark
- Queue Delay 分析
- Best Practice

---

## Part 6 Scalability Optimization（规模化优化）

> 回答：如何提升并发、扩展容量并降低成本？

### Chapter 22 Scalability 工作机制

#### 内容

- Capacity Model
- Memory Pool
- Multi-GPU

---

### Chapter 23 Scalability 性能分析

#### 内容

- Fragmentation
- Capacity Profiling
- KV Pool

---

### Chapter 24 Scalability 优化方法【调整】

#### Scale-up

- Quantization
- Tensor Parallel
- Pipeline Parallel
- **Expert Parallel → MoE 推理优化专项**（原大纲仅一句带过；2026 年主流开源模型 DeepSeek V3.2 / Llama 4 Maverick / Kimi K2 均为 MoE 架构，权重提升）：
  - Expert Parallel 基本机制
  - All-to-All 通信开销分析
  - 专家负载均衡与路由倾斜（Expert Load Balancing / Routing Skew）
  - "按激活参数而非总参数"的显存与成本模型 —— 例如 DeepSeek 的推理成本随其 37B 激活参数而非 671B 总参数变化。引用：spheron.network blog、arXiv 2512.09277、IntuitionLabs

#### Scale-out

- Replica
- Load Balance
- Autoscaling
- **【新增】** 呼应 Chapter 20：PD 分离在 Scale-out 场景下体现为独立的 Prefill 资源池与 Decode 资源池，二者可分别弹性伸缩、分别选择硬件配比

---

### Chapter 25 Scalability 实战验证

#### 内容

- Capacity Benchmark
- 并发实验
- 成本分析
- Best Practice

---

## Part 7 Production Performance Engineering（生产实践）

> 回答：企业如何持续进行性能优化，而不是只完成一次性调优？

### Chapter 26 Benchmark Automation

#### 内容

- 自动化 Benchmark
- 数据采集

---

### Chapter 27 Performance Regression【调整】

#### 内容

- Regression
- CI 集成
- 自动告警
- **【新增】"静默回归"案例素材** —— JSON-mode 遵循度悄然下降、未声明的量化配置变更、流量高峰下 p99 TTFT 骤增 3 倍等真实生产失效模式，用作"为什么需要这一章"的具体例证。

---

### Chapter 28 Observability

#### 内容

- Dashboard
- Grafana
- Prometheus
- 可观测性

（调研确认：本章指标口径与调研到的所有课程相比覆盖最完整，予以保留）

---

### Chapter 29 Performance Review

#### 内容

- Performance Checklist
- Optimization Matrix
- Performance Report

---

### Chapter 30 Final Project

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

---

## 修订摘要（2026-09-02 / 2026-09-03）

| 类型 | 位置 | 内容 |
|---|---|---|
| 新增章节 | Chapter 3（原 Chapter 1） | GPU 架构基础 |
| 排序调整 | Part 1 | 2026-09-03：Inference Lifecycle（→Ch1）和 Architecture（Ch2 不变）移到 GPU 架构基础（→Ch3）之前，理由是硬件规格作为全书开篇偏干、缺代入感 |
| 退休 | Part 1 开头 | "先睹为快"非正式场景导读已退休——Chapter 1 Lifecycle 本身现在承担这个作用 |
| 新增章节内容 | 开头 | 适用范围与边界声明 |
| 新增子条目 | Chapter 16 | 跨副本缓存感知路由 |
| 移入 | Chapter 16（原 Chapter 12） | CUDA Graph / Kernel Fusion / Persistent Kernel |
| 新增子条目 | Chapter 15 | CPU Dispatch / Kernel Launch Overhead |
| 新增子条目 | Chapter 18 | API 层 / 客户端协议 |
| 新增子条目 | Chapter 20 | Prefill-Decode 分离 |
| 扩展子条目 | Chapter 24 Scale-up | Expert Parallel → MoE 推理优化专项 |
| 新增子条目 | Chapter 24 Scale-out | 呼应 PD 分离的资源池弹性伸缩 |
| 新增素材 | Chapter 27 | 静默回归真实案例 |
| 结构 | 全局 | 29 章 → 30 章，7 Part 划分不变 |

未采纳的候选项：PD 分离单独成章（按外科手术式修改处理，未独立成章）；「计算 GPU 显存」的具体估算技能是否补进 Chapter 22/25——已给出分析方案，尚未拍板，不要默认采纳。
