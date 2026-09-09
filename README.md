# trading-agents-sop

**A股特化的股票分析与交易决策 agent skill** —— 把 TradingAgents 方法论做成便携 skill：多 Agent 多空辩论、风控辩论、集中式 5 档评级门禁、T+5 延迟反思，附 A股数据源手册（akshare / 雪球 / 东财股吧 / 集思录）。纯 Markdown、零 Python 框架；任何兼容 Agent Skills 的 harness（Claude Code、opencode、Codex、Gemini CLI、Cursor、DSH 等）都能直接执行。

适用 **A股 / 港股（0700.HK）/ 美股（NVDA）**。English documentation: [README.en.md](README.en.md)

## 为什么做这个

[TradingAgents](https://github.com/TauricResearch/TradingAgents)（Tauric Research，Apache-2.0）是一个优秀的多 Agent LLM 交易框架——但它是 Python/LangGraph 流水线：clone、装依赖、配 API key、才能跑。如果你的主力工具是 AI 编码 Agent，你不会想再维护一套环境。

本仓库把它的**方法论**（而非代码）重实现为 skill，并补上了原版没有以 skill 形式暴露的纪律层：

| | TradingAgents（框架） | trading-agents-sop（本 skill） |
|---|---|---|
| 形态 | Python + LangGraph 流水线 | 纯 Markdown skill（Agent Skills 格式） |
| 安装 | clone + 依赖 + API key | 复制一个目录 |
| 执行 | 每次跑完整流水线 | 分级：快速通道 / 完整 SOP / 仓位评估 / 纯反思 |
| 数据 | 内置以美股为中心的连接器 | 数据源手册：akshare / yfinance（免费、免 token）+ A股情绪源（雪球、东财股吧、集思录） |
| 评级 | 5 档（rating.py） | 集中式 5 档门禁 + 强制表态规则（references/rating.md） |
| 反思 | 进程内记忆日志 | T+5 延迟反思 + 跨 harness 可移植的 Markdown 决策记忆 |
| A股特化 | 有限 | 涨跌停 / T+1 / ST / 量纲 / 复权提醒 |

## 安装

- **OpenCode**：复制到 `~/.config/opencode/skills/trading-agents-sop/`（全局）或 `.opencode/skills/`（项目级）。
- **Claude Code**：把本目录复制到 `~/.claude/skills/trading-agents-sop/`（或 `<project>/.claude/skills/`）。
- **其他兼容 Agent Skills 的 harness**：同样约定——任何能读 `SKILL.md` 的 harness 都可以。
- 无需构建。`scripts/fetch_quotes.py` 是可选加速器（`pip install akshare yfinance`）；没有它 skill 会优雅降级为 web 检索，并把相应数字标注为未核实。

## 用法

直接对 Agent 说：

- 「帮我分析一下 600519」 → 完整 SOP
- "full analysis on NVDA" → 完整 SOP
- 「做个 0700.HK 的交易计划」 → 完整 SOP + 风控辩论
- 「评估我的 300750 仓位」 → 仓位评估路径
- 「反思一下上次茅台的决策」 → 仅反思

输出遵循 `references/workflow.md` 中的固定报告格式；虚构格式演示见 `examples/example-full-analysis.md`，真实端到端运行（600519，2026-09-02，带来源引用）见 `examples/real-example-600519.md`。

## 目录结构

```text
trading-agents-sop/
├── SKILL.md                        # 入口：触发条件、流程图、硬性规则
├── references/
│   ├── workflow.md                 # Phase 0-7、输入输出格式、验收门禁
│   ├── roles.md                    # 14 张角色卡（分析师 / 辩论员 / 交易员 / PM / 反思员）
│   ├── rating.md                   # 集中式 5 档评级（唯一权威）
│   ├── reflection.md               # T+5 延迟反思 + 决策记忆格式
│   ├── data-sources.md             # 免费数据源手册（A股 / 美股 / 港股）+ 坑位
│   └── methodology.md              # 设计理由
├── scripts/
│   └── fetch_quotes.py             # 可选的免 token 行情加速器（akshare/yfinance）
├── examples/
│   ├── example-full-analysis.md    # 虚构格式演示
│   └── real-example-600519.md      # 真实 Agent 运行（2026-09-02，23 处来源引用）
├── NOTICE                          # TradingAgents（Apache-2.0）署名
└── LICENSE                         # Apache-2.0
```

## 致谢与许可

- 方法论启发并改编自 Tauric Research 的 **TradingAgents**（Apache-2.0）：仓库与论文（arXiv:2412.20138）。见 `NOTICE`。
- 本仓库是独立的 prompt/编排实现；未再分发 TradingAgents 源码。与 Tauric Research 无关联。
- 基于 Apache-2.0 许可开源。

## 免责声明

仅供教育/研究用途。输出为分析演示，**不构成投资建议**。市场有风险，决策请自担。
