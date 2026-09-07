# 《LLM 推理性能工程实战》课程设计（v1.0）

> 副标题：从模型原理、性能分析到 Serving 与 Agent 优化

> **文档职责：说明为什么这样设计课程，以及整门课程采用什么统一方法。**  
> 本文档不展开 Part / Chapter 目录，也不规定每章的具体写作格式；课程内容见 `02_Course_Outline.md`，章节编写规范见 `03_Course_Template.md`。

---

## 1. 课程名称与核心理念

**课程名称：** LLM Performance Engineering：面向推理系统的性能优化实战

**核心理念：**

```text
理解推理系统 → 分析性能问题 → 优化系统 → 工程实践
```

本课程不按照 FlashAttention、PagedAttention、Speculative Decoding 等单项优化技术组织，也不单纯按照 TTFT、TPOT、TPS 等单一指标组织，而是以 **LLM 推理系统（Inference System）** 为主线。

课程希望建立的是一套可迁移的 Performance Engineering 思维：面对不同模型、推理框架和硬件环境，能够理解系统、分析瓶颈、选择优化方案，并通过实验验证真实收益，而不是孤立记忆一组优化技术。

---

## 2. 课程内容主线：推理系统生命周期

课程围绕一个推理请求在系统中的完整生命周期展开：

```text
Request
   ↓
Queue
   ↓
Prefill
   ↓
Decode
   ↓
Serving
   ↓
Scalability
```

这条主线回答的是：

> **推理系统由哪些阶段组成，性能问题发生在什么位置？**

课程各部分与系统主线的关系如下：

| 课程部分 | 主要作用 |
|---|---|
| Understanding LLM Inference System | 建立全局架构、请求生命周期、性能指标和全局性能模型 |
| Performance Analysis | 建立 Benchmark、Profiling、根因分析和诊断方法 |
| Prefill Optimization | 分析并优化 Prefill 阶段，重点关注 TTFT 与计算效率 |
| Decode Optimization | 分析并优化 Decode 阶段，重点关注 TPOT、KV Cache 与生成效率 |
| Serving Optimization | 分析并优化 Queue、Scheduler、Batch 和 Worker Runtime |
| Scalability Optimization | 分析容量、并发、多 GPU、Scale-up 与 Scale-out |
| Production Performance Engineering | 建立自动 Benchmark、性能回归、可观测性和 Performance Review |

---

## 3. 统一性能分析方法（Performance Analysis Process）

课程中的 Prefill、Decode、Serving、Scalability 等核心模块，均采用同一套性能分析方法：

```text
① 理解系统（Understand）
        ↓
② 理解瓶颈（Understand Bottleneck）
        ↓
③ 定位瓶颈（Profile & Root Cause）
        ↓
④ 优化方案（Optimize）
        ↓
⑤ 验证收益（Benchmark & Validation）
```

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

### 3.6 与原课程四步表达的关系

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

### 4.1 先系统，后技术

先建立推理系统和请求生命周期的整体认知，再进入 FlashAttention、KV Cache、Continuous Batching 等技术专题，避免技术点与系统位置脱节。

### 4.2 先分析，后优化

不从“有哪些优化技术”出发，而从“当前系统的瓶颈是什么”出发。只有完成 Benchmark、Profiling 和 Root Cause Analysis 后，才选择优化方案。

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

## 6. 两种配套练习格式：Lesson 与 Workshop

课程验证收益（第 3.5 节）这一步，落地为两种互不替代的配套材料：

- **Lesson**（历史遗留格式，见项目根目录 `../_archive/lesson/`）：单位是一整节 60-75 分钟课堂讲稿，含时间轴、讲授要点、slides 和学生材料，回答"如何把一章讲成一堂完整的课"。按旧版 8 篇大纲编号，与当前 30 章体系不再一一对应，仅作讲稿结构参考。
- **Workshop**（当前格式，见 `workshops/`）：单位是一个可复现实验，固定五步结构（环境搭建 → 加压制造瓶颈 → 优化措施 → 重跑验证 → 对比总结），针对一个具体优化技术，回答"如何让学员亲手验证一次优化收益"。按当前 30 章编号，随每章优化方法小节铺开。

两者可以组合：一节完整的课可以把某个 Workshop 实验作为动手环节。详细区分和归档说明见项目根目录的 `README.md`。

## 7. 当前尚未在源大纲中定义的内容

以下内容未在当前两份基础文档中明确规定，后续可单独补充，不在本次拆分中自行假设：

- 目标学员与前置知识
- 课程时长与授课节奏
- 统一实验硬件和软件版本
- Workshop 13 个技术点的难度分级（2026-09-03 已全部铺开草案，但预期现象都还只是定性描述，缺具体指标阈值，见 `workshops/README.md` 的"剩余待做"）
- 考核方式和结课标准
- Instructor Guide、PPT 和实验仓库的具体交付规格

## 8. v1.0 目标用户与交付目标

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
2. **可运行 Demo**：每个核心能力至少有一个可执行实验，包含环境、Baseline、压测、优化配置、重跑、指标对比和 Trade-off。

## 9. v1.0 学习路径

### 9.1 Core Track

面向后端和 Agent 工程师，主线为：

```text
第一个服务 → 推理原理 → 性能测量 → 单 GPU 优化
→ Serving → RAG / Agent → 容量与生产实践 → 综合项目
```

### 9.2 Advanced Track

面向平台和基础设施工程师，重点深入：

- Chapter 5 的 GPU 性能模型；
- Chapter 9、13、17、18 的 Profiling 和 Runtime 细节；
- Chapter 28 的 Multi-GPU Inference；
- Chapter 29 的 MoE、Expert Parallel 与 PD Disaggregation。

Advanced 内容不应成为 Core Track 的前置门槛。

## 10. v1.0 课程完成标准

课程 v1.0 只有在以下条件同时满足时才算完成：

- 30 章正文与课程大纲一致；
- RAG 性能工程和 Agent 性能工程有独立章节；
- Core Demo 可以在指定单卡环境中运行；
- Advanced Demo 明确多卡 / 多机前置条件；
- 每个核心 Demo 都有 Baseline、优化后结果和指标解释；
- Final Project 同时提供 Core 和 Advanced 两条路线；
- 课程环境、版本、作业和验收标准已文档化。
