"""
BTC Trend Trader Professional v4
Risk Statistics
"""

from __future__ import annotations

from typing import Any, Dict, List


class RiskStatistics:
    """
    Calculates risk-related trading statistics.
    """

    def calculate(
        self,
        trades: List[Any],
    ) -> Dict[str, Any]:

        if not trades:
            return {
                "max_drawdown": 0.0,
                "max_consecutive_wins": 0,
                "max_consecutive_losses": 0,
            }

        equity = 0.0
        peak = 0.0
        max_drawdown = 0.0

        consecutive_wins = 0
        consecutive_losses = 0

        max_consecutive_wins = 0
        max_consecutive_losses = 0

        for trade in trades:

            profit = getattr(trade, "profit", 0.0)

            equity += profit

            if equity > peak:
                peak = equity

            drawdown = peak - equity

            if drawdown > max_drawdown:
                max_drawdown = drawdown

            if profit > 0:
                consecutive_wins += 1
                consecutive_losses = 0
            elif profit < 0:
                consecutive_losses += 1
                consecutive_wins = 0

            max_consecutive_wins = max(
                max_consecutive_wins,
                consecutive_wins,
            )

            max_consecutive_losses = max(
                max_consecutive_losses,
                consecutive_losses,
            )

        return {
            "max_drawdown": round(max_drawdown, 2),
            "max_consecutive_wins": max_consecutive_wins,
            "max_consecutive_losses": max_consecutive_losses,
        }