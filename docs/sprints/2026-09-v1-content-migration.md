# v1.0 内容迁移 Sprint

## 目标

把现有章节迁移到《LLM 推理性能工程实战》v1.0 结构，优先形成适合后端工程师和 Agent 工程师的 Core Track，并保留平台与基础设施方向的 Advanced Track。

## 已批准设计

- 课程名：《LLM 推理性能工程实战》
- 副标题：从模型原理、性能分析到 Serving 与 Agent 优化
- 权威大纲：`LLM 推理性能优化实战/02_Course_Outline_v1.0.md`
- 章节交付：正文、Demo、Review、Storyboard、自动校验

## Task CH01：第一个 LLM 服务

### 验收条件

- [x] 第 1 章以“启动服务并完成一次流式请求”为首个学习结果。
- [x] 示例代码归属 `chapter01/demo/`，正文不存在旧的 `chapter02/demo/` 路径。
- [x] 默认模型支持 Chat Completions。
- [x] 启动脚本使用当前 vLLM 官方 `vllm serve` 接口。
- [x] Part 1 导读反映新版 7 章结构及 Core / Bridge 分层。
- [x] Review 和 Storyboard 与新版章节目标一致。
- [x] 单元测试、干运行和章节结构校验通过。
- [ ] 在课程目标 GPU 环境完成服务启动、模型加载和流式请求验证。

### 测试用例

1. 构造 OpenAI-compatible Chat Completions 请求。
2. 客户端正确计算 TTFT、ITL、总延迟和输出吞吐。
3. 默认模型为 `Qwen/Qwen2.5-0.5B-Instruct`。
4. 启动命令以 `vllm serve <model>` 开头。
5. 章节图片链接存在、图号连续、必要章节结构完整。

## Task CH02：Inference Lifecycle

### 验收条件

- [x] 区分业务任务、LLM 调用与推理请求三个层次。
- [x] 用统一事件描述请求从接收、排队、Prefill、Decode 到结束的路径。
- [x] 明确服务端首 token 与客户端首包不是同一个时间边界。
- [x] 覆盖完成、取消、失败和抢占后的异常路径。
- [x] Demo 能从 JSONL 事件计算 Queue、Prefill、Decode 等阶段时间。
- [x] Demo 对非法状态跳转、时间戳逆序和错误 JSONL 给出明确错误。
- [x] Review、Storyboard、10 张 SVG 线框与新版章节目标一致。
- [x] 单元测试、章节结构校验和代表性 SVG 原尺寸渲染抽查通过。

### 测试用例

1. 完成请求被拆分为 admission、queue、prefill、decode、response tail 和 end-to-end。
2. 取消请求只保留已经闭合的阶段时间，未闭合阶段返回空值而不是零。
3. 多请求事件按 request ID 分组并统计终态。
4. 非法状态跳转、逆序时间戳和错误 JSONL 被拒绝。
5. CLI 能打印报告，也能保存 JSON 报告。

## 下一批任务

1. 将现有 Architecture 内容迁移到 Chapter 3。
2. 新建 Chapter 4：Transformer 推理机制。
3. 依次对齐 Chapter 5–7 的 GPU、指标和全局性能模型。
