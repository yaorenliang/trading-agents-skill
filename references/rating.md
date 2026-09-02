# 集中化 5 档评级（单一来源）

> 所有决策 Agent（Research Manager / Portfolio Manager）只允许使用以下 5 档词汇，禁止发明新档位或同义改写——这是确定性解析与跨次对比的前提。

| 评级 | 含义 | 仓位建议（占组合比例） |
|---|---|---|
| Buy | 强烈看多，建议建仓或加仓 | 5-10% |
| Overweight | 看好，建议逐步加仓 | 3-5% |
| Hold | 中性，维持当前仓位 | 不变 |
| Underweight | 看淡，建议减仓 | 减仓约 50% |
| Sell | 强烈看空，建议清仓 | 清仓 |

## 强制决断规则

- 证据一边倒时必须给明确档位，禁止用 Hold 逃避。
- Hold 仅当多空最强论据确实势均力敌，且必须写明"哪两条论据对冲"。
- 评级必须引用辩论中的具体论据（至少 2 条）；无来源的评级无效，必须退回重裁。

## 档位衔接

- Research Manager 输出 5 档（研究向）；Trader 只允许 3 档动作 Buy / Hold / Sell（执行向，更粗）。
- 映射：Buy / Overweight → Buy；Hold → Hold；Underweight / Sell → Sell。
- 最终结论以 Portfolio Manager 为准；与 ResearchPlan 不一致时必须写明原因。

## 程序化解析

下游如需自动化：用正则匹配 Rating 字段的 5 个标准词（确定性解析，无 LLM 参与）。解析失败即流程错误，必须修复重跑，禁止猜测兜底。
