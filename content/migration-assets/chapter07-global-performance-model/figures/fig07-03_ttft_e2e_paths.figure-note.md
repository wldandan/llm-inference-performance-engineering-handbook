# 图7-3 制作说明

- 来源段落：7.2 TTFT 与 E2E。
- 图意：两条测量路径共享请求前半段，但在首内容与完整返回处终止。
- 首 token 口径：Prefill 产生 Logits，经 Sampling 选出首 token；后续才进入 Decode forward。
- 关键结论：TTFT 看首响，E2E 还受到剩余生成与返回的影响。
- 视觉约束：阶段轴唯一；下方两条路径长度必须明显不同。
