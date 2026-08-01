# 第 2 章 Storyboard 索引

| 图号 | 标题 | 核心问题 | 状态 |
|---|---|---|---|
| 图2-1 | 一次请求的生命周期总览 | Request -> Gateway -> Queue -> Prefill -> First Token -> Decode -> Response | wireframe |
| 图2-2 | Gateway 请求入口 | 协议、鉴权、参数校验和路由发生在模型计算前 | wireframe |
| 图2-3 | Queue 与 Scheduler | 队列等待是生命周期的一部分 | wireframe |
| 图2-4 | Prefill 在生命周期中的位置 | Prefill 处理完整输入并写入 KV Cache | wireframe |
| 图2-5 | 首个 token 与流式返回 | 首个 chunk 改变用户等待方式 | wireframe |
| 图2-6 | Decode Loop | Decode 是逐 token 循环 | wireframe |
| 图2-7 | KV Cache 生命周期 | KV Cache 在 Prefill 写入，在 Decode 读写增长 | wireframe |
| 图2-8 | 请求结束与资源回收 | 结束时返回 usage 并释放或复用资源 | wireframe |
| 图2-9 | Demo 字段映射到生命周期 | 客户端字段可以映射回生命周期阶段 | wireframe |
| 图2-10 | 生命周期与后续章节边界 | 本章只讲阶段，不展开指标和优化 | wireframe |

## 视觉规范

- 16:9 SVG，`1280x720`。
- 白底、黑灰线框、简单箭头。
- 一图一观点，不做知识海报。
- 不复制参考书图片，只重新表达本书正文支持的观点。
