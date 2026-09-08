# 课程 Demo 代码

所有章节 Demo 统一放在 Git 仓库根目录的本目录中，并使用两位章节编号命名：

```text
code/
├── chapter01/
├── chapter02/
├── ...
└── chapter30/
```

当前只为已有实现的章节创建目录。待建设章节先在下表登记，避免使用空目录冒充可交付代码。

## Demo 索引

| 章节 | 主题 | 代码 | 状态 |
|---|---|---|---|
| Ch01 | 第一个 LLM 服务 | [code/chapter01](chapter01/README.md) | 已实现 |
| Ch02 | Inference Lifecycle | [code/chapter02](chapter02/README.md) | 已实现 |
| Ch03 | LLM Inference Architecture | [code/chapter03](chapter03/README.md) | 已实现 |
| Ch04 | Transformer 推理机制 | [code/chapter04](chapter04/README.md) | 已实现 |
| Ch05 | GPU 性能心智模型 | [code/chapter05](chapter05/README.md) | 已实现 |
| Ch06 | LLM 性能指标 | [code/chapter06](chapter06/README.md) | 已实现 |
| Ch07 | Global Performance Model | [code/chapter07](chapter07/README.md) | 已实现 |
| Ch08 | Benchmark Design | — | 待建设 |
| Ch09 | Profiling Toolchain | — | 待建设 |
| Ch10 | Root Cause Analysis | — | 待建设 |
| Ch11 | Performance Diagnosis Lab | — | 待建设 |
| Ch12 | Prefill 工作机制 | — | 待建设 |
| Ch13 | Prefill 性能分析 | — | 待建设 |
| Ch14 | Prefill 优化方法 | — | 待建设 |
| Ch15 | Prefill 实战验证 | — | 待建设 |
| Ch16 | Decode 工作机制与 KV Cache | — | 待建设 |
| Ch17 | Decode 性能分析 | — | 待建设 |
| Ch18 | Decode 优化方法 | — | 待建设 |
| Ch19 | Decode 实战验证 | — | 待建设 |
| Ch20 | Serving 工作机制 | — | 待建设 |
| Ch21 | Serving 调度与性能分析 | — | 待建设 |
| Ch22 | Serving 优化方法 | — | 待建设 |
| Ch23 | RAG 性能工程 | — | 待建设 |
| Ch24 | Agent 性能工程 | — | 待建设 |
| Ch25 | Serving 与 Agent 综合实战 | — | 待建设 |
| Ch26 | 容量模型、显存与成本 | — | 待建设 |
| Ch27 | 多副本、Scale-out 与 Autoscaling | — | 待建设 |
| Ch28 | Multi-GPU Inference | — | 待建设 |
| Ch29 | MoE、Expert Parallel 与 PD Disaggregation | — | 待建设 |
| Ch30 | End-to-End Performance Engineering Project | — | 待建设 |

## 使用约定

- 从 Git 仓库根目录运行时，路径统一写成 `code/chapterNN/...`。
- 每个已实现目录必须有独立 `README.md`，说明环境、命令、输出和边界。
- 单元测试与对应实现放在同一个章节目录，测试不依赖当前工作目录。
- Workshop 继续保留在 `LLM 推理性能优化实战/workshops/`，不与章节 Demo 混放。
- 新增 Demo 时，同时更新本索引和 `LLM 推理性能优化实战/30章-Demo映射-v1.0.md`。

运行当前所有章节 Demo 单元测试：

```bash
for chapter in code/chapter*; do
  python3 -m unittest discover -s "$chapter" -p 'test_*.py'
done
```
