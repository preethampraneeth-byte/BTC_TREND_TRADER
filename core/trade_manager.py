"""
BTC Trend Trader v1.0
Trade Manager

Responsible for deciding whether a new trade
is allowed before execution.
"""

from __future__ import annotations

import MetaTrader5 as mt5
import config


class TradeManager:
    """
    Validates whether a new trade is allowed.
    """

    def can_open_trade(self, symbol: str) -> tuple[bool, str]:
        """
        Returns:
            (True, "Trade allowed")
            (False, "Reason")
        """

        positions = mt5.positions_get(symbol=symbol)

        if positions is None:
            return False, "Unable to retrieve open positions."

        if len(positions) >= config.MAX_OPEN_TRADES:
            return False, "Maximum open trades reached."

        return True, "Trade allowed."