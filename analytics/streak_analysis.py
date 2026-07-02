"""
BTC Trend Trader Professional v4
Streak Analysis
"""

from __future__ import annotations

from typing import Any, Dict, List


class StreakAnalysis:
    """
    Calculates winning and losing streaks.
    """

    # -------------------------------------------------

    def calculate(
        self,
        trades: List[Any],
    ) -> Dict[str, Any]:

        current_win_streak = 0
        current_loss_streak = 0

        longest_win_streak = 0
        longest_loss_streak = 0

        for trade in trades:

            profit = getattr(trade, "profit", 0.0)

            if profit > 0:

                current_win_streak += 1
                current_loss_streak = 0

            elif profit < 0:

                current_loss_streak += 1
                current_win_streak = 0

            longest_win_streak = max(
                longest_win_streak,
                current_win_streak,
            )

            longest_loss_streak = max(
                longest_loss_streak,
                current_loss_streak,
            )

        return {

            "current_win_streak": current_win_streak,

            "current_loss_streak": current_loss_streak,

            "longest_win_streak": longest_win_streak,

            "longest_loss_streak": longest_loss_streak,

        }