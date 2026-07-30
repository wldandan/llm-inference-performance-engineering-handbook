# Chapter 1 Demo

本 demo 只包含第一章需要的两个动作：

1. 使用 vLLM 启动一个 OpenAI-compatible 服务。
2. 使用客户端脚本访问这个服务，观察一次真实流式请求的生命周期。

模型下载、模型选择和环境准备由读者或实验环境提前完成。本章不提供下载模型脚本。

## 1. 启动 vLLM 服务

本章默认模型名：

```text
Qwen/Qwen2.5-0.5B
```

如果模型已经在 Hugging Face cache 中，或当前环境可以直接解析该模型 id：

```bash
python3 chapter01/demo/start_vllm.py \
  --model Qwen/Qwen2.5-0.5B \
  --served-model-name Qwen/Qwen2.5-0.5B \
  --host 0.0.0.0 \
  --port 8000
```

如果模型已经在本地目录，例如 GX10 上的 `/home/admin/models/Qwen2.5-0.5B`：

```bash
python3 chapter01/demo/start_vllm.py \
  --model /home/admin/models/Qwen2.5-0.5B \
  --served-model-name Qwen/Qwen2.5-0.5B \
  --host 0.0.0.0 \
  --port 8000
```

也可以不用封装脚本，直接启动 vLLM：

```bash
python3 -m vllm.entrypoints.openai.api_server \
  --model /home/admin/models/Qwen2.5-0.5B \
  --served-model-name Qwen/Qwen2.5-0.5B \
  --host 0.0.0.0 \
  --port 8000
```

## 2. 确认服务可访问

```bash
curl http://127.0.0.1:8000/v1/models
```

如果是远程机器，先确认网络或 SSH 隧道已经打通。

## 3. 使用脚本访问服务

从课程根目录运行：

```bash
python3 chapter01/demo/demo.py \
  --base-url http://127.0.0.1:8000/v1 \
  --model Qwen/Qwen2.5-0.5B \
  --prompt "请解释一次 LLM 在线推理请求从 Prompt 到完整回答的过程。" \
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

第 1 章只要求读者理解这些字段对应请求生命周期的哪个位置，不展开指标分析。

## 4. 单元测试

单元测试只验证命令构造、请求构造和客户端计算逻辑，不需要启动 vLLM：

```bash
cd chapter01/demo
python3 -m unittest test_demo.py test_start_vllm.py
```
