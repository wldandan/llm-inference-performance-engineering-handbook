# Chapter 2 Integration Report

## 已回填图片

- 图 2-1：推理请求生命周期与关键时间点。
- 图 2-2：业务任务、LLM 调用与推理请求是三个不同层级。
- 图 2-3：归一化状态机保留主路径，也允许取消和失败提前结束请求。
- 图 2-4：只有明确 queued 和 scheduled 两个时间点，Queue 才有可复核的边界。
- 图 2-5：Prefill 连接首次调度与服务端首 token，客户端首 chunk 还要经过返回链路。
- 图 2-6：一条请求跨越多个 Decode step，KV Cache 随生成长度增长。
- 图 2-7：服务端首 token、首个网络 chunk 和客户端首包属于三个观测点。
- 图 2-8：成功、取消和失败走不同终态，但都汇入资源与状态清理。
- 图 2-9：主 Demo 同时收集客户端、请求级服务端和服务端聚合证据；离线 JSONL 分析器只作辅助。
- 图 2-10：本章定义生命周期，架构、指标、分析和优化分别由后续章节展开。

## 修改位置

- 图 2-1 位于核心问题之后，作为全章生命周期总览。
- 图 2-2 位于 2.1 Business Task / LLM Call / Inference Request 三层说明之后。
- 图 2-3 位于 2.2 归一化事件序列与 Event/State/Phase/Duration 辨析之后。
- 图 2-4 位于 2.3 六个时间点与阶段公式之后。
- 图 2-5 位于 2.5 Prefill 到首 token 的顺序说明之后。
- 图 2-6 位于 2.6 Decode step 与 KV 追加数据流之后。
- 图 2-7 位于 2.7 四个流式观测点定义之后。
- 图 2-8 位于 2.8 三类终态与资源清理说明之后。
- 图 2-9 位于 2.9 Demo 的三类证据与四级证据表之后。
- 图 2-10 位于 2.11 常见误区之后，作为章节边界收口。

## 图号与路径检查

正文只包含图 2-1 到图 2-10，编号连续无跳号；10 个 SVG 路径、10 份 figure-note 与 `storyboard.md` 定义一致，`content/ch02/figures/test_figures.py` 的 4 项检查与 10 项 subtest 通过。

## 图文一致性

- 图 2-1 的阶段条只表达生命周期区间，不标注任何实测毫秒数。
- 图 2-3 把 cancelled 与 failed 画成旁路终态，不画成主路径的一个后继节点。
- 图 2-4 明确 queued 与 scheduled 是两个独立时间点，不把 Queue 画成"系统闲置"。
- 图 2-5 把服务端首 token 与客户端首 chunk 画在不同泳道，不连成同一时刻。
- 图 2-6 的 KV Cache 随 step 增长，但不给出容量数值或显存结论。
- 图 2-7 三个观测点各自独立，不用箭头暗示三者可以相减得到网络耗时。
- 图 2-9 区分主 Demo（真实 vLLM 三类证据）与离线 JSONL 分析器，后者标为辅助，不冒充 GPU 实测。

## 未解决问题

图 2-9 描述的主 Demo 产物 `content/ch02/evidence/gx10-real-lifecycle-report.json` 尚未在 GX10 生成，本章真机门禁仍未关闭。现有 `content/ch02/evidence/gx10-streaming-client-report.json` 只覆盖客户端观测层（见 2.9.2），不能替代完整生命周期证据。

## 验收结果

正文、storyboard、SVG、figure-note、图号与路径已经对齐；插图契约测试通过。真机证据待补，不影响图文一致性验收。
