# LLM Performance Engineering 课程模板（Course Templates）

> v1.0 补充：所有章节采用分层交付。Core 内容服务后端 / Agent 工程师；Advanced 内容服务平台 / 基础设施工程师，不要求 Core 学员完成全部 Advanced 实验。

> **文档职责：规定不同类型章节应该如何开发。**

为了保证课程结构统一，同时避免所有章节机械套用同一种结构，课程采用三类章节模板：

- Template A：基础理论与分析章节
- Template B：技术专题章节或技术专题小节
- Template C：综合实践章节

## 0. v1.0 分层章节结构

每章在选择 Template A / B / C 后，还需要明确以下层级：

### Core

- 目标用户：后端工程师、Agent 工程师、AI 应用工程师
- 目标：理解原理、完成基线、定位瓶颈、运行核心 Demo
- 结果：能够将方法迁移到 RAG、Agent 或普通 LLM 服务

### Advanced

- 目标用户：平台工程师、基础设施工程师、推理引擎工程师
- 目标：深入 GPU Runtime、多 GPU、通信、分布式缓存和容量规划
- 结果：能够设计和分析大规模推理基础设施

### 每章必备的交付字段

1. Core 学习目标；
2. Advanced 深入方向（如适用）；
3. Core Demo 或实验；
4. 运行环境与版本；
5. Baseline、指标和预期现象；
6. 优化后结果与 Trade-off；
7. Core / Advanced 学习检查清单。

课程统一性能分析方法见 `01_Course_Design.md`；具体 Part / Chapter 以 `02_Course_Outline_v1.0.md` 为准。

---

## 1. 模板选择原则

### 1.1 Template A 用于建立概念和分析能力

适用于架构、生命周期、指标、性能模型、Benchmark、Profiling、工作机制和性能分析等章节。

### 1.2 Template B 用于展开单项优化技术

适用于 FlashAttention、KV Cache、Continuous Batching、Speculative Decoding 等技术专题。

当 Outline 中一个“优化方法”章节包含多项技术时，Template B 应用于**章内每个技术专题小节**，而不是要求整章只套用一次。

### 1.3 Template C 用于完整调优闭环

适用于 Prefill、Decode、Serving、Scalability 的实战验证，以及 Final Project。

### 1.4 不要求所有栏目等长

模板规定的是必须回答的问题，不是固定页数。章节可根据难度调整篇幅，但不能省略影响理解和验证的关键环节。

---

## 2. Template A：基础理论与分析章节（Foundation / Analysis Chapter）

### 2.1 适用章节

典型适用范围：

- LLM Inference Architecture
- Inference Lifecycle
- Performance Metrics
- Global Performance Model
- Benchmark Design
- Profiling Toolchain
- Root Cause Analysis
- Performance Diagnosis
- Prefill / Decode / Serving / Scalability 的工作机制与性能分析章节
- Benchmark Automation
- Performance Regression
- Observability
- Performance Review

### 2.2 模板结构

#### 1. 学习目标（Learning Objectives）

回答：

> 本章结束后，学员能够做什么？

学习目标应使用可验证的能力描述，例如“能够解释”“能够比较”“能够设计”“能够识别”，避免只写“了解”。

#### 2. 核心问题（Key Questions）

回答：

> 本章重点解决哪些问题？

建议控制在 3～5 个问题，并与本章 Demo、练习或总结对应。

#### 3. 核心内容（Core Concepts）

根据章节性质组织：

- 理论与核心概念
- 系统架构或工作机制
- 方法与分析流程
- 关键指标、数据结构或工具
- 与前后章节的关系

#### 4. Demo / 实验

教师演示或简单实验，至少明确：

- 实验目的
- 环境与输入
- 操作步骤
- 观察指标
- 预期现象

#### 5. 本章总结（Summary）

至少输出：

- 三个关键结论
- 一份 Checklist 或分析要点
- 与下一章的衔接

### 2.3 完成标准

Template A 章节完成时，应保证学员能够：

- 建立清晰概念或方法框架
- 解释本章内容在推理系统中的位置
- 通过一个 Demo 或示例观察关键现象
- 使用总结或 Checklist 复述核心结论

---

## 3. Template B：技术专题章节（Technology Chapter / Section）

### 3.1 适用技术

典型适用范围：

- FlashAttention
- FlashInfer
- CUDA Graph
- Kernel Fusion
- Persistent Kernel
- KV Cache
- PagedAttention
- KV Quantization
- Prefix Cache
- Dynamic Batching
- Continuous Batching
- Chunked Prefill
- Admission Control
- Speculative Decoding
- MTP
- Medusa
- EAGLE
- Quantization
- Tensor Parallel
- Pipeline Parallel
- Expert Parallel
- Replica
- Load Balance
- Autoscaling

### 3.2 模板结构

#### 1. 为什么需要（Problem）

- 它解决什么性能问题？
- 在什么工作负载或系统条件下出现该问题？
- 为什么已有机制不足？

#### 2. 工作机制（How it Works）

- 执行流程
- 数据流
- 生命周期
- 对原有执行路径做了什么改变

#### 3. 性能模型（Performance Model）

- 为什么该技术可能有效？
- 改善哪些指标？
- 影响 Compute、Memory、Scheduling 或 Capacity 中的哪些资源？
- 收益依赖哪些条件？

#### 4. Profiling 与瓶颈分析

- 如何识别适用场景？
- 优化前有哪些 Profiling 特征？
- 哪些数据可以证明 Root Cause？
- 如何排除其他瓶颈？

#### 5. 优化实现（Optimization）

- 实现方式
- 参数配置
- 推理框架支持
- 启用、关闭或切换方式
- 与其他优化技术的组合关系

#### 6. Benchmark

- Baseline
- Workload 配置
- 优化后结果
- 核心指标对比
- 收益分析和可重复性

#### 7. Trade-off

- 优势
- 局限
- 副作用
- 对其他指标的影响
- 不适用场景

#### 8. Best Practice

- 推荐配置
- 适用场景
- 工程经验
- 上线前检查项

### 3.3 完成标准

Template B 技术专题完成时，应回答：

1. 为什么需要这项技术？
2. 它改变了哪一段执行机制？
3. 如何用 Profiling 判断是否适用？
4. Benchmark 是否证明了收益？
5. 收益的边界和 Trade-off 是什么？

---

## 4. Template C：综合实践章节（Case Study Chapter）

### 4.1 适用章节

- Prefill 实战验证
- Decode 实战验证
- Serving 实战验证
- Scalability 实战验证
- Final Project

### 4.2 模板结构

#### 1. 实验目标

定义本次调优要解决的问题，以及目标指标和约束条件。

#### 2. Baseline

记录初始配置和指标：

- TTFT
- TPOT
- TPS
- GPU Utilization
- GPU Memory
- Concurrency / Cost（根据场景选用）

#### 3. Profiling

采集性能数据：

- Timeline
- GPU
- Memory
- Kernel
- Queue / Scheduler / Worker（根据场景选用）

#### 4. Root Cause

- 区分症状与根因
- 列出证据
- 排除非主要瓶颈
- 形成明确诊断结论

#### 5. Optimization Plan

制定优化方案：

- 优化目标
- 候选技术
- 实施顺序
- 预期收益
- 风险与 Trade-off

#### 6. 实施优化

逐步完成优化，每次只改变可控变量，并记录配置变化。

#### 7. Benchmark Verification

- 使用与 Baseline 一致的 Workload
- 对比核心指标
- 检查 P50 / P95 / P99 和稳定性
- 检查是否出现性能转移或副作用

#### 8. Performance Report

形成完整调优报告，至少包括：

- 问题描述
- 实验环境
- Baseline
- Profiling 证据
- Root Cause
- 优化方案
- Benchmark 结果
- Trade-off 与结论

#### 9. Lessons Learned

- 哪些假设被验证或否定？
- 哪些优化有效，哪些无效？
- 结论能否迁移到其他模型、框架或负载？
- 后续还应进行哪些实验？

### 4.3 完成标准

Template C 章节必须形成完整闭环：

```text
Baseline
    ↓
Profiling
    ↓
Root Cause
    ↓
Optimization Plan
    ↓
Implementation
    ↓
Benchmark Verification
    ↓
Performance Report
```

---

## 5. 三类模板与课程大纲的对应关系

| 课程章节 | 推荐模板 |
|---|---|
| Chapter 1～10 | Template A |
| Chapter 11 中的各项 Prefill 技术专题 | Template B |
| Chapter 12 | Template C |
| Chapter 13～14 | Template A |
| Chapter 15 中的各项 Decode 技术专题 | Template B |
| Chapter 16 | Template C |
| Chapter 17～18 | Template A |
| Chapter 19 中的各项 Serving 技术专题 | Template B |
| Chapter 20 | Template C |
| Chapter 21～22 | Template A |
| Chapter 23 中的各项 Scalability 技术专题 | Template B |
| Chapter 24 | Template C |
| Chapter 25～28 | Template A |
| Chapter 29 | Template C |

---

## 6. 课程开发原则

- **课程结构：** 按推理系统组织，即 Request → Queue → Prefill → Decode → Serving → Scalability。
- **统一方法：** 各模块遵循“理解系统 → 理解瓶颈 → 定位瓶颈 → 优化方案 → 验证收益”。
- **模板选择：** 根据章节性质选择 Template A / B / C，不机械套用单一模板。
- **教学目标：** 建立 Performance Engineering 思维，而不是孤立学习优化技术。
- **实验要求：** 技术收益必须有 Baseline、Profiling 和 Benchmark 支撑。
- **工程要求：** 必须说明适用场景、限制条件和 Trade-off。
