# Chapter Review

## 总体评价

第 3 章已按 v1.0 大纲重构为 `LLM Inference Architecture`。章节以逻辑职责为主线，把 Client、Gateway、Router、Admission、Engine Scheduler、Worker、Runtime 与 Accelerator 串成完整请求链路，并进一步区分逻辑组件、部署单元、请求平面、控制平面和遥测平面。内容适合后端与 Agent 工程师建立第一张可排障的 Serving 架构图。

## 结构问题

- Chapter 2 与 Chapter 3 的分工清楚：前者定义请求状态与时间边界，后者定义组件责任与交接关系。
- Router、Admission 和 Engine Scheduler 被单独展开，避免用一个宽泛的“调度器”覆盖三种决策。
- Worker、Runtime 与 Accelerator 只解释软件和硬件边界，没有提前进入 Chapter 5 的 GPU 微架构。
- 成熟系统映射位于通用架构之后，读者先掌握抽象，再接触产品命名，顺序合理。
- Demo、主案例和两个补充案例都围绕组件与连线，没有变成 Benchmark 或优化实验。

## 技术与术语问题

- `Accelerator` 被定义为通用逻辑角色，同时说明本书默认以 GPU 为例，兼顾课程主线与其他硬件后端。
- `Router` 输出目标选择，`Admission` 输出准入/排队决定，`Engine Scheduler` 输出 iteration plan，三者术语一致。
- 逻辑组件没有被强行等同于进程、Pod 或物理节点；这是本章最重要的架构约束。
- vLLM、Ray Serve、KServe、Triton、Dynamo、TensorRT-LLM 与 llama.cpp 的描述均限定在各自覆盖层级，没有写成跑分或功能排名。
- 请求平面、控制平面和遥测平面只说明责任与信息流，分布式实现细节仍留在 Advanced Track。

## 内容缺口

- Demo 是静态架构契约检查，不会探测真实服务进程、端口、健康状态或 Trace；这一限制已在正文和 README 明确。
- SGLang 在成熟系统表中只保留 LLM Engine 层映射，没有绑定某一版本的具体进程名。后续若增加源码导读，应锁定版本后单独补充。
- Chapter 20 编写后需要复查 Serving 工作机制与本章是否重复；本章应保留架构责任，Chapter 20 应展开运行时 Queue、Streaming、取消与失败传播。

## 可删减内容

- 不建议继续扩充产品列表。新增系统只有在能说明一个新的架构层级或责任边界时才有价值。
- 不应在本章增加 Autoscaling 参数、KV-aware routing 算法或 PD Disaggregation 配置；这些属于后续规模化章节。
- 不应把可观测边界扩写成指标公式和工具教程，正式定义分别属于 Chapter 6 与 Chapter 9。

## 推荐插图位置

1. 章节开头用全局架构固定请求与返回方向。
2. Client/Gateway、三层流量决策、Worker/Runtime/Accelerator 分别单独成图。
3. 三类状态和部署形态各用一张图，避免把责任与拓扑挤在同一画面。
4. 成熟系统映射要突出“平台、推理服务器、LLM Engine”三层，不做功能排行榜。
5. Demo 图表现 JSON 契约、校验步骤与报告，不再画真实 vLLM 请求。
6. 末图只说明 Chapter 3 与 Chapter 2、4、5、6、20 的边界。

## 完成状态与后续优先级

1. 已完成：更新并原尺寸渲染检查 10 张 Architecture SVG，清除旧章节号和旧 Demo 路径。
2. 已完成：架构契约 Demo 的 13 项单元测试通过。
3. P1：Chapter 4 与 Chapter 20 完成后复查相邻章节交叉引用。
4. P2：后续可增加一个真实部署拓扑采集器，但不阻塞 Core 版本。

## 验收建议

- 标题、学习目标、Demo、案例、总结和练习都回答 LLM Inference Architecture。
- 正文恰好引用图 3-1 到图 3-10，文件存在且 SVG 可解析。
- Demo 能识别缺失角色、重复组件、未知连线端点、错误连线类型和不完整路径。
- `python3 -m unittest test_architecture_contract.py` 的 13 项测试全部通过。
- 成熟系统映射附近保留官方资料链接，产品事实不依赖旧版记忆。
- 章节不提前给出性能指标结论或具体优化参数。
