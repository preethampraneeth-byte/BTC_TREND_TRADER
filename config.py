"""
BTC Trend Trader
Version 4.1 Configuration

This file contains all configurable parameters used by the bot.

Version 4 additions
-------------------
✓ Break-even settings
✓ ATR trailing stop settings
✓ Partial profit settings
✓ Time exit settings
✓ Feature toggles

Version 4.1 additions
---------------------
✓ Execution mode selection
✓ Paper trading configuration
"""

# ======================================================
# MetaTrader 5 Settings
# ======================================================

LOGIN = 318045825
PASSWORD = "Trinity@2106"
SERVER = "XMGlobal-MT5 7"

# Leave as None unless MT5 is not detected automatically
MT5_PATH = None

# ======================================================
# Trading Settings
# ======================================================

SYMBOL = "BTCUSD#"
TIMEFRAME = "M1"

# ======================================================
# Execution Mode
# ======================================================

# Available modes:
#
# BACKTEST
# PAPER
# LIVE
#
# BACKTEST -> Existing backtester (default)
# PAPER     -> Simulated live trading
# LIVE      -> Real MT5 execution
#

EXECUTION_MODE = "PAPER"

# ======================================================
# Data Source
# ======================================================

# True = Load historical data from CSV
# False = Download historical data from MT5

USE_CSV_DATA = True

CSV_DATA_FILE = "data/BTCUSD_H1_500.csv"

# ======================================================
# Risk Settings
# ======================================================

RISK_PER_TRADE = 0.01

MAX_OPEN_TRADES = 1

# ======================================================
# Indicator Settings
# ======================================================

EMA_FAST = 50
EMA_SLOW = 200

ATR_PERIOD = 14
RSI_PERIOD = 14
ADX_PERIOD = 14

# ======================================================
# Strategy Settings
# ======================================================

ADX_THRESHOLD = 25

RSI_BUY_LEVEL = 50
RSI_SELL_LEVEL = 50

# ======================================================
# Stop Loss / Take Profit
# ======================================================

ATR_SL_MULTIPLIER = 2.0

RR_RATIO = 2.0

# ======================================================
# Backtesting
# ======================================================

INITIAL_BALANCE = 10000

# ======================================================
# Paper Trading
# ======================================================

PAPER_STARTING_BALANCE = 10000

PAPER_ALLOW_NEGATIVE_BALANCE = False

PAPER_COMMISSION_PER_LOT = 0.0

PAPER_SLIPPAGE = 0.0

# ======================================================
# Logging
# ======================================================

LOG_FOLDER = "logs"

TRADE_LOG = "logs/trades.csv"

ERROR_LOG = "logs/errors.log"

LOG_TO_CSV = True

# ======================================================
# Trading Mode
# ======================================================

DRY_RUN = True

ALLOW_LIVE_TRADING = False

# ======================================================
# Order Settings
# ======================================================

MAGIC_NUMBER = 20260627

DEVIATION = 20

ORDER_COMMENT = "BTC Trend Trader v4.1"

# ======================================================
# Trend Strength Filter
# ======================================================

EMA_DISTANCE_ATR_MULTIPLIER = 0.25

# ======================================================
# Version 4 - Trade Management
# ======================================================

ENABLE_TRADE_MANAGEMENT = True

# ------------------------------------------------------
# Break-even
# ------------------------------------------------------

ENABLE_BREAK_EVEN = True

BREAK_EVEN_R = 1.0

BREAK_EVEN_OFFSET = 0.0

# ------------------------------------------------------
# ATR Trailing Stop
# ------------------------------------------------------

ENABLE_TRAILING_STOP = True

TRAILING_STOP_ATR = 1.5

TRAILING_START_R = 1.0

# ------------------------------------------------------
# Partial Profit Taking
# ------------------------------------------------------

ENABLE_PARTIAL_TP = True

PARTIAL_TP_LEVELS = [
    0.5,
    1.0,
    2.0,
]

PARTIAL_TP_PERCENTAGES = [
    25,
    25,
    50,
]

# ------------------------------------------------------
# Time Exit
# ------------------------------------------------------

ENABLE_TIME_EXIT = False

MAX_BARS_IN_TRADE = 48

# ======================================================
# Optimization Settings
# ======================================================

OPTIMIZE_ADX_VALUES = [
    20,
    21,
    22,
    23,
    24,
    25,
]

OPTIMIZE_EMA_DISTANCE_VALUES = [
    0.10,
    0.15,
    0.20,
    0.25,
    0.30,
    0.35,
    0.40,
]
