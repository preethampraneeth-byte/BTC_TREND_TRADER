"""
BTC Trend Trader v1.0
Configuration File
"""

# ======================================================
# MetaTrader 5 Settings
# ======================================================

LOGIN = 318045825          # Your Demo Account
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

# True  = Load historical data from CSV
# False = Download historical data from MT5
USE_CSV_DATA = True

# Historical dataset used for reproducible backtesting
CSV_DATA_FILE = "data/BTCUSD_H1_500.csv"

# ======================================================
# Risk Settings
# ======================================================

RISK_PER_TRADE = 0.01      # 1%

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
# Logging
# ======================================================

LOG_FOLDER = "logs"

TRADE_LOG = "logs/trades.csv"

ERROR_LOG = "logs/errors.log"

# ======================================================
# Trading Mode
# ======================================================

# Safety switch.
# When True, the bot will NEVER send an order.
DRY_RUN = True

# Live trading is disabled by default.
ALLOW_LIVE_TRADING = False

# ======================================================
# CSV Logging
# ======================================================

LOG_TO_CSV = True

# ======================================================
# Order Settings
# ======================================================

MAGIC_NUMBER = 20260627

# Maximum price deviation (points)
DEVIATION = 20

# Order comment shown in MT5
ORDER_COMMENT = "BTC Trend Trader v1.0"

# ======================================================
# Trend Strength Filter
# ======================================================

EMA_DISTANCE_ATR_MULTIPLIER = 0.25

# ======================================================
# Trade Management
# ======================================================

# Enable break-even stop
ENABLE_BREAK_EVEN = True

# Move stop to entry after this many R multiples
BREAK_EVEN_R = 1.0

# Enable ATR trailing stop
ENABLE_TRAILING_STOP = False

# ATR multiplier for trailing stop
TRAILING_STOP_ATR = 1.5

# ======================================================
# Optimization Settings
# ======================================================

# Parameter values tested by optimizer.py

OPTIMIZE_ADX_VALUES = [
    20,
    21,
    22,
    23,
    24,
    25,
]