"""
BTC Trend Trader Professional v4
Milestone M3

Risk Limits

Responsibilities
----------------
- Daily loss protection
- Daily trade limits
- Maximum open positions
- Consecutive loss limits
- Drawdown protection

This module performs NO:
- MT5 operations
- Trade management
- Order execution
- Position sizing
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from core.risk_state import RiskState


@dataclass
class RiskLimitResult:
    """
    Result returned by every risk limit check.
    """

    approved: bool
    reason: str = ""


class RiskLimits:
    """
    Central risk limit validator.

    This class validates limits only.
    It never modifies trades or executes orders.
    """

    def __init__(
        self,
        max_daily_loss: float = float("inf"),
        max_daily_trades: int = 999999,
        max_open_positions: int = 999999,
        max_consecutive_losses: int = 999999,
        max_drawdown: float = float("inf"),
    ):

        self.max_daily_loss = max_daily_loss
        self.max_daily_trades = max_daily_trades
        self.max_open_positions = max_open_positions
        self.max_consecutive_losses = max_consecutive_losses
        self.max_drawdown = max_drawdown

    # -----------------------------------------------------
    # Configuration
    # -----------------------------------------------------

    def configure(
        self,
        *,
        max_daily_loss: Optional[float] = None,
        max_daily_trades: Optional[int] = None,
        max_open_positions: Optional[int] = None,
        max_consecutive_losses: Optional[int] = None,
        max_drawdown: Optional[float] = None,
    ):
        """
        Update one or more limits.
        """

        if max_daily_loss is not None:
            self.max_daily_loss = max_daily_loss

        if max_daily_trades is not None:
            self.max_daily_trades = max_daily_trades

        if max_open_positions is not None:
            self.max_open_positions = max_open_positions

        if max_consecutive_losses is not None:
            self.max_consecutive_losses = max_consecutive_losses

        if max_drawdown is not None:
            self.max_drawdown = max_drawdown

    # -----------------------------------------------------
    # Individual Checks
    # -----------------------------------------------------

    def check_daily_loss(
        self,
        state: RiskState,
    ) -> RiskLimitResult:

        if abs(state.daily_pnl) >= self.max_daily_loss and state.daily_pnl < 0:

            state.daily_loss_limit_reached = True

            return RiskLimitResult(
                False,
                "Maximum daily loss reached.",
            )

        return RiskLimitResult(True)

    def check_daily_trades(
        self,
        state: RiskState,
    ) -> RiskLimitResult:

        if state.daily_trade_count >= self.max_daily_trades:

            state.max_trades_reached = True

            return RiskLimitResult(
                False,
                "Maximum daily trades reached.",
            )

        return RiskLimitResult(True)

    def check_open_positions(
        self,
        state: RiskState,
    ) -> RiskLimitResult:

        if state.open_positions >= self.max_open_positions:

            state.max_positions_reached = True

            return RiskLimitResult(
                False,
                "Maximum open positions reached.",
            )

        return RiskLimitResult(True)

    def check_consecutive_losses(
        self,
        state: RiskState,
    ) -> RiskLimitResult:

        if (
            state.consecutive_losses
            >= self.max_consecutive_losses
        ):

            return RiskLimitResult(
                False,
                "Maximum consecutive losses reached.",
            )

        return RiskLimitResult(True)

    def check_drawdown(
        self,
        state: RiskState,
    ) -> RiskLimitResult:

        if (
            state.maximum_drawdown
            >= self.max_drawdown
        ):

            return RiskLimitResult(
                False,
                "Maximum drawdown reached.",
            )

        return RiskLimitResult(True)

    # -----------------------------------------------------
    # Combined Validation
    # -----------------------------------------------------

    def validate(
        self,
        state: RiskState,
    ) -> RiskLimitResult:
        """
        Execute every configured risk check.

        Stops at the first failed rule.
        """

        checks = (
            self.check_daily_loss,
            self.check_daily_trades,
            self.check_open_positions,
            self.check_consecutive_losses,
            self.check_drawdown,
        )

        for check in checks:

            result = check(state)

            if not result.approved:
                return result

        return RiskLimitResult(True)

    # -----------------------------------------------------
    # Utility
    # -----------------------------------------------------

    def reset_flags(
        self,
        state: RiskState,
    ):
        """
        Reset runtime limit flags.
        """

        state.daily_loss_limit_reached = False
        state.max_positions_reached = False
        state.max_trades_reached = False

    def snapshot(self):
        """
        Export configured limits.
        """

        return {
            "max_daily_loss": self.max_daily_loss,
            "max_daily_trades": self.max_daily_trades,
            "max_open_positions": self.max_open_positions,
            "max_consecutive_losses": self.max_consecutive_losses,
            "max_drawdown": self.max_drawdown,
        }