# 第1章 LLM 推理流程

## 本章定位

本章是整门课的入口，目标不是马上调参数，而是建立一张完整的推理性能地图。后续章节讲 TTFT、ITL、Profiling、FlashAttention、KV Cache、PagedAttention、Batching、Speculative Decoding 时，都会回到同一个问题：一次请求从进入推理服务到吐出最后一个 token，中间到底发生了什么，时间和显存花在了哪里。

本章建议授课时长：60-75 分钟。

## 60 分钟授课节奏

| 时间 | 模块 | 目标 |
|---|---|---|
| 0-5 分钟 | 课程导入 | 明确“推理性能优化”关注的是在线请求，而不是训练吞吐 |
| 5-15 分钟 | Transformer 推理回顾 | 讲清 embedding、attention、MLP、采样和自回归生成 |
| 15-28 分钟 | Prefill 阶段 | 解释为什么首 token 前要处理完整 prompt，以及为什么常见为 compute bound |
| 28-40 分钟 | Decode 阶段 | 解释逐 token 生成、KV Cache 读取、batch 调度和 memory bound |
| 40-50 分钟 | GPU 与 KV Cache 生命周期 | 把 kernel、HBM、显存增长和请求生命周期串起来 |
| 50-60 分钟 | Demo 与课堂讨论 | 运行 `ch01/demo.py`，观察一次真实 vLLM 流式请求生命周期 |
| 60-75 分钟 | 延展讨论 | 连接后续章节：指标、profiling、attention、cache、batching |

## 学习目标

完成本章后，学员应能够：

- 画出一次 LLM 请求从 prompt 到最后一个 token 的生命周期。
- 区分 prefill 和 decode 的输入、输出、主要计算形态和性能瓶颈。
- 解释 TTFT 为什么主要受 prefill 影响，ITL 为什么主要受 decode 影响。
- 描述 KV Cache 在请求生命周期中的创建、增长、读取和释放。
- 初步判断一个性能现象更可能是 compute bound、memory bound、调度受限，还是容量受限。
- 用结构化方式描述一次真实推理请求从进入服务到流式返回结束的过程。

## 1. 从在线推理问题开始

训练优化通常追求更高的训练 tokens/s、更好的 GPU 利用率和更短的训练周期。推理优化面对的是另一类问题：

- 用户是否能尽快看到第一个 token。
- 后续 token 是否稳定输出，是否有卡顿。
- 多个用户同时请求时，总吞吐是否上得去。
- 长 prompt 或长输出是否导致显存和延迟失控。
- 优化吞吐时，单个请求的 P95/P99 延迟是否被牺牲。

因此，推理性能优化不能只看一个数字。TPS 很高但 TTFT 很差，用户仍然会觉得慢；GPU 利用率很高但 P99 延迟爆炸，在线服务仍然不可接受。

课堂提问：

- 一个模型服务“平均 tokens/s 很高”，是否一定代表用户体验好？
- 当用户抱怨“第一次响应太慢”和“输出过程一卡一卡”，分别应优先观察哪些阶段？

## 2. Transformer 推理流程回顾

一次典型的 decoder-only LLM 推理包含以下步骤：

1. 文本经过 tokenizer 转成 token ids。
2. token ids 进入 embedding 层，得到向量表示。
3. 每一层 Transformer block 执行 attention、MLP、残差连接和归一化。
4. 最后一层输出经过 lm head 得到下一个 token 的 logits。
5. 采样器根据 temperature、top-p、top-k、repetition penalty 等策略选出下一个 token。
6. 新 token 追加到上下文，继续下一轮 decode，直到遇到停止条件。

这里最重要的事实是：LLM 是自回归生成。模型一次通常只预测下一个 token，而不是一次性生成完整答案。这个事实直接决定了 decode 阶段会反复执行很多次，也决定了 KV Cache 的价值。

### 2.1 Attention 的直觉

Attention 的作用是让当前 token 读取上下文中其他 token 的信息。对于一个长度为 `L` 的 prompt，prefill 阶段需要处理整个序列中的 token 关系；而 decode 阶段每次只新增一个 token，但它需要读取已有上下文的 KV Cache。

可以用一句话区分：

- Prefill：一次性处理已有 prompt，建立完整上下文状态。
- Decode：每轮追加一个 token，并读取已有上下文状态。

## 3. Token 生成过程

Token 生成不是“模型把一句话吐出来”，而是一个循环：

```text
prompt tokens
  -> prefill
  -> logits for first generated token
  -> sample token_1
  -> decode token_1
  -> sample token_2
  -> decode token_2
  -> ...
  -> EOS / max_tokens / stop words
```

每一轮 decode 的输入包括：

- 上一轮刚生成的 token。
- 历史上下文对应的 KV Cache。
- 当前请求的生成参数。
- 调度器分配给本轮的 batch 位置和 GPU 资源。

这也是为什么输出长度增加时，总延迟几乎会线性增长：decode 轮数增加了。

## 4. Prefill 阶段

Prefill 是从 prompt 到第一个 token 前的阶段。它的工作包括：

- 处理完整 prompt token 序列。
- 为每一层 attention 计算 Q/K/V。
- 建立后续 decode 会反复读取的 KV Cache。
- 得到第一个待采样 token 的 logits。

### 4.1 Prefill 为什么影响 TTFT

TTFT 表示 Time To First Token，即请求发出后到第一个生成 token 出现的时间。第一个 token 出现前，系统必须完成排队、调度、tokenization、prefill、采样和网络返回，其中 prefill 通常是核心开销之一。

Prompt 越长，prefill 处理的 token 越多，attention 和 MLP 的计算量越大。对于长上下文请求，TTFT 往往比 ITL 更容易先恶化。

### 4.2 Prefill 常见瓶颈

Prefill 常见为 compute bound，因为它有大量矩阵乘和 attention 计算，能比较充分地使用 Tensor Core 和 SM。判断时不要只凭直觉，应结合：

- SM 利用率是否高。
- Tensor Core 利用是否充分。
- HBM 带宽是否接近上限。
- Kernel timeline 中 GEMM/attention kernel 是否占主导。
- 改变 prompt length 时 TTFT 是否快速增长。

### 4.3 Prefill 相关优化方向

后续课程会展开：

- FlashAttention / FlashInfer：减少 attention 的访存和中间结果。
- Chunked Prefill：将长 prompt 分块，改善调度公平性。
- Prefix Cache：复用相同前缀，降低重复 prefill 成本。
- Prompt 管理：减少无效上下文，控制输入长度。

## 5. Decode 阶段

Decode 是第一个 token 之后的逐 token 生成阶段。每生成一个 token，都要执行一次或多次模型前向计算。

Decode 的关键特点：

- 每次新增 token 数很少，通常是每个请求 1 个 token。
- 需要读取已有上下文的 KV Cache。
- 输出越长，decode 循环次数越多。
- 单步计算粒度小，调度和 kernel launch 开销更明显。
- 多请求并发时，batching 策略对吞吐影响很大。

### 5.1 Decode 为什么影响 ITL

ITL 表示 Inter-Token Latency，即相邻输出 token 的间隔。用户看到流式输出时，体感是否顺滑，很大程度由 ITL 决定。

如果 ITL 偏高，常见原因包括：

- KV Cache 读取带宽压力大。
- batch 太小，GPU 没吃满。
- batch 太大，单请求等待时间增加。
- 请求长度差异大，调度效率低。
- kernel launch 或同步开销明显。
- 采样、后处理或网络发送成为瓶颈。

### 5.2 Decode 常见为 memory bound

Decode 阶段每一步需要读取每层历史 token 的 K/V。随着上下文变长，KV Cache 读取量增加。相比 prefill，decode 的矩阵计算规模较小，访存压力更容易成为瓶颈。

判断 decode 是否 memory bound，可以观察：

- HBM bandwidth 是否接近上限。
- SM 利用率不高但内存带宽很高。
- 上下文越长，ITL 越明显变差。
- KV Cache 量化或分页管理带来明显收益。

## 6. GPU 生命周期视角

从 GPU 看，一次请求不是一个单独 kernel，而是一串 kernel 的组合：

1. 输入 token 准备和拷贝。
2. Prefill 阶段的大块 attention / GEMM kernel。
3. KV Cache 写入。
4. Decode 阶段反复执行较小粒度 kernel。
5. KV Cache 读取和更新。
6. 采样、同步、返回 token。
7. 请求结束后释放或复用缓存块。

Profiling 时要避免只看平均 GPU utilization。平均值可能掩盖尖峰、空洞、排队和同步等待。更好的方式是看 timeline：每一段空白为什么出现，每一个 kernel 为什么等待。

## 7. KV Cache 生命周期

KV Cache 是推理性能优化的核心对象之一。它缓存每一层 attention 中历史 token 的 K/V，避免每次 decode 都重新计算完整上下文。

生命周期如下：

```text
请求进入
  -> 分配 cache block
  -> prefill 写入 prompt 的 K/V
  -> decode 每步读取历史 K/V
  -> decode 写入新 token 的 K/V
  -> 请求完成
  -> cache 释放、复用或保留为 prefix cache
```

KV Cache 的显存占用与以下因素有关：

- 层数。
- hidden size / attention heads / kv heads。
- dtype，例如 FP16、FP8、INT8。
- prompt length。
- generated tokens。
- batch size / concurrency。

直觉公式：

```text
KV Cache 显存 ≈ 层数 × token 数 × KV hidden 维度 × 2(K 和 V) × dtype bytes
```

这不是精确工程公式，但足够帮助学员理解：上下文长度、并发和 dtype 是显存压力的关键变量。

## 8. Compute Bound vs Memory Bound

性能优化的第一步不是“开某个优化选项”，而是判断瓶颈类型。

### 8.1 Compute Bound

Compute bound 表示主要受计算能力限制。典型现象：

- SM / Tensor Core 利用率高。
- HBM 带宽未必打满。
- 增加计算量时延迟明显增长。
- 更快的矩阵计算 kernel、Tensor Core、算子融合可能有效。

Prefill 更容易出现 compute bound。

### 8.2 Memory Bound

Memory bound 表示主要受数据读取和写入限制。典型现象：

- HBM 带宽高。
- SM 利用率可能不满。
- 上下文变长后 ITL 恶化。
- 减少读取量、优化 cache layout、量化 KV Cache 可能有效。

Decode 更容易出现 memory bound。

### 8.3 其他瓶颈

真实服务还可能遇到：

- Scheduling bound：调度策略导致 GPU 等待或请求等待。
- Capacity bound：显存容量限制 batch 或上下文长度。
- CPU bound：tokenization、采样、后处理或网络栈拖慢。
- Synchronization bound：频繁同步导致 GPU pipeline 被打断。

## 9. Demo：观察一次推理过程

本章代码目录：

```text
lesson/lesson-01/ch01
```

本章 Demo 只做两件事：

1. 使用 vLLm 启动一个 OpenAI-compatible 服务。
2. 使用脚本访问这个服务，观察一次真实流式请求从进入服务到结束的过程。

系统性的 TTFT、ITL、TPS、P95/P99 和 GPU 利用率实验放到第2章。本章只要求学员把请求生命周期跑通。

### 9.1 启动 vLLM 服务

如果模型可以通过模型 id 解析：

```bash
cd lesson/lesson-01/ch01
python3 start_vllm.py \
  --model Qwen/Qwen2.5-0.5B \
  --served-model-name Qwen/Qwen2.5-0.5B \
  --host 0.0.0.0 \
  --port 8000
```

如果模型已经在 GX10 本地目录：

```bash
cd lesson/lesson-01/ch01
python3 start_vllm.py \
  --model /home/admin/models/Qwen2.5-0.5B \
  --served-model-name Qwen/Qwen2.5-0.5B \
  --host 0.0.0.0 \
  --port 8000
```

### 9.2 确认服务可访问

```bash
curl http://127.0.0.1:8000/v1/models
```

如果服务在远程 GX10 上，可以使用 SSH tunnel：

```bash
ssh -L 8000:127.0.0.1:8000 <user>@<gx10-host>
```

### 9.3 发送一次流式请求

运行：

```bash
cd lesson/lesson-01/ch01
python3 demo.py \
  --base-url http://127.0.0.1:8000/v1 \
  --model Qwen/Qwen2.5-0.5B \
  --prompt "请解释一次 LLM 在线推理请求从 Prompt 到完整回答的过程。" \
  --max-tokens 128 \
  --requests 1 \
  --concurrency 1
```

观察问题：

- 请求是否成功。
- 原始 prompt 是否出现在输出中。
- 是否先等待首个流式 chunk。
- 后续 chunk 是否持续返回。
- 请求结束后是否有 token usage。

示例输出字段：

```json
{
  "model": "Qwen/Qwen2.5-0.5B",
  "prompt": "请解释一次 LLM 在线推理请求从 Prompt 到完整回答的过程。",
  "summary": {
    "requests": 1,
    "successes": 1,
    "failures": 0
  },
  "results": [
    {
      "success": true,
      "prompt_tokens": 36,
      "output_tokens": 128,
      "stream_chunks": 128
    }
  ]
}
```

### 9.4 课堂讨论

讨论时不要评价指标好坏，只回答：

- 请求进入服务前后，哪些步骤发生在服务侧？
- 首个 chunk 返回前，服务可能在做什么？
- 后续 chunk 持续返回时，对应的是 Prefill 还是 Decode？
- 请求结束后，KV Cache 会如何处理？

## 11. 常见误区

### 误区 1：GPU 利用率越高越好

GPU 利用率高只是说明 GPU 忙，不说明请求体验好。在线推理需要同时看 TTFT、ITL、P95/P99、吞吐和错误率。

### 误区 2：吞吐提升就是优化成功

吞吐提升可能来自更大的 batch，但更大的 batch 可能增加排队和单请求延迟。如果业务是交互式聊天，需要明确延迟预算。

### 误区 3：所有慢都靠 FlashAttention 解决

FlashAttention 主要改善 attention 相关计算和访存模式。如果瓶颈在调度、KV Cache 容量、CPU tokenization 或网络返回，它不会解决根因。

### 误区 4：Prefill 和 decode 可以用同一套直觉优化

Prefill 更像“大块计算”，decode 更像“反复读取历史状态的小步循环”。二者指标、瓶颈和优化策略不同。

## 12. 本章总结

一次 LLM 推理请求可以拆成 prefill 和 decode 两个主阶段。Prefill 负责处理完整 prompt 并生成第一个 token 前的上下文状态，通常强影响 TTFT；decode 负责逐 token 生成，通常强影响 ITL 和总输出时间。KV Cache 连接了两个阶段：prefill 写入，decode 反复读取和追加。

后续所有优化主题都可以放回这张图里理解：

- FlashAttention：优化 attention 计算和访存。
- CUDA Graph：降低重复执行路径的调度和 launch 开销。
- KV Cache / PagedAttention：控制显存增长和碎片。
- Prefix Cache：减少重复 prefill。
- Dynamic / Continuous Batching：改善吞吐和调度效率。
- Speculative Decoding：减少目标模型 decode 步数。

## 课后作业

1. 用自己的话画出 prefill 和 decode 流程图。
2. 运行 `ch01/demo.py`，保存一次真实请求的 JSON 输出。
3. 标注 JSON 输出中的 `prompt`、`stream_chunks`、`prompt_tokens`、`output_tokens` 分别对应请求生命周期的哪个位置。
4. 准备一个真实业务 prompt，说明它更可能在 Prefill 阶段重，还是 Decode 阶段重。

## 自检

- [ ] 能解释 Transformer 推理中的自回归循环。
- [ ] 能说明 prefill 的输入、输出和主要开销。
- [ ] 能说明 decode 的输入、输出和主要开销。
- [ ] 能解释 KV Cache 为什么能降低重复计算。
- [ ] 能把 vLLM 流式请求的输出字段对应回请求生命周期。
- [ ] 能初步区分 compute bound 和 memory bound 的现象。
- [ ] 能用本章 Demo 说明一次真实请求如何从 Prompt 走到完整回答。
