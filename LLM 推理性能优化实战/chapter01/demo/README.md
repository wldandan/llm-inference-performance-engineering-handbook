# Chapter 1 Demo：第一个 LLM 服务

本 Demo 是全书的起点，只完成两个动作：

1. 使用 vLLM 启动一个 OpenAI-compatible 服务。
2. 使用客户端脚本访问这个服务，观察请求、首个内容 chunk、后续 chunks 和结束信号。

模型下载、模型选择和环境准备由读者或实验环境提前完成。本章不提供下载模型脚本。

## 1. 运行前提

本章默认使用 Linux + NVIDIA GPU 环境。按照 vLLM 官方文档准备独立 Python 环境并安装 vLLM；不同 CUDA、ROCm、CPU 或 Apple Silicon 环境应使用对应的安装方式。

开始前记录环境信息，后续性能实验需要把这些版本写入报告：

```bash
python3 --version
vllm --version
nvidia-smi
```

vLLM 官方文档：

- [安装说明](https://docs.vllm.ai/en/stable/getting_started/installation/)
- [vLLM CLI](https://docs.vllm.ai/en/stable/cli/index.html)

## 2. 启动 vLLM 服务

本章默认模型名：

```text
Qwen/Qwen2.5-0.5B-Instruct
```

如果模型已经在 Hugging Face cache 中，或当前环境可以直接解析该模型 id：

```bash
python3 chapter01/demo/start_vllm.py \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --served-model-name Qwen/Qwen2.5-0.5B-Instruct \
  --host 0.0.0.0 \
  --port 8000
```

如果模型已经在本地目录，例如 GX10 上的 `/home/admin/models/Qwen2.5-0.5B-Instruct`：

```bash
python3 chapter01/demo/start_vllm.py \
  --model /home/admin/models/Qwen2.5-0.5B-Instruct \
  --served-model-name Qwen/Qwen2.5-0.5B-Instruct \
  --host 0.0.0.0 \
  --port 8000
```

也可以不用封装脚本，直接使用官方 CLI：

```bash
vllm serve /home/admin/models/Qwen2.5-0.5B-Instruct \
  --served-model-name Qwen/Qwen2.5-0.5B-Instruct \
  --host 0.0.0.0 \
  --port 8000
```

如果只想确认封装脚本生成的命令，不启动服务：

```bash
python3 chapter01/demo/start_vllm.py --dry-run
```

## 3. 确认服务可访问

```bash
curl http://127.0.0.1:8000/v1/models
```

如果是远程机器，先确认网络或 SSH 隧道已经打通。

## 4. 使用脚本访问服务

从课程根目录运行：

```bash
python3 chapter01/demo/demo.py \
  --base-url http://127.0.0.1:8000/v1 \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --prompt "请用三句话介绍 LLM 在线推理。" \
  --max-tokens 256 \
  --requests 1 \
  --concurrency 1
```

脚本会输出 JSON，记录客户端观察到的：

- 请求是否成功。
- `prompt`：实际发送给 vLLM 的原始输入。
- 首个流式 chunk 等待时间。
- 后续 chunk 间隔。
- 总请求耗时。
- token usage，如果服务端返回。
- GPU 快照，如果脚本运行机器本身支持 `nvidia-smi`。

第 1 章只要求读者把这些字段对应到客户端观察事件，不把观察值直接归因到服务端阶段，也不评价性能数值。第 6 章定义指标，第 8 章再讨论可信的 Benchmark。

正常情况下，终端会输出一份 JSON 报告。`summary.successes` 应为 `1`，`results[0].ttft_ms`、`total_latency_ms` 和 `stream_chunks` 应有值；服务未启动、模型名不匹配或网络不可达时，脚本会返回非零状态并输出错误原因。

## 5. 单元测试

单元测试只验证命令构造、请求构造和客户端计算逻辑，不需要启动 vLLM：

```bash
cd chapter01/demo
python3 -m unittest test_demo.py test_start_vllm.py
```
