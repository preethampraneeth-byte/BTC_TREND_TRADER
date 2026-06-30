"""
BTC Trend Trader v2.5
Performance Report

Calculates performance metrics from completed
simulated trades.
"""

from __future__ import annotations


class PerformanceReport:

    def generate(
        self,
        trades,
        starting_balance: float,
        ending_balance: float,
        equity_curve=None,
    ):

        if equity_curve is None:
            equity_curve = [starting_balance, ending_balance]

        total_trades = len(trades)

        if total_trades == 0:
            return {
                "Starting Balance": starting_balance,
                "Ending Balance": ending_balance,
                "Net Profit": 0.0,
                "Return (%)": 0.0,
                "Maximum Drawdown (%)": 0.0,
                "Recovery Factor": 0.0,
                "Expectancy": 0.0,
                "Total Trades": 0,
                "Winning Trades": 0,
                "Losing Trades": 0,
                "Win Rate (%)": 0.0,
                "Gross Profit": 0.0,
                "Gross Loss": 0.0,
                "Profit Factor": 0.0,
                "Average Win": 0.0,
                "Average Loss": 0.0,
                "Largest Win": 0.0,
                "Largest Loss": 0.0,
            }

        # -------------------------------------------------
        # Trade Statistics
        # -------------------------------------------------

        profits = [t.profit for t in trades if t.profit > 0]
        losses = [t.profit for t in trades if t.profit < 0]

        gross_profit = sum(profits)
        gross_loss = abs(sum(losses))

        winning_trades = len(profits)
        losing_trades = len(losses)

        win_rate = (winning_trades / total_trades) * 100

        average_win = (
            gross_profit / winning_trades
            if winning_trades > 0
            else 0.0
        )

        average_loss = (
            gross_loss / losing_trades
            if losing_trades > 0
            else 0.0
        )

        largest_win = max(profits) if profits else 0.0
        largest_loss = min(losses) if losses else 0.0

        if gross_loss == 0:
            profit_factor = (
                float("inf")
                if gross_profit > 0
                else 0.0
            )
        else:
            profit_factor = gross_profit / gross_loss

        # -------------------------------------------------
        # Return
        # -------------------------------------------------

        net_profit = ending_balance - starting_balance

        return_percent = (
            (net_profit / starting_balance) * 100
            if starting_balance != 0
            else 0.0
        )

        # -------------------------------------------------
        # Maximum Drawdown
        # -------------------------------------------------

        peak = equity_curve[0]
        max_drawdown = 0.0

        for equity in equity_curve:

            if equity > peak:
                peak = equity

            drawdown = (peak - equity) / peak

            if drawdown > max_drawdown:
                max_drawdown = drawdown

        max_drawdown_percent = max_drawdown * 100

        # -------------------------------------------------
        # Recovery Factor
        # -------------------------------------------------

        if max_drawdown > 0:
            recovery_factor = net_profit / (max_drawdown * starting_balance)
        else:
            recovery_factor = 0.0

        # -------------------------------------------------
        # Expectancy
        # -------------------------------------------------

        expectancy = (
            net_profit / total_trades
            if total_trades > 0
            else 0.0
        )

        # -------------------------------------------------
        # Final Report
        # -------------------------------------------------

        return {

            "Starting Balance": round(starting_balance, 2),

            "Ending Balance": round(ending_balance, 2),

            "Net Profit": round(net_profit, 2),

            "Return (%)": round(return_percent, 2),

            "Maximum Drawdown (%)": round(
                max_drawdown_percent,
                2,
            ),

            "Recovery Factor": round(
                recovery_factor,
                2,
            ),

            "Expectancy": round(
                expectancy,
                2,
            ),

            "Total Trades": total_trades,

            "Winning Trades": winning_trades,

            "Losing Trades": losing_trades,

            "Win Rate (%)": round(
                win_rate,
                2,
            ),

            "Gross Profit": round(
                gross_profit,
                2,
            ),

            "Gross Loss": round(
                gross_loss,
                2,
            ),

            "Profit Factor": (
                round(profit_factor, 2)
                if profit_factor != float("inf")
                else "Infinity"
            ),

            "Average Win": round(
                average_win,
                2,
            ),

            "Average Loss": round(
                average_loss,
                2,
            ),

            "Largest Win": round(
                largest_win,
                2,
            ),

            "Largest Loss": round(
                largest_loss,
                2,
            ),
        }