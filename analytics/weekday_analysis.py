"""
BTC Trend Trader Professional v4
Weekday Analysis
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, List


class WeekdayAnalysis:
    """
    Calculates trading performance by weekday.
    """

    WEEKDAYS = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    # -------------------------------------------------

    def calculate(
        self,
        trades: List[Any],
    ) -> Dict[str, Any]:

        data = defaultdict(
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

            weekday = self.WEEKDAYS[
                entry_time.weekday()
            ]

            profit = float(
                getattr(
                    trade,
                    "profit",
                    0.0,
                )
            )

            stats = data[weekday]

            stats["trades"] += 1

            stats["profit"] += profit

            if profit > 0:
                stats["wins"] += 1

            elif profit < 0:
                stats["losses"] += 1

        results = {}

        for weekday in self.WEEKDAYS:

            if weekday not in data:
                continue

            stats = data[weekday]

            trades_count = stats["trades"]

            win_rate = (
                (stats["wins"] / trades_count)
                * 100.0
                if trades_count
                else 0.0
            )

            results[weekday] = {

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