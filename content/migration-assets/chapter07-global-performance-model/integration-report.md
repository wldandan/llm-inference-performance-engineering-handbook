# 第 7 章图文集成报告

## 集成范围

- 正文：`chapter07.md`
- Demo：`code/chapter07/performance_model.py`、3 个合成场景和 8 项测试
- 图稿：`figures/fig07-01` 至 `fig07-09`
- 制作说明：9 份 `figure-note.md`
- 设计稿：`storyboard.md`
- 审校记录：`review.md`

## 图文映射

| 图号 | 正文段落 | 教学职责 |
|---|---|---|
| 图7-1 | 7.0 | 建立 Outcome → Evidence 五层闭环 |
| 图7-2 | 7.1 | 分解普通 LLM 请求 E2E |
| 图7-3 | 7.2 | 区分 TTFT 与 E2E 终点 |
| 图7-4 | 7.3 | 从阶段异常生成待验证假设 |
| 图7-5 | 7.4 | 说明 Workload 会移动瓶颈 |
| 图7-6 | 7.5 | 解释 DAG 与 Critical Path |
| 图7-7 | 7.6 | 扩展到 RAG 时间与工作量路径 |
| 图7-8 | 7.7 | 扩展到 Agent 任务路径 |
| 图7-9 | 7.8 | 说明 Demo 输入、计算和报告边界 |

## 一致性检查

- 9 个正文链接按图号连续排列，文件名与测试清单一致。
- 所有 SVG 使用 `chapter07-v2`，尺寸为 1280×720，包含可访问标题和描述。
- 图 7-6、正文、Storyboard 和 Demo 测试采用同一组关键路径关系：并行分支不直接相加。
- 图 7-3、正文与第 4 章采用同一首 token 口径：Prefill 后 Sampling 产生首 token，后续才进入 Decode。
- 图 7-7 与 RAG 样例都保留 Dense / Keyword 并行、Merge、Context 和 LLM 路径。
- 图 7-8 与 Agent 样例都保留重复 LLM、并行工具和 Merge。
- 图 7-9 与 Demo 报告都使用 `synthetic_global_performance_model` 和 `needs_evidence`。

## 视觉检查

- 已用系统 SVG 渲染器输出 1280×720 PNG，并按原尺寸检查 9 张图。
- 标题、卡片、路径、数值和底部关键结论均在画布内。
- 图 7-6 的 Critical Path 使用红色，非关键路径使用灰色。
- 图 7-7 的上下文工作量影响、图 7-8 的重试路径使用虚线，与主依赖线区分。
- 合成数字只用于教学，不标为真实生产结果。

## 章节边界

- 本章负责统一性能分析模型，不提供具体优化参数。
- Benchmark 的流量、Warmup、重复性和实验控制进入第 8 章。
- 服务、Runtime 和 GPU Profiling 工具进入第 9 章。
- RAG 与 Agent 的专项优化分别在后续章节展开，本章只建立端到端路径和指标接口。

## 验收状态

- 正文：通过结构校验。
- Demo：8 项测试通过。
- 插图：结构测试、XML 解析与原尺寸目检通过。
- 图文关系：路径、图号、Caption、Storyboard 和 figure-note 已对齐。
