import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import config
from core.mt5_connector import MT5Connector

connector = MT5Connector()

if connector.connect():
    connector.account_info()
    connector.symbol_info(config.SYMBOL)
    connector.disconnect()