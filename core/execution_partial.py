"""
BTC Trend Trader Professional v4
Milestone M3

Execution Partial Close

Responsibilities
----------------
- Partial close calculations
- Remaining volume calculations
- Percentage based close
- Quantity validation

This module performs NO:
- MT5 execution
- Order lifecycle
- Trade management
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class PartialCloseResult:
    """
    Result of a partial close calculation.
    """

    valid: bool

    close_volume: float

    remaining_volume: float

    close_percent: float

    reason: str = ""


class PartialCloseEngine:
    """
    Performs partial close calculations.

    Pure calculation engine.
    """

    DEFAULT_PRECISION = 2

    def __init__(
        self,
        volume_precision: int = DEFAULT_PRECISION,
    ):
        self.volume_precision = volume_precision

    # ----------------------------------------------------
    # Utilities
    # ----------------------------------------------------

    def _round(
        self,
        volume: float,
    ) -> float:

        return round(
            max(0.0, volume),
            self.volume_precision,
        )

    # ----------------------------------------------------
    # Validation
    # ----------------------------------------------------

    def validate(
        self,
        current_volume: float,
        close_volume: float,
    ) -> bool:

        if current_volume <= 0:
            return False

        if close_volume <= 0:
            return False

        if close_volume > current_volume:
            return False

        return True

    # ----------------------------------------------------
    # Generic Calculation
    # ----------------------------------------------------

    def calculate(
        self,
        current_volume: float,
        close_volume: float,
    ) -> PartialCloseResult:

        if not self.validate(
            current_volume,
            close_volume,
        ):

            return PartialCloseResult(
                valid=False,
                close_volume=0.0,
                remaining_volume=current_volume,
                close_percent=0.0,
                reason="Invalid close volume.",
            )

        remaining = self._round(
            current_volume - close_volume
        )

        percent = (
            close_volume / current_volume
        ) * 100.0

        return PartialCloseResult(
            valid=True,
            close_volume=self._round(close_volume),
            remaining_volume=remaining,
            close_percent=percent,
        )

    # ----------------------------------------------------
    # Percentage Helpers
    # ----------------------------------------------------

    def by_percentage(
        self,
        current_volume: float,
        percentage: float,
    ) -> PartialCloseResult:

        if percentage <= 0:

            return PartialCloseResult(
                False,
                0.0,
                current_volume,
                0.0,
                "Percentage must be positive.",
            )

        if percentage > 100:

            percentage = 100

        close_volume = self._round(
            current_volume * (percentage / 100.0)
        )

        return self.calculate(
            current_volume,
            close_volume,
        )

    # ----------------------------------------------------
    # Standard Helpers
    # ----------------------------------------------------

    def close_25(
        self,
        current_volume: float,
    ) -> PartialCloseResult:

        return self.by_percentage(
            current_volume,
            25.0,
        )

    def close_50(
        self,
        current_volume: float,
    ) -> PartialCloseResult:

        return self.by_percentage(
            current_volume,
            50.0,
        )

    def close_75(
        self,
        current_volume: float,
    ) -> PartialCloseResult:

        return self.by_percentage(
            current_volume,
            75.0,
        )

    def close_all(
        self,
        current_volume: float,
    ) -> PartialCloseResult:

        return self.calculate(
            current_volume,
            current_volume,
        )

    # ----------------------------------------------------
    # Custom Quantity
    # ----------------------------------------------------

    def close_quantity(
        self,
        current_volume: float,
        quantity: float,
    ) -> PartialCloseResult:

        return self.calculate(
            current_volume,
            quantity,
        )

    # ----------------------------------------------------
    # Remaining Position
    # ----------------------------------------------------

    @staticmethod
    def is_fully_closed(
        remaining_volume: float,
    ) -> bool:

        return remaining_volume <= 0.0

    # ----------------------------------------------------
    # Snapshot
    # ----------------------------------------------------

    def snapshot(
        self,
        result: Optional[PartialCloseResult],
    ):

        if result is None:
            return None

        return {
            "valid": result.valid,
            "close_volume": result.close_volume,
            "remaining_volume": result.remaining_volume,
            "close_percent": result.close_percent,
            "reason": result.reason,
        }