"""
BTC Trend Trader Professional v4
Trade Duration Analytics
"""

from __future__ import annotations

from datetime import timedelta
from typing import Any, Dict, List


class TradeDuration:
    """
    Calculates trade duration statistics.
    """

    # -------------------------------------------------

    def calculate(
        self,
        trades: List[Any],
    ) -> Dict[str, Any]:

        durations = []

        winning = []

        losing = []

        for trade in trades:

            entry_time = getattr(
                trade,
                "entry_time",
                None,
            )

            exit_time = getattr(
                trade,
                "exit_time",
                None,
            )

            if entry_time is None or exit_time is None:
                continue

            duration = exit_time - entry_time

            if not isinstance(duration, timedelta):
                continue

            seconds = duration.total_seconds()

            durations.append(seconds)

            profit = float(
                getattr(trade, "profit", 0.0)
            )

            if profit > 0:
                winning.append(seconds)

            elif profit < 0:
                losing.append(seconds)

        if not durations:

            return {

                "average_duration": 0,

                "shortest_duration": 0,

                "longest_duration": 0,

                "average_winning_duration": 0,

                "average_losing_duration": 0,

            }

        return {

            "average_duration": round(
                sum(durations) / len(durations),
                2,
            ),

            "shortest_duration": round(
                min(durations),
                2,
            ),

            "longest_duration": round(
                max(durations),
                2,
            ),

            "average_winning_duration": round(
                sum(winning) / len(winning),
                2,
            ) if winning else 0,

            "average_losing_duration": round(
                sum(losing) / len(losing),
                2,
            ) if losing else 0,

        }