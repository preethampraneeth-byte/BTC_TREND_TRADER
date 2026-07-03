"""
BTC Trend Trader Professional v4
Paper Trade Executor
"""

from __future__ import annotations

from typing import Any, Dict, List


class PaperTradeExecutor:
    """
    Executes simulated trades using
    live market signals.

    No orders are sent to MT5.
    """

    def __init__(self):

        self.trades: List[Dict[str, Any]] = []

        self.last_trade_time = None

    # -------------------------------------------------

    def execute(
        self,
        signal: str,
        price: float,
        stop_loss: float,
        take_profit: float,
        lot_size: float,
        timestamp,
    ) -> bool:
        """
        Record a paper trade.

        Returns True if a new trade was created.
        Returns False if this candle has already
        been traded.
        """

        if self.last_trade_time == timestamp:

            return False

        trade = {

            "signal": signal,

            "entry_price": price,

            "stop_loss": stop_loss,

            "take_profit": take_profit,

            "lot_size": lot_size,

            "timestamp": timestamp,

            "status": "OPEN",

        }

        self.trades.append(trade)

        self.last_trade_time = timestamp

        return True

    # -------------------------------------------------

    def get_open_trades(self):

        return self.trades

    # -------------------------------------------------

    def reset(self):

        self.trades.clear()

        self.last_trade_time = None