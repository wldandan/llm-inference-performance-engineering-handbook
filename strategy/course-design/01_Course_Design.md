# 《LLM 推理性能工程实战》课程设计（V0.2）

> 副标题：从模型原理、性能分析到 Serving 与 Agent 优化

> **文档职责：说明为什么这样设计课程，以及整门课程采用什么统一方法。**  
> 本文档不展开 Part / Chapter 目录，也不规定每章的具体写作格式；权威课程内容见 `02_Course_Outline_v0.2.md`，章节编写规范见 `03_Course_Template.md`。

---

## 1. 课程名称与核心理念

**课程名称：** LLM Performance Engineering：面向推理系统的性能优化实战

**核心理念：**

```text
理解推理系统 → 分析性能问题 → 优化系统 → 工程实践
```

本课程不按照 FlashAttention、PagedAttention、Speculative Decoding 等单项优化技术组织，也不单纯按照 TTFT、TPOT、TPS 等单一指标组织，而是以 **LLM 推理系统（Inference System）** 为主线。

课程希望建立的是一套可迁移的 Performance Engineering 思维：面对不同模型、推理框架和硬件环境，能够理解系统、分析瓶颈、选择优化方案，并通过实验验证真实收益，而不是孤立记忆一组优化技术。

V0.2 不追求覆盖完整 AI 基础设施栈，而是聚焦现有主线：模型推理原理、请求生命周期、性能测量与诊断、Prefill/Decode/Serving 优化，以及 RAG/Agent 的端到端性能。参考书中的客户端、部署和生产实践只在直接影响这条主线时进入课程。

---

## 2. 课程内容主线：三个正交视图

课程不再把 Request、Prefill、Serving 和 Scalability 串成一条伪生命周期，而是使用三个互补视图。

### 2.1 单请求路径

```text
Client
  → Gateway / API
  → Admission / Queue / Scheduler
  → Prefill
  → Decode
  → Streaming Response
  → Finish / Cancel / Fail / Resource Reclaim
```

单请求路径回答一次调用的时间花在哪里，用于解释 TTFT、TPOT、端到端延迟、取消和资源回收。

### 2.2 应用关键路径

```text
Chat:  Prompt → LLM → Response
RAG:   Query → Retrieve → Rerank → Context → LLM → Response
Agent: Plan → LLM → Tool(s) → LLM → ... → Result
```

应用关键路径回答哪些依赖真正决定用户等待时间，用于解释 RAG / Agent 的串并行、上下文增长和重试放大。

### 2.3 系统扩展路径

```text
Single Instance
  → Replica Pool
  → Routing / Load Balance
  → Autoscaling
  → Multi-GPU / Multi-Node（Advanced）
```

系统扩展路径回答容量如何扩展，用于解释 SLO、Goodput、单位 Token 成本和分布式通信。Serving 是承载 Queue、Prefill 和 Decode 的系统，不是 Decode 之后的阶段。

课程各部分与三个视图的关系如下：

| 课程部分 | 主要作用 |
|---|---|
| 从一个请求理解推理系统 | 建立真实请求、模型执行、Serving 架构和指标视图 |
| 测量、观测与根因分析 | 建立 Workload、Benchmark、Observability、Profiling 和 Root Cause 证据链 |
| Prefill 与上下文优化 | 优化首 Token 之前的输入与上下文处理 |
| Decode、KV Cache 与生成优化 | 优化逐 Token 生成、缓存容量和显存访问 |
| Serving、RAG 与 Agent 性能工程 | 优化多请求调度与应用 Critical Path |
| 容量、成本与生产工程 | 建立 Scale-out、回归门禁和上线评审 |
| 综合项目 | 交付可运行、可观测、可优化的系统 |

---

## 3. 统一性能工程方法（Performance Engineering Process）

课程中的 Prefill、Decode、Serving、RAG、Agent 和容量模块，均采用同一套方法。五步分析法保留为核心，但在开始前增加 Workload / SLO，在结束后增加 Regression Guard：

```text
Workload & SLO
  → ① 理解系统
  → ② 理解瓶颈
  → ③ 定位瓶颈
  → ④ 优化方案
  → ⑤ 同流量验证
  → Regression Guard
```

### 3.0 定义 Workload 与 SLO

先描述请求类型、输入/输出长度分布、到达模式、并发、RAG 文档规模、Agent 步数和质量要求，再选择指标。没有工作负载定义的性能数字不能作为优化结论。

课程以 **SLO-aware Goodput** 作为综合收口：只有在延迟、质量和可靠性约束内完成的请求，才计入有效吞吐；原始 TPS 或 GPU 利用率不能单独代表系统优化成功。

### 3.1 理解系统（Understand）

回答：

> **这个模块是怎么工作的？**

主要关注：

- 模块在推理系统中的位置
- 输入、输出和执行流程
- 关键组件与数据结构
- 生命周期及其与其他模块的关系

例如，分析 Prefill 时，先理解 Prompt 如何经过 Attention、GEMM 并创建 KV Cache；分析 Serving 时，先理解 Queue、Scheduler、Batch Formation 和 Worker 的关系。

### 3.2 理解瓶颈（Understand Bottleneck）

回答：

> **为什么这里可能会慢？**

主要关注：

- Compute、Memory、Scheduling 等资源约束
- 工作负载特征对性能的影响
- TTFT、TPOT、TPS、GPU Utilization、Memory、Concurrency 等指标之间的因果关系
- 优化一个指标时可能引入的 Trade-off

### 3.3 定位瓶颈（Profile & Root Cause）

回答：

> **如何证明瓶颈确实发生在这里？**

主要关注：

- Benchmark Baseline
- Timeline 与 Kernel 分析
- GPU Utilization 与 Memory Bandwidth
- CPU、Scheduler、Queue 与 Worker 状态
- 从表面指标追溯到 Root Cause

### 3.4 优化方案（Optimize）

回答：

> **针对已经确认的根因，应该选择什么优化手段？**

优化技术必须与瓶颈建立明确对应关系。例如：

- Attention 数据访问效率问题 → FlashAttention
- Kernel Launch 开销问题 → CUDA Graph / Kernel Fusion
- KV Cache 管理与碎片问题 → PagedAttention
- 逐 Token 串行生成问题 → Speculative Decoding / MTP
- GPU 空闲与 Batch 形成效率问题 → Continuous Batching / Scheduler Optimization

### 3.5 验证收益（Benchmark & Validation）

回答：

> **优化是否真的有效，收益在什么条件下成立？**

验证必须包括：

- 与 Baseline 的可重复对比
- 对核心指标和尾延迟的分析
- 对显存、并发、吞吐和成本的综合评估
- Trade-off、适用场景和限制条件
- 最终 Performance Report 或 Best Practice

### 3.6 建立 Regression Guard

优化通过后，把请求集、环境、指标口径和允许波动固化到自动 Benchmark 与发布门禁中，防止性能收益在模型、框架或配置升级后静默消失。

### 3.7 与原课程四步表达的关系

原课程中的四步表达：

```text
工作机制 → 性能分析 → 优化方法 → 实验验证
```

在本设计文档中被进一步拆分为五步：

| 原表达 | 五步方法 |
|---|---|
| 工作机制 | 理解系统 |
| 性能分析 | 理解瓶颈 + 定位瓶颈 |
| 优化方法 | 优化方案 |
| 实验验证 | 验证收益 |

五步方法没有改变原有课程逻辑，只是把“为什么慢”和“如何证明”明确区分开，便于课程开发和学员理解。

---

## 4. 课程组织原则

### 4.1 真实执行先于抽象模型

读者先运行真实服务并看到请求、Token 和服务端证据，再引入生命周期、架构与性能模型。模拟事件只用于单元测试和边界练习，不能冒充 GPU 实测。

### 4.2 先分析，后优化

不从“有哪些优化技术”出发，而从“当前系统的瓶颈是什么”出发。只有完成 Benchmark、Profiling 和 Root Cause Analysis 后，才选择优化方案，并优先采用配置调整、请求整形、缓存和调度等**最小侵入**手段，再考虑 Kernel 或分布式改造。

### 4.3 指标相互耦合，必须讨论 Trade-off

TTFT、TPOT、TPS、Concurrency、GPU Utilization、Memory 和 Cost 并非相互独立。课程不把某项技术简单归属到单一指标，而是分析它对多个指标的共同影响及副作用。

### 4.4 所有优化必须验证

每项优化都要通过可重复 Benchmark 进行验证，不能仅凭原理或单次运行结果判断收益。

### 4.5 理论、工具与工程实践闭环

课程同时覆盖：

- 工作机制与性能原理
- Benchmark 与 Profiling 工具
- 优化实现与参数配置
- Case Study、Performance Report 和 Best Practice

### 4.6 不强制所有章节使用同一结构

不同章节根据性质选择基础理论、技术专题或综合实践模板，既保证一致性，又避免内容重复。具体模板见 `03_Course_Template.md`。

### 4.7 工作负载先于 Benchmark

Chat、RAG 和 Agent 的延迟组成不同。课程先定义 Workload 和 SLO，再建立 Benchmark。测试数据应具备**生产代表性**，覆盖真实的输入/输出长度、到达模式、请求参数和内容类别，避免用单一固定 Prompt 代表生产流量。

### 4.8 先使用轻量证据，再下钻 GPU

Core Track 优先使用 API 时间点、vLLM 指标、日志、Trace 和系统资源指标。只有这些证据指向 GPU 执行问题时，才进入 Nsight、Roofline 或 Kernel 分析。

### 4.9 生产工程不能只存在于 Final Project

自动 Benchmark、性能回归、发布门禁、Dashboard 和 Performance Review 是 Core 能力，必须在最终项目之前单独讲清楚。

---

## 5. 三个核心文档的职责边界

| 文档 | 核心问题 | 主要内容 |
|---|---|---|
| `01_Course_Design.md` | 为什么这样设计？ | 课程理念、系统主线、统一性能分析方法、设计原则 |
| `02_Course_Outline.md` | 课程讲什么？ | Part、Chapter、每章问题和核心内容 |
| `03_Course_Template.md` | 每章怎么写？ | Template A / B / C、适用范围和完成标准 |

三份文档共同构成课程开发的基础规范：

```text
Course Design（Why）
        ↓
Course Outline（What）
        ↓
Course Template（How）
```

---

## 6. Demo、Workshop 与 Lesson

正式性能验收集中在 8 个递进实验，而不是要求 30 章各自制造一个互不相关的性能脚本：

1. 运行真实 vLLM 服务；
2. 追踪真实请求生命周期；
3. 建立 Workload、Benchmark 与请求级可观测性；
4. 完成 Prefill 与长上下文优化；
5. 完成 Decode、KV Cache 与量化优化；
6. 完成 Scheduler、Batching 与流量治理实验；
7. 完成 RAG / Agent 关键路径优化；
8. 完成容量、回归门禁和端到端项目。

三类教学资产职责不同：

- **Lesson**（历史遗留格式，见项目根目录 `../_archive/lesson/`）：单位是一整节 60-75 分钟课堂讲稿，含时间轴、讲授要点、slides 和学生材料，回答"如何把一章讲成一堂完整的课"。按旧版 8 篇大纲编号，与当前 30 章体系不再一一对应，仅作讲稿结构参考。
- **Demo**（当前格式，见项目根目录 `code/`）：章节级小程序或递进实验入口，回答“本章的机制或证据如何运行出来”。
- **Workshop**（当前格式，见 `workshops/`）：一个可复现的优化闭环，固定为 Workload → Baseline → Evidence → Optimization → Same-workload Verification → Trade-off。

三者可以组合：一节课可以引用章节 Demo，并把一个 Workshop 作为动手环节。

## 7. 技术内容归位

- Prefix Cache、上下文裁剪和 Chunked Prefill 归入 Prefill / 上下文路径。
- PagedAttention、KV Quantization 和容量估算归入 KV Cache / 内存路径。
- Dynamic / Continuous Batching 归入 Serving Scheduler。
- Weight Quantization 独立讨论性能、容量和质量边界。
- Multi-GPU、NCCL、MoE、Expert Parallel 和 PD Disaggregation 作为 Advanced 内容，不成为 Core 前置条件。

## 8. V0.2 目标用户与交付目标

### 8.1 目标用户

核心用户是后端工程师、Agent 工程师、AI 应用工程师和 MLOps / 平台工程师。课程不要求学员具备 CUDA 编程、GPU 微架构或分布式训练背景。

### 8.2 课程目标

课程结束后，核心用户应能够：

- 启动并调用一个 LLM 服务；
- 解释 Transformer 推理、Prefill、Decode 和 KV Cache；
- 设计可重复的性能 Benchmark；
- 使用指标和 Profiling 定位 Queue、Compute、Memory 或 Scheduling 瓶颈；
- 完成常见的单 GPU 推理优化；
- 分析 RAG / Agent 工作负载对延迟、吞吐和成本的影响；
- 为 LLM 服务加入限流、超时、缓存、观测和回归检查；
- 输出一份可复核的性能报告。

平台工程师和基础设施工程师可在 Advanced Track 中进一步学习 GPU Runtime、多 GPU、NCCL、MoE、Expert Parallel 和 PD Disaggregation。

### 8.3 两类交付物

课程必须同时交付：

1. **文字版教程**：用统一的“概念 → 系统位置 → 性能问题 → 分析方法 → 优化方法 → 验证结果”结构解释 30 章内容。
2. **可运行 Demo**：围绕同一个服务递进建设，每个核心能力至少有一个可执行实验，包含环境、Workload、Baseline、证据、优化配置、同流量重跑、指标对比和 Trade-off。

## 9. V0.2 学习路径

### 9.1 Core Track

面向后端和 Agent 工程师，主线为：

```text
第一个服务 → 推理原理 → 性能测量 → 单 GPU 优化
→ Serving → RAG / Agent → 容量与生产实践 → 综合项目
```

### 9.2 Advanced Track

面向平台和基础设施工程师，重点深入：

- Appendix A 的 GPU Architecture 与 Roofline；
- Appendix B 的 CUDA 与高级 Kernel Profiling；
- Appendix C 的 Multi-GPU 与 NCCL；
- Appendix D 的 MoE 与 Expert Parallel；
- Appendix E 的 PD Disaggregation 与 KV Transfer。

Advanced 内容不应成为 Core Track 的前置门槛。

## 10. V0.2 课程完成标准

课程 V0.2 只有在以下条件同时满足时才算完成：

- 30 章正文、Part 导读、Demo 索引和迁移矩阵使用同一版本编号；
- Ch1 跑通真实服务，Ch2 获取真实 vLLM 生命周期证据；
- Workload Modeling、Benchmark、Observability 和 Root Cause 形成完整证据链；
- RAG 性能工程和 Agent 性能工程有独立章节；
- Core Demo 可以在指定单卡环境中运行；
- Advanced Demo 明确多卡 / 多机前置条件；
- 每个核心 Demo 都有 Workload、Baseline、优化后结果和指标解释；
- 自动 Benchmark、性能回归和 Performance Review 已进入 Core 主线；
- Final Project 同时提供 Core 和 Advanced 两条路线；
- 课程环境、版本、作业和验收标准已文档化。
