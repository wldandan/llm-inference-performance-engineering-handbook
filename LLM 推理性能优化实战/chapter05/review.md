# Chapter Review

## 总体评价

第 5 章已按 v1.0 大纲重写为 `GPU 性能心智模型`，并落实 Bridge 定位。正文不再从 SM、Warp 等微架构名词起步，而是先回答后端和 Agent 工程师最需要的四个问题：算得过来吗、放得下吗、搬得够快吗、Kernel 提交开销大吗。进阶硬件内容保留为独立选修入口。

## 结构问题

- 第 4 章的权重、KV Cache、Attention、MLP 和算子序列被显式映射到四类 GPU 资源。
- 容量先于速度判断，避免在配置无法稳定运行时讨论吞吐优化。
- 带宽和算力分别给出时间下界，再用算术强度与 Ridge Point 建立 Roofline 直觉。
- Kernel Launch 单独成节，没有被混入“GPU 利用率低”这一宽泛描述。
- SM、Warp、Tensor Core 和 Occupancy 下沉到进阶选修，Core 主线无需理解 CUDA 编程。

## 技术与术语问题

- `Memory Capacity` 与 `Memory Bandwidth` 已明确区分，单位与工程问题对应。
- 权重估算、KV Cache 估算和显存总预算均标注为近似式，并保留 Workspace、Runtime 和 Reserve。
- KV Cache 公式使用 KV Head 数，GQA 示例不会误用 Query Head 数。
- Decode 带宽压力没有被单一归因于 KV Cache；正文同时保留权重读取、Batch、Cache 命中和 Kernel 实现等变量。
- Peak Throughput / Peak Bandwidth 与 Effective Throughput / Effective Bandwidth 已分开。
- Occupancy 被定位为线索，不写成越高越好的性能总分。

## 内容缺口

- 离线 Demo 不探测真实 GPU，不读取 `nvidia-smi` 或 Profiler 输出。
- FLOPs、Bytes Moved、有效带宽和 Launch Cost 目前由读者提供；后续可增加来自真实 Trace 的适配器。
- 多 GPU 通信、NCCL、Topology、Expert Parallel 和 PD Disaggregation 按课程设计留在 Advanced Track。

## 可删减内容

- 不应恢复以硬件微架构为主线的旧稿结构，它会提高 Core 入门门槛。
- 不建议在本章加入 GPU 型号排行榜、价格或采购建议；选型需要结合第 26 章的容量与成本模型。
- 不应展开 CUDA Graph、Kernel Fusion 或 FlashAttention 的操作步骤；这里只解释它们试图减少哪类约束。

## 推荐插图位置

1. 图 5-1 先固定四类约束。
2. 图 5-2 将模型工作逐行映射到硬件资源。
3. 容量、带宽、Roofline 和 Launch Timeline 分别单独成图。
4. 进阶硬件地图只保留名词位置，不扩成 GPU 架构海报。
5. Demo 图明确显示输入是假设、输出是待验证顺序，并保留 `NOT A BENCHMARK`。

## 完成状态与后续优先级

1. 已完成：正文、案例、Checklist 和练习按四类约束重写。
2. 已完成：GPU 预算 Demo 的 9 项单元测试通过，覆盖容量、GQA、算力、带宽和 Launch 场景。
3. 已完成：8 张 v2 SVG、8 份 figure-note、图号与正文链接对齐，并完成原尺寸目检。
4. P1：在目标 GPU 环境补一份真实规格、显存水位和 Timeline 报告。
5. P2：第 9 章 Profiling Toolchain 完成后，增加从工具字段回指四类约束的索引。

## 验收建议

- 正文恰好引用图 5-1 到图 5-8，文件存在且编号连续。
- 章节明确出现 Bridge 和四类约束，不以硬件微架构作为 Core 起点。
- `python3 -m unittest discover -s code/chapter05 -p 'test_*.py' -v` 的 9 项测试全部通过。
- 8 张 SVG 可解析，符合 `chapter05-v2` 视觉契约，并各有制作说明。
- Demo 输出 `synthetic_gpu_mental_model` 和“不是 Benchmark”。
- 任何 Compute、Bandwidth 或 Launch 判断都被表述为候选约束或待验证假设。
