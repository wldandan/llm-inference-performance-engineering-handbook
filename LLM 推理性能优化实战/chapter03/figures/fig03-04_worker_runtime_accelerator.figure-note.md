# 图 3-4 制作说明：Worker、Runtime 与 Accelerator

- 来源段落：第 3.4 节。
- 阅读顺序：从上到下看计划下发，从右侧虚线看 token 与状态返回。
- 关键结论：Worker 是软件执行单元，Accelerator 是承载计算与内存的硬件资源。
- 表达边界：不展开 SM、Warp、Tensor Core 和 Kernel Profiling。
