# BTC Trend Trader v1.0

## Overview

BTC Trend Trader is a modular algorithmic trading bot built in Python for MetaTrader 5.

The project is designed for:

- Learning algorithmic trading
- Professional software structure
- Safe development
- Backtesting
- Demo trading
- Live trading (only after successful validation)

---

## Broker

XM

Symbol:

BTCUSD#

Timeframe:

H1

---

## Strategy

Trend Following

Indicators:

- EMA 50
- EMA 200
- ATR 14
- RSI 14
- ADX 14

---

## Risk

Risk per trade:

1%

Maximum open trades:

1

Stop Loss:

ATR × 2

Risk Reward:

1 : 2

---

## Development Rules

Every module is built separately.

Every module is tested before continuing.

No live trading until:

- Backtesting completed
- Demo testing successful
- Risk calculations verified

---

## Project Structure

config.py

core/

tests/

logs/

backtesting/

docs/

---

## Current Status

Foundation Completed

Next:

Production Position Sizer