# 图 5-7 制作说明：进阶硬件地图

- 来源段落：第 5 章“5.7 进阶选修”。
- 阅读顺序：从 GPU 进入一个 SM，再沿 Warp Scheduler、Active Warps 和执行单元读取；底部是片上资源与 Occupancy。
- 关键结论：Core 先知道这些指标回答什么，Kernel 级分析时再深入。
- 边界：不进入 CUDA 代码、Bank Conflict 或指令流水线细节。
