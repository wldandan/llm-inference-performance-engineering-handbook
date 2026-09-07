# 《LLM 推理性能工程实战》v1.0 正文迁移计划

## 1. 迁移原则

新版仍保留 30 章，但不是旧目录的简单改名。迁移分为三类：

- **平移**：主题基本不变，迁移正文、插图和 Demo 后更新编号与前后依赖。
- **重写**：保留可复用材料，按新版核心问题重新组织章节。
- **合并 / 拆分**：把旧章中的内容拆到多个新章，或把多个旧章收敛成一章。

旧版正文以 Git 提交 `c4964fc` 为只读快照。后续直接在 `chapter01`–`chapter30` 原位重构，需要旧材料时从该提交读取，不在工作区复制第二套正文。

## 2. 30 章迁移矩阵

| v1.0 章节 | 主要来源 | 动作 | 说明 |
|---|---|---|---|
| Ch1 第一个 LLM 服务 | 旧 Ch1 + 旧 Ch2 Demo | 重写 | 已完成；先跑通服务，再建立请求链路直觉。 |
| Ch2 Inference Lifecycle | 旧 Ch1 | 重写 | 已完成；建立正式阶段模型、状态转换、取消与资源回收，避免重复 Ch1 操作说明。 |
| Ch3 LLM Inference Architecture | 旧 Ch2 | 平移 | 已完成；保留组件分层和成熟系统映射，统一更新图号与章节引用。 |
| Ch4 Transformer 推理机制 | Workshop 00 + 新内容 | 新建 | 补齐 Attention、Sampling、Prefill / Decode 与 KV Cache 的模型原理。 |
| Ch5 GPU 性能心智模型 | 旧 Ch3 | 重写 | Core 只保留算力、容量、带宽和 Kernel 直觉；高级 CUDA 下沉为 Advanced。 |
| Ch6 LLM 性能指标 | 旧 Ch4 | 平移 | 更新指标边界、统计口径与成本指标。 |
| Ch7 Global Performance Model | 旧 Ch5 | 平移 | 增加 Agent / RAG 端到端延迟分解。 |
| Ch8 Benchmark Design | 旧 Ch6 | 平移 | 对齐可信 Baseline 和可重复性要求。 |
| Ch9 Profiling Toolchain | 旧 Ch7 | 平移 | 分出 Core 工具链和 Advanced GPU 工具链。 |
| Ch10 Root Cause Analysis | 旧 Ch8 | 平移 | 保留“现象—证据—根因”主线。 |
| Ch11 Performance Diagnosis Lab | 旧 Ch9 | 重写 | 输出可复核诊断报告。 |
| Ch12 Prefill 工作机制 | 旧 Ch10 | 平移 | 与 Ch4 原理层、Ch13 分析层明确分工。 |
| Ch13 Prefill 性能分析 | 旧 Ch11 | 平移 | 补充长上下文与 RAG Prompt 特征。 |
| Ch14 Prefill 优化方法 | 旧 Ch12 | 平移 | 组织 FlashAttention、FlashInfer、Chunked Prefill 和上下文优化。 |
| Ch15 Prefill 实战验证 | 旧 Ch13 | 平移 | 使用相同请求集验证长 Prompt TTFT。 |
| Ch16 Decode 工作机制与 KV Cache | 旧 Ch14 + Workshop 00 | 重写 | 把 KV Cache 正式纳入 Decode 主线。 |
| Ch17 Decode 性能分析 | 旧 Ch15 | 平移 | 保留带宽、Kernel Gap 与 TPOT 分析。 |
| Ch18 Decode 优化方法 | 旧 Ch16 + 相关 Workshops | 重写 | 组合 Batching、Cache、量化和投机解码。 |
| Ch19 Decode 实战验证 | 旧 Ch17 | 平移 | 验证 TPOT、吞吐、显存与质量边界。 |
| Ch20 Serving 工作机制 | 旧 Ch18 | 平移 | 补充 Streaming、取消与失败传播。 |
| Ch21 Serving 调度与性能分析 | 旧 Ch19 | 平移 | 聚焦 Queue、Batch、Scheduler 和尾延迟。 |
| Ch22 Serving 优化方法 | 旧 Ch20 | 重写 | 增加 Admission、优先级、限流、缓存和资源池。 |
| Ch23 RAG 性能工程 | 新内容 + Prefix Cache Workshop | 新建 | 分解检索、重排、上下文、生成和缓存成本。 |
| Ch24 Agent 性能工程 | 新内容 | 新建 | 分解多步 LLM、工具调用、串并行、上下文增长和失败重试。 |
| Ch25 Serving 与 Agent 综合实战 | 旧 Ch21 + 新场景 | 重写 | 用一条 RAG / Agent 服务链路完成端到端优化闭环。 |
| Ch26 容量模型、显存与成本 | 旧 Ch22 + 旧 Ch23 | 合并 | 统一容量公式、显存水位、并发上限和单位成本。 |
| Ch27 多副本、Scale-out 与 Autoscaling | 旧 Ch24 + 旧 Ch25 | 合并 | Core 聚焦副本、负载均衡、扩缩容与 SLO。 |
| Ch28 Multi-GPU Inference | 旧 Ch23 + 旧 Ch24 | 拆分 | Advanced：TP、PP、通信证据与 Scaling Efficiency。 |
| Ch29 MoE、Expert Parallel 与 PD Disaggregation | 旧 Ch24 + 新内容 | 重写 | Advanced：All-to-All、EP、Prefill / Decode 分离和路由。 |
| Ch30 End-to-End Performance Engineering Project | 旧 Ch26–Ch30 | 合并 | 把自动化、回归、可观测、评审和 Final Project 收敛为 Core / Advanced 两条项目路线。 |

## 3. Part 迁移

| Part | 动作 |
|---|---|
| Part 1 | 已改为 7 章；按 Ch1 → Ch2 → Ch3 → Ch4 → Ch5 → Ch6 → Ch7 顺序完成。 |
| Part 2 | 把旧 Ch6–Ch9 迁移为新 Ch8–Ch11。 |
| Part 3 | 把旧 Ch10–Ch13 迁移为新 Ch12–Ch15。 |
| Part 4 | 把旧 Ch14–Ch17 迁移为新 Ch16–Ch19。 |
| Part 5 | 把旧 Ch18–Ch21 重构为 Ch20–Ch25，并新增 RAG / Agent。 |
| Part 6 | 重组旧 Scalability 内容，形成 Ch26–Ch29 的 Core / Advanced 分层。 |
| Part 7 | 将旧生产实践五章收敛进 Ch30 的项目要求和验收门禁。 |

## 4. 每章执行顺序

1. 从 v1.0 大纲确认标题、Track、核心问题和章节边界。
2. 从 `c4964fc` 读取旧正文、Review、Storyboard、插图和 Demo。
3. 先写或更新 Demo 测试，确认行为变化时测试会失败。
4. 重构正文与 Demo，统一修正章节号、路径和前后依赖。
5. 更新 Review 和 Storyboard；只有语义匹配的旧插图才迁移。
6. 运行单元测试、干运行、Markdown / SVG 校验和差异检查。
7. 一个章节或一组强关联章节一个本地提交，不推送远程。

## 5. 当前顺序

1. Ch1：已完成。
2. Ch2：已完成 Inference Lifecycle 重写。
3. Ch3：已完成 Architecture 迁移，旧 Ch3 的 GPU 插图已保留到 Chapter 5 迁移素材目录。
4. Ch4：下一步接入 Workshop 00，建立 Transformer 推理机制。
5. Ch5–Ch7：随后依次迁移 GPU、Metrics 和 Global Performance Model。

完成 Part 1 后，再批量推进可平移的 Ch8–Ch22；RAG、Agent、规模化与综合项目单独设计和验收。
