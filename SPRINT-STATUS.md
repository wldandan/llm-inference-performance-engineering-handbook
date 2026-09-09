# Sprint Status

## 当前 Sprint：V0.2 Part 1 内容与 Demo 交付

- 状态：正文已定稿，等实验室环境补录真机证据与配套代码
- 目标：完成 Part 1 五章正文和 `code/ch01`～`code/ch05`，并通过独立 Agent 审阅。
- 验收入口：`python3 scripts/test_part01_v0_2_delivery.py`

## 本轮完成（2026-09-09）

**流式证据归属修正。** 原 Ch1 正文已改写为同步调用（`stream=false`），但流式的配套资产和下游引用没有跟着改，导致 Ch3/Ch4/Ch5 引用了一份 Ch1 不可能产出的 chunk 数据。本轮把流式整体迁往 Ch2：

- `code/ch01/demo.py` → `code/ch02/streaming_client.py`
- `content/ch01/evidence/gx10-run-report.json` → `content/ch02/evidence/gx10-streaming-client-report.json`
- Ch2 新增 2.9.2，说明这份报告只覆盖客户端观测层，不能关闭本章真机门禁
- Ch3、Ch4、Ch5 共 11 处引用改指 Ch2

**Ch1 精简。** 原 1.8 课堂案例与 1.9 常见误区合并为 `1.8 课堂案例与常见误区`：三个案例平级化为案例一/二/三，误区从 5 条收到 2 条（删除与 1.3 三层检查表、1.7 失败定位表、案例一重复的三条）作为收尾子节。Ch1 由九节变为八节。同时修正学习目标与 Checklist 的表述问题。

## 待办：需要实验室环境（GX10）

| 项 | 说明 | 阻塞的验收 |
|---|---|---|
| Ch1 同步版 `demo.py` | 流式版已迁往 Ch2，Ch1 需要 `stream=false` 的替代实现 | `test_code_layout_matches_chapter_topics` |
| Ch2 完整生命周期报告 | 需带 `--enable-per-request-metrics` 启动 vLLM 后运行 `capture_lifecycle.py` | `test_chapter02_has_complete_real_gx10_evidence` |
| Ch1 同步运行证据 | 原证据已归 Ch2，Ch1 需重新采一份同步响应记录 | 无自动门禁，属证据缺口 |
| Ch1 四张插图 | 现有 4 张 SVG 仍是旧版流式主题，正文已不引用 | `content/ch01/test_figures.py` |
| `strategy/reviews/ch01/` 三份记录 | 三份记录仍描述旧版流式 Ch1，引用了已不存在的小节号 | 无自动门禁 |
| Ch1/Ch2 报告补录 `vllm_version` | 现有 GX10 报告该字段为 `null`，不能用于跨环境比较 | 无自动门禁 |

## 待办：正文改写

**去掉正文里的 Core Track / Advanced Track 分层标签。** 分层是课程设计的组织方式，属于作者视角；读者不需要知道自己在读哪一层，正文只写内容本身与边界。

Ch2 已改完（章首两段合并为"本章不展开哪些事件"、`Core Demo` → `Demo`、`Core Checklist` → `本章 Checklist`、`Advanced 延伸` → `延伸方向`），内容实质全部保留。

剩余待改（Ch3～Ch5 本轮暂不动，按用户要求）：

| 章节 | 处数 | 说明 |
|---|---|---|
| Ch4 | 12 | 最集中：章首三段定位、4.6 选读段、`Core Checklist`/`Advanced 延伸`、课后练习第 4 题 |
| Ch11 | 7 | 骨架章，待正文展开时一并处理 |
| Ch3 | 1 | |
| Ch10 | 1 | |
| Ch13 | 1 | |

注：Ch4 的 12 处中有 4 处（69、125、184、200 行）指的是 Advanced **附录**或多 GPU 内容位置，属于正常的交叉引用，不是分层标签，改写时需要区分。

## 已决事项

**Ch1 不设独立 Demo 小节。** Ch1 的 demo 就是 1.2–1.6 的 curl 流程，模板要求的五项（实验目的、环境与输入、操作步骤、观察指标、预期现象）已分别落在核心问题、1.1、1.2/1.4、1.5、1.5+1.7。第一章用一条能看懂全貌的裸 curl，比先让读者读 Python 脚本更合适。

因此 `test_each_chapter_has_a_complete_teaching_shape` 里对 Ch1 断言字符串 `Demo` 的那一条不成立，应改为检查别的标志；在改之前它会持续失败。这是测试要跟随内容，不是内容要迁就测试。

## 当前测试状态

- `scripts/test_part01_v0_2_delivery.py`：9 项中 **3 项失败** —— Ch1 `demo.py` 缺失、Ch2 真机报告未生成，以及上述 Ch1 `Demo` 断言
- `code/ch01`～`ch05`：66 项通过（ch01 2、ch02 27、ch03 8、ch04 15、ch05 14）
- 插图契约：ch02～ch05 全部通过；**ch01 失败**（正文 0 处图片引用，期望 4 处）

## 已知文档偏差

`strategy/course-design/PART01_DELIVERY_REPORT.md` 的测试计数与 Ch1 描述停留在流式迁移之前，尚未更新。
