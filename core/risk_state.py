"""
BTC Trend Trader Professional v4
Milestone M3

Risk State

This module stores all risk-related state.

Responsibilities
----------------
- Daily statistics
- Exposure tracking
- Win/Loss streaks
- Open position count
- Drawdown tracking

This module performs NO calculations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Dict


@dataclass
class RiskState:
    """
    Stores all runtime risk state.

    This class intentionally contains no business logic.
    """

    # ---------- Daily Statistics ----------

    current_date: date = field(default_factory=date.today)

    daily_pnl: float = 0.0

    daily_trade_count: int = 0

    daily_win_count: int = 0

    daily_loss_count: int = 0

    daily_drawdown: float = 0.0

    max_daily_drawdown: float = 0.0

    # ---------- Trade Streaks ----------

    consecutive_wins: int = 0

    consecutive_losses: int = 0

    longest_win_streak: int = 0

    longest_loss_streak: int = 0

    # ---------- Exposure ----------

    open_positions: int = 0

    portfolio_exposure: float = 0.0

    account_risk: float = 0.0

    symbol_exposure: Dict[str, float] = field(default_factory=dict)

    # ---------- Limits ----------

    daily_loss_limit_reached: bool = False

    max_positions_reached: bool = False

    max_trades_reached: bool = False

    # ---------- Drawdown ----------

    equity_peak: float = 0.0

    current_equity: float = 0.0

    maximum_drawdown: float = 0.0

    # ---------- Misc ----------

    metadata: Dict = field(default_factory=dict)

    # ============================================================
    # Daily State
    # ============================================================

    def reset_daily(self):
        """
        Reset daily counters.

        Called once per trading day.
        """

        self.current_date = date.today()

        self.daily_pnl = 0.0

        self.daily_trade_count = 0

        self.daily_win_count = 0

        self.daily_loss_count = 0

        self.daily_drawdown = 0.0

        self.daily_loss_limit_reached = False

        self.max_trades_reached = False

    # ============================================================
    # Trade Recording
    # ============================================================

    def record_trade(self, pnl: float):
        """
        Record completed trade result.
        """

        self.daily_trade_count += 1

        self.daily_pnl += pnl

        if pnl >= 0:

            self.daily_win_count += 1

            self.consecutive_wins += 1

            self.consecutive_losses = 0

            self.longest_win_streak = max(
                self.longest_win_streak,
                self.consecutive_wins,
            )

        else:

            self.daily_loss_count += 1

            self.consecutive_losses += 1

            self.consecutive_wins = 0

            self.longest_loss_streak = max(
                self.longest_loss_streak,
                self.consecutive_losses,
            )

    # ============================================================
    # Exposure
    # ============================================================

    def update_exposure(
        self,
        symbol: str,
        exposure: float,
    ):
        """
        Update exposure for one symbol.
        """

        self.symbol_exposure[symbol] = exposure

        self.portfolio_exposure = sum(
            self.symbol_exposure.values()
        )

    def remove_symbol(self, symbol: str):
        """
        Remove symbol exposure.
        """

        if symbol in self.symbol_exposure:
            del self.symbol_exposure[symbol]

        self.portfolio_exposure = sum(
            self.symbol_exposure.values()
        )

    # ============================================================
    # Positions
    # ============================================================

    def increment_open_positions(self):

        self.open_positions += 1

    def decrement_open_positions(self):

        if self.open_positions > 0:
            self.open_positions -= 1

    # ============================================================
    # Drawdown
    # ============================================================

    def update_equity(
        self,
        equity: float,
    ):
        """
        Update equity and drawdown statistics.
        """

        self.current_equity = equity

        if equity > self.equity_peak:
            self.equity_peak = equity

        drawdown = self.equity_peak - equity

        self.daily_drawdown = drawdown

        self.maximum_drawdown = max(
            self.maximum_drawdown,
            drawdown,
        )

        self.max_daily_drawdown = max(
            self.max_daily_drawdown,
            drawdown,
        )

    # ============================================================
    # Risk
    # ============================================================

    def set_account_risk(self, risk: float):

        self.account_risk = risk

    # ============================================================
    # Snapshot
    # ============================================================

    def snapshot(self):
        """
        Export state.

        Useful for persistence and dashboards.
        """

        return {
            "current_date": self.current_date.isoformat(),
            "daily_pnl": self.daily_pnl,
            "daily_trade_count": self.daily_trade_count,
            "daily_win_count": self.daily_win_count,
            "daily_loss_count": self.daily_loss_count,
            "daily_drawdown": self.daily_drawdown,
            "max_daily_drawdown": self.max_daily_drawdown,
            "consecutive_wins": self.consecutive_wins,
            "consecutive_losses": self.consecutive_losses,
            "longest_win_streak": self.longest_win_streak,
            "longest_loss_streak": self.longest_loss_streak,
            "open_positions": self.open_positions,
            "portfolio_exposure": self.portfolio_exposure,
            "account_risk": self.account_risk,
            "symbol_exposure": dict(self.symbol_exposure),
            "daily_loss_limit_reached": self.daily_loss_limit_reached,
            "max_positions_reached": self.max_positions_reached,
            "max_trades_reached": self.max_trades_reached,
            "equity_peak": self.equity_peak,
            "current_equity": self.current_equity,
            "maximum_drawdown": self.maximum_drawdown,
            "metadata": dict(self.metadata),
        }