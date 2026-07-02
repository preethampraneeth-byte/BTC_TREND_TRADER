"""
BTC Trend Trader
Version 4.0 Configuration

This file contains all configurable parameters used by the bot.

Version 4 additions
-------------------
✓ Break-even settings
✓ ATR trailing stop settings
✓ Partial profit settings
✓ Time exit settings
✓ Feature toggles
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
TIMEFRAME = "H1"

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

# Risk per trade (1%)
RISK_PER_TRADE = 0.01

# Maximum simultaneous trades
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

# Risk : Reward
RR_RATIO = 2.0

# ======================================================
# Backtesting
# ======================================================

INITIAL_BALANCE = 10000

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

# Safety switch
DRY_RUN = True

# Live trading disabled by default
ALLOW_LIVE_TRADING = False

# ======================================================
# Order Settings
# ======================================================

MAGIC_NUMBER = 20260627

DEVIATION = 20

ORDER_COMMENT = "BTC Trend Trader v4.0"

# ======================================================
# Trend Strength Filter
# ======================================================

EMA_DISTANCE_ATR_MULTIPLIER = 0.25

# ======================================================
# Version 4 - Trade Management
# ======================================================

# Master switch
ENABLE_TRADE_MANAGEMENT = True

# ------------------------------------------------------
# Break-even
# ------------------------------------------------------

ENABLE_BREAK_EVEN = True

# Move stop-loss to entry after this R multiple
BREAK_EVEN_R = 1.0

# Lock in a small profit after moving to break-even
BREAK_EVEN_OFFSET = 0.0

# ------------------------------------------------------
# ATR Trailing Stop
# ------------------------------------------------------

ENABLE_TRAILING_STOP = False

TRAILING_STOP_ATR = 1.5

# Minimum profit before trailing starts (R multiple)
TRAILING_START_R = 1.5

# ------------------------------------------------------
# Partial Profit Taking
# ------------------------------------------------------

ENABLE_PARTIAL_TP = False

PARTIAL_TP_LEVELS = [
    1.0,
    2.0,
    3.0,
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

# Close trade after this many completed candles
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