#!/usr/bin/env python3
# trading-agents-sop 行情加速器（可选组件）。
# 零 token 设计：A股走 akshare，美股/港股走 yfinance。
# 依赖缺失或取数失败时以非零码退出：调用方（agent）应降级为 web 检索，
# 并在报告中把 web 数字标注为"未经核实"。
#
# 用法:
#   python3 fetch_quotes.py 600519 000001 --days 60
#   python3 fetch_quotes.py NVDA 0700.HK --days 30
#
# 依赖（可选，按需安装）:
#   pip install akshare yfinance pandas

import argparse
import datetime as dt
import sys


def is_a_share(ticker):
    return len(ticker) == 6 and ticker.isdigit()


def fetch_a_share(code, days):
    import akshare as ak
    end = dt.date.today()
    start = end - dt.timedelta(days=days)
    return ak.stock_zh_a_hist(
        symbol=code,
        period="daily",
        start_date=start.strftime("%Y%m%d"),
        end_date=end.strftime("%Y%m%d"),
        adjust="qfq",
    )


def fetch_global(symbol, days):
    import yfinance as yf
    return yf.Ticker(symbol).history(period=str(max(days, 7)) + "d")


def to_markdown_rows(df, max_rows=10):
    cols = [str(c) for c in df.columns]
    lines = ["| " + " | ".join(cols) + " |"]
    lines.append("|" + "---|" * len(cols))
    for _, row in df.tail(max_rows).iterrows():
        vals = []
        for c in df.columns:
            v = row[c]
            try:
                v = float(v)
                v = round(v, 0) if abs(v) >= 1000 else round(v, 3)
            except (TypeError, ValueError):
                v = str(v)
            vals.append(str(v))
        lines.append("| " + " | ".join(vals) + " |")
    return lines


def main():
    parser = argparse.ArgumentParser(
        description="Fetch recent OHLCV and print a markdown table (optional accelerator)."
    )
    parser.add_argument("tickers", nargs="+", help="A股 6 位代码 / 美股符号 / 港股如 0700.HK")
    parser.add_argument("--days", type=int, default=60, help="回看自然日数，默认 60")
    args = parser.parse_args()

    hard_fail = False
    for ticker in args.tickers:
        print()
        print("## " + ticker)
        try:
            if is_a_share(ticker):
                df = fetch_a_share(ticker, args.days)
                source = "akshare.stock_zh_a_hist (qfq)"
            else:
                df = fetch_global(ticker, args.days)
                source = "yfinance"
            if df is None or len(df) == 0:
                print("- 无数据返回，降级为 web 检索")
                continue
            close_col = None
            for cand in ("收盘", "Close", "close"):
                if cand in df.columns:
                    close_col = cand
                    break
            if close_col is None:
                close_col = df.columns[-1]
            first = float(df[close_col].iloc[0])
            last = float(df[close_col].iloc[-1])
            chg = (last / first - 1.0) * 100.0
            sign = "+" if chg >= 0 else ""
            print("- 来源: " + source)
            print("- 区间: " + str(df.index[0])[:10] + " -> " + str(df.index[-1])[:10])
            print("- 期初->期末: " + str(round(first, 3)) + " -> " + str(round(last, 3))
                  + "（" + sign + str(round(chg, 2)) + "%）")
            print("- 近 " + str(min(10, len(df))) + " 个交易日:")
            for line in to_markdown_rows(df):
                print(line)
            print("- 量纲提醒: akshare 成交量单位为手、成交额为元；yfinance 为股 / 美元。写入报告前换算并注明。")
        except ImportError as exc:
            print("- 缺少依赖: " + str(exc))
            print("- 安装: pip install akshare yfinance pandas；或降级为 web 检索并标注未经核实")
            hard_fail = True
        except Exception as exc:
            print("- 取数失败: " + str(exc) + " -> 降级为 web 检索并标注未经核实")

    if hard_fail:
        sys.exit(2)


if __name__ == "__main__":
    main()
