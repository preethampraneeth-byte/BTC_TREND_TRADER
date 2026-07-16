# BTC Trend Trader Professional

# Configuration Guide

## Overview

All application settings are stored in `config.py`.

The application validates critical configuration values during startup before any connection to MetaTrader 5 or trading activity begins.

---

# MetaTrader 5

| Setting  | Description                    |
| -------- | ------------------------------ |
| LOGIN    | MT5 account login ID           |
| PASSWORD | MT5 account password           |
| SERVER   | Broker server name             |
| MT5_PATH | Optional MT5 installation path |

---

# Trading

| Setting   | Description                                     |
| --------- | ----------------------------------------------- |
| SYMBOL    | Trading instrument (for example BTCUSD#)        |
| TIMEFRAME | Candle timeframe (M1, M5, M15, M30, H1, H4, D1) |

---

# Execution

| Setting        | Description             |
| -------------- | ----------------------- |
| EXECUTION_MODE | BACKTEST, PAPER or LIVE |

---

# Data Source

| Setting       | Description                                |
| ------------- | ------------------------------------------ |
| USE_CSV_DATA  | Use historical CSV data during backtesting |
| CSV_DATA_FILE | CSV file used for historical testing       |

---

# Risk Management

| Setting         | Description                                              |
| --------------- | -------------------------------------------------------- |
| RISK_PER_TRADE  | Fraction of account balance risked per trade (0.01 = 1%) |
| MAX_OPEN_TRADES | Maximum simultaneous positions                           |

---

# Indicators

| Setting    | Description            |
| ---------- | ---------------------- |
| EMA_FAST   | Fast EMA period        |
| EMA_SLOW   | Slow EMA period        |
| ATR_PERIOD | ATR calculation period |
| RSI_PERIOD | RSI calculation period |
| ADX_PERIOD | ADX calculation period |

---

# Strategy

| Setting        | Description               |
| -------------- | ------------------------- |
| ADX_THRESHOLD  | Minimum trend strength    |
| RSI_BUY_LEVEL  | RSI confirmation for BUY  |
| RSI_SELL_LEVEL | RSI confirmation for SELL |

---

# Stops & Targets

| Setting           | Description                  |
| ----------------- | ---------------------------- |
| ATR_SL_MULTIPLIER | ATR multiplier for stop loss |
| RR_RATIO          | Risk-to-reward ratio         |

---

# Paper Trading

| Setting                      | Description                      |
| ---------------------------- | -------------------------------- |
| PAPER_STARTING_BALANCE       | Initial simulated balance        |
| PAPER_ALLOW_NEGATIVE_BALANCE | Allow simulated negative balance |
| PAPER_COMMISSION_PER_LOT     | Commission model                 |
| PAPER_SLIPPAGE               | Simulated slippage               |

---

# Trade Management

## Break-even

| Setting           | Description                  |
| ----------------- | ---------------------------- |
| ENABLE_BREAK_EVEN | Enable break-even            |
| BREAK_EVEN_R      | R multiple before activation |
| BREAK_EVEN_OFFSET | Offset beyond entry price    |

---

## ATR Trailing Stop

| Setting              | Description                       |
| -------------------- | --------------------------------- |
| ENABLE_TRAILING_STOP | Enable trailing stop              |
| TRAILING_STOP_ATR    | ATR multiplier                    |
| TRAILING_START_R     | R multiple before trailing begins |

---

## Partial Profit Taking

| Setting                | Description                               |
| ---------------------- | ----------------------------------------- |
| ENABLE_PARTIAL_TP      | Enable partial exits                      |
| PARTIAL_TP_LEVELS      | Target levels expressed as R multiples    |
| PARTIAL_TP_PERCENTAGES | Position percentages closed at each level |

---

## Time Exit

| Setting           | Description                        |
| ----------------- | ---------------------------------- |
| ENABLE_TIME_EXIT  | Enable maximum trade duration      |
| MAX_BARS_IN_TRADE | Maximum candles allowed in a trade |

---

# Logging

| Setting    | Description             |
| ---------- | ----------------------- |
| LOG_FOLDER | Directory for log files |
| TRADE_LOG  | CSV trade log           |
| ERROR_LOG  | Error log location      |
| LOG_TO_CSV | Enable CSV logging      |

---

# Validation

During startup the application validates:

* Trading symbol
* Timeframe
* Risk configuration
* Starting balances
* Magic number
* Time exit settings
* Partial profit configuration

If validation fails, the application exits before connecting to MetaTrader 5.

---

# Best Practices

* Keep risk per trade conservative.
* Validate configuration after every change.
* Use paper trading before enabling live trading.
* Create a Git checkpoint before modifying production settings.
