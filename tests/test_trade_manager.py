import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import config

from core.mt5_connector import MT5Connector
from core.trade_manager import TradeManager


def main():

    connector = MT5Connector()

    if not connector.connect():
        return

    manager = TradeManager()

    allowed, reason = manager.can_open_trade(config.SYMBOL)

    print("\n===== TRADE MANAGER =====\n")

    print(f"Symbol  : {config.SYMBOL}")
    print(f"Allowed : {allowed}")
    print(f"Reason  : {reason}")

    connector.disconnect()


if __name__ == "__main__":
    main()