# `_archive/lesson` 提取分析（v1.0）

## 结论

`_archive/lesson` 不是一套可以直接并入当前课程的 18 章正文，而是一份旧版课堂交付草稿。它的有效信息集中在三处：

1. Lesson 01 对“从请求生命周期建立性能地图”的讲授节奏和课堂问题；
2. Lesson 02–18 反复出现的实验闭环：建基线 → 找瓶颈 → 改变量 → 验收益；
3. Lesson 08–18 对 KV Cache、Batching、Prefill、Decode、Benchmark 和综合调优的主题切分。

当前课程已经吸收了其中的技术主线，但仍缺少适合教师直接使用的课堂辅助材料。因此，本次提取为新的教学资产，不改变当前 30 章正文和 `code/` 目录的交付边界。

## 按资产类型判断

| 资产 | 判断 | 处理方式 |
|---|---|---|
| `lesson-01/README.md` | 高价值，但范围比当前 Chapter 1 更宽 | 提取授课节奏、课堂问题、常见误区和收束方式 |
| `lesson-01/slides.html` | 高价值，18 页内容相对完整 | 作为后续课件重制的内容底稿，不直接作为 v1.0 正文 |
| `lesson-01/学生材料-播放版.html` | 有课堂练习和观察提示 | 提取练习设计，不直接复用旧路径和旧章节编号 |
| `lesson-02`～`lesson-18` README | 低到中价值，结构高度重复 | 提取统一实验记录字段和自检方式 |
| `lesson-02`～`lesson-18` slides | 低价值，基本是同一套 6 页模板 | 不迁移，后续按当前 30 章重新制作 |
| `lesson-02`～`lesson-18` `demo.py` | 不适合作为正式 Demo | 不迁入 `code/`；只保留 CLI 参数和 JSON 输出的形式参考 |

## 为什么不直接迁移旧 Demo

旧 Demo 有三个共同问题：

- Lesson 02–18 的脚本基本使用同一套 `simulate_run` 公式，只更换章节描述，不能代表对应技术的机制；
- 输出是人为生成的合成指标，却容易被误读成真实 Benchmark；
- 没有与当前章节的输入、测试、证据链和优化验收标准对齐。

因此，当前 `code/` 目录只保留经过重构、带测试并与正文边界一致的章节 Demo。旧 Demo 的价值是告诉我们后续章节需要提供 CLI、JSON 报告和可替换的真实采集入口，而不是直接复用公式。

## 旧 Lesson 到当前 30 章的映射

| 旧材料 | 可提取主题 | 当前承接章节 | 处理结论 |
|---|---|---|---|
| Lesson 01 | 请求生命周期、Prefill / Decode、KV Cache、用户体验指标 | Ch01–Ch07 | 技术内容已拆散并重写；课堂节奏和讨论题已单独提取 |
| Lesson 02 | TTFT、ITL、TPS、P95/P99、GPU 指标 | Ch06、Ch08 | 保留指标清单和实验记录字段 |
| Lesson 03 | nvidia-smi、Nsight Systems、Nsight Compute、PyTorch Profiler | Ch09 | 保留工具地图；不保留旧版模拟 Demo |
| Lesson 04 | Prefill、Prompt Length、Compute Bound | Ch12–Ch15 | 作为 Prefill 章节的实验变量设计参考 |
| Lesson 05 | Decode、KV Cache、Memory Bound | Ch16–Ch19 | 作为 Decode 章节的变量和假设参考 |
| Lesson 06 | FlashAttention、FlashInfer、Kernel Fusion、Tensor Core | Ch14、Ch18 | 作为优化技术清单，需重新绑定证据和适用条件 |
| Lesson 07 | CUDA Graph、Persistent Kernel、Kernel Fusion | Ch17、Ch18 | 作为 Advanced 选修素材，不进入 Core 起步路径 |
| Lesson 08–11 | KV Cache、PagedAttention、Prefix Cache、KV Quantization | Ch16、Ch18、Ch19 | 形成 Decode 优化组合，不直接复制旧 Demo |
| Lesson 12–14 | Dynamic / Continuous Batching、Chunked Prefill | Ch14、Ch18、Ch20–Ch22 | 分别归入 Prefill、Decode 和 Serving 调度 |
| Lesson 15–16 | Speculative Decoding、MTP / Medusa / EAGLE | Ch18、Ch19 | 作为 Decode 加速选修或进阶实验 |
| Lesson 17 | Benchmark 变量、指标、实验记录 | Ch08 | 提取为 Benchmark Contract 的课堂练习 |
| Lesson 18 | 基线、定位、优化、回归验证 | Ch11、Ch19、Ch25、Ch30 | 作为综合项目的实验闭环，不承诺固定收益数字 |

## 已提取的新资产

- [课堂实验记录模板](teaching-assets/实验记录模板-v1.0.md)：将旧 lesson 反复出现的实验记录表升级为可用于 Benchmark、Profiling 和优化验证的统一模板。
- [课堂讨论卡](teaching-assets/课堂讨论卡-v1.0.md)：提取 Lesson 01 的课堂提问、常见误区和“现象 → 假设 → 证据”的引导方式。

## 保留与清理边界

`_archive/lesson/` 继续作为历史底稿保留，方便后续制作视频课件和回看旧版讲授节奏。它不进入学员默认导航，也不作为当前章节 Demo 的来源目录。

后续每建设一个新章节，优先从当前 30 章大纲和统一模板出发；只有在需要课堂表达、练习设计或案例问法时，才回看对应旧 lesson。
