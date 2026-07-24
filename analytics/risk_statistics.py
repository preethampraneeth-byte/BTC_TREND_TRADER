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
                "winning_trades": 0,
                "losing_trades": 0,
                "gross_profit": 0.0,
                "gross_loss": 0.0,
                "average_win": 0.0,
                "average_loss": 0.0,
                "profit_factor": 0.0,
            }

        equity = 0.0
        peak = 0.0
        max_drawdown = 0.0

        consecutive_wins = 0
        consecutive_losses = 0

        max_consecutive_wins = 0
        max_consecutive_losses = 0

        winning_trades = 0
        losing_trades = 0

        gross_profit = 0.0
        gross_loss = 0.0

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

                winning_trades += 1
                gross_profit += profit

            elif profit < 0:
                consecutive_losses += 1
                consecutive_wins = 0

                losing_trades += 1
                gross_loss += abs(profit)

            max_consecutive_wins = max(
                max_consecutive_wins,
                consecutive_wins,
            )

            max_consecutive_losses = max(
                max_consecutive_losses,
                consecutive_losses,
            )

        average_win = (
            gross_profit / winning_trades
            if winning_trades > 0
            else 0.0
        )

        average_loss = (
            gross_loss / losing_trades
            if losing_trades > 0
            else 0.0
        )

        profit_factor = (
            gross_profit / gross_loss
            if gross_loss > 0
            else 0.0
        )

        return {
            "max_drawdown": round(max_drawdown, 2),
            "max_consecutive_wins": max_consecutive_wins,
            "max_consecutive_losses": max_consecutive_losses,
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "gross_profit": round(gross_profit, 2),
            "gross_loss": round(gross_loss, 2),
            "average_win": round(average_win, 2),
            "average_loss": round(average_loss, 2),
            "profit_factor": round(profit_factor, 2),
        }