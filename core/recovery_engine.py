"""
BTC Trend Trader v4.0

Recovery Engine

Responsible for restoring an interrupted trading session.

Responsibilities
----------------
- Restore persisted trade state
- Reattach state to TradeManager
- Validate recovered state
- Clear invalid/corrupt state

This module does NOT:
- Execute trades
- Calculate risk
- Manage MT5 connections
"""

from typing import Optional

from core.trade_persistence import TradePersistence


class RecoveryEngine:
    """
    Restores TradeManager state after restart.
    """

    def __init__(
        self,
        trade_manager,
        persistence: Optional[TradePersistence] = None,
    ):
        self.trade_manager = trade_manager
        self.persistence = persistence or TradePersistence()

    def recover(self):
        """
        Recover the last persisted trade.

        Returns:
            TradeState | None
        """

        trade = self.persistence.load()

        if trade is None:
            return None

        if not self.validate_trade(trade):
            self.persistence.clear()
            return None

        self.trade_manager.trade = trade

        return trade

    def save(self):
        """
        Persist current trade state.

        Returns:
            bool
        """

        trade = self.trade_manager.get_trade()

        if trade is None:
            return False

        return self.persistence.save(trade)

    def clear(self):
        """
        Remove persisted recovery state.
        """

        self.persistence.clear()

    def has_recovery(self):
        """
        Returns True if recovery data exists.
        """

        return self.persistence.exists()

    @staticmethod
    def validate_trade(trade):
        """
        Basic validation of recovered trade.
        """

        required = (
            "trade_id",
            "symbol",
            "side",
            "entry_price",
            "quantity",
            "entry_time",
        )

        for field in required:
            if not hasattr(trade, field):
                return False

        if trade.quantity < 0:
            return False

        if trade.remaining_quantity < 0:
            return False

        if trade.realized_quantity < 0:
            return False

        if trade.remaining_quantity > trade.original_quantity:
            return False

        if trade.realized_quantity > trade.original_quantity:
            return False

        return True