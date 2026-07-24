"""
BTC Trend Trader Professional v4
Monthly Performance Analytics
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, List


class MonthlyPerformance:
    """
    Calculates monthly trading performance.
    """

    def calculate(
        self,
        trades: List[Any],
    ) -> Dict[str, Dict[str, float]]:

        monthly = defaultdict(
            lambda: {
                "trades": 0,
                "wins": 0,
                "losses": 0,
                "net_profit": 0.0,
            }
        )

        for trade in trades:

            exit_time = getattr(trade, "exit_time", None)

            if exit_time is None:
                continue

            month = exit_time.strftime("%Y-%m")

            profit = float(getattr(trade, "profit", 0.0))

            stats = monthly[month]

            stats["trades"] += 1
            stats["net_profit"] += profit

            if profit > 0:
                stats["wins"] += 1
            elif profit < 0:
                stats["losses"] += 1

        results = {}

        for month in sorted(monthly):

            stats = monthly[month]

            trades_count = stats["trades"]

            win_rate = (
                stats["wins"] / trades_count * 100
                if trades_count
                else 0.0
            )

            results[month] = {
                "trades": trades_count,
                "wins": stats["wins"],
                "losses": stats["losses"],
                "win_rate": round(win_rate, 2),
                "net_profit": round(stats["net_profit"], 2),
            }

        return results