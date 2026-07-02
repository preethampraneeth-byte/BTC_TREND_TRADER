"""
BTC Trend Trader Professional v4
Performance Metrics
"""

from __future__ import annotations

from typing import Any, Dict, List


class PerformanceMetrics:
    """
    Calculates overall trading performance metrics.
    """

    def calculate(
        self,
        trades: List[Any],
    ) -> Dict[str, Any]:

        total_trades = len(trades)

        winning_trades = sum(
            1 for trade in trades
            if getattr(trade, "profit", 0.0) > 0
        )

        losing_trades = total_trades - winning_trades

        total_profit = sum(
            getattr(trade, "profit", 0.0)
            for trade in trades
        )

        gross_profit = sum(
            getattr(trade, "profit", 0.0)
            for trade in trades
            if getattr(trade, "profit", 0.0) > 0
        )

        gross_loss = abs(
            sum(
                getattr(trade, "profit", 0.0)
                for trade in trades
                if getattr(trade, "profit", 0.0) < 0
            )
        )

        win_rate = (
            (winning_trades / total_trades) * 100.0
            if total_trades
            else 0.0
        )

        profit_factor = (
            gross_profit / gross_loss
            if gross_loss > 0
            else 0.0
        )

        return {
            "total_trades": total_trades,
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "win_rate": round(win_rate, 2),
            "gross_profit": round(gross_profit, 2),
            "gross_loss": round(gross_loss, 2),
            "net_profit": round(total_profit, 2),
            "profit_factor": round(profit_factor, 2),
        }