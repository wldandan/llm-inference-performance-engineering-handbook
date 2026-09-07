# 图 6-3 制作说明：TTFT、TPOT 与 ITL

- 来源段落：第 6 章“6.2 TTFT、E2E、TPOT 与 ITL”。
- 阅读顺序：沿客户端时间线从 t0 读到 t_end，再比较上下方的区间标注。
- 关键结论：TTFT 看首响，ITL / TPOT 看输出节奏，E2E 看完整请求。
- 边界：一个输出 token 时没有 ITL，TPOT 应报告为空值。
