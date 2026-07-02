"""
BTC Trend Trader Professional v4
Equity Curve
"""

from __future__ import annotations

from typing import Any, Dict, List


class EquityCurve:
    """
    Generates cumulative equity curve data from completed trades.
    """

    def calculate(
        self,
        trades: List[Any],
    ) -> Dict[str, Any]:

        equity = 0.0
        curve: List[float] = []

        peak = 0.0
        drawdown = 0.0

        for trade in trades:

            profit = getattr(trade, "profit", 0.0)

            equity += profit
            curve.append(round(equity, 2))

            if equity > peak:
                peak = equity

            current_drawdown = peak - equity

            if current_drawdown > drawdown:
                drawdown = current_drawdown

        return {
            "curve": curve,
            "final_equity": round(equity, 2),
            "peak_equity": round(peak, 2),
            "max_drawdown": round(drawdown, 2),
        }