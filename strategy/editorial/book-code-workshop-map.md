# 书稿—代码—Workshop 映射表

> 盘点日期：2026-09-08  
> 编号基线：`02_Course_Outline_v1.0.md` 的 30 章体系  
> 证据规则：“有文件”不等于“已验收性能”。只有锁定环境并产生可追溯实验产物后，才能把性能结论标成“已验证”。

## 状态口径

| 状态 | 含义 |
|---|---|
| 单测已验证 | 纯函数、输入校验或报告契约已在当前环境通过自动测试 |
| 合成实验已验证 | 样例输入可运行并生成可解释输出，但不代表真实服务性能 |
| 脚本存在 | 存在命令或实现，本次最多完成语法/纯函数检查 |
| 部分已有 | 可复用公共工具或其他章节实验，未形成本章闭环 |
| 待建设 | 没有对应章节代码或实验闭环 |
| 待验证 | 尚无锁定环境的原始 Benchmark 证据 |

## 30 章映射

| 章节 | 书稿 | 代码 / Workshop | 当前可证明的内容 | 主要缺口 |
|---|---|---|---|---|
| Ch1 第一个 LLM 服务 | `content/ch01/ch01.md` | `code/ch01/` | 12 项单测通过 | GPU 服务启动与流式调用待实跑 |
| Ch2 Inference Lifecycle | `content/ch02/ch02.md` | `code/ch02/` | 9 项单测通过 | 真实服务事件采集待验收 |
| Ch3 LLM Inference Architecture | `content/ch03/ch03.md` | `code/ch03/` | 13 项单测通过 | 主流框架版本对应关系待核对 |
| Ch4 Transformer 推理机制 | `content/ch04/ch04.md` | `code/ch04/`；`workshops/00-model-internals/` | 章节 8 项、Workshop 纯函数 25 项单测通过 | 真实模型加载、KV Cache 增长与计时仍待实跑 |
| Ch5 GPU 性能心智模型 | `content/ch05/ch05.md` | `code/ch05/` | 9 项单测通过 | 硬件指标与 Nsight 实测证据待补 |
| Ch6 LLM 性能指标 | `content/ch06/ch06.md` | `code/ch06/` | 10 项单测通过 | 真实 Streaming API 与服务端时钟对齐待验收 |
| Ch7 Global Performance Model | `content/ch07/ch07.md` | `code/ch07/`；`workshops/01-global-performance-model/` | 8 项单测通过；LLM/RAG/Agent 合成报告已验证 | 真实分布式 Trace 接入与 Root Cause 闭环待建 |
| Ch8 Benchmark Design | `content/ch08/ch08.md` | `workshops/common/` | 公共压测与报告工具已有 | 22 项中 2 项失败；章节专属 Baseline 未闭环 |
| Ch9 Profiling Toolchain | `content/ch09/ch09.md` | 零散脚本 / 待整合 | 书稿和插图存在 | Nsight Systems / Compute、PyTorch Profiler 的可复现采集流程待建 |
| Ch10 Root Cause Analysis | `content/ch10/ch10.md` | 无章节代码 | 书稿和插图存在 | 现象 → 证据 → 根因的可运行案例待建 |
| Ch11 Performance Diagnosis Lab | `content/ch11/ch11.md` | 无章节代码 | 书稿和插图存在 | 诊断报告 Schema、输入证据包和验收测试待建 |
| Ch12 Prefill 工作机制 | `content/ch12/ch12.md` | 可参考 `workshops/00-model-internals/` | 书稿和插图存在 | Prompt / KV Cache 形状实验待迁移 |
| Ch13 Prefill 性能分析 | `content/ch13/ch13.md` | 无章节代码 | 书稿和插图存在 | TTFT、Compute Utilization 与 Roofline 实验待建 |
| Ch14 Prefill 优化方法 | `content/ch14/ch14.md` | Workshop 总纲中 FlashAttention；未建目录 | 教学方案存在 | 旧编号 Ch12 需迁移到 Ch14；无可运行实验 |
| Ch15 Prefill 实战验证 | `content/ch15/ch15.md` | 可组合 FlashAttention / Chunked Prefill | 书稿和插图存在 | 长 Prompt Baseline → 优化 → 报告闭环待建 |
| Ch16 Decode 工作机制与 KV Cache | `content/ch16/ch16.md` | `workshops/00-model-internals/` 可迁移 | 纯函数测试已通过 | 需形成 `code/ch16/` 的本章契约 |
| Ch17 Decode 性能分析 | `content/ch17/ch17.md` | `workshops/07-kernel-level-cuda-graph/` 可提供部分证据 | Shell 语法通过 | GPU Timeline、HBM、TPOT 原始产物待实跑 |
| Ch18 Decode 优化方法 | `content/ch18/ch18.md` | `02-batching-tiers/`、`04-kv-quantization/`、`05-prefix-cache/`、`07-kernel-level-cuda-graph/`、`08-speculative-decoding/` | 脚本存在；KV 质量检查 2 项通过 | 旧 Ch16 编号漂移；GPU 收益、接受率和质量护栏待验收 |
| Ch19 Decode 实战验证 | `content/ch19/ch19.md` | 可组合 Ch18 Workshops | 书稿和插图存在 | 统一负载下 TPOT / TPS / 显存 / 质量闭环待建 |
| Ch20 Serving 工作机制 | `content/ch20/ch20.md` | `workshops/common/naive_baseline_server/` 可参考 | 基础服务实现存在 | Queue、Streaming、取消的本章 Demo 待建 |
| Ch21 Serving 调度与性能分析 | `content/ch21/ch21.md` | `02-batching-tiers/`、`09-chunked-prefill/` | Chunked Prefill 分析函数 2 项单测通过 | GPU 下 Queue Delay / P99 / Batch 效率待实跑 |
| Ch22 Serving 优化方法 | `content/ch22/ch22.md` | `02-batching-tiers/`、`09-chunked-prefill/` 可组合 | Shell 语法通过 | 旧 Ch20 编号漂移；限流、准入、优先级和资源池 Demo 待建 |
| Ch23 RAG 性能工程 | `content/ch23/ch23.md` | `05-prefix-cache/`；Ch7 RAG sample 可作分析入口 | 脚本与合成路径存在 | 检索质量、Top-K、TTFT 和 Token 成本的联合实验待建 |
| Ch24 Agent 性能工程 | `content/ch24/ch24.md` | Ch7 Agent sample 可作分析入口 | 合成 Agent Critical Path 报告已验证 | 真实多步 Agent、工具 Trace、Token / cost per task 待建 |
| Ch25 Serving 与 Agent 综合实战 | `content/ch25/ch25.md` | 可复用 Ch7 和 `workshops/common/` | 书稿和通用工具存在 | Goodput、SLO、成本和成功率的端到端闭环待建 |
| Ch26 容量模型、显存与成本 | `content/ch26/ch26.md` | 可复用 Ch4/5 纯函数 | 局部容量公式已有 | 最大并发、OOM 边界与单位成本实验待建 |
| Ch27 多副本、Scale-out 与 Autoscaling | `content/ch27/ch27.md` | Workshop 总纲中 Scale-out；未建目录 | 教学方案存在 | 旧 Ch24 编号漂移；负载爬升、扩容延迟和新副本冷启动待建 |
| Ch28 Multi-GPU Inference | `content/ch28/ch28.md` | Workshop 总纲中 TP / PP；未建目录 | 教学方案存在 | 多卡环境、NCCL 证据与 Scaling Efficiency 待建 |
| Ch29 MoE、EP 与 PD Disaggregation | `content/ch29/ch29.md` | Workshop 总纲中 MoE / PD；未建目录 | 教学方案和降级思路存在 | 框架版本、多机资源、专家路由日志与 Goodput 待建 |
| Ch30 End-to-End Project | `content/ch30/ch30.md` | 待整合全课程产物 | 书稿和插图存在 | Core / Advanced 两条可执行路线、证据包与评分规程待建 |

## 跨章复用规则

1. `code/chapterNN/` 是章节 Demo 的权威路径；`content/workshops/` 保留跨章或完整优化实验。
2. Workshop 可被多章引用，但每个章节必须说明自己只使用哪一段证据。
3. 机制演示、合成 DAG 和纯函数测试可以验证逻辑，不得写成真实性能收益。
4. 对比实验必须使用相同请求集、warmup、重复次数和指标口径，且保留原始报告。

