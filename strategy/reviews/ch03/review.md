# Chapter Review

## 总体评价

第 3 章沿 token 生成顺序解释 Decoder-only Transformer、Attention、GQA、Prefill、Sampling、Decode 与 KV Cache。主课堂案例已绑定第 2 章 GX10 客户端流式报告的真实请求计数，离线脚本降为公式与形状检查器，不输出硬件性能结论。

## 结构问题

新增参数、临时激活和请求状态三类数据对照，补齐了模型权重与 KV Cache 之间的概念边界。真实请求的 30 个输入 tokens、256 个输出 tokens 和 254 个 chunks 被用于解释模型动作，不被写成性能测量。

## 技术与术语问题

GQA 已正确表述为 14 个 Query Heads、2 个 KV Heads，每个 KV Head 被 7 个 Query Heads 共享。Demo 要求 temperature 大于 0；temperature 为 0 时应走 greedy/argmax，不进入除法 Softmax。

## 内容缺口

现有真实报告只提供 token 与 chunk 计数，不提供内部张量。正文已明确区分“请求直接观测”和“依据 Transformer 定义解释的机制”。真实模型 Workshop 可补充张量证据，但不阻塞本章正文。

## 可删减内容

不加入 GPU、Kernel、量化、虚构耗时和吞吐比较，保持机制章节边界。

## 推荐插图位置

八张图按 Tokenizer、Block、Attention、GQA、Prefill、Sampling、Decode、Demo 排列，数量与概念密度匹配。

## 修改优先级

- P0/P1：无。
- P2：后续建立跨章术语索引时再补链接。

## 验收建议

验收重点是：真实 vLLM 报告负责请求计数，机制检查器负责形状推导、采样边界和 KV Cache 事件顺序；两类证据不能互相替代。代码验证留待代码阶段，本轮只检查正文与图文一致性。
