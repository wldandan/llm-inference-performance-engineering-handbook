# 第 6 章 Storyboard：LLM 性能指标

本章插图围绕指标口径、测量边界和分母展开，不提前讲 Benchmark Design 或性能优化。

| 图号 | 标题 | 核心问题 | 状态 |
|---|---|---|---|
| 图6-1 | 指标先回答问题 | 不同角色的问题该看哪类指标？ | final v2 |
| 图6-2 | 客户端与服务端测量边界 | 同一个请求有哪些不等价时钟？ | final v2 |
| 图6-3 | TTFT、TPOT 与 ITL | 四种延迟覆盖哪段时间？ | final v2 |
| 图6-4 | TPS、RPS 与 Goodput | 产能与达标产能有何不同？ | final v2 |
| 图6-5 | P50、P95 与 P99 | 分位数怎样描述尾部？ | final v2 |
| 图6-6 | 资源指标与结果指标 | GPU 很忙是否等于用户体验好？ | final v2 |
| 图6-7 | 成本指标的分母 | 同一笔成本除以什么才有意义？ | final v2 |
| 图6-8 | 可比较的指标合同 | 两个数字可比较需要哪些共同条件？ | final v2 |
| 图6-9 | Demo 输出指标报告 | 合成记录怎样生成可审计报告？ | final v2 |

## 全局视觉规范

- 1280×720；浅灰底、白卡片、深色主节点和结论栏。
- 最小字号 14 px，系统字体包含 `PingFang SC`。
- 实线箭头表示事件、筛选或计算路径；虚线表示跨层关联或不可直接相减。
- 每张图包含 title、desc、`chapter06-v2` 和“关键结论”。

## 图6-1 指标先回答问题

- 来源：6.0。
- Wireframe：`[业务问题] -> [体验 | 产能 | 可靠性 | 资源 | 成本] -> [对应指标]`。
- 重点：TTFT/ITL/E2E、TPS/RPS、Goodput、GPU/Queue、Cost Denominator 五组。
- 不出现：优化手段或指标阈值。
- 关键结论：先写问题，再选择指标与护栏。

## 图6-2 客户端与服务端测量边界

- 来源：6.1。
- Wireframe：三条对齐泳道 Client / Server / GPU；同一墙钟方向，不同起止点。
- 重点：Client request→first content→end；Server receive→first token→finish；GPU kernels。
- 不出现：把三个 TTFT 画成相等。
- 关键结论：同名时长只有边界和时钟一致时才能比较。

## 图6-3 TTFT、TPOT 与 ITL

- 来源：6.2。
- Wireframe：`t0 ---- t1 ---- t2 ---- t3 ---- tn ---- tend`，上方标 TTFT/E2E，下方标 ITL 与 TPOT。
- 重点：TPOT 不包含 t0→t1；一个输出 token 时 TPOT 未定义。
- 关键结论：TTFT 看首响，ITL / TPOT 看输出节奏，E2E 看完整请求。

## 图6-4 TPS、RPS 与 Goodput

- 来源：6.3。
- Wireframe：共享 Window 中若干请求和 tokens，分别进入三个分子；Goodput 还通过 Success + SLO Filter。
- 重点：三者共用墙钟分母但分子不同。
- 关键结论：Throughput 统计完成量，Goodput 只统计成功且达标的有效量。

## 图6-5 P50、P95 与 P99

- 来源：6.4。
- Wireframe：100 个已排序小块，标出第 50、95、99 个；最右侧为 Tail。
- 重点：nearest-rank 和 sample size。
- 关键结论：分位数要连同样本量、算法和 workload 分桶一起报告。

## 图6-6 资源指标与结果指标

- 来源：6.5。
- Wireframe：左侧 GPU/Memory/Bandwidth/Queue 经虚线连接右侧 TTFT/TPS/Goodput/Cost，中间标“需要因果证据”。
- 重点：资源指标是解释线索，不是结果代理。
- 关键结论：资源变化不能单独证明用户体验或业务产能改善。

## 图6-7 成本指标的分母

- 来源：6.6。
- Wireframe：同一个 Total Serving Cost 分成 Input Tokens、Output Tokens、Successful Requests、Good Requests 四个分母。
- 重点：失败资源计入总成本；输入输出 token 不混称。
- 关键结论：成本范围相同、分母相同，单位成本才可比较。

## 图6-8 可比较的指标合同

- 来源：6.7。
- Wireframe：十项 Contract Card 进入 `[Comparable Metric]`。
- 重点：Question、Workload、Boundary、Clock、Window、Unit、Aggregation、Denominator、Failures、Sample。
- 关键结论：指标名称相同，不代表测量合同相同。

## 图6-9 Demo 输出指标报告

- 来源：6.8。
- Wireframe：`[JSONL Records + SLO + Workload] -> metrics_report.py -> [Latency | Throughput | Goodput | Cost | Contract]`。
- 重点：synthetic_client_metrics、nearest-rank、shared wall clock、NOT A BENCHMARK。
- 关键结论：Demo 把公式和口径写入报告，不把合成记录包装成实测。
