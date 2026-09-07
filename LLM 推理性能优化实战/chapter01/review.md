# Chapter Review

## 总体评价

第 1 章已经按 v1.0 大纲改成“第一个 LLM 服务”。读者先启动服务、发出流式请求，再把客户端现象映射到 Queue、Prefill、Decode 和 Response。正文、Demo、总结、练习和 Checklist 已形成一条可执行的入门路径。

## 结构问题

章节边界需要持续守住：第 1 章只负责“跑通 + 观察 + 建立粗粒度地图”；第 2 章正式讲 Inference Lifecycle；第 3 章再解释 Gateway、Scheduler、Worker 和 Runtime 的职责。当前正文保留了生命周期概览，但没有展开调度算法、性能公式或优化参数，边界可接受。

## 技术与术语问题

- 启动脚本已切换到 vLLM 官方推荐的 `vllm serve <model>` 入口。
- `ttft_ms`、`itl_*` 和 `tokens_per_second` 在本章只作为客户端观察值，不承担正式指标定义。
- Prefill、Decode、KV Cache 和 Streaming Response 的用法与后续章节一致。

## 内容缺口

- 发布前需在课程指定 GPU 环境完成一次端到端实跑，记录 vLLM、Python、驱动、GPU 和模型版本。
- 可在实跑后补一份脱敏的成功输出样例，帮助读者判断自己的结果是否正常。

## 可删减内容

如果第 2 章重写后与本章重复，应优先从第 1 章删掉机制细节，保留操作步骤、现象和直觉；不要删掉第一个可运行请求。

## 推荐插图位置

图 1-1 到图 1-10 已覆盖请求总览、入口、排队、Prefill、首 token、Decode、KV Cache、资源回收、Demo 字段映射和章节边界。后续制图时，图 1-1 应突出“客户端发起请求—服务流式返回”，不要画成完整 Serving 架构图。

## 修改优先级

1. P0：在目标 GPU 环境执行一次端到端验证并保存环境版本。
2. P1：重写第 2 章时做重复度检查，确保它提供更正式的生命周期模型。
3. P2：正式制图前确认图 1-1 和图 1-9 是否能直接承接 Demo。

## 验收建议

- `python3 -m unittest test_demo.py test_start_vllm.py` 全部通过。
- `start_vllm.py --dry-run` 生成 `vllm serve` 命令。
- Markdown 图片链接全部存在，图号从图 1-1 到图 1-10 连续。
- 在目标 GPU 环境中，服务可启动、`/v1/models` 可访问、流式请求成功。
- 章节不提前给出 Benchmark 结论或具体优化方案。
