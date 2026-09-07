# 第1章课堂 Demo

本 demo 用于课堂上观察一次真实 vLLM 流式请求的生命周期。

它包含两个动作：

1. 使用 `start_vllm.py` 启动 vLLM OpenAI-compatible 服务。
2. 使用 `demo.py` 访问服务，获得一次请求的客户端观察数据。

## 启动 vLLM 服务

如果模型可通过 Hugging Face id 解析：

```bash
python3 start_vllm.py \
  --model Qwen/Qwen2.5-0.5B \
  --served-model-name Qwen/Qwen2.5-0.5B \
  --host 0.0.0.0 \
  --port 8000
```

如果模型已在本地目录，例如 GX10 上的 `/home/admin/models/Qwen2.5-0.5B`：

```bash
python3 start_vllm.py \
  --model /home/admin/models/Qwen2.5-0.5B \
  --served-model-name Qwen/Qwen2.5-0.5B \
  --host 0.0.0.0 \
  --port 8000
```

## 访问服务

```bash
python3 demo.py \
  --base-url http://127.0.0.1:8000/v1 \
  --model Qwen/Qwen2.5-0.5B \
  --prompt "请解释一次 LLM 在线推理请求从 Prompt 到完整回答的过程。" \
  --max-tokens 128 \
  --requests 1 \
  --concurrency 1
```

课堂只要求学员观察：

- 请求是否成功。
- 首个流式 chunk 什么时候返回。
- 后续 chunk 是否持续返回。
- 请求结束后是否有 token usage。

系统性的 TTFT、ITL、TPS 指标实验放到第2章。

## 测试

```bash
python3 -m unittest test_demo.py test_start_vllm.py
```
