# 第 3 章 Storyboard：Transformer 推理机制

本章插图只解释模型机制，不引入 GPU 性能结论、指标阈值或优化技术。

| 图号 | 标题 | 核心问题 | 状态 |
|---|---|---|---|
| 图3-1 | 从文本到下一个 token | 一次 token 生成经过哪些模型阶段？ | final v2 |
| 图3-2 | Decoder-only Transformer Block | Attention、MLP、Norm 与 Residual 怎样连接？ | final v2 |
| 图3-3 | Causal Self-Attention | 一个位置怎样读取允许访问的历史？ | final v2 |
| 图3-4 | MHA 与 GQA | Query Heads 与 KV Heads 的数量为何不同？ | final v2 |
| 图3-5 | Prefill | 完整 Prompt 怎样产生首个输出 token？ | final v2 |
| 图3-6 | Sampling | Logits 怎样变成具体 token？ | final v2 |
| 图3-7 | Decode 与 KV Cache | 每个生成步骤怎样复用并追加历史状态？ | final v2 |
| 图3-8 | 机制检查器输出 | 离线检查器怎样串起形状、采样与执行事件？ | final v2 |

## 图3-1 从文本到下一个 token

### 对应正文
4.0 从文本到下一个 token

### 核心问题
一次 token 生成经过哪些模型阶段？

### 核心观点
- 文本先变成 Token IDs，再变成 Hidden States。
- Transformer Blocks 处理上下文，LM Head 产生 Logits。
- Sampling 选择一个 token，Tokenizer 再将 token 解码成文本。

### 不应出现的内容
GPU、性能指标、优化技术或 Serving 组件。

### 阅读路径
从左到右读取 Text、Tokenizer、Embedding、Blocks、LM Head、Logits、Sampling、Token。

### Wireframe
~~~text
[Text] -> [Tokenizer] -> [Embedding] -> [N x Blocks] -> [LM Head] -> [Logits] -> [Sampling] -> [Token]
~~~

### 图中文字
Text、Chat Template + Tokenizer、Token IDs、Embedding、Hidden States、N × Transformer Blocks、Final Norm + LM Head、Logits、Sampling、Next Token。

### 关键结论
模型先计算词表分数，Sampling 才决定下一个 token。

## 图3-2 Decoder-only Transformer Block

### 对应正文
4.2 Decoder-only Transformer Block

### 核心问题
一个现代 Decoder Block 内部怎样流动？

### 核心观点
- 使用 Pre-Norm。
- Attention 和 MLP 各有一条 Residual Connection。
- Qwen2.5 的 MLP 使用 gate、up 与 down 三组投影。

### 不应出现的内容
Kernel、吞吐或不同模型性能比较。

### 阅读路径
主线由左向右，Residual 从输入跨过子层加回主线。

### Wireframe
~~~text
x -> RMSNorm -> Attention -> + -> RMSNorm -> SwiGLU MLP -> + -> y
|___________________________| |_____________________________|
~~~

### 图中文字
Input x、RMSNorm、Causal Attention、Residual Add、RMSNorm、SwiGLU MLP、gate_proj、up_proj、down_proj、Output y。

### 关键结论
一个 Block 用两次“归一化—子层—残差”逐步更新 hidden state。

## 图3-3 Causal Self-Attention

### 对应正文
4.3 Causal Self-Attention

### 核心问题
当前位置怎样读取自己和历史位置，同时看不到未来？

### 核心观点
- Hidden States 投影为 Q、K、V。
- QK 转成注意力权重，再加权汇总 V。
- Causal Mask 遮住未来位置。

### 不应出现的内容
FlashAttention、Kernel Fusion 或性能分析。

### 阅读路径
左侧 X 分成 Q/K/V，Q 与 K 进入 Score + Mask，Softmax 后与 V 汇合。

### Wireframe
~~~text
       -> Q ----+[X] ---+-> K ---> [QKᵀ / sqrt(d)] -> [Causal Mask] -> [Softmax] --+       -> V -------------------------------------------------------> [Weighted Sum]
~~~

### 图中文字
Hidden States X、Q Projection、K Projection、V Projection、Scaled Dot Product、Causal Mask、Softmax Weights、Weighted Values、Attention Output。

### 关键结论
Causal Attention 只汇总当前位置允许访问的历史信息。

## 图3-4 MHA 与 GQA

### 对应正文
4.4 Multi-Head Attention 与 GQA

### 核心问题
为什么 Query 有 14 个 Head，而 K/V 只有 2 个？

### 核心观点
- MHA 的 Q/K/V Head 数相同。
- GQA 保留 Query Heads，让一组 Query Heads 共享 K/V。
- 示例中每 7 个 Query Heads 共享 1 组 K/V。

### 不应出现的内容
显存节省比例或性能收益。

### 阅读路径
先看上方 MHA 一一对应，再看下方 GQA 的分组共享。

### Wireframe
~~~text
MHA: [Q][Q][Q][Q]  [K][K][K][K]  [V][V][V][V]
GQA: [Q x7] -> [KV 1]     [Q x7] -> [KV 2]
~~~

### 图中文字
MHA、Q Heads = K/V Heads、GQA、14 Query Heads、2 KV Heads、Group 1、Group 2、7 Q share 1 KV。

### 关键结论
GQA 减少的是 K/V Heads，不是 Query Heads。

## 图3-5 Prefill

### 对应正文
4.5 Prefill：一次处理整段 Prompt

### 核心问题
完整 Prompt 怎样产生第一个输出 token？

### 核心观点
- S 个 Prompt Tokens 一次进入模型。
- 每层所有 Prompt 位置的 K/V 写入 Cache。
- 最后位置 Logits 经 Sampling 产生首个输出 token。

### 不应出现的内容
TTFT、Compute Bound 或 Prefill 优化。

### 阅读路径
从 Prompt Tokens 进入 Full-sequence Forward，向下写 KV Cache，向右产生 Last-position Logits 和首 token。

### Wireframe
~~~text
[S Prompt Tokens] -> [Full-sequence Forward] -> [Last-position Logits] -> [Sampling] -> [First Token]
                              |
                              v
                    [KV Cache length = S]
~~~

### 图中文字
S Prompt Tokens、Full-sequence Forward、All Transformer Layers、KV Cache、K/V for every prompt position、Last-position Logits、Sampling、First Generated Token。

### 关键结论
Prefill 写入完整 Prompt 的 K/V，并为首个输出 token 产生 Logits。

## 图3-6 Sampling

### 对应正文
4.6 Sampling：从 Logits 选择 token

### 核心问题
一组词表分数怎样收敛成一个 token？

### 核心观点
- Temperature 改变概率分布形状。
- Top-k / Top-p 缩小候选集合。
- Greedy 或随机抽样选出 token。

### 不应出现的内容
质量评测或 Sampling 性能比较。

### 阅读路径
从 Logits 经过 Temperature、Candidate Filter、Selection 到 Selected Token。

### Wireframe
~~~text
[Vocabulary Logits] -> [Temperature] -> [Top-k / Top-p] -> [Greedy or Sample] -> [Selected Token]
~~~

### 图中文字
Vocabulary Logits、Temperature、Probability Distribution、Top-k / Top-p、Candidate Set、Greedy、Random Sample、Selected Token。

### 关键结论
Logits 只是分数，解码策略决定最终选择哪个 token。

## 图3-7 Decode 与 KV Cache

### 对应正文
4.7 Decode：一次消费一个新 token

### 核心问题
每个普通 Decode step 怎样使用历史 K/V 并生成下一 token？

### 核心观点
- Prefill 后 Cache 长度等于 Prompt 长度。
- 每个 Decode step 只输入一个新 token。
- 当前 token 的 K/V 被追加，Cache 长度增加 1。

### 不应出现的内容
PagedAttention、KV Quantization 或性能瓶颈。

### 阅读路径
从 Prefill 状态进入循环：新 token + past K/V，执行一步，追加 K/V，Sampling，再回到循环入口。

### Wireframe
~~~text
[Prefill: cache=S] -> [new token + past K/V] -> [one-token forward] -> [append K/V] -> [Sampling]
                              ^                                                  |
                              |__________________________________________________|
~~~

### 图中文字
Prefill Complete、Cache Length S、New Token、Past K/V、One-token Forward、Append Current K/V、Cache Length +1、Next-token Logits、Sampling、Repeat Until Stop。

### 关键结论
普通 Decode 每步复用历史 K/V，只为当前 token 追加一份新状态。

## 图3-8 机制检查器输出

### 对应正文
3.8 Demo：用真实请求约束机制检查

### 核心问题
离线检查器怎样把本章三条机制线索组合起来？

### 核心观点
- Config 推导 Shapes。
- Logits 经过 Sampling 得到 selected token。
- Prompt length 与 Decode steps 生成 Execution Trace。

### 不应出现的内容
真实模型耗时、GPU 数据或 Benchmark 结果。

### 阅读路径
从三类输入进入 mechanics.py，输出同一份 JSON 报告的三个区域。

### Wireframe
~~~text
[Model Config] ---+[Logits + Params] ---> [mechanics.py] -> [Shapes | Sampling | Execution Trace]
[Prompt + Steps] --/
~~~

### 图中文字
Model Config、Prompt Tokens、Decode Steps、Logits、Temperature、Top-k、mechanics.py、Shapes、Sampling、Execution Trace、synthetic_mechanics、Not a Benchmark。

### 关键结论
真实 vLLM 报告提供请求计数；检查器只验证结构关系与事件顺序。

## 全局视觉规范

- 画布为 1280x720 SVG。
- 使用浅灰画布、白色卡片、Slate 深色标题区和显式箭头。
- 中文承担主叙事，保留必要英文术语；最小字号 14px。
- 每张图只回答一个问题，底部统一使用“关键结论”条。
- 每张 SVG 包含 title、desc、视觉系统标记和独立 figure-note。

## 总体验收清单

- [x] 图 3-1 到图 3-8 与正文引用一一对应。
- [x] 图中没有 GPU 性能结论、指标阈值或优化技术。
- [x] Prefill、Sampling 与首个输出 token 的先后关系准确。
- [x] Decode step 与输出 token 数的关系没有混淆。
- [x] GQA 没有被画成 Query Head 数减少。
- [x] Demo 图明确标注 synthetic_mechanics 和 Not a Benchmark。
