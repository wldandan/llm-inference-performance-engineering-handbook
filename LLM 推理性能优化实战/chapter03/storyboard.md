# 第 3 章 Storyboard：LLM Inference Architecture

## 索引

| 图号 | 标题 | 核心问题 | 状态 |
|---|---|---|---|
| 图3-1 | LLM 推理系统全局架构 | 请求与响应分别经过哪些逻辑组件？ | wireframe |
| 图3-2 | Client 与 Gateway 边界 | 业务调用和服务入口分别负责什么？ | wireframe |
| 图3-3 | 三层流量决策 | Router、Admission、Engine Scheduler 如何分工？ | wireframe |
| 图3-4 | Worker、Runtime 与 Accelerator | 执行计划如何变成硬件计算？ | wireframe |
| 图3-5 | 推理服务的三类状态 | 请求、执行和资源状态由谁拥有？ | wireframe |
| 图3-6 | LLM Serving 部署形态 | 逻辑角色如何映射到不同部署单元？ | wireframe |
| 图3-7 | 成熟系统的架构层级映射 | 平台、推理服务器和 LLM Engine 有何区别？ | wireframe |
| 图3-8 | 从现象到组件和观测点 | 架构图如何指导证据采集？ | wireframe |
| 图3-9 | 架构契约 Demo | JSON 如何变成可验证的路径与部署报告？ | wireframe |
| 图3-10 | Chapter 3 的章节边界 | 架构与生命周期、模型机制、硬件和指标如何分工？ | wireframe |

## 图3-1 LLM 推理系统全局架构

- 对应正文：核心问题与第 3.1 节。
- 核心问题：请求从 Client 到 Accelerator，再如何返回？
- 核心观点：八个逻辑角色组成请求主路径，返回路径不需要重复做路由和准入。
- 不应出现：独立进程假设、框架专有类名、性能数字。
- 阅读路径：上方从左到右看请求，下方虚线从右向左看响应。

```text
Client -> Gateway -> Router -> Admission -> Scheduler
                                      -> Worker -> Runtime -> Accelerator
Client <- Gateway <---------------------- Worker <- Runtime <- Accelerator
```

- 图中文字：Request Path、Response Path、Client、Gateway、Router、Admission、Engine Scheduler、Worker、Runtime、GPU / Accelerator。
- Key Takeaway：先固定逻辑责任，再决定进程和设备如何部署。

## 图3-2 Client 与 Gateway 边界

- 对应正文：第 3.2 节。
- 核心问题：哪些责任属于调用方，哪些属于服务入口？
- 核心观点：Client 管业务调用与用户侧观测，Gateway 管协议、身份、校验和流式输出。
- 不应出现：Router 目标选择、Engine Scheduler、模型 forward。
- 阅读路径：左右对照，中间是协议边界。

```text
[Client]       | protocol boundary |       [Gateway]
task/context   | request + trace    | protocol/auth/validate
timeout/cancel | <--- chunks -------| normalize/stream
```

- 图中文字：Business Context、Timeout / Cancel、Protocol Boundary、Auth / Quota、Validate / Normalize、Streaming Response。
- Key Takeaway：Gateway 决定请求能否进入服务，不决定下一轮 token batch。

## 图3-3 三层流量决策

- 对应正文：第 3.3 节。
- 核心问题：三种常被统称为 scheduling 的决策有什么不同？
- 核心观点：Router 选目标，Admission 决定进入与否，Engine Scheduler 形成 iteration plan。
- 不应出现：具体路由算法、batch 参数、优化结论。
- 阅读路径：从请求依次经过三道决策门。

```text
[Router] --------> [Admission] --------> [Engine Scheduler]
target instance     accept/queue/reject    iteration plan
placement state     traffic budget         token + KV budget
```

- 图中文字：Where、Whether Now、Who Runs Next、Replica、Priority / SLO、Token / KV Budget。
- Key Takeaway：三层决策的输入、频率和输出都不同。

## 图3-4 Worker、Runtime 与 Accelerator

- 对应正文：第 3.4 节。
- 核心问题：执行计划如何下沉到硬件？
- 核心观点：Worker 拥有模型执行状态，Runtime 组织执行路径，Accelerator 执行张量计算。
- 不应出现：SM、Warp、Tensor Core 或 Kernel Profiling 细节。
- 阅读路径：由上到下看计划下发，由下到上看结果返回。

```text
[Worker: model + request state]
              ⇅
[Runtime: operator / engine / kernel]
              ⇅
[Accelerator: tensor compute + device memory]
```

- 图中文字：Execution Plan、Worker、Runtime、GPU / Accelerator、Token / Status。
- Key Takeaway：Worker 是软件执行单元，Accelerator 是硬件资源。

## 图3-5 推理服务的三类状态

- 对应正文：第 3.5 节。
- 核心问题：一次调度或清理需要同时读取哪些状态？
- 核心观点：请求、执行和资源状态由不同组件拥有，决策依赖它们协同。
- 不应出现：完整 KV Cache 机制、显存公式、具体状态枚举。
- 阅读路径：从三个状态域汇入 Decision / Cleanup。

```text
[Request State]  [Execution State]  [Resource State]
       \                |                /
             [Decision + Cleanup]
```

- 图中文字：Prompt / Params / Cancel、Batch / Model / Sampling、Queue / KV / Device、Authoritative Owner。
- Key Takeaway：状态副本可以很多，权威拥有者必须明确。

## 图3-6 LLM Serving 部署形态

- 对应正文：第 3.7 节。
- 核心问题：同一组逻辑职责可以怎样部署？
- 核心观点：从单进程、API/Engine 分离到多副本和平台化，变化的是部署与故障边界。
- 不应出现：容量结论、Autoscaling 参数、多 GPU 通信。
- 阅读路径：从左到右观察拆分和扩展。

```text
[Single Unit] -> [API | Engine] -> [Router | Replica A/B] -> [Platform + Models]
```

- 图中文字：Single Unit、API / Engine Split、Multi-Replica、Platform Control、Deployment Boundary。
- Key Takeaway：部署会变化，入口、路由、准入、执行和返回责任仍要可追踪。

## 图3-7 成熟系统的架构层级映射

- 对应正文：第 3.8 节。
- 核心问题：不同系统覆盖架构中的哪一层？
- 核心观点：Serving Platform、Inference Server 与 LLM Engine 是互补层，不是同类排行榜。
- 不应出现：功能勾选矩阵、跑分、谁最好。
- 阅读路径：先看三层，再把系统名称放入主要覆盖区。

```text
Serving Platform   Ray Serve | KServe | Dynamo
Inference Server   Triton    | Dynamo Frontend
LLM Engine         vLLM | SGLang | TensorRT-LLM | llama.cpp
```

- 图中文字：Platform、Inference Server、LLM Engine、Orchestrates、Hosts、Executes。
- Key Takeaway：比较系统前，先确认它们是否处于同一抽象层。

## 图3-8 从现象到组件和观测点

- 对应正文：第 3.9 节。
- 核心问题：一条模糊故障如何落到可检查边界？
- 核心观点：现象先映射到组件，再确定交接事件，最后才选择指标与工具。
- 不应出现：指标公式、Profiler 截图、优化参数。
- 阅读路径：从左到右。

```text
[Symptom] -> [Component / Handoff] -> [Minimal Evidence] -> [Later: Metric / Tool]
```

- 图中文字：Timeout、Wrong Replica、No Dispatch、Cancel Leak、Trace ID、Event Boundary。
- Key Takeaway：没有组件定位，日志、指标和工具只会变成盲查。

## 图3-9 架构契约 Demo

- 对应正文：第 3.10 节。
- 核心问题：静态架构如何接受自动检查？
- 核心观点：JSON 经过角色、端点和路径校验，输出请求路径、响应路径和部署单元。
- 不应出现：真实服务探测、GPU 指标、Benchmark 数字。
- 阅读路径：左侧输入，经中间检查，右侧报告。

```text
[JSON Components + Flows]
       -> [Validate Roles / Edges / Paths]
       -> [Request + Response + Deployment Report]
```

- 图中文字：reference-architecture.json、Required Roles、Known Endpoints、Complete Paths、deployment_units。
- Key Takeaway：架构图可以成为契约，而不只是一张静态图片。

## 图3-10 Chapter 3 的章节边界

- 对应正文：第 3.12 节与本章总结。
- 核心问题：本章和前后章节分别回答什么？
- 核心观点：Chapter 2 给阶段，Chapter 3 给组件，Chapter 4/5 给模型和硬件机制，Chapter 6 给指标，Chapter 20 展开 Serving 运行机制。
- 不应出现：具体优化技术清单。
- 阅读路径：以 Chapter 3 为中心向前后展开。

```text
[Ch2 Lifecycle] -> [Ch3 Architecture]
                         ├-> [Ch4 Model Mechanics]
                         ├-> [Ch5 GPU Model]
                         ├-> [Ch6 Metrics]
                         └-> [Ch20 Serving Mechanics]
```

- 图中文字：Stages、Component Ownership、Model Mechanics、Hardware Constraints、Metrics、Serving Runtime。
- Key Takeaway：先回答“谁负责”，再研究“为什么慢”和“怎么优化”。

## 全局视觉规范

- 画布：16:9 SVG，`1280x720`。
- 风格：白底、黑灰线框、空心节点、简单箭头。
- 颜色：只用黑、深灰、浅灰；请求与响应用实线/虚线区分，不使用彩色填充。
- 字体：系统无衬线字体；标题 32px，节点 18–22px，说明 15–17px。
- 每张图只保留一个主阅读方向，底部放一条 Key Takeaway。
- 不把开源项目官方架构图复制到本书，只画本章自己的抽象映射。

## 总体验收清单

- [x] 图 3-1 到图 3-10 与正文引用一一对应。
- [x] Router、Admission 与 Engine Scheduler 没有合并成一个框。
- [x] Worker、Runtime 与 Accelerator 没有混为同一层。
- [x] 逻辑组件和部署单元在至少两张图中明确区分。
- [x] 成熟系统映射没有形成产品优劣排名。
- [x] Demo 图与实际 JSON 输入和报告字段一致。
- [x] 所有图均无旧 Chapter 1/2 编号和旧 `chapter02/demo` 路径。
