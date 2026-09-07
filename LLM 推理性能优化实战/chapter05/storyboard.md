# 第 5 章 Storyboard 索引

| 图号 | 标题 | 核心问题 | 状态 |
|---|---|---|---|
| 图5-1 | 全局性能模型 | Latency = Queue + Prefill + Decode | wireframe |
| 图5-2 | Queue 对延迟的影响 | Queue 是模型计算前的等待 | wireframe |
| 图5-3 | Prefill 对首包的影响 | Prefill 影响第一个 token 前的时间 | wireframe |
| 图5-4 | Decode 对总延迟的影响 | Decode 时间随输出长度增长 | wireframe |
| 图5-5 | Compute Bottleneck | 计算单元忙不过来时需要计算侧优化 | wireframe |
| 图5-6 | Memory Bottleneck | 数据读写和带宽限制会拖慢生成 | wireframe |
| 图5-7 | Scheduling Bottleneck | 资源可用但调度没有用好 | wireframe |
| 图5-8 | 指标因果关系 | Queue、Prefill、Decode 同时牵动多个指标 | wireframe |
| 图5-9 | Demo 结果进入全局模型 | 先提出假设，再做验证 | wireframe |
| 图5-10 | 从模型到验证 | 优化结论必须回到同 workload 验证 | wireframe |

## 视觉规范

- 16:9 SVG，`1280x720`。
- 白底、黑灰线框、简单箭头。
- 一图一观点，不做知识海报。
- 不复制参考书图片，只重新表达本书正文支持的观点。
