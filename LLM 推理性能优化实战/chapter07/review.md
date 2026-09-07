# Chapter Review

## 总体评价

第 7 章已从旧版 `Profiling Toolchain` 重构为 `Global Performance Model`。新版承担 Part 1 的收束任务：把服务入口、Inference Lifecycle、系统架构、Transformer、GPU 心智模型和性能指标放进 Outcome、Workload、Stage、Resource、Evidence 五层框架。Profiling 工具链按 v1.0 大纲后移到第 9 章。

## 结构检查

- 先定义五层全局模型，再分解普通 LLM 请求的 E2E 与 TTFT 路径。
- 明确区分阶段位置、候选假设、验证证据和 Root Cause。
- Workload 位于瓶颈判断之前，避免给模型贴固定的“计算受限”或“带宽受限”标签。
- 串行阶段加法与 DAG Critical Path 分开说明，没有把 RAG / Agent 强塞进 `Queue + Prefill + Decode`。
- RAG 说明检索对时间路径和 prompt tokens 的双重影响；Agent 使用任务级路径，保留重复 LLM、工具、重试和上下文增长。
- Demo、课堂案例、Checklist 和练习都围绕同一模型，没有提前展开第 8 章 Benchmark Design 或第 9 章 Profiling Toolchain。

## 技术与术语检查

- 普通请求的 E2E 分解被标为近似式，并写明仅适用于边界明确、近似串行的请求视图。
- TTFT 包含首个 Decode Step 与首内容返回；E2E 继续包含剩余 Decode 和 Egress。
- Critical Path 定义为 DAG 上最长依赖路径；并行分支取最晚必要分支，不相加全部节点。
- 图 7-6 的数值自洽：节点总和 630 ms，关键路径 530 ms，并行重叠 100 ms。
- “最长阶段”始终写作候选入口，Demo 使用 `needs_evidence`，不输出 `root_cause` 字段。
- GPU Utilization 保持为 Resource Signal，不被当成业务结果或根因。
- RAG 优化包含质量护栏；Agent 指标区分 LLM 调用、工具调用和完整任务。

## Demo 检查

- `performance_model.py` 支持 `llm_request`、`rag` 和 `agent` 三类合成场景。
- 依赖图会校验空输入、重复 ID、未知依赖、负时长与循环依赖。
- 最长路径算法保留每个阶段的 earliest finish、关键路径标记和路径占比。
- 报告包含节点总时间、关键路径时间、并行重叠、候选假设和待采证据。
- 8 项单元测试覆盖串行、并行、异常图、Queue / Decode 假设和 Agent 重复调用。
- `synthetic_global_performance_model` 与报告注释明确说明结果不是 Benchmark，也不是 Root Cause。

## 内容缺口

- Demo 当前分析单请求/单任务的离线依赖图，没有接入 OpenTelemetry 或真实服务 Trace。
- 节点耗时由输入直接提供，没有处理跨主机时钟偏差、Span 丢失和异步后台任务。
- `parallel_overlap_ms` 是教学用途的节点总时间与关键路径之差，不等同于 GPU Kernel overlap 或节省的资源成本。
- 共享资源争抢、动态 Batch 与跨请求耦合无法仅由单任务 DAG 判断，需要第 8、9 章补充 Benchmark 与 Profiling 证据。
- Agent 的任务成功和质量合同只给出接口，正式优化留到第 24 章。

## 插图检查

1. 图 7-1 用五层闭环完成 Part 1 总结。
2. 图 7-2、7-3 先建立普通请求的阶段和终点线。
3. 图 7-4、7-5 分别阻止“慢阶段等于根因”和“瓶颈永久不变”两类误判。
4. 图 7-6 用数值化 DAG 解释 Critical Path。
5. 图 7-7、7-8 分别扩展到 RAG 和 Agent。
6. 图 7-9 保留 Demo 的合成数据边界。
7. 9 张 SVG 已按 1280×720、`chapter07-v2`、最小 14 px、title/desc 和关键结论栏制作，并配套 figure-note。

## 完成状态与后续优先级

1. 已完成：正文、RAG / Agent 桥接、课堂案例、Checklist 与练习。
2. 已完成：离线依赖图 Demo、三类样例与 8 项单元测试。
3. 已完成：9 张 v2 SVG、9 份 figure-note、Storyboard 与正文链接对齐。
4. P1：第 8 章完成后，复查 Workload 字段能否直接成为 Benchmark Contract 输入。
5. P1：第 9 章完成后，为 Evidence Map 增加真实工具与 Trace 字段映射。
6. P2：Agent 章节完成后，将任务级质量和成本合同接回本章模板。

## 验收建议

- 正文恰好引用图 7-1 到图 7-9，文件、图号与 Storyboard 连续一致。
- `python3 -m unittest discover -s chapter07/demo -p 'test_*.py' -v` 的 8 项测试全部通过。
- 9 张 SVG 可解析、可渲染，正文与结论栏无裁切或重叠。
- LLM 串行样例的关键路径等于阶段和；RAG / Agent 并行样例不把所有节点直接相加。
- 报告中的候选项都保持 `needs_evidence`，不伪装成 Root Cause。
- 章节能自然承接第 8 章 Benchmark Design，而不是继续展开工具细节。
