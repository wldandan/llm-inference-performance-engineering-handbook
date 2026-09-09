# Chapter 3 Demo：Transformer 生成机制报告

这个 Demo 用纯 Python 展示三件事：

1. 根据模型配置推导 Token、Hidden State、Q/K/V 和 Logits 的形状。
2. 把 Logits 经过 Temperature 与 Top-k 转成概率并采样。
3. 生成一条 Prefill 加多步 Decode 的事件记录，观察 KV Cache 长度变化。

它不加载真实模型，不测量性能，也不输出优化结论。报告中的 Logits 和 token ID 都是教学数据。

Demo 的 `temperature` 必须大于零。部分推理 API 用 `temperature=0` 表示 Greedy Decoding，但这里的 `softmax()` 保持数学定义，不接受除零；Greedy 的概念由正文单独解释。

## 运行

从 Git 仓库根目录运行：

```bash
python3 code/ch03/mechanics.py \
  --prompt-tokens 8 \
  --decode-steps 4 \
  --temperature 1.0 \
  --top-k 3 \
  --seed 7
```

保存 JSON：

```bash
python3 code/ch03/mechanics.py --output mechanics-report.json
```

## 阅读输出

- shapes 展示各阶段张量形状，Q 有 14 个头，K/V 有 2 个头，用来说明 GQA。
- sampling 展示候选 token 的概率与最终选中的 token ID。
- execution_trace 的第 0 步是 Prefill，后续步骤是 Decode。
- Prefill 一次写入全部 Prompt 的 K/V；每个普通 Decode step 把 Cache 长度增加 1。

## 真实模型扩展

需要加载真实 Qwen2.5 模型时，继续运行 `content/workshops/00-model-internals`。该 Workshop 会读取真实 config、注册 forward hook，并观察 past_key_values 增长。它属于扩展实验，不改变本章 Demo 的离线可运行要求。

## 测试

```bash
python3 -m unittest discover -s code/ch03 -p 'test_*.py'
```
