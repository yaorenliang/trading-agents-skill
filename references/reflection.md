# T+5 延迟反思机制

## 设计理由

收益需要时间窗口才能评判决策质量。延迟到 T+5（默认，可按持有期调整）复盘，且只在 Portfolio Manager 决策点注入——避免未成熟的盈亏污染当次分析。这是本 skill 相对"跑完即扔"式分析工具的核心纪律层。

## 触发

- **自动补做**：下次同 ticker 分析的 Phase 0 扫描 pending 条目，到期即补做（主路径，零额外设施）。
- **手动**：用户说"反思一下 XX 股票上次决策" / "上次买对了吗"。
- **定时（可选）**：宿主支持定时任务时可登记 T+5 提醒，但不是必需。

## 流程

1. 拉实际收益：T0 vs T0+5 收盘价算 raw_return；对标基准（见下表）算 alpha_return。
2. 数据不可得（新股 / 长期停牌 / 退市）：跳过本次，条目保持 pending，下次重试。
3. Decision Reflector 按 3 问生成反思（见下）。
4. 写回决策记忆条目：补 REFLECTION 块，状态 pending → reflected。

## 决策记忆

- **位置**：agent 工作区下 `decision-memory/<ticker>/<YYYY-MM-DD>.md`（宿主有既定 memory 目录则放其下，并在 README 说明迁移方式）。
- **append-only**：只追加不改写历史；每条目以 `<!-- ENTRY_END -->` 行结尾作硬分隔。
- **轮转**：每 ticker 保留最近 20 条，超出按日期淘汰最旧。
- **注入规则**：同 ticker 最近 5 条（DECISION + REFLECTION 全量）；跨 ticker 最近 3 条（仅 REFLECTION）。只注入 Portfolio Manager。

## 条目格式

```markdown
---
ticker: 600519
date: 2026-06-24
rating: Buy
holding_period: 5d
raw_return: +3.2%
alpha_return: +1.8%
benchmark: 000300.SH
status: pending | reflected
---

## DECISION
**Rating**: Buy
**Executive Summary**: ...
**Investment Thesis**: ...

## REFLECTION
[Decision Reflector 生成 2-4 句散文；pending 时此块留空]

<!-- ENTRY_END -->
```

**pending 占位规则**：pending 状态时 `raw_return` / `alpha_return` 一律填 `pending`（不用空值、`-` 或 null），反思补做后替换为实际数字并更新 status。

**T+5 日期推定**：优先用数据源交易日历（akshare `tool_trade_date_hist_sina()`，或用行情数据的工作日序列推断）；无法取得日历时按 T+7 自然日近似，并在反思钩子中标注「自然日近似，以交易日历校准」。

## 反思 3 问

1. 方向判断对吗？（必须引用 alpha 数字）
2. 论据哪部分成立、哪部分失败？
3. 一条下次可复用的具体教训。

输出 2-4 句散文，无 bullet / 标题 / markdown 修饰。

## 基准映射

| 市场 | 默认基准 |
|---|---|
| A股 | 000300.SH（沪深300）；中小盘标的可用 000905.SH |
| 美股 | SPY |
| 港股 | 恒生指数 |

显式配置优先于市场默认。
