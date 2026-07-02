"""
BTC Trend Trader Professional v4
Milestone M3

Trailing Stop Engine

Responsibilities
----------------
- Fixed trailing stop
- ATR trailing stop
- Highest/Lowest price tracking
- BUY/SELL support
- Pure calculations only

This module performs NO:
- MT5 operations
- Trade management
- Risk approval
- Position sizing
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class TrailingResult:
    """
    Result of trailing stop calculation.
    """

    updated: bool
    new_stop: float
    trail_price: float


class TrailingEngine:
    """
    Stateless trailing stop calculator.
    """

    def __init__(
        self,
        trailing_distance: float = 0.0,
        atr_period: int = 14,
        atr_multiplier: float = 2.0,
    ):
        self.trailing_distance = trailing_distance
        self.atr_period = atr_period
        self.atr_multiplier = atr_multiplier

    # -------------------------------------------------
    # Configuration
    # -------------------------------------------------

    def set_trailing_distance(
        self,
        distance: float,
    ):
        if distance >= 0:
            self.trailing_distance = distance

    def set_atr_period(
        self,
        period: int,
    ):
        if period > 0:
            self.atr_period = period

    def set_atr_multiplier(
        self,
        multiplier: float,
    ):
        if multiplier > 0:
            self.atr_multiplier = multiplier

    # -------------------------------------------------
    # Fixed Trailing
    # -------------------------------------------------

    def calculate_fixed(
        self,
        current_stop: float,
        current_price: float,
        highest_price: float,
        lowest_price: float,
        side: str,
        trailing_distance: Optional[float] = None,
    ) -> TrailingResult:
        """
        Fixed trailing stop.
        """

        if trailing_distance is None:
            trailing_distance = self.trailing_distance

        if trailing_distance <= 0:
            return TrailingResult(
                False,
                current_stop,
                current_price,
            )

        side = side.upper()

        if side == "BUY":

            proposed = highest_price - trailing_distance

            if proposed > current_stop:
                return TrailingResult(
                    True,
                    proposed,
                    highest_price,
                )

            return TrailingResult(
                False,
                current_stop,
                highest_price,
            )

        proposed = lowest_price + trailing_distance

        if proposed < current_stop:
            return TrailingResult(
                True,
                proposed,
                lowest_price,
            )

        return TrailingResult(
            False,
            current_stop,
            lowest_price,
        )

    # -------------------------------------------------
    # ATR Trailing
    # -------------------------------------------------

    def calculate_atr(
        self,
        current_stop: float,
        highest_price: float,
        lowest_price: float,
        atr: float,
        side: str,
        multiplier: Optional[float] = None,
    ) -> TrailingResult:
        """
        ATR trailing stop.

        ATR calculation is intentionally NOT performed here.
        """

        if multiplier is None:
            multiplier = self.atr_multiplier

        if atr <= 0:
            return TrailingResult(
                False,
                current_stop,
                highest_price if side.upper() == "BUY" else lowest_price,
            )

        side = side.upper()

        if side == "BUY":

            proposed = highest_price - (atr * multiplier)

            if proposed > current_stop:
                return TrailingResult(
                    True,
                    proposed,
                    highest_price,
                )

            return TrailingResult(
                False,
                current_stop,
                highest_price,
            )

        proposed = lowest_price + (atr * multiplier)

        if proposed < current_stop:
            return TrailingResult(
                True,
                proposed,
                lowest_price,
            )

        return TrailingResult(
            False,
            current_stop,
            lowest_price,
        )

    # -------------------------------------------------
    # Compatibility Helpers
    # -------------------------------------------------

    def calculate_stop(
        self,
        current_stop: float,
        current_price: float,
        highest_price: float,
        lowest_price: float,
        side: str,
    ) -> float:
        """
        Backward-compatible helper.

        Uses fixed trailing.
        """

        return self.calculate_fixed(
            current_stop=current_stop,
            current_price=current_price,
            highest_price=highest_price,
            lowest_price=lowest_price,
            side=side,
        ).new_stop

    def should_update(
        self,
        current_stop: float,
        current_price: float,
        highest_price: float,
        lowest_price: float,
        side: str,
    ) -> bool:
        """
        Returns True if fixed trailing
        should update the stop.
        """

        return self.calculate_fixed(
            current_stop=current_stop,
            current_price=current_price,
            highest_price=highest_price,
            lowest_price=lowest_price,
            side=side,
        ).updated

    # -------------------------------------------------
    # Utility
    # -------------------------------------------------

    @staticmethod
    def update_highest(
        highest_price: float,
        current_price: float,
    ) -> float:
        """
        Update highest traded price.
        """

        return max(highest_price, current_price)

    @staticmethod
    def update_lowest(
        lowest_price: float,
        current_price: float,
    ) -> float:
        """
        Update lowest traded price.
        """

        return min(lowest_price, current_price)