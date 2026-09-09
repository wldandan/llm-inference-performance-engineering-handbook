# 《LLM 推理性能工程实战》30 章 - Demo 映射（V0.2）

## 1. 交付原则

课程维护一个持续演进的示例系统。30 章可以提供小程序、计算器和分析练习，但正式性能验收集中在 8 个递进实验中，避免重复启动服务或使用合成数据冒充性能结果。

环境分级：Level 1 为 CPU/离线分析；Level 2 为单 GPU Core 实验；Level 3 为多 GPU/多机 Advanced 实验。

## 2. 章节映射

| 章节 | 章节级代码或所属实验 | 主要证据 | 环境 | 当前状态 |
|---|---|---|---|---|
| Ch1 | Lab 1：第一个真实服务 | 请求成功、SSE 完整性 | Level 2 | 已实跑，指标解释已按 V0.2 收窄；待补 vLLM 版本 |
| Ch2 | Lab 2：真实请求生命周期 | 客户端事件、请求级 Queue/TTFT/Generation、Prometheus 增量 | Level 2 | 采集器已实现；待 GX10 真实运行，离线分析器仅作辅助 |
| Ch3 | Token 生成与 KV Cache 小程序 | Logits、Sampling、Cache 正确性 | Level 1/2 | 已迁移至 `code/ch03` 并通过测试 |
| Ch4 | Serving 组件与请求路径检查器 | 单实例/Scale-out profile、组件边界、请求/响应路径 | Level 1/2 | 已迁移至 `code/ch04` 并通过测试 |
| Ch5 | 指标与延迟预算计算器 | TTFT、TPOT、SLO-aware Goodput、质量、Cost、预算 | Level 1/2 | 已迁移至 `code/ch05` 并通过测试 |
| Ch6 | Lab 3：Workload Builder | 长度分布、到达模式、并发、Agent 步数 | Level 1 | 待建设 |
| Ch7 | Lab 3：Benchmark Baseline | Warmup、Repeat、P50/P95/P99 | Level 2 | 公共工具可迁移 |
| Ch8 | Lab 3：请求级可观测性 | Request ID、日志、指标、Trace | Level 2 | 待建设 |
| Ch9 | 分层 Profiling 练习 | API、CPU、Scheduler、GPU Timeline | Level 2/3 | 部分素材可迁移 |
| Ch10 | Lab 3：Root Cause 报告 | 现象、证据、假设、验证 | Level 1/2 | 待建设 |
| Ch11 | Prefill 机制与计算量计算器 | FLOPs、KV 写入、Prompt 长度 | Level 1/2 | 待建设 |
| Ch12 | RAG 上下文成本分析器 | 有效上下文、TTFT、Token Cost | Level 1/2 | 待建设 |
| Ch13 | Lab 4：Prefill 优化配置 | Cache 命中、Chunk、Attention 证据 | Level 2 | Workshops 可迁移 |
| Ch14 | Lab 4：Prefill 同流量验证 | TTFT、TPS、显存、P99 | Level 2 | 待建设 |
| Ch15 | Decode Timeline 分析器 | TPOT、带宽、Kernel Gap | Level 1/2 | 素材可迁移 |
| Ch16 | KV Cache 容量计算器 | KV 大小、Block、碎片、最大并发 | Level 1/2 | 可迁移旧素材 |
| Ch17 | Lab 5：量化与内存优化 | 显存、TPS、质量 | Level 2 | KV 量化 Workshop 可迁移 |
| Ch18 | Lab 5：生成与 Runtime 优化 | 接受率、TPOT、Kernel 开销 | Level 2/3 | Speculative/CUDA Workshops 可迁移 |
| Ch19 | Lab 5：Decode 同流量验证 | TPOT、TPS、显存、质量边界 | Level 2 | 待建设 |
| Ch20 | Lab 6：Continuous Batching | Queue、Batch、Token Budget、利用率 | Level 2 | Batching Workshop 可迁移 |
| Ch21 | Lab 6：流量治理 | 连接复用、流式取消、拒绝率、超时、P99 | Level 2 | 待建设 |
| Ch22 | 框架与路由决策练习 | 部署方式、能力矩阵、Cache 命中、路由结果 | Level 1/2 | 待建设 |
| Ch23 | Lab 7：RAG 关键路径 | Retrieval、Rerank、TTFT、Cost | Level 1/2 | 待建设 |
| Ch24 | Lab 7：Agent 关键路径 | Step、Tool、Retry、Token、E2E | Level 1/2 | 待建设 |
| Ch25 | Lab 7：Serving/Agent 综合优化 | SLO、Goodput、质量、成本 | Level 2 | 待建设 |
| Ch26 | 容量与成本规划器 | 模型/KV 显存、并发、单位成本 | Level 1/2 | 待建设 |
| Ch27 | Lab 8：多副本与 Autoscaling | Goodput、P99、扩容时间 | Level 2 | 待建设 |
| Ch28 | Lab 8：性能回归门禁 | 基线差异、Shadow/Canary、阈值、通过/阻断 | Level 1/2 | 旧 Ch26、Ch27 可迁移 |
| Ch29 | Lab 8：上线 Performance Review | Dashboard、容量、冷启动、回滚、风险项 | Level 1/2 | 旧 Ch28、Ch29 可迁移 |
| Ch30 | Lab 8：End-to-End Project | 完整性能报告与回归门禁 | Level 2 | 待建设 |

## 3. 八个正式实验

| Lab | 覆盖章节 | 可验收结果 |
|---|---|---|
| Lab 1 第一个真实服务 | Ch1 | vLLM 可启动、流式请求完整返回 |
| Lab 2 真实请求生命周期 | Ch2 | 客户端与服务端事件关联，包含正常与取消路径 |
| Lab 3 Workload、Benchmark 与诊断 | Ch6-Ch10 | 可重复 Baseline 和一份根因报告 |
| Lab 4 Prefill 与长上下文优化 | Ch11-Ch14 | 同流量 TTFT/吞吐对比与边界说明 |
| Lab 5 Decode、KV 与量化优化 | Ch15-Ch19 | TPOT/TPS/显存/质量联合对比 |
| Lab 6 Scheduler 与流量治理 | Ch20-Ch21 | Queue/P99/拒绝率/取消的受控实验 |
| Lab 7 RAG/Agent 关键路径 | Ch23-Ch25 | 节点时间、Critical Path、Token 与成本优化 |
| Lab 8 容量、回归与最终项目 | Ch26-Ch30 | 容量计划、自动回归、上线评审和最终报告 |

Ch3-Ch5、Ch22 的章节级代码用于建立认知和决策，不单独制造性能结论。

## 4. Advanced Labs

- GPU Architecture / Roofline / Nsight Compute；
- CUDA Graph 与 Kernel Fusion；
- Tensor Parallel / Pipeline Parallel / NCCL；
- MoE / Expert Parallel / All-to-All；
- PD Disaggregation / KV Transfer。

Advanced Lab 使用 Level 3 环境，结果不作为 Core Track 完成条件。

## 5. 正式性能实验验收标准

- README 明确环境、模型、框架版本和启动参数；
- Workload 描述输入/输出长度、到达模式、并发和请求数量；
- Baseline 与 optimized 使用相同请求集；
- 包含 Warmup 和重复运行；
- 至少报告平均值与 P50/P95/P99 中适用的统计量；
- 同时检查质量、延迟、吞吐、显存、失败率和成本中适用的指标；
- 区分客户端测量、服务端测量和推导值；
- 说明收益成立条件、噪声来源和不适用场景；
- 纯函数、数据解析和输入校验具备自动化测试。
