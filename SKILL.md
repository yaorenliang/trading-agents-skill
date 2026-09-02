---
name: trading-agents-sop
description: Multi-agent stock analysis and trading-decision SOP - the TradingAgents methodology as a portable, zero-dependency agent skill (A-share / HK / US). Use when the user asks to analyze a stock or ticker, whether to buy/sell/hold, for a trade plan, to size or review a position, or to reflect on a past decision - e.g. "analyze NVDA", "600519 能不能买", "帮我分析一下贵州茅台", "做个交易计划", "评估我的仓位", "上次决策对了吗". 触发词：股票分析/个股分析/能不能买/交易计划/仓位评估/持仓怎么办/选股/复盘/反思. Not for pure backtests, factor research, or market screeners.
---

# Trading Agents SOP（股票多空辩论决策 SOP）

把 TradingAgents（Tauric Research, Apache-2.0）的多 Agent 决策方法论做成 agent 可直接执行的 skill：零 Python 框架依赖，装上即用；并附加原框架没有的纪律层（集中化 5 档评级门禁 + T+5 延迟反思回写）与 A股数据源手册。

## 触发后先做

1. 读 `references/workflow.md`（触发分级 + Phase 0-7 全流程 + 输出格式 + 验收门禁）。
2. 按阶段按需加载其余 references（角色卡 / 评级 / 反思 / 数据源），不要一次全读。

## 流程一览

```
[Phase 0] 预处理：补做历史反思 → 解析标的身份（防身份幻觉）
[Phase 1] 五维分析师并行：市场 / 基本面 / 新闻 / 情绪（社媒自由抓取已废弃，防幻觉）
[Phase 2] 多空辩论：默认 2 轮（Bull→Bear→Bull 共 3 次发言，Bear 无第二轮；每次发言必须反驳对方最新论点）
[Phase 3] Research Manager 裁决 → ResearchPlan（5 档评级，强制决断）
[Phase 4] Trader 提案 → TraderProposal（3 档动作 + 入场/止损/仓位）
[Phase 5] 风控三方辩论（条件触发）：Conservative / Aggressive / Neutral
[Phase 6] Portfolio Manager 终裁 → PortfolioDecision（唯一注入历史反思的角色）
[Phase 7] 持久化：决策记忆写入 + 反思钩子登记
```

## 硬规则（任何时候不可省略）

- **可追溯**：报告中每个精确数字必须来自工具输出或可核实的公开来源；禁止编造"历史验证 / 支撑位反弹"。
- **真辩论**：Bull/Bear 必须引用对方最新发言逐点反驳，禁止各说各话。
- **强制决断**：证据一边倒时不允许用 Hold 逃避；Hold 仅用于多空最强论据确实势均力敌。
- **评级单一来源**：5 档词汇以 `references/rating.md` 为准，禁止发明档位或同义改写。
- **免责**：最终输出末尾固定附「本分析为研究流程演示，不构成投资建议」。

## 文件地图

| 文件 | 何时读 |
|------|--------|
| references/workflow.md | 每次执行（必读） |
| references/roles.md | 进入每个阶段前，读对应角色卡 |
| references/rating.md | Phase 3 / Phase 6 |
| references/reflection.md | Phase 0 补做反思 / Phase 7 登记 / 手动反思 |
| references/data-sources.md | Phase 1 取数前 |
| references/methodology.md | 需要理解设计理由时 |
| scripts/fetch_quotes.py | 有 Python 环境时的行情加速器（可选） |
| examples/example-full-analysis.md | 需要输出格式样例时 |
