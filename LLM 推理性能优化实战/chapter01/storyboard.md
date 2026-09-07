# 第 1 章 Storyboard：第一个 LLM 服务

本章插图服务于“先运行，再观察”的入门路径。图中只呈现读者此刻需要理解的请求阶段，不展开完整 Serving 拓扑、GPU 内部结构或优化技术。

| 图号 | 标题 | 核心问题 | 状态 |
|---|---|---|---|
| 图1-1 | 第一个请求与生命周期总览 | 客户端发出请求后，服务如何开始并持续返回 token | wireframe |
| 图1-2 | Gateway 请求入口 | 协议、鉴权、参数校验和路由发生在模型计算前 | wireframe |
| 图1-3 | Queue 与 Scheduler | 队列等待是生命周期的一部分 | wireframe |
| 图1-4 | Prefill 在生命周期中的位置 | Prefill 处理完整输入并写入 KV Cache | wireframe |
| 图1-5 | 首个 token 与流式返回 | 首个 chunk 改变用户等待方式 | wireframe |
| 图1-6 | Decode Loop | Decode 是逐 token 循环 | wireframe |
| 图1-7 | KV Cache 生命周期 | KV Cache 在 Prefill 写入，在 Decode 读写增长 | wireframe |
| 图1-8 | 请求结束与资源回收 | 结束时返回 usage 并释放或复用资源 | wireframe |
| 图1-9 | Demo 字段映射到生命周期 | 客户端字段可以映射回生命周期阶段 | wireframe |
| 图1-10 | 本章与后续章节边界 | 第 1 章观察现象，第 2 章讲生命周期，第 3 章讲架构，第 6 章讲指标 | wireframe |

## 视觉规范

- 16:9 SVG，`1280x720`。
- 白底、黑灰线框、简单箭头。
- 一图一观点，不做知识海报。
- 不复制参考书图片，只重新表达本书正文支持的观点。
