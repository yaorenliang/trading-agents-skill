# trading-agents-sop

Give it a ticker, get a decision card: rating, entry, stop, the reason it says no, and a hook that makes it face the outcome later.

Below is the final output of one real run on 600519.SH (Kweichow Moutai), quoted as produced on 2026-09-02 with 23 cited sources. Full transcript: [examples/real-example-600519.md](examples/real-example-600519.md).

```text
Rating      Overweight (tier 2 of 5)
Entry       1285-1305, staged, 2% position (up to 4% on a balanced book)
Stop        1116 CNY (about 3% below the 52-week low of 1151.01)
Target      1689.48 CNY (consensus mean, not set by this analysis)
Horizon     3-6 months, decided by the Q3 report and wholesale price
Why not Buy earnings inflection unconfirmed. Why not Hold downside case was weaker than the bottoming case.
Confidence  medium
Reflection  due 5 trading days later; the verdict is written back into the next analysis of the same ticker
```

Data as of 2026-09-02. It shows the output shape, not today's market; ask the agent to fetch fresh numbers. Works for A-share, HK (0700.HK) and US (NVDA). Chinese: [README.md](README.md)

## What differs from upstream TradingAgents

Upstream ([TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents), Apache-2.0) is a Python + LangGraph pipeline: clone it, install dependencies, wire API keys. This repo has no framework at all, just Markdown, so an agent can execute it as installed. Two disciplines upstream does not expose as a skill:

- **A five-tier forced verdict**: the rating has to land in one of five tiers. "Depends" and "needs more observation" are not accepted ([references/rating.md](references/rating.md)).
- **Delayed reflection at T+5**: the decision is persisted to a Markdown memory file, revisited five trading days later against a benchmark, and injected into the next analysis of the same ticker ([references/reflection.md](references/reflection.md)).

Bull/bear debate, the three-way risk debate and fourteen role cards live in references/ and are loaded on demand.

## Install

skills.sh installer, one command for several harnesses (Claude Code, Codex, Cursor, opencode, ...):

```bash
npx skills@latest add yaorenliang/trading-agents-skill
```

Claude Code native marketplace:

```text
/plugin marketplace add yaorenliang/trading-agents-skill
/plugin install trading-agents-sop@trading-agents-skill
```

Manual install for any harness that reads `SKILL.md`: drop this directory into that harness's skills directory under the name `trading-agents-sop`. For opencode that is `~/.config/opencode/skills/trading-agents-sop/`, for Claude Code `~/.claude/skills/trading-agents-sop/`.

Nothing to build. `scripts/fetch_quotes.py` is an optional quote accelerator (`pip install akshare yfinance`). Without it the skill degrades to web retrieval and marks every number it could not verify.

## Prompts that work

- "analyze 600519" full SOP
- "full analysis on NVDA" full SOP
- "make a trade plan for 0700.HK" full SOP plus the risk debate
- "size my 300750 position" position path
- "reflect on my last Moutai call" reflection only

Output follows the fixed report format in [references/workflow.md](references/workflow.md). A fabricated format demo lives in [examples/example-full-analysis.md](examples/example-full-analysis.md).

## Layout

```text
trading-agents-sop/
├── SKILL.md                        # entry point: triggers, flow, hard rules
├── references/
│   ├── workflow.md                 # Phase 0-7, I/O formats, acceptance gates
│   ├── roles.md                    # fourteen role cards
│   ├── rating.md                   # the single source of truth for ratings
│   ├── reflection.md               # T+5 reflection and the memory format
│   ├── data-sources.md             # free data sources and their traps
│   └── methodology.md              # why it is built this way
├── scripts/
│   └── fetch_quotes.py             # optional, token-free quote fetcher
├── examples/
│   ├── example-full-analysis.md    # fabricated format demo
│   └── real-example-600519.md      # real run, 2026-09-02, 23 citations
├── NOTICE                          # TradingAgents (Apache-2.0) attribution
└── LICENSE                         # Apache-2.0
```

## Credits and license

- Method inspired by and adapted from **TradingAgents** by Tauric Research (Apache-2.0), repository plus paper (arXiv:2412.20138). See [NOTICE](NOTICE).
- This repository is an independent prompt/orchestration implementation. It does not redistribute TradingAgents source and is not affiliated with Tauric Research.
- Released under Apache-2.0.

## Disclaimer

Educational use only. The output is a demonstration of an analysis process, not investment advice.
