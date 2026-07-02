"""
BTC Trend Trader Professional v4
Milestone M3

Break-Even Engine

Responsibilities
----------------
- Calculate break-even stop
- Support configurable R trigger
- Support BUY/SELL trades
- Optional lock-in profit
- Pure calculation only

This module performs NO:
- MT5 operations
- Trade management
- Position sizing
- Risk approval
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class BreakEvenResult:
    """
    Result returned by BreakEvenEngine.
    """

    triggered: bool
    new_stop: float
    current_rr: float


class BreakEvenEngine:
    """
    Professional break-even engine.

    Calculates whether a stop-loss should move
    to break-even (or beyond).

    This class is intentionally stateless.
    """

    def __init__(
        self,
        trigger_rr: float = 1.0,
        lock_in_profit: float = 0.0,
    ):
        self.trigger_rr = trigger_rr
        self.lock_in_profit = lock_in_profit

    # --------------------------------------------------
    # Configuration
    # --------------------------------------------------

    def set_trigger(self, rr: float):
        """
        Configure break-even trigger.
        """

        if rr > 0:
            self.trigger_rr = rr

    def set_lock_in_profit(self, value: float):
        """
        Configure lock-in profit.
        """

        self.lock_in_profit = value

    # --------------------------------------------------
    # Core
    # --------------------------------------------------

    def calculate(
        self,
        entry_price: float,
        current_price: float,
        current_stop: float,
        side: str,
    ) -> BreakEvenResult:
        """
        Calculate proposed break-even stop.

        Returns a BreakEvenResult.
        """

        side = side.upper()

        risk = abs(entry_price - current_stop)

        if risk <= 0:
            return BreakEvenResult(
                False,
                current_stop,
                0.0,
            )

        if side == "BUY":

            reward = current_price - entry_price

            rr = reward / risk

            if rr >= self.trigger_rr:

                new_stop = max(
                    current_stop,
                    entry_price + self.lock_in_profit,
                )

                return BreakEvenResult(
                    True,
                    new_stop,
                    rr,
                )

            return BreakEvenResult(
                False,
                current_stop,
                rr,
            )

        reward = entry_price - current_price

        rr = reward / risk

        if rr >= self.trigger_rr:

            new_stop = min(
                current_stop,
                entry_price - self.lock_in_profit,
            )

            return BreakEvenResult(
                True,
                new_stop,
                rr,
            )

        return BreakEvenResult(
            False,
            current_stop,
            rr,
        )

    # --------------------------------------------------
    # Compatibility Helpers
    # --------------------------------------------------

    def should_trigger(
        self,
        entry_price: float,
        current_price: float,
        current_stop: float,
        side: str,
    ) -> bool:
        """
        Returns True if break-even should trigger.
        """

        return self.calculate(
            entry_price,
            current_price,
            current_stop,
            side,
        ).triggered

    def calculate_stop(
        self,
        entry_price: float,
        current_price: float,
        current_stop: float,
        side: str,
    ) -> float:
        """
        Returns only the proposed stop.

        Useful for backward-compatible integrations.
        """

        return self.calculate(
            entry_price,
            current_price,
            current_stop,
            side,
        ).new_stop

    def current_reward_risk(
        self,
        entry_price: float,
        current_price: float,
        current_stop: float,
        side: str,
    ) -> float:
        """
        Calculate current reward:risk ratio.
        """

        return self.calculate(
            entry_price,
            current_price,
            current_stop,
            side,
        ).current_rr