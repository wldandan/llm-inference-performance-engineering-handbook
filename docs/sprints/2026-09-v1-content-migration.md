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
- [x] Review、Storyboard、4 张目的明确的 v2 SVG 与新版章节目标一致，每张图均有制作说明。
- [x] 单元测试、插图视觉契约测试、干运行、章节结构校验、SVG 解析和原尺寸渲染检查通过。
- [ ] 在课程目标 GPU 环境完成服务启动、模型加载和流式请求验证。

### 测试用例

1. 构造 OpenAI-compatible Chat Completions 请求。
2. 客户端正确计算 TTFT、ITL、总延迟和输出吞吐。
3. 默认模型为 `Qwen/Qwen2.5-0.5B-Instruct`。
4. 启动命令以 `vllm serve <model>` 开头。
5. 章节的 4 张图片链接存在、图号连续、必要章节结构完整。
6. 开篇图明确区分客户端观察与服务内部过程，不把 chunk 等同于 token。

## Task CH02：Inference Lifecycle

### 验收条件

- [x] 区分业务任务、LLM 调用与推理请求三个层次。
- [x] 用统一事件描述请求从接收、排队、Prefill、Decode 到结束的路径。
- [x] 明确服务端首 token 与客户端首包不是同一个时间边界。
- [x] 覆盖完成、取消、失败和抢占后的异常路径。
- [x] Demo 能从 JSONL 事件计算 Queue、Prefill、Decode 等阶段时间。
- [x] Demo 对非法状态跳转、时间戳逆序和错误 JSONL 给出明确错误。
- [x] Review、Storyboard、10 张 v2 SVG 与新版章节目标一致，每张图均有制作说明。
- [x] 单元测试、插图视觉契约测试、章节结构校验、SVG 解析和原尺寸渲染检查通过。

### 测试用例

1. 完成请求被拆分为 admission、queue、prefill、decode、response tail 和 end-to-end。
2. 取消请求只保留已经闭合的阶段时间，未闭合阶段返回空值而不是零。
3. 多请求事件按 request ID 分组并统计终态。
4. 非法状态跳转、逆序时间戳和错误 JSONL 被拒绝。
5. CLI 能打印报告，也能保存 JSON 报告。

## Task CH03：LLM Inference Architecture

### 验收条件

- [x] 用 Client、Gateway、Router、Admission、Engine Scheduler、Worker、Runtime 和 Accelerator 描述完整请求链路。
- [x] 区分逻辑角色、进程或 Pod 等部署单元，不把架构图误当作固定拓扑。
- [x] 区分请求平面、控制平面和遥测平面，并明确三类状态的权威所有者。
- [x] 成熟系统映射覆盖 Serving Platform、Inference Server 和 LLM Engine 三个层级，不形成产品排名。
- [x] Demo 能校验角色、组件 ID、连线类型、连线端点以及请求和响应路径完整性。
- [x] 旧 Chapter 3 的 GPU 正文插图被释放并完整保留到 Chapter 5 的迁移素材目录。
- [x] Review、Storyboard 和 10 张 v2 SVG 与新版章节目标一致，每张图均有制作说明。
- [x] 13 项 Demo 单元测试、2 项插图契约测试、章节结构校验、SVG 解析和原尺寸渲染检查通过。

### 测试用例

1. 合法架构输出请求路径、响应路径、部署单元和角色契约。
2. 重复组件 ID、缺失必要角色、未知端点和不支持的连线类型被拒绝。
3. 不完整的请求或响应角色路径被拒绝。
4. CLI 能读取 JSON、打印报告并保存报告文件。
5. 仓库自带参考架构能通过全部校验。

## Task CH04：Transformer 推理机制

### 验收条件

- [x] 从 Token IDs 到 Selected Token 解释完整 Decoder-only 生成路径。
- [x] 说明 Block、Causal Attention、GQA、Prefill、Sampling、Decode 和 KV Cache。
- [x] 明确 Prefill 后首 token 与后续 Decode step 的计数关系。
- [x] 离线 Demo 能输出 Shapes、Sampling 和 Execution Trace 合成报告。
- [x] Review、Storyboard、8 张 v2 SVG 和 figure-note 与章节目标一致。
- [x] 8 项 Demo 测试、25 项扩展 Workshop 测试、视觉契约、SVG 解析和原尺寸检查通过。

### 测试用例

1. GQA 的 Q 与 K/V Head 形状不同且关系合法。
2. Softmax 概率归一化，Top-k 之外候选归零。
3. Prefill 后 Cache 长度等于 Prompt，Decode 每步增长 1。
4. 合成报告不声称运行真实模型或 Benchmark。

## Task CH05：GPU 性能心智模型

### 验收条件

- [x] Core 主线只保留 Compute、Capacity、Bandwidth 和 Launch 四类约束。
- [x] 权重、KV Cache、工作区、Runtime 与安全余量进入显存预算。
- [x] 使用算术强度与 Ridge Point 建立 Roofline 直觉，不把估算当成实测。
- [x] SM、Warp、Tensor Core 与 Occupancy 下沉为进阶选修入口。
- [x] 离线 Demo 能识别四类候选约束并输出验证顺序。
- [x] Review、Storyboard、8 张 v2 SVG 和 figure-note 与章节目标一致。
- [x] 9 项 Demo 测试、视觉契约、SVG 解析和原尺寸检查通过。

### 测试用例

1. 权重精度和 GQA / MHA 配置正确改变容量预算。
2. 安全余量保留后，超出可用显存会标为 Capacity 约束。
3. Compute、Bandwidth 和 Launch 三类合成场景能被区分。
4. 报告明确标记为 `synthetic_gpu_mental_model`，不冒充 Benchmark。

## Task CH06：LLM 性能指标

### 验收条件

- [x] 指标按用户体验、产能、可靠产能、资源和成本五类问题组织。
- [x] Client、Server 与 GPU 测量边界在公式之前明确区分。
- [x] TTFT、E2E、ITL、TPOT、Output TPS、RPS 与 Goodput 公式和空值语义清楚。
- [x] 分位数固定使用 nearest-rank，并连同样本量、算法和 workload 分桶报告。
- [x] 成本口径区分输入 token、输出 token、成功请求与 good request。
- [x] 离线 Demo 使用共享墙钟窗口，输出完整 measurement contract。
- [x] Review、Storyboard、9 张 v2 SVG 和 figure-note 与章节目标一致。
- [x] 8 项 Demo 测试、视觉契约、SVG 解析和原尺寸检查通过。

### 测试用例

1. 请求级 TTFT、E2E、ITL 与 TPOT 按同一客户端时钟计算。
2. Output TPS 和 RPS 使用共享墙钟窗口，不相加单请求速度。
3. Goodput 只统计成功且同时满足 TTFT / E2E SLO 的请求。
4. 逆序时间、token 数不一致和失败请求伪造输出会被拒绝。
5. 报告保留 nearest-rank、成本分母、workload 和合成数据标记。

## Task CH07：Global Performance Model

### 验收条件

- [x] 用 Outcome、Workload、Stage、Resource、Evidence 五层收束 Part 1。
- [x] 区分普通串行请求的阶段加法与并行任务的 DAG Critical Path。
- [x] TTFT 与 E2E 使用不同终点，并沿用第 6 章测量边界。
- [x] 慢阶段只生成候选假设，所有候选项保持 `needs_evidence`。
- [x] RAG 同时覆盖检索路径、上下文工作量和质量护栏。
- [x] Agent 覆盖重复 LLM、并行工具、Merge、重试和任务级指标。
- [x] Demo 能校验依赖图、计算关键路径、并行重叠和待采证据。
- [x] Review、Storyboard、9 张 v2 SVG 和 figure-note 与正文一致。
- [x] 8 项 Demo 测试、视觉契约、SVG 解析和原尺寸检查通过。

### 测试用例

1. 串行 LLM 请求的 Critical Path 等于全部阶段时间之和。
2. 并行 RAG 分支使用最长必要分支，不把所有节点直接相加。
3. 循环依赖、未知依赖、重复 ID 和负时长被拒绝。
4. Queue 与 Decode 只产生候选假设和待采证据，不输出 Root Cause。
5. Agent 报告保留重复 LLM 与工具节点，并计算任务级路径。

## 下一批任务

1. 更新 Part 章节范围校验，使 Part 1 覆盖 Chapter 1–7。
2. 完成 Part 1 全量测试、图片渲染、链接与交付审计。
3. 在目标 GPU 环境补做 Chapter 1 的真实服务启动与流式请求验证。
