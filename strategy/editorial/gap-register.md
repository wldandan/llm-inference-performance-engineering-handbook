# 书稿、代码与 Workshop 缺口清单

> 盘点日期：2026-09-08  
> 原则：只记录从当前仓库可复现的缺口；未执行的 GPU / 多卡 / 多机结论统一标记为“待验证”。

## P0：阻断“可信交付”

| ID | 缺口 | 证据 | 影响 | 建议验收 |
|---|---|---|---|---|
| P0-01 | 权威大纲指向不一致 | `02_Course_Outline.md` 自称“历史大纲”；当前 30 章权威文件是 `02_Course_Outline_v1.0.md`，但 `01_Course_Design.md`、`03_Course_Template.md`、Workshop 总纲和多个评审文件仍指向前者 | 章号、边界和 Workshop 归属会继续漂移 | 全库活跃文档只使用 v1.0 编号；历史文件明确隔离 |
| P0-02 | 项目路径迁移未闭环 | 根 `README.md` 仍把已不存在的 `LLM 推理性能优化实战/` 称为当前权威版；实际内容在 `content/` | 新老命令、链接、技能脚本和校验程序可能找错目录 | 根 README、写作技能、校验脚本和 CI 统一识别 `content/` |
| P0-03 | 章节校验脚本在真实仓库布局下失败 | 运行 `python3 content/scripts/validate_part.py --chapter 7` 报“根目录下缺少 ch07”，实际路径是 `content/ch07/` | 无法用项目规定命令验收正文、图和链接 | 先写一个在当前布局下失败的测试，修正根路径后确认 `--chapter 7` 通过 |
| P0-04 | Workshop 公共报告契约有 2 项失败 | `content/workshops/common/` 的 22 项测试中，`schema_version` 与 `input_tokens` / `output_tokens` 分布相关测试报 `KeyError` | 优化前后报告无法满足版本化和工作负载可重现要求 | 按现有失败测试最小实现字段，确认 22/22 通过，并生成一份符合 Schema 的样例报告 |
| P0-05 | 绝大多数性能结论没有原始实验产物 | 现有 Workshop 明确说明 GPU 无法实跑；总纲也承认预期现象仍是定性描述 | 不能把“预期收益”作为已验证书稿结论 | 每个核心 Demo 保留环境清单、配置、原始 JSON/CSV/Trace、重复次数和统计摘要；未完成前统一写“待验证” |

## P1：影响“一章一闭环”

| ID | 缺口 | 当前现状 | 建议优先动作 |
|---|---|---|---|
| P1-01 | Chapter 8–30 缺少对应 `code/chapterNN/` | 只有 Chapter 1–7 有独立代码目录 | 按 Ch8 Benchmark → Ch10/11 诊断 → Ch23/24 RAG/Agent 的 Core 路线优先建设 |
| P1-02 | Workshop 与 30 章新编号不一致 | 总纲仍使用 Ch12 / Ch16 / Ch20 / Ch24 的旧优化章号 | 迁移到 Ch14 / Ch18 / Ch22 / Ch27–29，并在每个 Workshop README 写明主章与次要复用章 |
| P1-03 | 13 个 Workshop 样板只有 7 个目录含代码 | PagedAttention、FlashAttention、Cache-aware Routing、PD 分离、TP/PP、MoE/EP、Scale-out 仍停留在总纲文字 | 先建立 Core 单卡 Workshop，再做需多卡/多机的 Advanced Workshop |
| P1-04 | Workshop 实验元数据不统一 | 现有说明书未统一包含目标、前置知识、准备时间、步骤、预期输出、练习、排错和证据边界 | 以 `workshops/01-global-performance-model/README.md` 为元数据样板，将五步实验嵌入其中 |
| P1-05 | 章节正文与代码的 API 漂移没有自动检查 | 现有校验主要覆盖目录、图、链接和局部结构 | 新增正文命令可执行性、字段名与输出 Schema 校验 |
| P1-06 | 性能证据没有统一存放契约 | 当前未见通用的 run manifest、环境指纹和原始报告目录约定 | 定义 `runs/<date>-<scenario>/manifest.json + raw/ + summary.json`，并让书稿表格引用 run ID |

## P2：一致性与教学可用性

| ID | 缺口 | 证据 | 建议 |
|---|---|---|---|
| P2-01 | QA 章号过时 | `strategy/course-design/QA.md` 仍将 Global Performance Model 标为 Chapter 5，将 Prefill/Decode 分析标为 Chapter 11/15 | 按 v1.0 更新为 Ch7 / Ch13 / Ch17，并增加链接而不只写章号 |
| P2-02 | `.learnings/` 同时存在 29 章和 30 章规则 | 旧 pending 经验仍宣称 29 章，新 promoted 经验要求 v1.0 30 章 | 将已失效经验标为 superseded，保留历史但不再作为写作输入 |
| P2-03 | 章节篇幅和证据密度不均 | Chapter 1–7 约 5.9k–14.4k 字符，Chapter 14–30 多数约 3.8k–4.4k；后半部又缺 Demo 引用 | 优先补“问题场景—代码—实验—结果—练习”，不为字数而扩写 |
| P2-04 | Workshop 难度与准备时间未分级 | Course Design 已把此列为未定义内容 | 按 Level 1/2/3 增加硬件、下载、编译、授课与重跑时长 |
| P2-05 | 课后练习缺少可自动验收的产物契约 | 多数练习为讨论题，没有明确提交物或检查方式 | 每个 Workshop 至少产出一份 JSON/CSV/Trace、一份分析报告和一个可自动检查的条件 |

## 建议的交付顺序

1. 先修复 P0-03 和 P0-04，恢复章节验收与 Workshop 报告契约。
2. 再统一 P0-01 / P0-02，让所有新工作侜用于正确的 30 章与 `content/` 路径。
3. 用 Chapter 7 + Workshop 01 作为编辑基准，补 Chapter 8 的 Benchmark 闭环。
4. 沿 Core Track 依次建设 Ch10/11、Ch14/15、Ch18/19、Ch23–25。
5. 最后在 Level 3 资源准备好后验收 Ch28–29，期间保持“待验证”。

