# 课程 04：《LLM 推理性能工程实战》

> 副标题：从模型原理、性能分析到 Serving 与 Agent 优化

本文件说明这个目录下各个子文件夹的用途，避免"哪个是当前版本、哪个是历史遗留"混淆。

## 目录结构

| 路径 | 状态 | 说明 |
|---|---|---|
| `content/` | **面向读者的正文目录** | 30 章 / 7 Part 正文、插图与插图测试。课程结构以 V0.2 大纲为准。 |
| `strategy/` | **面向我们自己的策略目录** | 课程设计、编辑、实验规范与逐章审阅记录，不进入读者手中的正文。入口见 [`strategy/README.md`](strategy/README.md)。 |
| `code/` | **当前 Demo 代码目录** | 按 `code/chapterNN/` 组织已实现的章节 Demo，入口见 [`code/README.md`](code/README.md)。 |
| `index.html` | 已发布落地页 | 面向学员的宣传主页，内容与仓库内 `LLM 推理性能优化实战/index.html` 保持同步（同一份文件的两个副本，手动同步）。 |
| `ref/` | 参考资料 | 写作时用到的外部链接和图片，非课程正文。 |
| `_archive/lesson/` | **历史遗留，不是当前基线** | 旧版 18 讲课堂讲稿（slides.html + 学生材料 + demo 脚本），对应已废弃的"8 篇"旧大纲，章节编号与当前 30 章体系不对应。保留用于参考讲稿结构；可复用内容已提取到 `docs/teaching-assets/`。 |

2026-09-08 确认 V0.2 方案：保留现有推理优化主线，并吸收两本参考书中与主线直接相关的方法。权威课程结构见 [`strategy/course-design/02_Course_Outline_v0.2.md`](strategy/course-design/02_Course_Outline_v0.2.md)，正文迁移关系见 [`strategy/course-design/04_Content_Migration_Plan_v0.2.md`](strategy/course-design/04_Content_Migration_Plan_v0.2.md)，Demo 交付关系见 [`strategy/course-design/30章-Demo映射-v0.2.md`](strategy/course-design/30章-Demo映射-v0.2.md)。旧版本文档只保留历史记录与跳转说明。

当前章节 Demo 统一从 [`code/README.md`](code/README.md) 进入。目录按 `code/ch01`、`code/ch02`……命名；尚未实现的章节只登记状态，不保留空目录。

## Lesson 与 Workshop 的区别

课程里出现过两种"配套练习"格式，容易混淆，这里明确区分：

**Lesson（`_archive/lesson/lesson-NN/`，历史遗留格式）**
- 单位是"一整节课"：60-75 分钟的完整课堂讲稿，含逐分钟时间轴、讲授要点、课堂提问、`slides.html` 幻灯片和 `学生材料-播放版.html` 学生讲义。
- 目标是"如何把一章内容讲成一节完整的课"，是**教学交付格式**。
- 按旧版 8 篇大纲编号（lesson-01~18），与当前 30 章体系的章节号不再一一对应，需要重新映射才能复用。

**Workshop（`content/workshops/`，当前格式）**
- 单位是"一个可复现实验"：固定五步结构——环境搭建 → 性能脚本加压制造瓶颈 → 执行优化措施 → 重跑相同脚本验证 → 对比总结，针对**一个具体优化技术**（如 PagedAttention、Continuous Batching）。
- 目标是"如何让学员亲手复现一次性能问题、亲手验证一次优化收益"，是**动手实验格式**，对应 `strategy/course-design/01_Course_Design.md` 里"验证收益"这一步的操作化落地。
- 按 V0.2 的 30 章体系重新映射，具体状态见 [`strategy/course-design/30章-Demo映射-v0.2.md`](strategy/course-design/30章-Demo映射-v0.2.md)。

两者不是互斥关系：一节完整的课（Lesson 形态）完全可以把某个 Workshop 实验作为它的“动手环节”。如果后续要重新制作课堂讲稿，可以参考 `_archive/lesson/` 的时间轴和讲授节奏结构，但内容和章节编号必须对齐 `strategy/course-design/02_Course_Outline_v0.2.md`，不能直接照搬旧编号。
