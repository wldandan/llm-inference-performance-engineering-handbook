# Chapter 4 Integration Report

## 已回填图片

- 图 4-1：从文本到下一个 token。
- 图 4-2：Decoder-only Transformer Block。
- 图 4-3：Causal Self-Attention。
- 图 4-4：MHA 与 GQA。
- 图 4-5：Prefill。
- 图 4-6：Sampling。
- 图 4-7：Decode 与 KV Cache。
- 图 4-8：Demo 输出模型机制报告。

## 修改位置

- 图 4-1 位于模型生成总路径之后。
- 图 4-2 位于 Decoder Block 与 SwiGLU 数据流之后。
- 图 4-3 位于 Causal Attention 公式和 Mask 说明之后。
- 图 4-4 位于 GQA Head 形状说明之后。
- 图 4-5 位于 Prefill 产生首个 token 的顺序说明之后。
- 图 4-6 位于 Sampling 停止条件说明之后。
- 图 4-7 位于普通 Decode 与 KV Cache 更新说明之后。
- 图 4-8 位于离线 Demo 报告结构之后。

## 图号检查

正文只包含图 4-1 到图 4-8，编号连续，alt 文本和图注与 Storyboard 一致。

## 路径检查

8 个相对 SVG 路径和 8 份 figure-note 均存在，文件名与 Storyboard、视觉测试一致。

## 图文一致性

- 图 4-1 将模型计算输出 Logits 与 Sampling 选择 token 分成两个动作。
- 图 4-2 保留两条 Residual Connection，没有把 Attention 与 MLP 画成并行分支。
- 图 4-3 表达 Q/K 形成权重、权重汇总 V，并保留 Causal Mask。
- 图 4-4 明确 14 个 Query Heads 按 7 个一组共享 2 组 K/V。
- 图 4-5 同时表达 Prefill 写 Cache 与产生最后位置 Logits。
- 图 4-7 的循环从采样结果返回下一步输入，Cache 每步增加 1。
- 图 4-8 明确标记合成报告，不把离线计算包装成真实 Benchmark。

## 未解决问题

尚未在课程指定模型与 GPU 环境运行 `LLM 推理性能优化实战/workshops/00-model-internals`，因此没有交付真实张量快照和运行环境报告。

## 验收结果

正文、Storyboard、最终 SVG、figure-note、Demo、图片链接和图号已经对齐；单元测试、视觉契约、XML 解析与原尺寸渲染检查通过。
