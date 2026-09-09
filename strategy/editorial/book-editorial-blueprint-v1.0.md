# 《LLM 推理性能工程实战》图书主编蓝图（v1.0）

> 状态：试点提案，待作者确认后升格为全书编辑基线  
> 盘点日期：2026-09-08  
> 适用对象：正文、Demo、Workshop、插图、练习与最终项目  
> 证据原则：文件存在不等于内容已迁移；合成实验通过不等于真实性能收益已验证。

## 1. 图书简报

### 1.1 图书身份

- **建议正式中文名**：《LLM 推理性能工程实战》。
- **建议英文名**：*LLM Performance Engineering*。
- **建议副标题**：从模型原理、性能分析到 Serving 与 Agent 优化。
- **一句话定位**：面向已经训练好的纯文本 decoder-only LLM 在线服务，用一条可迁移的性能工程主线，带读者完成“运行、测量、定位、优化、验证、工程化”的闭环。
- **产品形态**：可独立阅读的技术实践书，同时配套可运行 Demo、跨章 Workshop 和可复核证据包；旧 Lesson 仅作为授课节奏参考，不作为现行目录基线。

### 1.2 目标读者

| 层级 | 核心读者 | 主要诉求 | 阅读结果 |
|---|---|---|---|
| Core | 后端工程师、Agent 工程师、AI 应用工程师 | 把 LLM 服务跑起来、测清楚、定位慢在哪里，并完成单 GPU 与应用链路优化 | 能交付一份可复核的性能报告和一个可运行的 Core 项目 |
| Bridge | MLOps、平台工程师 | 把应用指标与 GPU、Serving、容量和成本连接起来 | 能设计容量、SLO、回归与观测方案 |
| Advanced | 基础设施工程师、推理引擎工程师 | 深入 GPU Runtime、多 GPU、通信、MoE、EP 与 PD Disaggregation | 能分析大规模推理基础设施及其证据边界 |

MLOps / 平台工程师被定义为 **Bridge 读者**：Core 方法必修，分布式与 Runtime 深度按职责选修。这样可以消除“既是核心用户、又只属于 Advanced”的现有口径冲突。

### 1.3 阅读前置条件

**Core 阅读所需：**

- 能阅读基础 Python、JSON 和命令行输出；
- 理解 HTTP 请求、客户端/服务端和基本并发概念；
- 能阅读折线图、分位数和简单统计结果；
- 不要求预先掌握 CUDA、GPU 微架构、分布式训练或 Transformer 数学推导。

**动手实验所需：**

- Level 1：CPU / 无 GPU，用于机制、输入校验和数据分析；
- Level 2：项目指定的单 GPU 环境，用于 Core 性能实验；具体硬件、驱动、框架版本仍是发布阻断项；
- Level 3：多 GPU / 多机环境，用于 Advanced 实验，不得成为 Core Track 的前置条件。

### 1.4 范围与非目标

**覆盖：**在线文本 LLM 推理、请求生命周期、Transformer 推理、GPU 性能直觉、Benchmark、Profiling、Prefill、Decode、Serving、RAG / Agent 性能路径、容量、分布式推理和综合工程项目。

**不覆盖：**训练侧量化、蒸馏、剪枝、NAS，多模态 / VLM 推理，以及 RAG 检索算法或 Agent 产品设计本身。RAG 与 Agent 章节只讨论它们如何改变推理链路的延迟、吞吐、稳定性、质量与成本。

### 1.5 全书双主线

```text
系统生命周期：Request → Queue → Prefill → Decode → Serving → Scalability

性能方法：理解系统 → 理解瓶颈 → 定位瓶颈 → 选择优化 → 验证收益
```

前两 Part 建立系统地图和证据方法；Part 3～6 把同一方法应用到不同瓶颈域；Part 7 用综合项目收束。章节不得绕过“定位瓶颈”直接给优化配方。

### 1.6 读完后的最终成果

读者应能提交一套可复核的性能工程证据包，至少包括：

1. 一个可启动并可流式调用的 LLM 服务；
2. 一份固定输入、Warmup、重复次数和指标口径的 Benchmark 配置；
3. 原始 JSON / CSV / Trace 与环境指纹；
4. 一份区分现象、证据和根因的诊断报告；
5. 一次单变量优化及同负载复测；
6. 一份包含 P50 / P95 / P99、吞吐、显存、质量或成本中适用指标的对比报告；
7. 一个 Core 或 Advanced Final Project，以及收益边界和未验证项说明。

## 2. 权威来源与版本规则

### 2.1 当前权威顺序

1. `strategy/course-design/02_Course_Outline_v1.0.md`：唯一章号、标题、Track 和核心问题来源；
2. `strategy/course-design/01_Course_Design.md`：定位、系统主线和统一五步方法；
3. `strategy/course-design/03_Course_Template.md`：A / B / C 章节合同和 Core / Advanced 分层；
4. 本蓝图：把前三者转成图书级阅读结果、章节边界、验收证据和编辑任务；
5. `strategy/course-design/04_Content_Migration_Plan_v1.0.md`：旧稿迁移来源与动作；
6. `strategy/editorial/gap-register.md`：缺口事实，不作为目录来源。

`strategy/course-design/02_Course_Outline.md` 已自称历史大纲，只能用于追溯，不得继续驱动章号。外部书籍、专栏和旧 Lesson 只能提供研究线索与教学形式参考，不得覆盖现行目录，也不得复制受版权保护的表述或图片。

### 2.2 版本与状态

每章使用同一状态机：

```text
Planned → Drafted → Editorial Reviewed → Technically Reviewed
        → Demo Verified → Evidence Verified → Release Ready
```

- `Drafted` 只表示正文存在。
- `Demo Verified` 只表示代码在声明环境下通过，不代表性能收益成立。
- `Evidence Verified` 要求 Baseline、相同 Workload 复测、原始产物和统计摘要齐全。
- `Release Ready` 还要求章号、术语、链接、插图、版权和前后依赖一致。

### 2.3 技术时效规则

框架命令、参数、架构图和性能结论必须绑定版本与复核日期。发布前只从官方文档或一手论文核对；无法锁定版本的内容改写为机制层描述或标记“待验证”，不能把旧命令包装成通用事实。

## 3. 建议目录与逐章验收标准

模板建议：`A` 为概念/分析章，`B` 为技术专题章或小节，`C` 为完整实践闭环，`A+B` 为领域方法章加技术专题，`A-light` 为入门操作章。下表是 v1.0 目录的主编合同；每章都必须同时回答“读完后理解什么、读完后做到什么、用什么验收、不得越界到哪里”。

| 章节 | 标题 / 模板 | 读完后理解什么 | 读完后做到什么 | 验收证据 | 不得越界 |
|---|---|---|---|---|---|
| Ch1 | 第一个 LLM 服务 / A-light | 一次调用的最小链路和客户端可观察事件 | 启动、流式调用并保存脱敏运行报告 | 可重复启动说明、成功请求、完整流结束、环境记录 | 不讲完整生命周期、架构职责或性能调优 |
| Ch2 | Inference Lifecycle / A | Request、Queue、Prefill、Decode、Response 与资源回收 | 从事件记录还原请求状态与阶段边界 | 生命周期报告、取消/失败案例、状态转换检查 | 不展开组件架构、指标公式或优化技术 |
| Ch3 | LLM Inference Architecture / A | Client、Gateway、Scheduler、Worker、Runtime、GPU 的职责和连接 | 为一个服务画出组件边界与请求/响应路径 | 架构契约或可检查架构图 | 不深入 Transformer、GPU 微架构或性能结论 |
| Ch4 | Transformer 推理机制 / A | Attention、Sampling、Prefill、Decode、KV Cache 如何协作 | 用最小演示解释张量形状、缓存增长和 token 生成 | Level 1 机制测试；Level 2 真实模型观察可选 | 不做 Kernel Profiling 或优化收益比较 |
| Ch5 | GPU 性能心智模型 / A | Compute、容量、带宽、Kernel Launch 四类约束 | 根据模型与负载形成资源约束假设 | 容量/带宽计算练习和带单位结果 | 不要求 Core 读者写 CUDA 或完成 Nsight 深挖 |
| Ch6 | LLM 性能指标 / A | TTFT、TPOT/ITL、TPS、RPS、Goodput、分位数与成本的测量边界 | 生成口径一致的指标报告并识别不可比数据 | 指标 Schema、时间线测试、样例报告 | 不据单一指标判断根因或推荐优化 |
| Ch7 | Global Performance Model / A | Queue、Prefill、Decode 与应用阶段如何组成 Critical Path | 把 LLM、RAG、Agent 场景分解为可验证瓶颈假设 | 阶段 DAG、Critical Path 报告、待采证据清单 | 不把模型估算写成 Root Cause 或真实性能收益 |
| Ch8 | Benchmark Design / A | Baseline、Warmup、Repeat、Workload 与可重复性的关系 | 写出可复跑的 Benchmark 合同 | 固定请求集、manifest、重复运行和统计摘要 | 不教授 Profiling 工具或提前诊断根因 |
| Ch9 | Profiling Toolchain / A | 不同层级工具各能回答什么、不能回答什么 | 选择并采集一组与问题匹配的 Trace / Profile | 采集步骤、版本、原始文件和最小解读 | 不把工具截图直接当作根因 |
| Ch10 | Root Cause Analysis / A | 症状、证据、根因与排除项之间的因果关系 | 从给定证据包形成可反驳的根因判断 | “现象→证据→根因→排除项”报告 | 不进入综合调优实现 |
| Ch11 | Performance Diagnosis Lab / C-lite | 一次现场诊断如何串联 Benchmark、Profile 与 Root Cause | 独立完成诊断流程并提交报告 | 可自动检查的诊断 Schema 和证据包 | 只诊断，不要求完成后续模块优化闭环 |
| Ch12 | Prefill 工作机制 / A | Prompt 如何经过 Attention / GEMM 并创建 KV Cache | 解释长度、形状和执行路径如何变化 | Prompt / KV 形状演示 | 不讨论 FlashAttention 收益或系统调度优化 |
| Ch13 | Prefill 性能分析 / A | 为什么 Prefill 可能 Compute Bound，以及 Roofline / Tensor Core 证据 | 用 TTFT、Timeline 和资源指标判断主要约束 | 长短 Prompt 基线与 Profile | 不启用优化后直接宣布结论 |
| Ch14 | Prefill 优化方法 / B | FlashAttention、FlashInfer 与上下文优化改变哪段路径、何时有效 | 为已证实的 Prefill 根因选择并配置候选技术 | 每项技术的版本、配置、适用证据和 Trade-off | 不混入完整综合实验或 Decode 优化 |
| Ch15 | Prefill 实战验证 / C | 如何把长 Prompt 问题形成可复核调优闭环 | 在同一 Workload 下完成 Baseline、优化和 TTFT 复测 | 原始结果、统计比较、报告与失败实验 | 不把单一模型/硬件结果外推为通用规律 |
| Ch16 | Decode 工作机制与 KV Cache / A | 逐 token 生成、Sampling、KV 读取与增长 | 估算并观察上下文增长对 KV 和生成路径的影响 | KV 增长报告和机制测试 | 不讨论优化组合的收益 |
| Ch17 | Decode 性能分析 / A | HBM、Kernel Gap、CPU Dispatch 与 TPOT 的关系 | 用 Profile 区分带宽受限、启动受限和其他原因 | TPOT 基线、Timeline、HBM / Gap 证据 | 不先验指定 Cache、量化或投机解码 |
| Ch18 | Decode 优化方法 / B | Batching、Cache、KV 量化、Kernel 优化和投机解码的机制与边界 | 为不同 Decode 根因构造候选优化矩阵 | 各专题最小 Demo、质量护栏、接受率/命中率等适用指标 | 不把多技术叠加结果归因于单项技术 |
| Ch19 | Decode 实战验证 / C | TPOT、吞吐、显存与质量之间如何权衡 | 完成单变量和组合优化的可重复复测 | 同负载对比、质量检查、原始证据和报告 | 不省略质量与稳定性副作用 |
| Ch20 | Serving 工作机制 / A | API、Queue、Scheduler、Worker、Streaming、取消和失败传播 | 追踪一个请求跨组件的状态与资源生命周期 | 可运行最小服务或事件模拟 | 不提前给调度优化配方 |
| Ch21 | Serving 调度与性能分析 / A | Queue Delay、Batch Efficiency、GPU Idle 和 P99 的因果关系 | 用负载变化与调度证据定位服务瓶颈 | 并发阶梯实验、队列/批次/尾延迟报告 | 不把 GPU Utilization 低直接等同于 GPU 不够快 |
| Ch22 | Serving 优化方法 / B | 限流、准入、优先级、缓存、批处理和资源池改变什么 | 根据 SLO 和瓶颈选择并配置服务策略 | 策略前后同负载对比、失败与降级行为 | 不扩展到 RAG/Agent 业务算法或多机底层通信 |
| Ch23 | RAG 性能工程 / A+B | 检索、重排、上下文和生成如何构成延迟/成本路径 | 建立 RAG 性能预算并验证 Top-K、上下文与缓存变化 | 阶段 Trace、质量护栏、TTFT / Token / Cost 报告 | 不教授检索模型训练或宣称性能等同于答案质量 |
| Ch24 | Agent 性能工程 / A+B | 多步 LLM、工具调用、串并行、重试和上下文增长如何放大 E2E | 找出 Agent Critical Path 并优化可并行或可缓存环节 | 工具 Trace、step E2E、token / cost per task、成功率 | 不讨论 Agent 产品设计或用单请求替代任务成功率 |
| Ch25 | Serving 与 Agent 综合实战 / C | 应用链路与推理服务指标如何共同决定 Goodput、SLO 和成本 | 完成一条 RAG / Agent 服务链路的端到端优化 | API 到模型的统一 Trace、前后对比和报告 | 不引入多 GPU 作为 Core 路线必需条件 |
| Ch26 | 容量模型、显存与成本 / A | 权重、KV、运行时、并发和单位成本如何形成容量边界 | 计算并实测单实例最大安全并发与成本 | 容量表、OOM 边界、显存水位和成本计算 | 不把公式上限写成生产安全容量 |
| Ch27 | 多副本、Scale-out 与 Autoscaling / B | 副本、负载均衡、冷启动、扩容延迟与 SLO 的关系 | 设计负载爬升和扩缩容策略 | TPS / P99 / 扩容生效时间与故障场景 | 不深入 TP/PP/NCCL 或 MoE 通信 |
| Ch28 | Multi-GPU Inference / A+B | TP、PP 与 NCCL 通信如何影响 Scaling Efficiency | 在声明的 Level 3 环境比较并行策略 | 多卡拓扑、版本、通信 Profile 和 Scaling Efficiency | 不把多卡结果作为 Core 单卡优化前置 |
| Ch29 | MoE、Expert Parallel 与 PD Disaggregation / A+B | All-to-All、路由倾斜、EP 和 Prefill/Decode 分离的系统约束 | 为 MoE 或分离式部署形成容量与通信诊断 | 专家路由/通信日志、Goodput、降级路线 | 无 Level 3 证据时只能给机制和实验设计 |
| Ch30 | End-to-End Performance Engineering Project / C | 如何把全书方法变成持续可运行的工程系统 | 完成 Core 或 Advanced 项目并通过评分规程 | 代码、manifest、raw、summary、诊断、优化、回归、Dashboard、终稿报告 | 不允许只交演示截图或缺少 Baseline 的最终结论 |

## 4. 全书统一完成标准

### 4.1 每章通用 DoD

- 标题、章号、Track、核心问题与 v1.0 大纲一致；
- 开头明确前置章、本章位置、Core 目标和 Advanced 深入方向；
- 学习目标使用“解释、比较、设计、运行、诊断、验证”等可验收动词；
- 正文明确“本章做到哪里、下一章继续什么”，不替后续章节提前完成闭环；
- Demo 写明环境、版本、输入、步骤、观测指标、预期现象和可重复性边界；
- 练习至少产生一个可检查交付物，而不只是讨论题；
- 章节目录 `content/chXX/` 按 `chXX.md` 与 `figures/`（插图与插图测试）两块组织，配套的 `storyboard.md`、`review.md` 与 `integration-report.md` 集中在 `strategy/reviews/chXX/`，所需插图和代码链接齐全；插图数量由教学任务决定，不设固定十图配额；
- 术语、公式、单位、API 字段、命令和文件路径与配套代码一致；
- 所有引用可追溯，外部技术事实注明来源和复核日期；
- 所有性能陈述使用证据标签，并通过对应级别的检查。

### 4.2 模板附加门槛

| 模板 | 附加验收 |
|---|---|
| A | 概念框架清楚；能解释系统位置；有一个可观察 Demo；输出 Checklist 与下一章衔接 |
| B | 每项技术分别回答 Problem、Mechanism、Performance Model、Profiling、Implementation、Benchmark、Trade-off、Best Practice |
| C | 必须完成 Baseline → Profiling → Root Cause → Plan → Implementation → Verification → Report；每次只改变可控变量 |

### 4.3 证据等级

| 标签 | 可以声称 | 不可以声称 |
|---|---|---|
| `[原理]` | 公式、机制和理论关系 | 某配置在真实系统中一定更快 |
| `[合成实验·已验证]` | 代码逻辑、Schema、计算和离线现象通过测试 | 真实 GPU / 服务收益 |
| `[真实测量·已验证]` | 在锁定环境与 Workload 下的结果 | 未测试环境、模型或负载上的通用收益 |
| `[待验证]` | 假设、实验计划、预期观测 | 确定收益、生产推荐或排名 |

### 4.4 Part 与全书门槛

一个 Part 只有在导读、所有章节、代码/Workshop 映射、跨章术语、前后依赖和 Part 级验证全部通过后才能标记完成。全书发布还需：

- 30 章正文与实际标题全部迁移到 v1.0；
- Core Demo 可在指定单卡环境复跑；Advanced Demo 明确资源前置与降级路线；
- RAG 与 Agent 各有独立性能章；
- Final Project 有 Core / Advanced 两条路线和评分规程；
- 环境锁定、证据目录、勘误、变更日志、版权清单和发布校验全部文档化。

## 5. 章节依赖与阅读路径

### 5.1 主依赖

```text
Ch1 → Ch2 → Ch3 → Ch4 → Ch5 → Ch6 → Ch7
                                  ↓
Ch8 Benchmark → Ch9 Profiling → Ch10 Root Cause → Ch11 Diagnosis Lab
     ↓                  ↓                  ↓
Ch12–15 Prefill   Ch16–19 Decode    Ch20–25 Serving / RAG / Agent
        └───────────────┴──────────────────┘
                         ↓
                  Ch26–27 Capacity / Scale-out
                         ↓
                  Ch28–29 Advanced Distributed
                         ↓
                      Ch30 Project
```

### 5.2 推荐路径

- **Core 自学**：Ch1–8 → Ch10–12 → Ch14–16 → Ch18–27 → Ch30；Ch9、13、17 先读 Core 段，Advanced Profile 选读。
- **Agent / RAG 工程师**：Core 自学路径 + 深读 Ch23–25。
- **平台 / 基础设施工程师**：完整 Ch1–30，重点 Ch5、9、13、17–18、26–29。
- **只想先跑项目的读者**：Ch1、6–8、11、25、30；这是一条速通路径，不替代完整机制学习。

## 6. 当前差距与执行任务

### 6.1 已确认事实

- Part 1 的 Ch1–7 已迁移到 v1.0，并有正文、Review、Storyboard、插图和集中 Demo；其性能证据仍需按“合成/真实”严格区分。
- 实际 `content/ch08`–`ch30` 的正文标题仍是旧 30 章体系：Ch8 从 Root Cause Analysis 开始，Ch30 仍是旧 Final Project；它们尚未按 v1.0 目录完成迁移。
- `content/part02.md`–`part07.md` 仍使用旧篇章范围；Part 5 尚未在导读中纳入独立 RAG / Agent 章节，Part 7 仍保留旧五章生产实践结构。
- `strategy/course-design/03_Course_Template.md` 顶部要求使用 v1.0，但底部章节模板映射仍是旧 29 章编号。
- 根 README、部分技能说明、校验脚本与真实 `content/` 布局不一致。
- 当前只有 Ch1–7 有独立 `code/chapterNN/`；后续章节以零散 Workshop、旧稿或待建设为主。
- 自动图谱工具在解析参考 PDF 字体映射时产生海量错误并被终止，因此本蓝图只采用人工核查到的仓库事实。

### 6.2 可执行任务

| 优先级 | 任务 | 交付物 | 验收条件 |
|---|---|---|---|
| P0 | 确立单一编辑基线 | 作者批准本蓝图；README、Course Design、Template 统一指向 v1.0 与 `content/` | 活跃文档不再把历史 Outline 或旧目录称为权威 |
| P0 | 修正模板映射 | 更新 `03_Course_Template.md` 的 30 章 A/B/C 对应表 | 与本蓝图和 v1.0 大纲逐章一致 |
| P0 | 重写 Part 导读 | 更新 part02–part07 | 章号、主题、能力和过渡与 v1.0 一致 |
| P0 | 迁移 Ch8–30 | 按迁移计划逐章平移、重写、合并或拆分 | 正文首标题、核心问题、Track、边界、Review、Storyboard 全部对齐 |
| P0 | 恢复验证入口 | 修复 `validate_part.py` 对真实根路径的识别 | 先有失败测试，再使按章/Part 校验通过 |
| P0 | 建立证据契约 | `runs/<run-id>/manifest + raw + summary` 规范及样例 | 书稿性能表能回链 run ID，未验证结论自动可识别 |
| P1 | 建设 Core Demo 主链 | 优先 Ch8、10–11、14–15、18–19、23–27 | 每章有可运行路径、相同 Workload 复测和自动验收产物 |
| P1 | 统一术语与 Schema | 全书术语表、指标测量合同、字段兼容检查 | TTFT、TPOT/ITL、TPS、Goodput、E2E、Cost 等只有一个定义 |
| P1 | 重做编辑台账 | 从真实正文标题和测试结果自动生成映射 | “有文件、已迁移、Demo 通过、性能已验证”四种状态不再混淆 |
| P2 | 教学与出版产品化 | 自学说明、讲师指南、作业、评分、勘误、变更日志 | 自学与授课两种使用方式都有明确入口和完成标准 |

### 6.3 主编决策门槛

在继续扩写新内容前，先确认三项决策：

1. 正式书名是否采用《LLM 推理性能工程实战》；
2. 本蓝图是否升格为图书级编辑基线；
3. 是否按“先修正权威入口与 Part 导读，再迁移 Ch8–30”的顺序推进。

未确认前，可以继续做只读盘点和验证工具修复，但不应新增会扩大章号漂移的正文。

## 7. 依据与待核对项

主要本地依据：

- `README.md:1-35`：当前命名、目录职责、Lesson / Workshop 区分；
- `strategy/course-design/01_Course_Design.md:10-22, 62-76, 242-302`：定位、统一方法、读者、成果和全书完成标准；
- `strategy/course-design/02_Course_Outline_v1.0.md:5-125`：30 章权威目录、Track、Demo 等级和 Final Project；
- `strategy/course-design/03_Course_Template.md:13-65, 69-352`：分层交付、A/B/C 模板与插图规则；
- `strategy/course-design/04_Content_Migration_Plan_v1.0.md:13-78`：逐章迁移动作与顺序；
- `strategy/editorial/gap-register.md:6-43`：当前可复现 P0/P1/P2 缺口；
- `strategy/editorial/book-code-workshop-map.md:18-58`：目标映射和证据口径。

发布前仍需作者拍板：指定单卡/多卡环境、软件版本锁定策略、篇幅与版式、考核方式、讲师资产规格、证据包存放合同和出版版权清单。
