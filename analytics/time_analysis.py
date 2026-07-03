"""
BTC Trend Trader Professional v4
Time Analysis
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, List


class TimeAnalysis:
    """
    Calculates trading performance by entry hour.
    """

    # -------------------------------------------------

    def calculate(
        self,
        trades: List[Any],
    ) -> Dict[str, Any]:

        hourly = defaultdict(
            lambda: {
                "trades": 0,
                "wins": 0,
                "losses": 0,
                "profit": 0.0,
            }
        )

        for trade in trades:

            entry_time = getattr(
                trade,
                "entry_time",
                None,
            )

            if entry_time is None:
                continue

            hour = entry_time.hour

            profit = float(
                getattr(trade, "profit", 0.0)
            )

            hourly[hour]["trades"] += 1

            hourly[hour]["profit"] += profit

            if profit > 0:
                hourly[hour]["wins"] += 1

            elif profit < 0:
                hourly[hour]["losses"] += 1

        results = {}

        for hour in sorted(hourly.keys()):

            stats = hourly[hour]

            trades_count = stats["trades"]

            win_rate = (
                (stats["wins"] / trades_count) * 100.0
                if trades_count
                else 0.0
            )

            results[f"{hour:02d}:00"] = {

                "trades": trades_count,

                "wins": stats["wins"],

                "losses": stats["losses"],

                "win_rate": round(
                    win_rate,
                    2,
                ),

                "profit": round(
                    stats["profit"],
                    2,
                ),

            }

        return results