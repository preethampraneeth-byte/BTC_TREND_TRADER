"""
BTC Trend Trader Professional v4
Trade Management Service

Shared trade-management logic for all execution modes.

Responsibilities
----------------
- Break-even management
- Trailing stop management
- Partial profit management
- Time exit evaluation

This service does NOT:
- Execute trades
- Maintain balances
- Submit orders
- Calculate position size
"""

from __future__ import annotations


class TradeManagementService:
    """
    Shared trade-management service.

    Both the backtester and paper trader will use this
    service so that trade-management behaviour remains
    consistent across execution modes.
    """

    def __init__(self, risk_manager):

        self.risk_manager = risk_manager

    # -------------------------------------------------

    def update_break_even(self, trade, high, low):

        raise NotImplementedError

    # -------------------------------------------------

    def update_trailing_stop(self, trade, high, low, atr):

        raise NotImplementedError

    # -------------------------------------------------

    def update_partial_profit(
        self,
        trade,
        high,
        low,
        timestamp,
    ):

        raise NotImplementedError

    # -------------------------------------------------

    def check_time_exit(
        self,
        trade,
        close,
    ):

        raise NotImplementedError