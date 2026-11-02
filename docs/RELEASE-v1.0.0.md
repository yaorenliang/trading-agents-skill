# v1.0.0

装上之后，对 agent 说一句「帮我分析一下 600519」，你会拿到这样一张卡：

```text
评级       Overweight（5 档中的第 2 档）
入场       1285-1305 分批建 2% 底仓
止损       1116 元（52 周低点下方约 3%）
不做的理由  盈利拐点未确认，所以不给 Buy
事后钩子   T+5 个交易日后补做反思，结论回写进下一次同标的分析
```

## 装

```bash
npx skills@latest add yaorenliang/trading-agents-skill
```

Claude Code 也可以走原生市场：`/plugin marketplace add yaorenliang/trading-agents-skill`，再 `/plugin install trading-agents-sop@trading-agents-skill`。

## 这一版加了什么

- 决策卡前置：README 第一屏就是一次真实运行的最终产出，不再从方法论讲起。
- 标准安装路径：skills.sh 一行命令，加 Claude Code 原生市场（`.claude-plugin/marketplace.json`）。
- 一条可核验的样例：600519.SH，2026-09-02，23 条来源引用，附「未能核实清单」。

## 它不做什么

不预测。不保证收益。不替你做仓位决定。它把一次分析里该问的问题问完、该吵的架吵完，然后把结论压成一个必须表态的档位，并逼自己在五个交易日后回来对账。
