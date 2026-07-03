"""
BTC Trend Trader Professional v4
Risk Metrics
"""

from __future__ import annotations

import math
from typing import Any, Dict, List


class RiskMetrics:
    """
    Calculates professional trading risk metrics.

    Current metrics
    ----------------
    • Sharpe Ratio
    • Sortino Ratio
    • Calmar Ratio
    """

    # -------------------------------------------------

    def calculate(
        self,
        trades: List[Any],
        risk_free_rate: float = 0.0,
    ) -> Dict[str, Any]:

        returns = [
            float(getattr(trade, "profit", 0.0))
            for trade in trades
        ]

        if len(returns) < 2:

            return {

                "sharpe_ratio": 0.0,

                "sortino_ratio": 0.0,

                "calmar_ratio": 0.0,

            }

        #
        # Mean Return
        #

        mean_return = sum(returns) / len(returns)

        #
        # Standard Deviation
        #

        variance = sum(

            (r - mean_return) ** 2

            for r in returns

        ) / (len(returns) - 1)

        std_dev = math.sqrt(variance)

        sharpe = (

            (mean_return - risk_free_rate) / std_dev

            if std_dev > 0

            else 0.0

        )

        #
        # Downside Deviation
        #

        downside = [

            r

            for r in returns

            if r < risk_free_rate

        ]

        if len(downside) > 1:

            downside_mean = sum(downside) / len(downside)

            downside_variance = sum(

                (r - downside_mean) ** 2

                for r in downside

            ) / (len(downside) - 1)

            downside_std = math.sqrt(

                downside_variance

            )

            sortino = (

                (mean_return - risk_free_rate)

                / downside_std

                if downside_std > 0

                else 0.0

            )

        else:

            sortino = 0.0

        #
        # Calmar Ratio
        #

        total_return = sum(returns)

        peak = 0.0
        equity = 0.0
        max_drawdown = 0.0

        for value in returns:

            equity += value

            peak = max(

                peak,

                equity,

            )

            max_drawdown = max(

                max_drawdown,

                peak - equity,

            )

        calmar = (

            total_return / max_drawdown

            if max_drawdown > 0

            else 0.0

        )

        return {

            "sharpe_ratio": round(

                sharpe,

                4,

            ),

            "sortino_ratio": round(

                sortino,

                4,

            ),

            "calmar_ratio": round(

                calmar,

                4,

            ),

        }