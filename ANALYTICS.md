# BTC Trend Trader Professional

# Analytics Guide

## Overview

The analytics system measures trading performance beyond simple profit and loss.

Every completed trade contributes to a growing set of statistics that help evaluate profitability, consistency, risk, and trade management effectiveness.

These metrics are available in both backtesting and paper trading.

---

# Performance Summary

The session summary reports the following core metrics.

| Metric           | Description                             |
| ---------------- | --------------------------------------- |
| Starting Balance | Balance at the beginning of the session |
| Ending Balance   | Balance after the final trade           |
| Net Profit       | Ending Balance − Starting Balance       |
| Return (%)       | Percentage account growth or decline    |
| Total Trades     | Number of completed trades              |
| Winning Trades   | Number of profitable trades             |
| Losing Trades    | Number of losing trades                 |
| Win Rate         | Percentage of winning trades            |

---

# Profitability Metrics

## Gross Profit

Total profit from all winning trades.

---

## Gross Loss

Total loss from all losing trades.

---

## Profit Factor

Formula:

```text
Gross Profit / Gross Loss
```

Interpretation:

* Greater than 1.0 → profitable
* Equal to 1.0 → break-even
* Less than 1.0 → losing system

---

## Average Win

Average profit across winning trades.

---

## Average Loss

Average loss across losing trades.

---

## Largest Win

Highest individual profitable trade.

---

## Largest Loss

Largest individual losing trade.

---

# Risk Metrics

## Maximum Drawdown

Largest decline from peak equity.

Lower values generally indicate better capital preservation.

---

## Recovery Factor

Formula:

```text
Net Profit / Maximum Drawdown
```

Higher values indicate faster recovery from losses.

---

## Sharpe Ratio

Measures return relative to total volatility.

Higher values indicate better risk-adjusted performance.

---

## Sortino Ratio

Measures return relative to downside volatility only.

Unlike Sharpe Ratio, positive volatility is not penalized.

---

## Calmar Ratio

Formula:

```text
Annual Return / Maximum Drawdown
```

Useful for evaluating trend-following systems.

---

# Trade Duration Statistics

The application records trade duration for every completed trade.

Reported statistics include:

* Average Duration
* Shortest Trade
* Longest Trade
* Average Winning Duration
* Average Losing Duration

These values help identify whether profitable trades typically require more or less time than losing trades.

---

# Bars Held

The application records how many completed candles each trade remains open.

Statistics include:

* Average Bars Held
* Average Winning Bars
* Average Losing Bars

This information is useful when tuning time exits and evaluating trade efficiency.

---

# Exit Reason Analysis

Every trade records its closing reason.

Supported exit categories include:

* Stop Loss
* Take Profit
* Break-even
* Trailing Stop
* Time Exit

Exit statistics help evaluate the effectiveness of trade management rules.

---

# CSV Logging

Every completed trade can be exported to CSV.

Typical fields include:

* Entry Time
* Exit Time
* Direction
* Entry Price
* Exit Price
* Stop Loss
* Take Profit
* Lot Size
* Profit
* Result
* Exit Reason
* Bars Held
* Trade Duration

These files can be imported into spreadsheet software for further analysis.

---

# Using Analytics

Analytics should be interpreted across a large sample of trades rather than individual outcomes.

For this project, the recommended validation process is:

1. Complete historical backtesting.
2. Run at least 100 paper trades.
3. Review all performance metrics.
4. Identify recurring weaknesses.
5. Make one controlled improvement at a time.
6. Repeat validation before changing additional logic.

This approach helps prevent optimisation based on small sample sizes.

---

# Design Philosophy

The analytics system exists to support objective decision-making.

Trading decisions should be based on measured performance rather than isolated winning or losing trades.

Consistent evaluation over large datasets produces more reliable conclusions than short-term results.
