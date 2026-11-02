# trading-agents-sop

输入一个代码，输出一张决策卡：评级、入场、止损、不做的理由、事后复盘钩子。

下面是 600519.SH 一次真实运行的最终产出，原文照搬（2026-09-02，23 条来源引用，完整样例见 [examples/real-example-600519.md](examples/real-example-600519.md)）：

```text
评级       Overweight（5 档中的第 2 档）
入场       1285-1305 分批建 2% 底仓（平衡账户至 4%）
止损       1116 元（52 周低点 1151.01 下方约 3%）
目标       1689.48 元（机构目标均价，非本分析自设）
期限       3-6 个月，以 2026Q3 财报与飞天批价验证
不做的理由  盈利拐点未确认，所以不给 Buy；底部论据强于持平论据，所以不给 Hold
置信度     medium
事后钩子   T+5 个交易日后补做反思，结论回写进下一次同标的分析
```

数据时点 2026-09-02，仅用于展示输出形态；要看当前市况，让 agent 重新取数。适用 A 股、港股（0700.HK）、美股（NVDA）。English: [README.en.md](README.en.md)

## 它和原版 TradingAgents 差在哪

原版（[TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents)，Apache-2.0）是 Python + LangGraph 流水线：clone、装依赖、配 key 才能跑。这里没有 Python 框架，只有一份 Markdown，装上就能让 agent 执行，另外补了两条原版没有以 skill 形式暴露的纪律：

- **5 档强制决断**：评级必须落到 5 档之一，不接受"看情况""需要进一步观察"这类不表态（[references/rating.md](references/rating.md)）。
- **T+5 延迟反思**：决策写进 Markdown 记忆文件，5 个交易日后回来对账（真实收益对基准），结论注入下一次同标的分析（[references/reflection.md](references/reflection.md)）。

多空辩论、风控三方辩论、14 张角色卡都在 references/ 里，按需要加载，不一次全读。

## 安装

skills.sh 安装器（一次装到多个 harness，Claude Code / Codex / Cursor / opencode 等）：

```bash
npx skills@latest add yaorenliang/trading-agents-skill
```

Claude Code 原生市场：

```text
/plugin marketplace add yaorenliang/trading-agents-skill
/plugin install trading-agents-sop@trading-agents-skill
```

手动安装（任何能读 `SKILL.md` 的 harness）：把本目录放进该 harness 的 skills 目录，目录名用 `trading-agents-sop`。opencode 是 `~/.config/opencode/skills/trading-agents-sop/`，Claude Code 是 `~/.claude/skills/trading-agents-sop/`。

无需构建。`scripts/fetch_quotes.py` 是可选的行情加速器（`pip install akshare yfinance`）；没有它 skill 会退化为 web 检索，并把核实不到的数字明确标注出来。

## 一句话就能用

- 「帮我分析一下 600519」 完整 SOP
- "full analysis on NVDA" 完整 SOP
- 「做个 0700.HK 的交易计划」 完整 SOP + 风控辩论
- 「评估我的 300750 仓位」 仓位评估路径
- 「反思一下上次茅台的决策」 只走反思

输出遵循 [references/workflow.md](references/workflow.md) 里的固定报告格式。虚构的格式演示见 [examples/example-full-analysis.md](examples/example-full-analysis.md)。

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
│   └── real-example-600519.md      # 真实运行（2026-09-02，23 处来源引用 + 未核实清单）
├── NOTICE                          # TradingAgents（Apache-2.0）署名
└── LICENSE                         # Apache-2.0
```

## 致谢与许可

- 方法论启发并改编自 Tauric Research 的 **TradingAgents**（Apache-2.0）：仓库与论文（arXiv:2412.20138）。见 [NOTICE](NOTICE)。
- 本仓库是独立的 prompt/编排实现，未再分发 TradingAgents 源码，与 Tauric Research 无关联。
- 基于 Apache-2.0 许可开源。

## 免责声明

仅供教育研究。输出是分析演示，不构成投资建议。
