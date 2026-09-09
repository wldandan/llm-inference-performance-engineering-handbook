# 课程 QA

收集与课程内容相关、值得沉淀的问题，后续按需补充答案，并标注对应章节以便交叉核对内容是否已覆盖。

## 待解答问题

1. LLM 服务中的主要瓶颈及如何缓解它们
   - 关联章节：Chapter 3（GPU 架构基础）、Chapter 5（Global Performance Model）、Chapter 11（Prefill 性能分析）、Chapter 15（Decode 性能分析）、Chapter 16（Decode 优化方法）

2. 加载 LLM 进行服务时的约束
   - 关联章节：Chapter 2（系统架构 / 部署形态演进）

3. 执行 LLM 时的瓶颈，特别是在预填充和解码阶段
   - 关联章节：Chapter 3（计算密集 vs 访存密集）、Chapter 11（Prefill 性能分析）、Chapter 15（Decode 性能分析）

4. 为何模型服务会在不同阶段出现瓶颈
   - 关联章节：Chapter 3（GPU 架构基础）、Chapter 5（Global Performance Model）

5. 模型服务是受限于 GPU 计算 FLOPS 还是 GPU 内存带宽？
   - 关联章节：Chapter 3（计算密集 vs 访存密集）、Chapter 5（Global Performance Model）、Chapter 11（Prefill 性能分析）、Chapter 15（Decode 性能分析）

## 使用说明

- 新问题追加到「待解答问题」列表末尾，保留编号顺序。
- 有了明确答案后，将该问题连同答案移到对应的「已解答」小节（首次出现时新建），并保留关联章节标注，便于回溯依据。
