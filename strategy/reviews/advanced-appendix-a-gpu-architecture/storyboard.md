# 第 5 章 Storyboard：GPU 性能心智模型

本章插图只建立四类 GPU 工程约束。硬件结构图属于进阶选修，不展开 CUDA 编程、GPU 选购或具体优化方案。

| 图号 | 标题 | 核心问题 | 状态 |
|---|---|---|---|
| 图5-1 | GPU 的四类工程约束 | 推理为什么会受四种不同资源限制？ | final v2 |
| 图5-2 | LLM 工作怎样落到 GPU 资源 | 模型工作分别消耗什么资源？ | final v2 |
| 图5-3 | 显存容量预算 | GPU 显存需要为哪些对象留位置？ | final v2 |
| 图5-4 | 显存带宽 | 数据从哪里移动到计算单元？ | final v2 |
| 图5-5 | 算力与 Roofline 直觉 | 如何比较计算和搬运下界？ | final v2 |
| 图5-6 | Kernel Launch Overhead | 大量短 Kernel 为什么会暴露固定开销？ | final v2 |
| 图5-7 | 进阶硬件地图 | SM、Warp、Tensor Core、Occupancy 各在什么位置？ | final v2 |
| 图5-8 | Demo 输出 GPU 约束报告 | 离线预算怎样给出验证顺序？ | final v2 |

## 全局视觉规范

- 画布：1280×720，浅灰底、白色卡片、深色主节点和深色结论栏。
- 字体：系统无衬线，包含 `PingFang SC`；正文最小字号 14 px。
- 连线：深灰实线表示数据或推理路径，虚线表示假设、余量或待验证关系。
- 所有图片必须包含标题、描述、`chapter05-v2` 标识和“关键结论”。

## 图5-1 GPU 的四类工程约束

### 对应正文
5.0 把 GPU 看成四种预算。

### 核心观点
- Compute Throughput 回答运算速度。
- Memory Capacity 回答能否放下。
- Memory Bandwidth 回答搬运速度。
- Launch Overhead 回答短 Kernel 的固定提交成本。

### 阅读路径与 Wireframe

~~~text
                        [GPU Inference Workload]
                     /       |       |          \
[Compute Throughput] [Memory Capacity] [Memory Bandwidth] [Launch Overhead]
~~~

### 不应出现
厂商型号、价格、Benchmark 排名或优化建议。

### 关键结论
四类约束回答四个不同问题，不能用一个利用率数字代替。

## 图5-2 LLM 工作怎样落到 GPU 资源

### 对应正文
5.1 第 4 章的模型工作怎样落到 GPU 资源。

### 核心观点
- 权重和 KV Cache 先占容量。
- Attention、MLP、LM Head 产生计算。
- 权重、激活和 K/V 需要搬运。
- 算子序列需要 Runtime 提交 Kernel。

### 阅读路径与 Wireframe

~~~text
[Weights + KV] -> [Capacity]
[Attention + MLP + LM Head] -> [Compute]
[Weights + Activations + KV] -> [Bandwidth]
[Operator Sequence] -> [Kernel Launch]
~~~

### 不应出现
Prefill 或 Decode 的固定瓶颈结论。

### 关键结论
一次模型前向同时消耗容量、算力、带宽和提交预算。

## 图5-3 显存容量预算

### 对应正文
5.2 显存容量：先判断能不能放下。

### 核心观点
- 总容量不是只有模型权重。
- KV Cache 随活跃 token 增长。
- 工作区、Runtime 与安全余量不可删除。

### 阅读路径与 Wireframe

~~~text
GPU Memory 100%
[Weights][KV Cache][Workspace][Runtime][Reserve]
                  required <= usable ?
~~~

### 图中文字
Weights、KV Cache、Workspace、Runtime、Reserve、Usable Budget、Fits / Overflow。

### 关键结论
稳定运行要给 KV Cache、工作区和运行时留出显式余量。

## 图5-4 显存带宽

### 对应正文
5.3 显存带宽：放得下，不等于搬得快。

### 核心观点
- HBM 容量大，数据经 L2、片上存储靠近计算单元。
- 有效带宽决定 Bytes moved 的时间下界。
- 近处复用能减少反复访问 HBM。

### 阅读路径与 Wireframe

~~~text
[HBM: Weights / KV] <-> [L2] <-> [Shared / Register] <-> [Compute]
T_bandwidth >= Bytes moved / Effective bandwidth
~~~

### 不应出现
精确延迟数字或特定 GPU 缓存容量。

### 关键结论
容量决定放多少，带宽决定数据多快到达计算单元。

## 图5-5 算力与 Roofline 直觉

### 对应正文
5.4 算力：有多少运算，能获得多少有效吞吐。

### 核心观点
- 计算下界来自 FLOPs / Throughput。
- 带宽下界来自 Bytes / Bandwidth。
- Arithmetic Intensity 与 Ridge Point 用于选择优先验证方向。

### 阅读路径与 Wireframe

~~~text
Low Arithmetic Intensity -------- Ridge Point -------- High Arithmetic Intensity
      Bandwidth candidate                               Compute candidate
T_floor ~= max(T_compute, T_bandwidth)
~~~

### 不应出现
把 Prefill / Decode 永久贴成固定瓶颈。

### 关键结论
Roofline 给出候选上限，真实瓶颈仍需用有效值和 Profiling 验证。

## 图5-6 Kernel Launch Overhead

### 对应正文
5.5 Kernel Launch Overhead。

### 核心观点
- 长 Kernel 中固定启动开销占比小。
- 大量短 Kernel 中 Gap 占比会放大。
- 需要同时看 CPU 提交和 GPU Timeline。

### 阅读路径与 Wireframe

~~~text
Long work:  [========== kernel ==========]
Tiny work:  [k] gap [k] gap [k] gap [k]
Launch estimate ~= count x visible launch cost
~~~

### 不应出现
CUDA Graph 或 Kernel Fusion 的操作步骤。

### 关键结论
Kernel 越短、数量越多，固定提交与调度开销越值得检查。

## 图5-7 进阶硬件地图

### 对应正文
5.7 进阶选修。

### 核心观点
- GPU 包含多个 SM。
- SM 调度 Warp，并使用 Tensor Core、Register 和 Shared Memory。
- Occupancy 是活跃 Warp 比例，不是性能总分。

### 阅读路径与 Wireframe

~~~text
[GPU]
  -> [SM x N]
       -> [Warp Scheduler -> Warps]
       -> [Tensor Core]
       -> [Register + Shared Memory]
       -> [Occupancy: active warps / limit]
~~~

### 不应出现
CUDA 代码、Bank Conflict、指令流水线细节。

### 关键结论
Core 先知道这些指标回答什么，Kernel 级分析时再深入。

## 图5-8 Demo 输出 GPU 约束报告

### 对应正文
5.8 Demo：生成一份 GPU 约束预算报告。

### 核心观点
- 模型、上下文、硬件假设进入 `gpu_model.py`。
- 输出容量预算、三个时间下界和一个优先验证项。
- 报告必须标记为合成结果和非 Benchmark。

### 阅读路径与 Wireframe

~~~text
[Model + Context] --\
[Hardware Specs] ----> [gpu_model.py] -> [Capacity | Compute | Bandwidth | Launch]
[Work Estimates] --/                         -> [Verify First]
~~~

### 图中文字
synthetic_gpu_mental_model、Memory Budget、Execution Lower Bounds、Dominant Constraint、NOT A BENCHMARK。

### 关键结论
Demo 只排序待验证假设，不替代真实测量。
