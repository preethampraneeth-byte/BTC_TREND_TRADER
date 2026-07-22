"""
BTC Trend Trader Professional v4
Trade Statistics
"""

from __future__ import annotations

from typing import Any, Dict, List


class TradeStatistics:
    """
    Calculates trade-related statistics.
    """

    def calculate(
        self,
        trades: List[Any],
    ) -> Dict[str, Any]:

        if not trades:
            return {
                "total_trades": 0,
                "winning_trades": 0,
                "losing_trades": 0,
                "average_profit": 0.0,
                "average_win": 0.0,
                "average_loss": 0.0,
                "largest_win": 0.0,
                "largest_loss": 0.0,
            }

        profits = [
            getattr(trade, "profit", 0.0)
            for trade in trades
        ]

        wins = [
            p
            for p in profits
            if p > 0
        ]

        losses = [
            p
            for p in profits
            if p < 0
        ]

        average_profit = (
            sum(profits)
            / len(profits)
        )

        average_win = (
            sum(wins)
            / len(wins)
            if wins
            else 0.0
        )

        average_loss = (
            sum(losses)
            / len(losses)
            if losses
            else 0.0
        )

        return {

            "total_trades": len(trades),

            "winning_trades": len(wins),

            "losing_trades": len(losses),

            "average_profit": round(
                average_profit,
                2,
            ),

            "average_win": round(
                average_win,
                2,
            ),

            "average_loss": round(
                average_loss,
                2,
            ),

            "largest_win": round(
                max(wins),
                2,
            ) if wins else 0.0,

            "largest_loss": round(
                min(losses),
                2,
            ) if losses else 0.0,

        }