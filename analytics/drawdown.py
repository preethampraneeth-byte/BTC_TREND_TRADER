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

    # -------------------------------------------------

    def calculate(
        self,
        trades: List[Any],
    ) -> Dict[str, Any]:

        equity = 0.0
        peak = 0.0

        current_drawdown = 0.0
        maximum_drawdown = 0.0

        for trade in trades:

            profit = getattr(trade, "profit", 0.0)

            equity += profit

            if equity > peak:
                peak = equity

            drawdown = peak - equity

            if drawdown > maximum_drawdown:
                maximum_drawdown = drawdown

            current_drawdown = drawdown

        maximum_drawdown_percent = (
            (maximum_drawdown / peak) * 100.0
            if peak > 0
            else 0.0
        )

        return {

            "current_equity": round(equity, 2),

            "peak_equity": round(peak, 2),

            "current_drawdown": round(
                current_drawdown,
                2,
            ),

            "maximum_drawdown": round(
                maximum_drawdown,
                2,
            ),

            "maximum_drawdown_percent": round(
                maximum_drawdown_percent,
                2,
            ),

        }