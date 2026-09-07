# Chapter 3 Demo：架构契约检查器

这个 Demo 用一份 JSON 描述 LLM Serving 的逻辑组件、部署单元和组件间连线，然后检查请求路径与响应路径是否完整。它只使用 Python 标准库，不需要模型或 GPU。

Demo 检查的是架构职责，不是运行时健康状态。报告通过，表示图上的角色和交接关系自洽；它不代表服务已经部署，也不代表性能满足要求。

## 1. 运行环境

- Python 3.10 或更高版本
- 无第三方依赖
- Level 1：CPU / 无 GPU

## 2. 输入文件

`reference-architecture.json` 包含三类信息：

- `components`：逻辑组件及其部署单元；
- `flows`：请求、响应、控制和遥测连线；
- `deployment_unit`：多个逻辑组件是否位于同一进程、服务或设备中。

参考架构的请求路径是：

```text
client -> gateway -> router -> admission
       -> scheduler -> worker -> runtime -> accelerator
```

简化后的响应路径是：

```text
accelerator -> runtime -> worker -> gateway -> client
```

返回链路没有再次经过 Router、Admission 和 Engine Scheduler，因为它们通常不再做目标选择或执行准入。真实框架可能还有 Output Processor、Detokenizer 或消息总线；接入时可以扩展组件，但不要混淆逻辑责任。

## 3. 运行检查

从课程目录运行：

```bash
python3 chapter03/demo/architecture_contract.py \
  --input chapter03/demo/reference-architecture.json
```

保存报告：

```bash
python3 chapter03/demo/architecture_contract.py \
  --input chapter03/demo/reference-architecture.json \
  --output chapter03/demo/architecture-report.json
```

报告包含：

| 字段 | 含义 |
|---|---|
| `request_path` | 从 Client 到 Accelerator 的完整请求路径 |
| `response_path` | 从 Accelerator 返回 Client 的简化响应路径 |
| `deployment_units` | 逻辑组件与进程、服务或设备的部署关系 |
| `role_contracts` | Router、Admission、Scheduler 等角色的职责边界 |

重点比较 `router` 与 `scheduler`：前者输出目标实例选择，后者输出下一轮模型执行计划。两者都叫“调度”时，架构图很容易失去排障价值。

## 4. 制造一个错误

复制参考文件，删除下面这条请求连线：

```json
{"from": "scheduler", "to": "worker", "kind": "request"}
```

再次运行后，程序应拒绝该架构并报告缺少完整请求路径。你也可以尝试：

- 删除 `router` 角色；
- 写入重复的组件 ID；
- 把连线指向不存在的组件；
- 把 `kind` 改成未支持的值。

## 5. 单元测试

```bash
cd chapter03/demo
python3 -m unittest test_architecture_contract.py
```

13 项测试覆盖完整请求与响应路径、职责分离、部署单元、缺失角色、重复 ID、错误连线、JSON 读取、CLI 输出和报告保存。

## 6. 边界

- 这是一份教学用参考架构，不是特定框架的源码模型。
- 逻辑组件不等于独立进程；多个角色可以部署在同一个单元中。
- Demo 不连接真实服务，也不采集 TTFT、吞吐或 GPU 指标。
- 多副本、多 GPU、PD Disaggregation 和控制面扩缩容在后续章节展开。
