# BTC Trend Trader Professional v4

An algorithmic Bitcoin trend-following trading system built with Python and MetaTrader 5.

The project focuses on disciplined trend trading, professional risk management, comprehensive trade analytics, and production-ready engineering practices.

---

# Project Status

**Current Version**

**v4.4 – Sprint 11 Production Readiness**

### Completed

* Backtesting Engine
* Paper Trading Engine
* Risk-Based Position Sizing
* ATR Stop Loss
* Break-even Management
* ATR Trailing Stop
* Partial Profit Taking
* Time Exit
* CSV Trade Logging
* Exit Reason Tracking
* Trade Duration Analytics
* Enhanced Session Summary
* Startup Diagnostics
* Runtime Heartbeat
* Configuration Validation

### Current Development Stage

**Sprint 11 – Production Readiness**

Next milestone:

* Complete 100 paper trades
* Review analytics
* Freeze trading logic
* Begin Sprint 12 (Small Live Account)

---

# Features

## Trading Strategy

* EMA Trend Following
* ADX Trend Strength Filter
* RSI Confirmation
* ATR-Based Stop Loss
* Configurable Risk-to-Reward Ratio

## Risk Management

* Risk-Based Position Sizing
* Break-even Protection
* ATR Trailing Stop
* Partial Profit Taking
* Time-Based Exit

## Trading Modes

* Historical Backtesting
* Paper Trading
* Live Trading (planned)

## Analytics

* Performance Statistics
* Exit Reason Tracking
* Trade Duration Statistics
* Bars Held Analysis
* Profit Factor
* Recovery Factor
* Sharpe Ratio
* Sortino Ratio
* Calmar Ratio
* CSV Trade Export

---

# Project Structure

```text
BTC_TREND_TRADER/

├── core/
│   ├── indicators
│   ├── mt5_connector
│   ├── risk_manager
│   └── config_validator
│
├── live/
│   ├── live_runtime
│   ├── live_market_feed
│   └── paper_trade_executor
│
├── runtime/
│   ├── application_runtime
│   └── backtest_runtime
│
├── services/
│
├── analytics/
│
├── reports/
│
├── data/
│
├── logs/
│
├── config.py
└── main.py
```

---

# Running the Project

## Backtesting

```bash
python main.py
```

## Paper Trading

```bash
python main.py paper
```

## Live Trading

Reserved for Sprint 12.

```bash
python main.py live
```

---

# Runtime Workflow

```text
main.py
      │
      ▼
ApplicationRuntime
      │
      ▼
LiveTradingService
      │
      ▼
LiveRuntime
      │
      ▼
LiveMarketFeed
      │
      ▼
LiveStrategyService
      │
      ▼
RiskManager
      │
      ▼
PaperTradeExecutor
```

---

# Trading Workflow

1. Retrieve latest market data.
2. Calculate indicators.
3. Generate BUY / SELL / HOLD signal.
4. Manage any existing position.
5. Calculate risk-based position size.
6. Open a new trade when appropriate.
7. Manage trade until exit.
8. Record analytics and update session statistics.

---

# Configuration

Application settings are stored in:

```text
config.py
```

Startup validation ensures critical configuration values are checked before trading begins.

---

# Production Readiness

Sprint 11 introduced:

* Safe Startup
* Runtime Lifecycle Management
* Idempotent Shutdown
* Startup Diagnostics
* Runtime Heartbeat
* Configuration Validation

These improvements increase operational reliability without changing the trading strategy.

---

# Roadmap

## Sprint 11

Production Readiness

* Runtime Reliability
* Configuration Validation
* Documentation
* Regression Testing
* Release Candidate

## Sprint 12

Small Live Account

* Freeze Trading Logic
* Execute Live Trades
* Monitor Performance
* Review Risk Controls

---

# Development Principles

* Preserve trading logic unless intentionally improving the strategy.
* Make small, reviewable changes.
* Validate every change before continuing.
* Create a Git checkpoint after each completed phase.
* Prioritize reliability and maintainability over feature growth.

---

# License

This project is intended for educational and personal algorithmic trading research.

Trading financial markets involves substantial risk. Past performance does not guarantee future results.
