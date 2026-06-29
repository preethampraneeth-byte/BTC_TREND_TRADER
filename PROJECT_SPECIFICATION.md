# BTC Trend Trader v1.0
## Project Specification

---

# Objective

Develop a professional, modular Bitcoin trend-following trading bot for MetaTrader 5.

Primary broker:

XM

Primary symbol:

BTCUSD#

Primary timeframe:

H1

---

# Trading Strategy

Trend Following

Indicators

- EMA 50
- EMA 200
- ATR 14
- RSI 14
- ADX 14

Signal Rules

BUY

- EMA 50 > EMA 200
- ADX > 25
- RSI > 50

SELL

- EMA 50 < EMA 200
- ADX > 25
- RSI < 50

Otherwise

HOLD

---

# Risk Rules

Risk per trade:

1%

Maximum open trades:

1

Stop Loss:

ATR × 2

Take Profit:

Risk : Reward = 1 : 2

---

# Development Principles

- Modular architecture
- One responsibility per module
- One complete file at a time
- Every module tested before continuing
- No duplicate code
- Type hints
- Docstrings
- Professional project structure

---

# Trading Modes

Mode 1

Backtesting

↓

Mode 2

Demo Trading

↓

Mode 3

Live Trading

Live trading will only be enabled after successful validation.

---

# Planned Modules

Configuration

MT5 Connector

Market Data

Indicators

Strategy

Risk Manager

Position Size

Order Preview

Trade Executor

Trade Manager

CSV Logger

Backtester

Dashboard

Main Bot

---

# Safety Rules

No live trading by default.

Demo mode first.

Every order must be previewed before execution.

Every trade must be logged.

Maximum one open trade.

Risk management is mandatory.

---

# Current Status

Foundation Completed

Next Module

Production Position Sizer