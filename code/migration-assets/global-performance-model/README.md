# Chapter 7 Demo：全局性能依赖图

这个 Demo 把一次 LLM 请求、RAG 请求或 Agent 任务表示成有向无环依赖图，计算：

- 端到端 Critical Path；
- 所有节点时间之和与并行重叠时间；
- 关键路径上的阶段占比；
- 每个候选阶段仍需补采的证据。

从 Git 仓库根目录运行三类样例：

```bash
python3 code/chapter07/performance_model.py code/chapter07/sample_llm_request.json
python3 code/chapter07/performance_model.py code/chapter07/sample_rag.json
python3 code/chapter07/performance_model.py code/chapter07/sample_agent.json
```

保存报告：

```bash
python3 code/chapter07/performance_model.py \
  code/chapter07/sample_agent.json \
  --output global-performance-report.json
```

报告会拒绝循环依赖、未知节点、重复 ID 和负时长。`synthetic_global_performance_model` 表示它只分析输入的合成依赖图。最长节点或关键路径只是候选分析入口，不是 Root Cause；还要用 Benchmark、Trace、服务指标和 GPU Profiling 验证。

## 测试

```bash
python3 -m unittest discover -s code/chapter07 -p 'test_*.py'
```
