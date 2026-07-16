# BTC Trend Trader Professional

# Trade Management

## Overview

The trade management system is responsible for protecting capital, reducing risk, and maximizing profitable trades after an entry signal has been generated.

Trade management operates independently of the strategy logic. Once a trade is opened, every subsequent decision is handled by the trade management system.

---

# Trade Lifecycle

A trade progresses through the following stages:

```text
Signal
    │
    ▼
Position Size Calculation
    │
    ▼
Trade Entry
    │
    ▼
Stop Loss Protection
    │
    ▼
Break-even Management
    │
    ▼
ATR Trailing Stop
    │
    ▼
Partial Profit Taking
    │
    ▼
Time Exit (if required)
    │
    ▼
Trade Closed
```

---

# Position Sizing

Position size is calculated before every trade.

Inputs:

* Account Balance
* Risk Per Trade
* Entry Price
* Stop Loss

The objective is to maintain consistent percentage risk regardless of stop-loss distance.

---

# Initial Stop Loss

Every position is opened with an initial stop loss.

The stop loss is calculated using:

* ATR
* ATR Stop Multiplier

This adapts the stop distance to current market volatility.

---

# Take Profit

The initial take-profit target is calculated using the configured Risk-to-Reward ratio.

Example:

* Risk = 100 points
* RR Ratio = 2

Target:

200 points

---

# Break-even

Break-even protection moves the stop loss to the entry price after a predefined profit threshold.

Configuration:

* ENABLE_BREAK_EVEN
* BREAK_EVEN_R
* BREAK_EVEN_OFFSET

Purpose:

* Protect capital
* Eliminate unnecessary losses after favourable movement

---

# ATR Trailing Stop

After sufficient profit has been achieved, the stop loss begins trailing price using ATR.

Configuration:

* ENABLE_TRAILING_STOP
* TRAILING_STOP_ATR
* TRAILING_START_R

Advantages:

* Locks in profit
* Allows larger trends to continue
* Adapts to changing volatility

---

# Partial Profit Taking

The system can close portions of a position while allowing the remaining volume to continue.

Configuration:

* ENABLE_PARTIAL_TP
* PARTIAL_TP_LEVELS
* PARTIAL_TP_PERCENTAGES

Example:

| R Multiple | Position Closed |
| ---------: | --------------: |
|       0.5R |             25% |
|       1.0R |             25% |
|       2.0R |             50% |

---

# Time Exit

Trades that remain open beyond the configured maximum duration may be closed automatically.

Configuration:

* ENABLE_TIME_EXIT
* MAX_BARS_IN_TRADE

Purpose:

* Prevent capital from being tied up indefinitely
* Reduce exposure during prolonged consolidation

---

# Exit Reasons

Every completed trade records the reason for closure.

Typical exit reasons include:

* Stop Loss
* Take Profit
* Break-even
* Trailing Stop
* Partial Profit
* Time Exit

These values are included in analytics and CSV exports.

---

# Design Principles

The trade management system follows these principles:

* Preserve capital before maximizing returns.
* Automate risk management.
* Separate trade management from strategy generation.
* Keep all management rules configurable.
* Ensure every exit is recorded for analysis.

---

# Future Enhancements

Potential future improvements include:

* Volatility-adjusted profit targets
* Dynamic risk scaling
* Multi-position management
* Portfolio-level risk controls
* Advanced trailing stop models
