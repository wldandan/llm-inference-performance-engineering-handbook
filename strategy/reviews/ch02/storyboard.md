# 第 2 章 Storyboard：Inference Lifecycle

## 索引

| 图号 | 标题 | 核心问题 | 状态 |
|---|---|---|---|
| 图2-1 | 推理请求生命周期与关键时间点 | 一条正常请求经过哪些事件和阶段？ | final v2 |
| 图2-2 | 业务任务、LLM 调用与推理请求 | 三种常被混称为“请求”的对象如何嵌套？ | final v2 |
| 图2-3 | 归一化请求状态机 | 成功、取消和失败如何进入终态？ | final v2 |
| 图2-4 | Queue 与首次调度的边界 | Queue 时间由哪两个事件闭合？ | final v2 |
| 图2-5 | Prefill 与首 token 的边界 | 服务端首 token 与客户端首 chunk 差在哪里？ | final v2 |
| 图2-6 | Decode step 与 KV Cache 增长 | 一条请求如何跨越多轮引擎执行？ | final v2 |
| 图2-7 | 服务端事件与客户端观测 | 两类时间为什么不能直接混算？ | final v2 |
| 图2-8 | 三类终态与资源清理 | 请求怎样结束，资源怎样收口？ | final v2 |
| 图2-9 | 真实 vLLM 请求生成生命周期证据报告 | Demo 如何组合客户端、请求级服务端和聚合证据？ | final v2 |
| 图2-10 | Chapter 2 与后续章节边界 | 生命周期与架构、原理、指标、调度如何分工？ | final v2 |

## 图2-1 推理请求生命周期与关键时间点

- 对应正文：核心问题与第 2.3 节。
- 核心问题：一条正常请求经过哪些事件和阶段？
- 核心观点：六个时间点闭合五段阶段时间和端到端时间。
- 不应出现：框架组件、优化参数、真实性能数值。
- 阅读路径：从左到右。

```text
[t0 received] --Admission--> [t1 queued] --Queue--> [t2 scheduled]
      --Prefill--> [t3 first token] --Decode--> [t4 last token]
      --Response Tail--> [t5 finished]
```

- 图中文字：`request_received`、`queued`、`scheduled`、`first_token`、`last_token`、`finished`。
- Key Takeaway：没有事件边界，就没有可复核的阶段时间。

## 图2-2 业务任务、LLM 调用与推理请求

- 对应正文：第 2.1 节。
- 核心问题：三种“请求”如何嵌套？
- 核心观点：一个业务任务可包含多次 LLM 调用，一次调用也可能因重试产生多条推理请求。
- 不应出现：Agent 调度算法、工具内部实现。
- 阅读路径：从外层 Task 向内展开。

```text
[Business Task]
   ├─ [LLM Call 1] ─ [Inference Request 1]
   ├─ [Tool Calls]
   └─ [LLM Call 2] ─ [Request 2] ─ [Retry 3]
```

- 图中文字：Business Task、LLM Call、Tool Call、Inference Request、Retry。
- Key Takeaway：本章追踪的是最内层的 Inference Request。

## 图2-3 归一化请求状态机

- 对应正文：第 2.2 节。
- 核心问题：正常和异常路径如何结束？
- 核心观点：主路径之外，非终态可进入 cancelled 或 failed。
- 不应出现：把课程事件写成 vLLM 内部类名。
- 阅读路径：主路径横向，异常路径向下。

```text
received -> queued -> scheduled -> first token -> last token -> finished
    \          \          \             \
     +----------+----------+-------------+--> cancelled / failed
```

- 图中文字：Main Path、Terminal States、cancelled、failed。
- Key Takeaway：所有请求都必须有明确终态。

## 图2-4 Queue 与首次调度的边界

- 对应正文：第 2.3、2.4 节。
- 核心问题：Queue 从哪里开始，到哪里结束？
- 核心观点：首次 queued 到首次 scheduled 才是本章的 Queue 区间。
- 不应出现：队列策略优劣、SLO 阈值。
- 阅读路径：入口事件进入等待区，再由 Scheduler 取出。

```text
[queued] -> | waiting requests | -> [scheduled first time]
             <--- Queue --->
```

- 图中文字：queued、Waiting Queue、scheduled、Queue = t2 - t1。
- Key Takeaway：客户端等待时间不能直接当作 Queue 时间。

## 图2-5 Prefill 与首 token 的边界

- 对应正文：第 2.5 节。
- 核心问题：Prefill 结束后，用户是否已经看到首包？
- 核心观点：服务端生成首 token 后，还要经过协议组装和网络返回。
- 不应出现：Attention 公式、FlashAttention、Benchmark 数字。
- 阅读路径：上方为模型路径，下方虚线延伸到客户端。

```text
scheduled -> prompt compute -> KV Cache -> logits -> first token
                                                    - - -> first chunk received
```

- 图中文字：Prompt Compute、KV Cache、Sampling、First Token Generated、First Chunk Received。
- Key Takeaway：首 token 生成与首包到达不是同一个时间点。

## 图2-6 Decode step 与 KV Cache 增长

- 对应正文：第 2.6 节。
- 核心问题：Decode 为什么是一串步骤？
- 核心观点：每个 step 生成 token 并追加 K/V，一条请求跨越多轮 iteration。
- 不应出现：KV Cache 容量公式、量化和分页实现。
- 阅读路径：上方从左到右看 step，下方看缓存增长。

```text
step 1 -> token 2 -> step 2 -> token 3 -> step 3 -> last token
KV: [prompt]      [prompt + 1]          [prompt + 1 + 1]
```

- 图中文字：Engine Iteration、Decode Step、Append K/V、KV Cache Grows。
- Key Takeaway：Decode 时间可能包含执行间隙和抢占等待。

## 图2-7 服务端事件与客户端观测

- 对应正文：第 2.7 节。
- 核心问题：服务端与客户端时钟如何对应？
- 核心观点：生成、发送和接收是三个观测点，需要 Trace ID 对齐。
- 不应出现：跨机器直接相减的伪精确数字。
- 阅读路径：上方服务端，下方客户端，中间用网络箭头连接。

```text
Server: [first token] -> [first chunk sent] ------>
                                               network
Client:                         [request sent] -> [first chunk received]
```

- 图中文字：Server Clock、Client Clock、Network、Trace ID。
- Key Takeaway：指标名相同，不代表采集边界相同。

## 图2-8 三类终态与资源清理

- 对应正文：第 2.8 节。
- 核心问题：成功、取消和失败之后都要做什么？
- 核心观点：三类终态最终都进入停止计算、状态清理和资源交接。
- 不应出现：缓存一定立即删除的表述。
- 阅读路径：三条终态分支汇入 Cleanup。

```text
[finished]  \
[cancelled] ---> [stop compute] -> [state cleanup] -> [release or reuse]
[failed]    /
```

- 图中文字：Terminal State、Stop Compute、Cleanup、Release / Reuse、Log Reason。
- Key Takeaway：结束不是返回一个状态码，资源也必须完成交接。

## 图2-9 真实 vLLM 请求生成生命周期证据报告

- 对应正文：第 2.9 节。
- 核心问题：主 Demo 如何为一次真实 vLLM 请求收集生命周期证据？
- 核心观点：同时采集客户端流、响应中的请求级指标和 Prometheus 前后快照；每项证据标明作用域与可信级别。
- 不应出现：根据客户端时间猜测服务端 Queue 或 Prefill，或把聚合指标增量归因给并发环境中的单个请求。
- 阅读路径：左侧输入，经中间处理，右侧输出。

```text
[Real vLLM Request] -> [Client Stream | Per-request Metrics | Prometheus Delta] -> [Evidence Report]
```

- 图中文字：真实 vLLM 请求、请求级 Metrics、Prometheus 增量、证据分级报告、complete / incomplete。
- 关键结论：真实请求是主 Demo；离线 JSONL 状态机只负责验证边界和异常路径。

## 图2-10 Chapter 2 与后续章节边界

- 对应正文：第 2.11 节和本章总结。
- 核心问题：生命周期之后还要学什么？
- 核心观点：本章给阶段，Chapter 3 解释模型机制，Chapter 4 解释 Serving 组件，Chapter 5 定义指标与延迟预算。
- 不应出现：具体优化技术清单。
- 阅读路径：以 Chapter 2 为中心向后展开。

```text
[Ch1 Run Service] -> [Ch2 Lifecycle]
                          ├-> [Ch3 Transformer]
                          ├-> [Ch4 Serving]
                          ├-> [Ch5 Metrics]
                          └-> [Part 2 Measure & Diagnose]
```

- 图中文字：Run、Lifecycle、Transformer、Serving、Metrics、Measure & Diagnose。
- Key Takeaway：先知道请求在哪个阶段，再问组件、指标和优化。

## 全局视觉规范

- 画布：16:9 SVG，`1280x720`。
- 风格：浅灰画布、白色内容卡片、深色标题区和显式方向箭头。
- 颜色：统一使用 Slate 黑、灰、浅灰与白色；异常路径使用虚线，不依赖彩色填充。
- 字体：系统无衬线字体，中文承担主要叙事，保留必要英文技术词；图中文字不小于 14px。
- 每张图只保留一个主阅读方向，底部统一放置深色“关键结论”条。
- 每张图包含可访问的 `title`、`desc`、视觉系统标记及独立 `.figure-note.md` 制作说明。

## 总体验收清单

- [x] 图 2-1 到图 2-10 与正文引用一一对应。
- [x] 图中文字全部能在正文中找到依据。
- [x] 没有 Architecture 旧图、优化参数或虚构性能数据。
- [x] `first_token` 与 `first_chunk_received` 没有混为一个节点。
- [x] 合成数据明确标记为教学用途。
