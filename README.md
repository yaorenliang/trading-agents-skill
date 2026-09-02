# trading-agents-sop

**The TradingAgents methodology as a portable agent skill** — multi-agent bull/bear debate, risk debate, centralized 5-tier rating gates, and T+5 deferred reflection, in pure Markdown that any Agent-Skills-compatible harness (Claude Code, Codex, Gemini CLI, Cursor, DSH, ...) can execute directly. Zero Python framework required. Ships with an A-share data-source playbook.

中文速览见文末。

## Why this exists

[TradingAgents](https://github.com/TauricResearch/TradingAgents) (Tauric Research, Apache-2.0) is an excellent multi-agent LLM trading framework — but it is a Python/LangGraph pipeline: clone, install dependencies, configure API keys, run. If your daily driver is an AI coding agent, you do not want another environment to maintain.

This repo re-implements the **methodology** (not the code) as a skill, and adds a **discipline layer** the original does not expose in skill form:

| | TradingAgents (framework) | trading-agents-sop (this skill) |
|---|---|---|
| Form | Python + LangGraph pipeline | Pure Markdown skill (Agent Skills format) |
| Install | clone + deps + API keys | copy one folder |
| Execution | full pipeline every run | tiered: quick path / full SOP / position review / reflection-only |
| Data | built-in US-centric connectors | data-source playbook: akshare / yfinance (free, tokenless), A-share sentiment sources (Xueqiu, Eastmoney guba, Jisilu) |
| Rating | 5-tier via rating.py | centralized 5-tier gate + forced-decisiveness rule (references/rating.md) |
| Reflection | in-process memory log | T+5 deferred reflection with portable Markdown decision memory (readable across harnesses) |
| A-share specifics | limited | price-limit / T+1 / ST / unit / adjustment reminders |

## Install

- **OpenCode**: copy to `~/.config/opencode/skills/trading-agents-sop/` (global) or `.opencode/skills/` (per project).
- **Claude Code**: copy this folder to `~/.claude/skills/trading-agents-sop/` (or `<project>/.claude/skills/`).
- **Other Agent-Skills-compatible harnesses**: same convention — any harness that reads `SKILL.md`.
- No build step. `scripts/fetch_quotes.py` is an optional accelerator (`pip install akshare yfinance`); without it the skill degrades gracefully to web retrieval and marks such numbers as unverified.

## Usage

Talk to your agent:

- 「帮我分析一下 600519」 → full SOP
- "full analysis on NVDA" → full SOP
- 「做个 0700.HK 的交易计划」 → full SOP + risk debate
- 「评估我的 300750 仓位」 → position-review path
- 「反思一下上次茅台的决策」 → reflection only

Outputs follow the fixed report formats in `references/workflow.md`; a complete fictional worked example is in `examples/example-full-analysis.md`.

## Structure

```text
trading-agents-sop/
├── SKILL.md                        # entry: trigger, flow map, hard rules
├── references/
│   ├── workflow.md                 # Phase 0-7, input/output formats, acceptance gates
│   ├── roles.md                    # 14 role cards (analysts / debaters / trader / PM / reflector)
│   ├── rating.md                   # centralized 5-tier rating (single source of truth)
│   ├── reflection.md               # T+5 deferred reflection + decision memory format
│   ├── data-sources.md             # free data playbook (A-share / US / HK) + pitfalls
│   └── methodology.md              # design rationale
├── scripts/
│   └── fetch_quotes.py             # optional tokenless quote accelerator (akshare/yfinance)
├── examples/
│   └── example-full-analysis.md    # fictional end-to-end worked example
├── NOTICE                          # attribution to TradingAgents (Apache-2.0)
└── LICENSE                         # Apache-2.0
```

## Attribution and License

- Methodology inspired by and adapted from **TradingAgents** by Tauric Research (Apache-2.0): repository and paper (arXiv:2412.20138). See `NOTICE`.
- This repo is an independent prompt/orchestration implementation; no TradingAgents source code is redistributed. Not affiliated with Tauric Research.
- Licensed under Apache-2.0.

## Disclaimer

Educational / research tooling. Outputs are analytical demonstrations and **do not constitute investment advice**. Markets involve risk; you are responsible for your own decisions.

## 中文速览

把 TradingAgents 的多 Agent 决策方法论（五大分析师 → 多空辩论 → 研究裁决 → 交易提案 → 风控三方辩论 → 组合终裁 → T+5 延迟反思）做成装上就能用的 agent skill：零 Python 依赖、分级执行（快速通道 / 完整流程 / 仓位评估 / 纯反思）、集中化 5 档评级门禁、决策记忆跨 harness 可移植，并附 A股数据源手册（akshare 免费行情、雪球 / 东财股吧 / 集思录情绪源、涨跌停 / T+1 / 量纲 / 复权提醒）。安装 = 复制目录。仅供研究学习，不构成投资建议。
