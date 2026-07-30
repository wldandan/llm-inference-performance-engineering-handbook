# Chapter Review

## 总体评价

第一章《LLM 推理流程》已经形成可用初稿，正文围绕一次 LLM 在线推理请求的完整生命周期展开，覆盖用户体感、请求链路、decoder-only Transformer 生成机制、Prefill、Decode、KV Cache、核心指标、瓶颈类型、实验和自检。

当前版本符合 `book-chapter-writer` 的基础交付要求：正文完整，10 张 SVG wireframe 已生成并插入正文，图片路径使用章节内相对路径。章节可以作为后续正式插图和教学打磨的基础版本。

## 结构问题

1. 章节主线清楚：从“用户觉得慢”进入，再逐步拆解生命周期、模型生成过程、Prefill、Decode、KV Cache 和观测指标。
2. 10 张 wireframe 已分布在导读、Serving、Transformer、Prefill、Decode、KV Cache、GPU、瓶颈、Profiling、诊断树等位置，基本覆盖第一章应建立的性能地图。
3. `图1-7：GPU Memory & Compute Lifecycle` 当前放在 KV Cache 段落之后，正文对 GPU 视角的独立解释偏少。后续可单独增加一个小节，例如“从 GPU 视角看一次请求”，让该图有更强正文支撑。
4. `图1-8：Compute Bound vs Memory Bound` 插在指标小节末尾、瓶颈小节之前，可以接受；若后续精修，可移到 `1.8 Compute Bound 与 Memory Bound` 小节开头。

## 技术与术语问题

1. Prefill、Decode、KV Cache、TTFT、ITL、TPS 的术语使用一致。
2. “Prefill 更容易表现为 compute bound”和“Decode 更容易表现为 memory bound”均保留了工程判断空间，没有写成绝对结论。
3. KV Cache 显存估算公式已明确是直觉公式，不是生产系统精确模型。
4. Demo 明确说明使用确定性模拟数据，符合当前课程材料状态。

## 内容缺口

1. 正式出版图尚未生成。目前 10 张图是 wireframe，不是最终视觉插图。
2. `storyboard.md` 目前是索引级 storyboard，尚未为每一张图展开详细版式、图中文字、线型说明和验收清单。
3. 第一章正文尚未加入真实 GX10 环境 baseline 记录表。若要面向实操培训，可在实验小节补充真实环境观察模板。

## 可删减内容

当前正文篇幅适中，不建议删减。若未来压缩课件版，可压缩 `1.10 常见误区`，但教材正文中建议保留。

## 推荐插图位置

| 图号 | 当前正文位置 | 核心问题 | 当前状态 |
|---|---|---|---|
| 图1-1 | 本章导读 | 一次请求发生了什么？ | wireframe |
| 图1-2 | 1.1 后 | 请求经过哪些 Serving 模块？ | wireframe |
| 图1-3 | 1.2 后 | decoder-only 模型如何生成 token？ | wireframe |
| 图1-4 | 1.4 后 | Prefill 做什么？ | wireframe |
| 图1-5 | 1.5 后 | Decode 做什么？ | wireframe |
| 图1-6 | 1.6 中 | KV Cache 如何变化？ | wireframe |
| 图1-7 | 1.6 后 | GPU 如何执行一次请求？ | wireframe |
| 图1-8 | 1.7 后 | Compute Bound 与 Memory Bound 如何区分？ | wireframe |
| 图1-9 | 1.8 后 | 如何观察和定位瓶颈？ | wireframe |
| 图1-10 | 1.9 后 | 如何从现象走到诊断路径？ | wireframe |

## 修改优先级

P0：

- 保持当前正文和 10 张 wireframe 的链接有效。
- 将 `storyboard.md` 状态更新为 `wireframe`。
- 跑图号、链接和插图校验。

P1：

- 为 `图1-7` 增加更明确的 GPU 生命周期正文支撑。
- 为 10 张图补详细 storyboard，而不仅是索引。

P2：

- 用户确认 storyboard 后，再将 wireframe 升级为正式插图。
- 补充真实 GX10 环境下的 baseline 记录模板。

## 验收建议

当前阶段建议验收为“第1章正文 + 10 张 wireframe 初稿完成”。下一步最有价值的动作是选择 1-2 张关键图，例如图1-1和图1-4，先补详细 storyboard，再升级为正式插图。
