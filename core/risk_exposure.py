"""
BTC Trend Trader Professional v4
Milestone M3

Exposure Manager

Responsibilities
----------------
- Portfolio exposure
- Symbol exposure
- Account risk
- Open trade risk
- Risk aggregation

This module performs NO:
- MT5 operations
- Trade management
- Position sizing
- Order execution
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class ExposureSnapshot:
    """
    Immutable exposure snapshot.
    """

    total_exposure: float
    account_risk: float
    open_positions: int
    symbol_exposure: Dict[str, float]


class ExposureManager:
    """
    Tracks portfolio exposure.

    Pure state calculations.
    """

    def __init__(self):

        self._symbol_exposure: Dict[str, float] = {}

        self._symbol_risk: Dict[str, float] = {}

        self._open_positions = 0

    # --------------------------------------------------
    # Position Management
    # --------------------------------------------------

    def add_position(
        self,
        symbol: str,
        exposure: float,
        risk: float,
    ):
        """
        Register a new open position.
        """

        self._symbol_exposure[symbol] = (
            self._symbol_exposure.get(symbol, 0.0)
            + exposure
        )

        self._symbol_risk[symbol] = (
            self._symbol_risk.get(symbol, 0.0)
            + risk
        )

        self._open_positions += 1

    def remove_position(
        self,
        symbol: str,
        exposure: float,
        risk: float,
    ):
        """
        Remove exposure from a closed trade.
        """

        if symbol in self._symbol_exposure:

            self._symbol_exposure[symbol] -= exposure

            if self._symbol_exposure[symbol] <= 0:
                del self._symbol_exposure[symbol]

        if symbol in self._symbol_risk:

            self._symbol_risk[symbol] -= risk

            if self._symbol_risk[symbol] <= 0:
                del self._symbol_risk[symbol]

        self._open_positions = max(
            0,
            self._open_positions - 1,
        )

    # --------------------------------------------------
    # Updates
    # --------------------------------------------------

    def update_symbol_exposure(
        self,
        symbol: str,
        exposure: float,
    ):
        """
        Replace exposure for one symbol.
        """

        self._symbol_exposure[symbol] = exposure

    def update_symbol_risk(
        self,
        symbol: str,
        risk: float,
    ):
        """
        Replace risk for one symbol.
        """

        self._symbol_risk[symbol] = risk

    # --------------------------------------------------
    # Queries
    # --------------------------------------------------

    def get_symbol_exposure(
        self,
        symbol: str,
    ) -> float:

        return self._symbol_exposure.get(symbol, 0.0)

    def get_symbol_risk(
        self,
        symbol: str,
    ) -> float:

        return self._symbol_risk.get(symbol, 0.0)

    def total_exposure(self) -> float:
        """
        Total portfolio exposure.
        """

        return sum(self._symbol_exposure.values())

    def total_account_risk(self) -> float:
        """
        Aggregate account risk.
        """

        return sum(self._symbol_risk.values())

    def open_positions(self) -> int:
        """
        Number of open positions.
        """

        return self._open_positions

    # --------------------------------------------------
    # Limits
    # --------------------------------------------------

    def within_max_positions(
        self,
        maximum: int,
    ) -> bool:
        """
        Check position limit.
        """

        return self._open_positions < maximum

    def within_account_risk(
        self,
        maximum_risk: float,
    ) -> bool:
        """
        Check account risk limit.
        """

        return self.total_account_risk() <= maximum_risk

    def within_symbol_risk(
        self,
        symbol: str,
        maximum: float,
    ) -> bool:
        """
        Check symbol-specific risk.
        """

        return (
            self.get_symbol_risk(symbol)
            <= maximum
        )

    # --------------------------------------------------
    # Snapshot
    # --------------------------------------------------

    def snapshot(self) -> ExposureSnapshot:
        """
        Export current exposure.
        """

        return ExposureSnapshot(
            total_exposure=self.total_exposure(),
            account_risk=self.total_account_risk(),
            open_positions=self._open_positions,
            symbol_exposure=dict(self._symbol_exposure),
        )

    # --------------------------------------------------
    # Reset
    # --------------------------------------------------

    def reset(self):
        """
        Clear all exposure information.
        """

        self._symbol_exposure.clear()

        self._symbol_risk.clear()

        self._open_positions = 0