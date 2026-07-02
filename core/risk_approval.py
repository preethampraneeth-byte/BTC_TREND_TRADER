"""
BTC Trend Trader Professional v4
Milestone M3

Risk Approval Engine

Responsibilities
----------------
- Trade approval
- Risk validation
- Exposure validation
- Consolidated decision making

This module performs NO:
- MT5 execution
- Trade management
- Position sizing
- Stop calculations
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from core.risk_exposure import ExposureManager
from core.risk_limits import RiskLimitResult, RiskLimits
from core.risk_state import RiskState


@dataclass
class TradeApproval:
    """
    Final trade approval result.
    """

    approved: bool
    reason: str = ""
    warnings: List[str] = field(default_factory=list)
    metrics: Dict[str, float] = field(default_factory=dict)


class TradeApprovalEngine:
    """
    Combines all risk checks into one decision.

    This class never modifies trades.
    """

    def __init__(
        self,
        limits: Optional[RiskLimits] = None,
        exposure: Optional[ExposureManager] = None,
    ):
        self.limits = limits or RiskLimits()
        self.exposure = exposure or ExposureManager()

    # ----------------------------------------------------
    # Main Approval
    # ----------------------------------------------------

    def approve_trade(
        self,
        state: RiskState,
        symbol: str,
        trade_risk: float,
        symbol_limit: Optional[float] = None,
        account_limit: Optional[float] = None,
    ) -> TradeApproval:
        """
        Perform all approval checks.

        Returns a TradeApproval object.
        """

        # ----------------------------------------
        # Global Risk Limits
        # ----------------------------------------

        result: RiskLimitResult = self.limits.validate(state)

        if not result.approved:

            return TradeApproval(
                approved=False,
                reason=result.reason,
                metrics=self._metrics(state),
            )

        # ----------------------------------------
        # Account Risk
        # ----------------------------------------

        projected_account_risk = (
            self.exposure.total_account_risk()
            + trade_risk
        )

        if (
            account_limit is not None
            and projected_account_risk > account_limit
        ):

            return TradeApproval(
                approved=False,
                reason="Maximum account risk exceeded.",
                metrics=self._metrics(state),
            )

        # ----------------------------------------
        # Symbol Risk
        # ----------------------------------------

        projected_symbol_risk = (
            self.exposure.get_symbol_risk(symbol)
            + trade_risk
        )

        if (
            symbol_limit is not None
            and projected_symbol_risk > symbol_limit
        ):

            return TradeApproval(
                approved=False,
                reason=f"Risk limit exceeded for {symbol}.",
                metrics=self._metrics(state),
            )

        # ----------------------------------------
        # Warnings
        # ----------------------------------------

        warnings = []

        if state.consecutive_losses >= 2:

            warnings.append(
                "Multiple consecutive losing trades."
            )

        if state.daily_drawdown > 0:

            warnings.append(
                "Account currently in drawdown."
            )

        if (
            state.open_positions
            >= max(1, self.limits.max_open_positions - 1)
        ):

            warnings.append(
                "Approaching maximum open positions."
            )

        return TradeApproval(
            approved=True,
            warnings=warnings,
            metrics=self._metrics(state),
        )

    # ----------------------------------------------------
    # Utility
    # ----------------------------------------------------

    def _metrics(
        self,
        state: RiskState,
    ) -> Dict[str, float]:
        """
        Export useful approval metrics.
        """

        return {
            "daily_pnl": state.daily_pnl,
            "daily_drawdown": state.daily_drawdown,
            "maximum_drawdown": state.maximum_drawdown,
            "daily_trade_count": state.daily_trade_count,
            "open_positions": state.open_positions,
            "portfolio_exposure": self.exposure.total_exposure(),
            "account_risk": self.exposure.total_account_risk(),
            "consecutive_wins": state.consecutive_wins,
            "consecutive_losses": state.consecutive_losses,
        }

    # ----------------------------------------------------
    # Convenience Methods
    # ----------------------------------------------------

    def approve(
        self,
        state: RiskState,
        symbol: str,
        trade_risk: float,
    ) -> bool:
        """
        Backward-compatible helper.

        Returns only True/False.
        """

        return self.approve_trade(
            state=state,
            symbol=symbol,
            trade_risk=trade_risk,
        ).approved

    def rejection_reason(
        self,
        state: RiskState,
        symbol: str,
        trade_risk: float,
    ) -> str:
        """
        Return rejection reason only.
        """

        return self.approve_trade(
            state=state,
            symbol=symbol,
            trade_risk=trade_risk,
        ).reason