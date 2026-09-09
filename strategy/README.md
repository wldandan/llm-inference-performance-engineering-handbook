# 策略目录：面向我们自己的文档

这里保存**写书的人**需要的文档：课程怎么设计、章节怎么写、实验怎么做、每章审到什么程度。
读者手里的正文只在 `../content/`，两边不再混在同一层。

判断标准：一份文档如果只在我们决定"下一步写什么、按什么标准验收"时才需要打开，它就属于这里。

## 目录

| 路径 | 内容 |
|---|---|
| [`course-design/`](course-design/) | 课程设计理念、权威大纲、章节模板、正文迁移计划、Demo 映射与 Part 1 交付/审阅报告 |
| [`editorial/`](editorial/) | 图书主编蓝图、写作样板、书稿—代码—Workshop 映射、缺口清单，入口见 [`editorial/README.md`](editorial/README.md) |
| [`architecture/`](architecture/) | 技术主线与实验架构、实验规范与指标体系、第一批 Spike 计划、experiment manifest 样例 |
| [`reviews/`](reviews/) | 逐章 `storyboard.md` / `review.md` / `integration-report.md`，按 `chNN/` 组织 |

## 权威基线

- 章号与标题：[`course-design/02_Course_Outline_v0.2.md`](course-design/02_Course_Outline_v0.2.md)
- 章节写作合同：[`course-design/03_Course_Template.md`](course-design/03_Course_Template.md)
- 实验与指标口径：[`architecture/实验规范与指标体系-v1.0.md`](architecture/实验规范与指标体系-v1.0.md)

## 与 content/ 的分工

- `content/chNN/` 只留 `chNN.md`、`figures/`（SVG、figure-note 与插图测试）和该章证据（如 `evidence/`）。
- 同一章的 storyboard 与审阅记录在 `reviews/chNN/`；正文里不写取舍理由，理由写进审阅记录。
- 结构校验入口不变：在 `content/` 下执行 `python3 scripts/validate_part.py --part N`，它会同时检查 `content/chNN/` 的正文插图和 `strategy/reviews/chNN/` 的审阅记录。
