# BTC Trend Trader Professional

# Architecture

## Overview

BTC Trend Trader Professional is designed as a layered application.

Each layer has a single responsibility and communicates only with the adjacent layer. This separation makes the project easier to maintain, test, and extend.

---

# High-Level Architecture

```text
                 main.py
                     │
                     ▼
         ApplicationRuntime
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
 BacktestRuntime        LiveTradingService
                                 │
                                 ▼
                           LiveRuntime
                                 │
          ┌──────────────┬──────────────┐
          ▼              ▼              ▼
   LiveMarketFeed  LiveStrategyService  RiskManager
          │                              │
          ▼                              ▼
     MT5Connector                Position Size
                                 Calculation
          │
          ▼
  PaperTradeExecutor
          │
          ▼
      Analytics
```

---

# Layer Responsibilities

## main.py

Application entry point.

Responsibilities:

* Parse execution mode.
* Validate configuration.
* Start the application runtime.
* Handle startup failures.

---

## ApplicationRuntime

Responsible for selecting the execution mode.

Supports:

* Backtesting
* Paper Trading

The runtime does not contain trading logic.

---

## BacktestRuntime

Executes historical simulations.

Responsibilities:

* Load historical data.
* Execute the strategy.
* Calculate statistics.
* Generate reports.

---

## LiveTradingService

Acts as a lightweight service layer between the application and the live runtime.

Responsibilities:

* Start the runtime.
* Stop the runtime.

---

## LiveRuntime

The central runtime for paper trading.

Responsibilities:

* Retrieve market data.
* Process completed candles.
* Execute strategy decisions.
* Manage open positions.
* Generate heartbeat messages.
* Perform graceful shutdown.

---

## LiveMarketFeed

Retrieves market data from MetaTrader 5.

Responsibilities:

* Connect to MT5.
* Download the latest candles.
* Disconnect during shutdown.

---

## MT5Connector

Low-level wrapper around the MetaTrader 5 API.

Responsibilities:

* Initialize MT5.
* Authenticate.
* Retrieve market data.
* Disconnect cleanly.

---

## LiveStrategyService

Transforms market data into trading signals.

Outputs:

* BUY
* SELL
* HOLD

---

## RiskManager

Calculates position size.

Inputs:

* Account balance
* Risk percentage
* Entry price
* Stop-loss

Output:

* Lot size

---

## PaperTradeExecutor

Responsible for paper trade management.

Responsibilities:

* Open trades.
* Update trades.
* Close trades.
* Track statistics.
* Print session summaries.

---

# Runtime Flow

Paper Trading executes in the following order:

1. Retrieve the latest candles.
2. Calculate indicators.
3. Generate a trading signal.
4. Update any existing position.
5. Check for new entries.
6. Calculate position size.
7. Execute paper trade.
8. Update analytics.
9. Wait for the next completed candle.

---

# Design Principles

The project follows these principles:

* Single Responsibility Principle
* Layered Architecture
* Separation of Concerns
* Configuration-Driven Behaviour
* Production-Ready Runtime
* Preserve Trading Logic During Refactoring

---

# Future Architecture

Sprint 12 will introduce:

* Live MT5 order execution.
* Live order management.
* Live account monitoring.

The current layered design allows these features to be added without changing the strategy or risk management components.
