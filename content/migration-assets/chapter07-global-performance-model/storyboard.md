# 第 7 章 Storyboard：Global Performance Model

本章插图用于把前六章收束成一套端到端分析框架。普通 LLM 请求用阶段时间线；RAG 与 Agent 出现并行分支后，统一切换到依赖图和 Critical Path。

| 图号 | 标题 | 核心问题 | 状态 |
|---|---|---|---|
| 图7-1 | Global Performance Model | 结果如何追溯到可验证证据？ | final v2 |
| 图7-2 | 请求端到端延迟分解 | 普通 LLM 请求的时间花在哪里？ | final v2 |
| 图7-3 | TTFT 与 E2E 的两条路径 | 首响与完整响应的终点有何不同？ | final v2 |
| 图7-4 | 从阶段时间到候选假设 | 慢阶段如何转成待验证假设？ | final v2 |
| 图7-5 | Workload 改变瓶颈 | 为什么瓶颈不能脱离负载讨论？ | final v2 |
| 图7-6 | 关键路径不是简单求和 | 并行分支如何计算真实等待时间？ | final v2 |
| 图7-7 | RAG 端到端性能路径 | 检索如何直接和间接影响 LLM？ | final v2 |
| 图7-8 | Agent 端到端性能路径 | 重复调用、工具与重试如何进入任务路径？ | final v2 |
| 图7-9 | Demo 输出全局性能报告 | 合成依赖图怎样生成可审计报告？ | final v2 |

## 全局视觉规范

- 1280×720；浅灰背景、白色分组卡片、深色结论栏。
- 最小字号 14 px，系统字体包含 `PingFang SC`。
- 灰色实线箭头表示依赖；红色表示 Critical Path；虚线表示回退、重试或工作量影响。
- 每张图包含 title、desc、`chapter07-v2` 与“关键结论”。
- 图中的数字是教学样例，不标成生产 Benchmark。

## 图7-1 Global Performance Model

- 来源：7.0。
- Wireframe：`Outcome → Workload → Stage → Resource → Evidence ↩`。
- 重点：Evidence 不支持时回到前层修正；不能从资源信号直接跳到根因。
- 关键结论：先定义结果与负载，再定位阶段和资源，最后用证据确认。

## 图7-2 请求端到端延迟分解

- 来源：7.1。
- Wireframe：客户端 E2E 横跨 Ingress、Gateway、Queue、Preprocess、Prefill、Decode 与 Egress。
- 重点：仅在边界明确、近似串行时使用阶段加法。
- 关键结论：把“模型很慢”还原为可以独立测量的阶段。

## 图7-3 TTFT 与 E2E 的两条路径

- 来源：7.2。
- Wireframe：同一阶段轴下，Prefill 产生 Logits，经 Sampling 选出首 token；TTFT 终止于首内容，E2E 延伸到完整返回。
- 重点：首 token 不是额外一次 Decode forward；Remaining Decode 只属于 E2E 的后半段。
- 关键结论：先确认用户说的“慢”到哪一个终点。

## 图7-4 从阶段时间到候选假设

- 来源：7.3。
- Wireframe：四行 `慢阶段 → 候选假设 → 最低成本证据`。
- 重点：每行明确 `needs_evidence`，不出现自动 Root Cause。
- 关键结论：阶段时间决定调查方向，证据决定结论。

## 图7-5 Workload 改变瓶颈

- 来源：7.4。
- Wireframe：输入、输出、并发、RAG/Agent 四张卡指向中央“当前关键阶段”。
- 重点：输入影响 Prefill/KV，输出影响 Decode，并发影响 Queue，编排改变依赖图。
- 关键结论：性能结论必须绑定完整负载条件。

## 图7-6 关键路径不是简单求和

- 来源：7.5。
- Wireframe：Ingress 分叉为两条 Retrieval，汇合后进入 LLM；慢分支用红色标出。
- 重点：分支为 100 / 200 ms；节点总和 630 ms、Critical Path 530 ms、并行重叠 100 ms。
- 关键结论：端到端收益由关键路径决定，非关键分支优化可能没有当前收益。

## 图7-7 RAG 端到端性能路径

- 来源：7.6。
- Wireframe：Request / Retrieval / Context / LLM 四个区，检索并行，Context Build 到 Prefill 有工作量影响线。
- 重点：时间路径和 prompt tokens 的间接影响同时保留。
- 关键结论：RAG 性能不能只看 LLM，也不能丢掉质量护栏。

## 图7-8 Agent 端到端性能路径

- 来源：7.7。
- Wireframe：LLM Plan 分叉到两个工具，汇合后 LLM Answer；CRM 上方画重试回路。
- 重点：第二轮 prompt 增长；指标分为 LLM、Tool 与 Task 三层。
- 关键结论：Agent 的优化对象是完整任务依赖图。

## 图7-9 Demo 输出全局性能报告

- 来源：7.8。
- Wireframe：三类 Synthetic DAG → `performance_model.py` → Critical Path / Overlap / Evidence Report。
- 重点：图校验、最长依赖路径、`needs_evidence`、`synthetic_global_performance_model`。
- 关键结论：Demo 可验证算法，但不能被描述成真实 Benchmark 或 Root Cause。
