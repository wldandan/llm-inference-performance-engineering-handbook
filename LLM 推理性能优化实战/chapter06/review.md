# Chapter Review

## 总体评价

第 6 章已迁移为 `LLM 性能指标`。新版不只列出 TTFT、TPOT 和 TPS，而是先固定问题、测量边界、共享窗口、聚合算法和成本分母。正文、离线 Demo 与 9 张插图采用同一套客户端口径，同时说明真实服务端与 GPU 指标不能直接混用。

## 结构问题

- 先按体验、产能、可靠产能、资源和成本选择指标，再展开公式。
- Client、Server、GPU 三层边界位于指标定义之前，避免同名时间被错误相减。
- 延迟、吞吐、分位数、资源和成本各有独立口径，最终由“指标合同”统一收束。
- Demo 读取请求级记录并输出完整合同，案例再把指标迁移到 RAG 与 Agent 场景。
- Warmup、Repeat、流量模型和实验控制没有抢占第 8 章 Benchmark Design 的内容。

## 技术与术语问题

- 客户端首内容 chunk 与严格首 token 已明确区分。
- 本书 TPOT 定义为首 token 后 ITL 的均值；单输出 token 时为未定义，不写 0。
- Output TPS 和成功 RPS 使用共享墙钟窗口，不相加并发请求的单请求速度。
- Goodput 只统计成功且满足显式 SLO 的请求。
- 分位数算法固定为 nearest-rank，并要求同时报告样本量和 workload 分桶。
- Resource Signal 与 Outcome Metric 之间需要因果证据，GPU Utilization 不被当成最终目标。
- 成本口径区分 input tokens、output tokens、successful requests 和 good requests。

## 内容缺口

- Demo 使用合成的客户端 token 时间点，尚未接入真实 OpenAI-compatible 流式事件。
- 生产接入需要决定 chunk 到 token 的映射方式，并记录 tokenizer 版本。
- 当前 Demo 使用 nearest-rank；Prometheus 直方图和其他插值算法的适配器留到工具链章节。
- Agent 的任务级成功条件只做桥接，正式定义留给第 24 章。

## 可删减内容

- 不建议加入更多同义指标缩写；新增指标必须先说明它回答的新问题。
- 不应在本章加入压测流量生成、Warmup 或统计显著性教程。
- 不应把 GPU 指标扩写成具体 Kernel 优化建议；第 5 章提供心智模型，第 9 章提供采集工具。

## 推荐插图位置

1. 指标问题地图放在全章开头。
2. 三层测量边界必须先于 TTFT / TPOT 公式。
3. 延迟时间线和共享吞吐窗口各自成图。
4. 分位数图突出样本量与 nearest-rank，不画平滑但无口径的分布曲线。
5. 资源、成本和指标合同三图用于防止常见报告误读。
6. Demo 图保留合成模式与 `NOT A BENCHMARK`。

## 完成状态与后续优先级

1. 已完成：正文、RAG / Agent 桥接案例、Checklist 与练习。
2. 已完成：离线指标 Demo 的 8 项单元测试，覆盖延迟、吞吐、Goodput、分位数、成本与脏数据。
3. 已完成：9 张 v2 SVG、9 份 figure-note、图号和正文路径对齐，并完成原尺寸目检。
4. P1：接入一次真实客户端记录，验证 chunk 与 token 口径。
5. P2：第 8 章完成后复查指标合同与 Benchmark 合同的分工。

## 验收建议

- 正文恰好引用图 6-1 到图 6-9，文件存在且编号连续。
- `python3 -m unittest discover -s code/chapter06 -p 'test_*.py' -v` 的 8 项测试全部通过。
- 9 张 SVG 可解析，符合 `chapter06-v2` 视觉契约，并各有制作说明。
- Demo 报告保存 Client Clock、共享 Window、nearest-rank、TPOT 公式、SLO 和成本分母。
- 章节明确区分 chunk / token、Throughput / Goodput、Resource / Outcome。
- 合成结果不被描述为真实 Benchmark。
