# 《LLM 推理性能工程实战》V0.2 正文迁移计划

## 1. 当前状态

Part 1 的 Ch1～Ch5 已按 V0.2 完成正文、代码、图和测试迁移。Chapter 2 的真实采集器已经实现，旧离线状态机已降为辅助练习；GX10 真实报告仍待生成。Chapter 6 之后尚未按 V0.2 全面迁移。

V0.2 从现有文件和 Git 历史提取可复用内容，按新章节问题重新组织；旧版文档保留为历史快照，不作为当前课程入口。

## 2. 迁移原则

- 先冻结大纲，再迁移正文、Part 导读、图和代码。
- 先建立章节边界和实验契约，再写实现。
- 真实实验与离线模拟分开标注。
- 同一机制只设一个主讲章节，其他章节只引用。
- Advanced 内容移入附录，不阻塞 Core 主线。
- 每次只迁移一章或一组强依赖章节，验证后提交。

## 3. 30 章迁移矩阵

| V0.2 章节 | 主要来源 | 动作 | 迁移重点 |
|---|---|---|---|
| Ch1 第一个 LLM 服务 | 当前 Ch1 | 保留并收窄 | 只负责启动、调用和流式链路，不提前评价性能。 |
| Ch2 真实请求生命周期 | 当前 Ch2 + vLLM 实测 | 重写 | 增加真实 Queue/Prefill/Decode/Cancel 证据；离线状态机降为辅助练习。 |
| Ch3 Transformer 生成机制 | 当前 Ch4 | 平移重写 | 聚合 Attention、自回归、Sampling、Prefill/Decode 和 KV Cache。 |
| Ch4 LLM Serving 架构 | 当前 Ch3 + 当前 Ch18 | 合并 | 统一 API、Gateway、Scheduler、Worker、Runtime 组件定义。 |
| Ch5 性能指标与延迟预算 | 当前 Ch6 + 当前 Ch7 | 合并 | 指标、延迟分解、SLO-aware Goodput、质量与成本预算。 |
| Ch6 LLM 工作负载建模 | 新内容 | 新建 | Chat、RAG、Agent、长度分布、到达模式、并发和 SLO。 |
| Ch7 Benchmark Design | v1.0 Ch8 规划 + 旧 Benchmark 素材 | 重写 | Baseline、Warmup、Repeat，以及长度、到达模式、参数和内容的生产代表性。 |
| Ch8 请求级可观测性 | 当前 Ch28 + 新内容 | 重写前置 | Request ID 贯通客户端、服务端日志、指标和 Trace。 |
| Ch9 Profiling Toolchain | v1.0 Ch9 规划 + 旧 Profiling 素材 | 重写 | Core/Advanced 分层，先轻后重。 |
| Ch10 Root Cause Analysis Lab | 当前 Ch8、Ch9 + v1.0 Ch10、Ch11 规划 | 合并重写 | 输出完整诊断报告，避免理论与 Lab 重复。 |
| Ch11 Prefill 工作机制与性能模型 | 当前 Ch10、Ch11 | 合并重写 | 机制与 Compute/Memory 模型连在一起。 |
| Ch12 长上下文与 RAG 上下文成本 | 当前 Ch13 素材 + 新内容 | 新建 | 长 Prompt、有效上下文、RAG 输入与 TTFT。 |
| Ch13 Prefill 优化方法 | 当前 Ch12 + Workshops | 重写 | FlashAttention、上下文裁剪、Prefix Cache、Chunked Prefill。 |
| Ch14 Prefill 优化实验 | 当前 Ch13 + v1.0 Ch15 规划 | 平移重写 | 同一长 Prompt 工作负载验证。 |
| Ch15 Decode 工作机制与性能模型 | 当前 Ch14、Ch15 | 合并重写 | 逐 Token、Memory Bound、Kernel Gap。 |
| Ch16 KV Cache 管理与容量 | 当前 Ch16、Ch22、Ch23 素材 | 拆分重写 | KV 大小、增长、PagedAttention、碎片与容量。 |
| Ch17 量化与内存优化 | 当前 Ch16、Ch24 + 量化 Workshop | 新建 | Weight/KV 量化、容量、性能与质量边界。 |
| Ch18 生成与 Runtime 优化 | 当前 Ch16 + Advanced 素材 | 重写 | Speculative Decoding 为 Core；CUDA/Kernel 深度下沉附录。 |
| Ch19 Decode 优化实验 | 当前 Ch17 + v1.0 Ch19 规划 | 平移重写 | 联合验证 TPOT、TPS、显存、接受率和质量。 |
| Ch20 Scheduler 与 Continuous Batching | 当前 Ch18-Ch20 + Batching Workshop | 合并重写 | Waiting/Running、Token Budget、Continuous Batching。 |
| Ch21 流量治理与可靠性 | 当前 Ch20 + 新内容 | 重写 | 连接复用、异步/流式调用、Admission、Timeout、Cancel、Retry、Backpressure。 |
| Ch22 Serving 架构选择与模型路由 | 当前 Ch3、Ch20、Ch24 + 新内容 | 新建 | 共享 API/专用部署/自托管、模型与引擎选择、Cache-aware Routing。 |
| Ch23 RAG 性能工程 | v1.0 Ch23 规划 + Prefix Cache 素材 | 新建 | Retrieval、Rerank、Context、Generation 关键路径。 |
| Ch24 Agent 性能工程 | v1.0 Ch24 规划 | 新建 | 多步 LLM、工具并行、上下文增长、失败和重试。 |
| Ch25 Serving 与 Agent 综合实验 | 当前 Ch21 + v1.0 Ch25 规划 | 重写 | 完整 RAG/Agent 链路的 SLO 优化。 |
| Ch26 容量、显存与成本模型 | 当前 Ch22、Ch23 + v1.0 Ch26 规划 | 合并重写 | 模型/KV 显存、并发上限、单位成本。 |
| Ch27 多副本、路由与 Autoscaling | 当前 Ch24、Ch25 + v1.0 Ch27 规划 | 合并重写 | Scale-out、负载均衡、弹性和 Goodput。 |
| Ch28 性能回归与发布门禁 | 当前 Ch26、Ch27 | 合并重写 | 自动 Benchmark、Shadow/Canary、阈值、版本对比和 CI 阻断。 |
| Ch29 Performance Review 与上线检查 | 当前 Ch28、Ch29 | 合并重写 | Dashboard、容量、成本、模型加载/冷启动、回滚和上线风险。 |
| Ch30 End-to-End Project | 当前 Ch30 + v1.0 Ch30 规划 | 重写 | Core/Advanced 共用报告契约，整合回归门禁。 |

## 4. Advanced 内容迁移

| 目标附录 | 主要来源 | 动作 |
|---|---|---|
| Appendix A GPU Architecture 与 Roofline | 当前 Ch5、Ch11、Ch15 | 保留必要心智模型，深入内容移入附录。 |
| Appendix B CUDA 与高级 Profiling | 当前 Ch9、Ch16 | 迁移 CUDA Graph、Kernel Fusion、Nsight Compute。 |
| Appendix C Multi-GPU 与 NCCL | v1.0 Ch28、当前 Ch24 | 独立成多卡实验。 |
| Appendix D MoE 与 Expert Parallel | v1.0 Ch29 素材 | 与 PD 分离，聚焦 All-to-All 和专家负载。 |
| Appendix E PD Disaggregation | v1.0 Ch29 素材 | 聚焦 KV Transfer、Prefill/Decode 池和扩缩容。 |

## 5. 实施顺序

1. 更新权威指针、Part 导读和章节状态索引。
2. 重做 Ch2 真实生命周期 Demo，修正 Part 1 的证据链。
3. 迁移 Ch3-Ch5，完成 Part 1。
4. 新建 Ch6，并迁移 Ch7-Ch10，完成测量与诊断底座。
5. 按 Ch11-Ch19 完成 Prefill/Decode 两组实验。
6. 按 Ch20-Ch25 完成 Serving、RAG 与 Agent 主线。
7. 按 Ch26-Ch30 恢复生产工程与最终项目。
8. 最后建设 Advanced Appendices / Labs，不阻塞 Core 发布。

## 6. 每批迁移的完成定义

- 章节标题、边界、Part 导读和代码索引一致；
- 代码先有失败测试，再实现或迁移；
- 模拟数据与真实运行证据明确区分；
- Markdown 链接、图片编号和测试通过；
- GX10 实验记录环境与版本；
- Git 提交不夹带无关工作区修改。
