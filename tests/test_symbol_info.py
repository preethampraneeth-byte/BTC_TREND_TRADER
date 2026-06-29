import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import config
import MetaTrader5 as mt5

from core.mt5_connector import MT5Connector


def main():

    connector = MT5Connector()

    if not connector.connect():
        return

    symbol = mt5.symbol_info(config.SYMBOL)

    if symbol is None:
        print("Symbol not found.")
        connector.disconnect()
        return

    print("\n===== SYMBOL INFORMATION =====\n")

    print(f"Symbol           : {symbol.name}")
    print(f"Digits           : {symbol.digits}")
    print(f"Point            : {symbol.point}")
    print(f"Trade Contract   : {symbol.trade_contract_size}")
    print(f"Volume Min       : {symbol.volume_min}")
    print(f"Volume Max       : {symbol.volume_max}")
    print(f"Volume Step      : {symbol.volume_step}")
    print(f"Trade Tick Size  : {symbol.trade_tick_size}")
    print(f"Trade Tick Value : {symbol.trade_tick_value}")

    connector.disconnect()


if __name__ == "__main__":
    main()