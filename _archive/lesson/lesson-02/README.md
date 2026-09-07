# 第2章 LLM 性能指标

## 学习目标

完成本章后，学员应能够把「现象、指标、瓶颈、优化动作」连接起来，而不是只记住单个工具或参数。本章重点围绕 `LLM 性能指标` 建立可操作的分析框架。

## 核心内容

- TTFT
- ITL / TPOT
- Throughput
- Latency P50/P95/P99
- GPU Utilization
- GPU Memory Usage
- SM Occupancy
- HBM Bandwidth

## 关键概念

1. **观察对象**：先定义要看的指标，例如 TTFT、ITL、TPS、显存、SM 利用率或 HBM 带宽。
2. **实验变量**：一次只改变一个主要变量，例如 prompt 长度、输出长度、batch size、并发数、缓存策略或 kernel 配置。
3. **瓶颈判断**：用指标组合判断是计算受限、访存受限、调度受限，还是工程实现带来的额外开销。
4. **优化闭环**：记录基线，实施优化，再用同一组 workload 验证收益和副作用。

## Demo

使用 vLLM Benchmark 测试不同配置下的性能指标。

建议实验流程：

1. 准备同一模型、同一数据集和固定随机种子。
2. 运行本章 `./ch02/demo.py` 生成一组可复现的模拟指标。
3. 在真实环境中替换为 vLLM、TensorRT-LLM、SGLang 或本地推理服务的测量结果。
4. 对比优化前后数据，输出结论：瓶颈是什么、优化是否有效、代价是什么。

## 实战记录模板

| 项目 | 记录 |
|---|---|
| 模型 |  |
| GPU / Driver / CUDA |  |
| Workload |  |
| Baseline 指标 |  |
| 优化动作 |  |
| 优化后指标 |  |
| 结论 |  |

## 自检

- [ ] 能解释：TTFT
- [ ] 能解释：ITL / TPOT
- [ ] 能解释：Throughput
- [ ] 能解释：Latency P50/P95/P99
- [ ] 能说明本章 Demo 中的实验变量和控制变量
- [ ] 能给出下一步优化建议及其验证方式
