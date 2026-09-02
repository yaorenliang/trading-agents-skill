# 执行工作流（Phase 0-7）

## 0. 触发分级（先分级，再决定深度）

| 触发 | 级别 | 流程 |
|---|---|---|
| "XX股票怎么样 / 最近走势" | 快速通道 | 单分析师简答 + 免责声明，不走辩论 |
| "分析XX股票" / "能不能买" | 完整流程 | Phase 0-7 全量 |
| "做个交易计划" | 完整流程 | 全量，risk_level 默认 medium |
| "评估我的XX仓位" | 仓位通道 | Phase 1 精简（只做与持仓相关维度）+ 多空辩论 + PM 终裁 |
| "上次决策对了吗 / 反思一下" | 反思通道 | 只跑 `references/reflection.md` 流程 |

## 1. 输入参数

```yaml
ticker: <必填。A股 6 位代码 / 港股如 0700.HK / 美股如 NVDA>
analysis_date: <默认今天>
holding_period: 5d            # 反思窗口（可按用户意图调整）
risk_level: low | medium | high   # 用户未指定时默认 medium
enable_risk_debate: auto      # medium/high 或提案仓位 > 10% 时强制开启
```

## Phase 0 预处理

1. **反思补做**：扫描决策记忆中该 ticker 的 pending 条目，按 `references/reflection.md` 补做到期反思，产出 past_context。
2. **身份解析**：把 ticker 解析为 交易所 + 全名 + 代码（防身份幻觉：如 000001 是平安银行，不是上证指数）。解析不了就先问用户。
3. 建任务清单（宿主有 todo 工具则建，逐阶段更新）。

## Phase 1 五维分析师（并行）

按 `references/roles.md` 角色卡产出 4 份报告（市场 / 基本面 / 新闻 / 情绪）+ 可选资金流报告。统一输出格式：

```markdown
## [维度] 报告
### 核心结论        # 3-5 条要点
### 数据支撑        # 具体数字 + 来源，每个数字可追溯
### 风险点
### 关键判断        # 一句话
### 关键数据表      # | 指标 | 数值 | 来源 | 判断 |
```

取数：优先 `scripts/fetch_quotes.py` + 数据源手册（`references/data-sources.md`）；无 Python 环境则全部 web 检索，检索不到的数字不得写入报告；web 数字按手册「来源分级」规则引用（权威页面可见数字可引用，摘要级仅方向性）。

长度预算（默认紧凑模式，用户显式要求深挖时放开）：每份分析师报告**正文（数据表以外的叙述部分）**≤200 字、核心结论 ≤5 条；辩论与风控每轮发言 ≤150 字。跳过可选报告（资金流）时，必须在交付清单注明「跳过 + 原因」。

## Phase 2 多空辩论（默认 2 轮）

- R1：Bull 基于 4 份报告给 3-5 条多头论据 + 1 条对潜在空头论点的预防；Bear 读 Bull 发言逐点反驳。
- R2（默认执行）：Bull 针对 Bear 指出的弱点回应。2 轮 = Bull→Bear→Bull 共 3 次发言（Bear 全程发言 1 次），2 轮后必终止，更多轮次需用户显式要求。
- 纪律：必须引用对方最新发言反驳；禁止重复已说过的论据。

## Phase 3 Research Manager 裁决

读完整辩论历史（不是单方转述），输出：

```markdown
## ResearchPlan
Recommendation: Buy / Overweight / Hold / Underweight / Sell   # 见 rating.md
Rationale: [引用双方论据裁决]
Strategic Actions: [2-4 条建议动作]
```

## Phase 4 Trader 提案

输出 TraderProposal（格式见下）。Trader 是翻译者不是辩论者。

## Phase 5 风控三方辩论（条件触发）

- 触发：risk_level 属于 medium / high，或 Trader 提案仓位 > 10%。
- 顺序：Conservative → Aggressive → Neutral 各发言 1 次（口语化，必须反驳前面发言者），3 次后终止。

## Phase 6 Portfolio Manager 终裁

唯一注入 past_context（历史反思）的角色。输出 PortfolioDecision（格式见下）。评级与 ResearchPlan 不一致时必须解释原因。

## Phase 7 持久化

1. 决策写入 `decision-memory/<ticker>/<YYYY-MM-DD>.md`（格式见 `references/reflection.md`，状态 pending）。
2. 登记反思钩子：T+5 个交易日后补做（下次同 ticker 分析的 Phase 0 会自动补做；宿主支持定时任务时可另行登记）。
3. 跑验收门禁（下文）后交付。

## 输出格式

### TraderProposal

```markdown
## 交易员提案
**Action**: Buy / Hold / Sell（3 档）
**Reasoning**: [2-4 句推理，基于 ResearchPlan + 分析师报告]
**Entry Price**: [具体价格或区间]
**Stop Loss**: [具体价格]（给出方法：ATR × N 倍，或关键支撑位下方 X%）
**Position Sizing**: [建议仓位百分比]（按账户规模和 ATR 调整）
- 保守账户：X%
- 平衡账户：Y%
- 激进账户：Z%
**Holding Period**: [建议持有期，如 5-10 个交易日]
**Invalidation Condition**: [何时失效退出，如"跌破 MA50"或"财报低于预期 X%"]
```

### PortfolioDecision

```markdown
## 最终投资决策
**Rating**: Buy / Overweight / Hold / Underweight / Sell（5 档，见 rating.md）
**Executive Summary**: [2-4 句行动方案：入场策略 + 仓位 + 关键价位 + 持有期]
**Investment Thesis**: [详细推理，引用分析师报告 + 辩论 + 历史反思的具体证据]
**Price Target**: [目标价]（可选）
**Time Horizon**: [持有期，如 3-6 个月]（可选）
**Key Risks**: [3-5 条关键风险]
**Decision Confidence**: low / medium / high
---
**Reflection Hook**: T+5 个交易日后将补做反思，结果注入下次同标的分析。
*本分析为研究流程演示，不构成投资建议。*
```

## 验收门禁（交付前必查，任一不过即返工）

- [ ] 4 份分析师报告齐全，每个精确数字可追溯
- [ ] 辩论是真反驳（引用对方论点），不是各说各话
- [ ] ResearchPlan / PortfolioDecision 使用 5 档标准词汇，评级有至少 2 条论据支撑
- [ ] 风控辩论触发条件检查过（该触发而未触发 = 返工）
- [ ] PM 终裁注入了历史反思（如存在）
- [ ] 决策记忆已写入，反思钩子已登记
- [ ] 跳过的可选件（如资金流报告）已注明原因
- [ ] 免责声明已附
