# Chapter 2 Demo：请求生命周期追踪

这个 Demo 把一组标准化事件还原成请求生命周期。它不依赖 GPU，也不伪装成真实压测结果；`sample-events.jsonl` 是教学用合成数据，用来练习阶段划分、异常路径和时间边界。

## 1. 运行环境

- Python 3.10 或更高版本
- 只使用 Python 标准库

## 2. 事件格式

每行是一个 JSON 对象：

```json
{"request_id":"req-ok","event":"queued","ts_ms":2}
```

本 Demo 使用以下标准事件：

```text
request_received
  -> queued
  -> scheduled
  -> first_token
  -> token ...
  -> last_token
  -> finished
```

请求也可能从非终态进入 `cancelled` 或 `failed`。这些名称是课程统一的归一化事件，不等同于某个框架的内部类名。接入真实系统时，应先把框架日志或 Trace 转成这套格式。

## 3. 运行分析器

从课程目录运行：

```bash
python3 chapter02/demo/lifecycle_trace.py \
  --input chapter02/demo/sample-events.jsonl
```

也可以保存报告：

```bash
python3 chapter02/demo/lifecycle_trace.py \
  --input chapter02/demo/sample-events.jsonl \
  --output chapter02/demo/lifecycle-report.json
```

生成的报告会包含每条请求的终态，以及能够从事件边界算出的阶段时间：

| 字段 | 计算边界 |
|---|---|
| `admission` | `request_received -> queued` |
| `queue` | `queued -> scheduled` |
| `prefill` | `scheduled -> first_token` |
| `decode` | `first_token -> last_token` |
| `response_tail` | `last_token -> finished` |
| `end_to_end` | `request_received -> terminal event` |

取消或失败的请求只报告已经闭合的时间段。例如请求在 Prefill 中被取消，就能算出 admission、queue 和 end-to-end，但没有完整的 prefill、decode 或 response tail。

## 4. 预期现象

样例包含三条请求：一条完成、一条取消、一条失败。报告摘要应为：

```json
{
  "requests": 3,
  "finished": 1,
  "cancelled": 1,
  "failed": 1
}
```

这里的毫秒数只用于检查计算是否正确，不能当作任何模型或硬件的性能结论。

## 5. 单元测试

```bash
cd chapter02/demo
python3 -m unittest test_lifecycle_trace.py
```

测试覆盖正常完成、取消、非法状态跳转、时间戳逆序、多请求分组、JSONL 读取，以及 CLI 输出与报告保存。
