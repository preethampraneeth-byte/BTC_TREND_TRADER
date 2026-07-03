"""
BTC Trend Trader Professional v4
Drawdown Analytics
"""

from __future__ import annotations

from typing import Any, Dict, List


class Drawdown:
    """
    Calculates equity drawdown statistics.

    Returns:
        - Current Equity
        - Peak Equity
        - Current Drawdown
        - Maximum Drawdown
        - Maximum Drawdown %
    """

    def calculate(
        self,
        trades: List[Any],
        starting_equity: float = 0.0,
    ) -> Dict[str, Any]:

        equity = float(starting_equity)
        peak = float(starting_equity)

        current_drawdown = 0.0
        maximum_drawdown = 0.0

        for trade in trades:

            profit = float(getattr(trade, "profit", 0.0))

            equity += profit

            if equity > peak:
                peak = equity

            drawdown = peak - equity

            current_drawdown = drawdown
            maximum_drawdown = max(
                maximum_drawdown,
                drawdown,
            )

        denominator = (
            starting_equity
            if starting_equity > 0
            else peak
        )

        maximum_drawdown_percent = (
            (maximum_drawdown / denominator) * 100.0
            if denominator > 0
            else 0.0
        )

        return {
            "current_equity": round(equity, 2),
            "peak_equity": round(peak, 2),
            "current_drawdown": round(current_drawdown, 2),
            "maximum_drawdown": round(maximum_drawdown, 2),
            "maximum_drawdown_percent": round(
                maximum_drawdown_percent,
                2,
            ),
        }