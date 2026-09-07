# Chapter Review

## 总体评价

第 2 章已从旧版“LLM 推理流程”收敛为新版 Outline 要求的 `LLM Inference Architecture`。章节采用 Template A，重点回答“LLM 推理系统长什么样”，主线围绕 Client、Gateway、Scheduler、Worker、Runtime、GPU 和框架架构取向展开。

## 结构问题

- 已包含学习目标、核心问题、核心内容、Demo / 实验、本章总结、课后练习和自检清单。
- 章节从全局架构进入入口层、调度层、执行层、部署形态和框架取向，顺序符合“先系统，后技术”的课程设计。
- Demo 只验证最小服务架构能跑通，没有把第 2 章写成 Benchmark 章节。

## 技术与术语问题

- 术语保持为 Client、Gateway、Scheduler、Worker、Runtime、GPU、KV Cache、vLLM、SGLang、TensorRT-LLM、Llama.cpp。
- TTFT、ITL、tokens/s 只作为 demo 脚本输出字段提及，没有在本章展开指标定义或优劣判断。

## 课堂案例补充

本章已补充主课堂案例、补充案例 A/B 和讨论题，用于支撑 20 分钟以上讲授。案例只服务本章边界，不展开后续章节的完整优化方案。

## 内容缺口

- 后续可以根据真实教学环境补充统一硬件和软件版本，例如 GPU 型号、vLLM 版本、Python 版本。本章规范未强制这些信息，因此当前只保留通用命令。
- 如果后续确认目标读者背景，可以在开头增加“前置知识”短段，但不应改变章节主线。

## 可删减内容

- 当前已删除旧版中 Prefill、Decode、KV Cache 生命周期、Compute Bound vs Memory Bound 和 Profiling Workflow 的大段展开。这些内容应移至第 2、4、9、10、13、14 等后续章节。

## 推荐插图位置

- 图2-1 放在核心问题后，建立全局地图。
- 图2-2 到图2-5 分别跟随组件职责段落。
- 图2-6 放在部署形态段落。
- 图2-7 放在框架取向段落。
- 图2-8 放在架构到性能分析的过渡段。
- 图2-9 放在 Demo 段。
- 图2-10 放在常见误区后，强调章节边界。

## 修改优先级

1. 2026-09-03 排序调整：Lifecycle 已移到第 1 章、排在本章之前，本章开头已改为回指第 1 章（"第 1 章已经带你跟着一个请求走了一遍生命周期……"），不再是"后续第 3 章会展开生命周期"的正向预告。第 3 章现在是 GPU 架构基础，与 Request/Queue/Prefill/Decode/Response/KV Cache 生命周期无关。
2. 如果 demo 脚本继续输出性能字段，课堂说明应持续强调本章不做指标结论。
3. 如果要正式制图，应先确认本 storyboard，再制作最终图。

## 验收建议

- Markdown 图片链接应全部存在。
- 图号应从图 2-1 到图 2-10 连续。
- 章节标题和 Outline 中 `Chapter 2 LLM Inference Architecture` 一致。
- 不应出现大段来自已发布参考书的原文、标题结构或图片复制。
