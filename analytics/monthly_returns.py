"""
BTC Trend Trader Professional v4
Monthly Returns Analytics
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List


class MonthlyReturns:
    """
    Calculates monthly trading performance.
    """

    # -------------------------------------------------

    def calculate(
        self,
        trades: List[Any],
        starting_balance: float = 0.0,
    ) -> Dict[str, Any]:

        monthly = defaultdict(
            lambda: {
                "net_profit": 0.0,
                "trades": 0,
                "wins": 0,
                "losses": 0,
            }
        )

        for trade in trades:

            exit_time = getattr(
                trade,
                "exit_time",
                None,
            )

            if exit_time is None:
                continue

            if isinstance(exit_time, datetime):

                month = exit_time.strftime("%Y-%m")

            else:

                month = str(exit_time)[:7]

            profit = float(
                getattr(trade, "profit", 0.0)
            )

            monthly[month]["net_profit"] += profit

            monthly[month]["trades"] += 1

            if profit > 0:
                monthly[month]["wins"] += 1

            elif profit < 0:
                monthly[month]["losses"] += 1

        results = {}

        for month, stats in monthly.items():

            trades_count = stats["trades"]

            win_rate = (
                (stats["wins"] / trades_count) * 100.0
                if trades_count
                else 0.0
            )

            return_percent = (
                (stats["net_profit"] / starting_balance)
                * 100.0
                if starting_balance > 0
                else 0.0
            )

            results[month] = {

                "net_profit": round(
                    stats["net_profit"],
                    2,
                ),

                "return_percent": round(
                    return_percent,
                    2,
                ),

                "trades": trades_count,

                "wins": stats["wins"],

                "losses": stats["losses"],

                "win_rate": round(
                    win_rate,
                    2,
                ),

            }

        return dict(
            sorted(results.items())
        )