# Part 1 V0.2 交付报告

## 当前结论

Part 1 已收紧为五章，主线是“先跑通一个请求，再理解请求、模型、Serving 与指标”。五章正文、Demo、README、插图和自动测试已经对齐。Chapter 2 的真实 vLLM 采集器已完成，但 GX10 当前拒绝 SSH 会话，因此真实运行报告仍待补录；旧的离线事件报告不再作为 GPU 实测证据。

## 章节与 Demo

| 章节 | 本章回答的问题 | Demo | 状态 |
|---|---|---|---|
| Ch1 第一个 LLM 服务 | 服务能否启动、调用、流式返回并留下客户端记录？ | 真实 OpenAI-compatible 流式客户端 | GX10 已跑通；历史报告缺 vLLM 版本 |
| Ch2 真实请求生命周期 | 一个请求在客户端和服务端分别经历了什么？ | 真实请求采集器 + 离线状态机辅助练习 | 代码完成；GX10 真实报告待生成 |
| Ch3 Transformer 生成机制 | 模型怎样从 token IDs 生成下一个 token？ | Shapes、Sampling、Prefill/Decode 合成机制报告 | 完成 |
| Ch4 LLM Serving 架构 | 哪个组件负责请求链路的哪一段？ | 单实例 / Scale-out 架构契约检查 | 完成 |
| Ch5 性能指标与延迟预算 | 怎样定义延迟、吞吐、Goodput 与阶段预算？ | 指标、预算和质量门槛报告 | 完成 |

## Ch1 与 Ch2 的区别

- Ch1 是“跑通”：从客户端证明服务可用，记录首个内容、流式结束、usage 和请求窗口。
- Ch2 是“解释”：把同一个真实请求映射到 Queue、Scheduled-to-first-token、Generation 等服务端证据，并标明哪些值是直接观测、客户端推导或暂时不可得。

因此，Ch2 不能只重复 Ch1 的流式计时，也不能用合成状态机冒充真实生命周期。

## 验证结果

- Part 1 结构与交付测试：8 项通过，GX10 真实报告门禁 1 项按预期失败。
- `code/ch01`～`code/ch05`：66 项测试通过。
- 五章插图契约：17 项测试通过。
- 合计：91 项通过，1 项外部证据门禁未通过。
- Part 1 范围内 68 份 Markdown：本地链接检查无缺失。
- Chapter 3～5 的图号、内部标题和视觉契约已同步为当前章号。
- Chapter 4 总图已区分单实例最小路径与规模化可选的 Router / Admission。
- Chapter 5 Goodput 同时要求成功、质量通过和 TTFT/E2E SLO 达标。

## 已知边界

1. Chapter 1 的 GX10 历史报告证明链路跑通，但没有记录 vLLM 版本，不能用于跨环境比较。
2. Chapter 2 的 `capture_lifecycle.py` 需要 vLLM GPU 服务启用 per-request metrics；当前 GX10 SSH 连接被远端关闭，尚未生成 `gx10-real-lifecycle-report.json`。
3. Chapter 3～5 的样例是教学用合成输入或静态契约，不是 Benchmark。它们验证概念、公式和边界，不声明真实硬件性能。
4. GPU 架构、多 GPU、NCCL、Expert Parallel 与 PD Disaggregation 不放在 Part 1 Core 主线中。

## 剩余验收

恢复 GX10 登录后，需要完成两件事：

1. 启动带 per-request metrics 的 vLLM，运行 Chapter 2 真实采集器并保存脱敏报告；
2. 补录 Chapter 1 的 vLLM 版本，或重新生成完整环境报告。
