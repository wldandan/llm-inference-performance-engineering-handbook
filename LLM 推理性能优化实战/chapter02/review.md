# Chapter Review

## 总体评价

第 2 章已按 v1.0 大纲重写为 `Inference Lifecycle`。主线集中在归一化状态、关键时间点、正常与异常终态、请求时间线与引擎时间线、服务端与客户端观测边界。Demo 用可离线运行的事件分析器把概念落到具体输出，符合 Core Track 的入门定位。

## 结构问题

- Chapter 1 与 Chapter 2 的分工清楚：前者跑通服务并观察流式输出，后者建立正式生命周期模型。
- Chapter 2 没有继续讲 Gateway、Router、Worker 等组件职责，这部分留给 Chapter 3。
- 时间分段用于定义生命周期边界，没有提前进入 Chapter 6 的指标统计、分位数或 Benchmark 方法。
- 主案例和补充案例分别覆盖并发、长 Prompt 与 Agent 取消传播，仍停留在事件和状态层。

## 技术与术语问题

- `request_received -> queued -> scheduled -> first_token -> last_token -> finished` 被明确标注为课程归一化事件，不冒充 vLLM 内部 API。
- Queue、Prefill 和 Decode 的边界与 vLLM 当前指标设计相符，同时说明了不同系统可能采用不同观测点。
- 服务端 `first_token`、`first_chunk_sent` 和客户端 `first_chunk_received` 已分开，避免把生成时间与网络返回混算。
- 取消与失败路径保留已经闭合的时间段，缺失阶段返回未知值，不写成零耗时。

## 内容缺口

- 当前 Demo 使用合成事件，尚未提供 vLLM、SGLang 或 OpenTelemetry Trace 到归一化事件的适配器。
- 抢占、恢复、Prefix Cache 命中和 Remote KV 只列为 Advanced 延伸；这是有意保留的章节边界。
- Chapter 3 迁移时需要接住“事件由哪个组件产生、Trace 应在哪里采集”这一问题。

## 可删减内容

- 不建议再增加框架内部状态枚举。列得过细会把生命周期章节写成特定版本源码导读。
- 不应在本章加入 TTFT / TPOT 的负载对比或优化结论；这些内容属于 Chapter 6 及后续分析章节。

## 推荐插图位置

1. 章节开头用总时间线固定六个关键事件。
2. 三层对象、归一化状态机、Queue 边界和 Prefill 边界分别单独成图。
3. Decode 图要同时表现多轮 step 与 KV Cache 增长。
4. 客户端 / 服务端边界、异常终态清理和 Demo 数据流各用一张图。
5. 末图只说明与 Chapter 1、3、4、6、21、24 的边界，不列优化技术清单。

## 完成状态与后续优先级

1. 已完成：按 v2 视觉系统重画并验证 10 张生命周期图，每张图均有独立制作说明；旧 Architecture 图片已迁出并保留给 Chapter 3。
2. 已完成：Demo 的 9 项单元测试与样例 CLI 通过，覆盖正常、取消、失败三类路径。
3. P1：Chapter 3 完成后复查相邻章节交叉引用。
4. P2：后续增加一个真实框架 Trace 适配器，但不阻塞本章 Core 版本。

## 验收建议

- 章节标题、学习目标、Demo、总结和练习都回答 Inference Lifecycle。
- 正文恰好引用图 2-1 到图 2-10，文件存在且 SVG 可解析。
- 10 张图通过插图视觉契约测试和 `1280x720` 原尺寸渲染目检。
- `python3 -m unittest discover -s code/chapter02 -p 'test_*.py'` 全部通过。
- 样例 CLI 输出 3 条请求，其中 finished、cancelled、failed 各 1 条。
- 非法状态跳转和逆序时间戳会被拒绝。
- 合成数据和真实性能数据的边界写清楚。
