"""
BTC Trend Trader v1.0
Trade Executor (Dry Run)

Builds an MT5 order request but does NOT send it.
"""

from __future__ import annotations

import MetaTrader5 as mt5
import config


class TradeExecutor:
    """
    Builds an MT5 order request.

    In DRY_RUN mode, the request is only displayed.
    """

    def build_request(self, trade: dict) -> dict | None:

        # Do not build an order for HOLD
        if trade["Signal"] == "HOLD":
            return None

        tick = mt5.symbol_info_tick(config.SYMBOL)

        if tick is None:
            raise RuntimeError(f"Unable to get tick data for {config.SYMBOL}")

        if trade["Signal"] == "BUY":
            order_type = mt5.ORDER_TYPE_BUY
            price = tick.ask

        else:
            order_type = mt5.ORDER_TYPE_SELL
            price = tick.bid

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": config.SYMBOL,
            "volume": trade["LotSize"],
            "type": order_type,
            "price": round(price, 2),
            "sl": trade["StopLoss"],
            "tp": trade["TakeProfit"],
            "deviation": config.DEVIATION,
            "magic": config.MAGIC_NUMBER,
            "comment": config.ORDER_COMMENT,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        return request

    def preview(self, request: dict | None) -> None:

        print("\n" + "=" * 60)
        print("         MT5 ORDER REQUEST (DRY RUN)")
        print("=" * 60)

        if request is None:
            print("No order generated (Signal = HOLD)")
        else:
            for key, value in request.items():
                print(f"{key:15}: {value}")

        print("=" * 60)

        if config.DRY_RUN:
            print("DRY RUN ENABLED")
            print("NO ORDER SENT")
        else:
            print("LIVE EXECUTION ENABLED")