"""
BTC Trend Trader v1.0
Performance Report

Calculates performance metrics from completed
simulated trades.
"""

from __future__ import annotations


class PerformanceReport:

    def generate(self, trades, starting_balance: float, ending_balance: float):

        total_trades = len(trades)

        if total_trades == 0:
            return {
                "Starting Balance": starting_balance,
                "Ending Balance": ending_balance,
                "Net Profit": 0.0,
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
            profit_factor = float("inf") if gross_profit > 0 else 0.0
        else:
            profit_factor = gross_profit / gross_loss

        return {

            "Starting Balance": round(starting_balance, 2),
            "Ending Balance": round(ending_balance, 2),
            "Net Profit": round(ending_balance - starting_balance, 2),

            "Total Trades": total_trades,
            "Winning Trades": winning_trades,
            "Losing Trades": losing_trades,
            "Win Rate (%)": round(win_rate, 2),

            "Gross Profit": round(gross_profit, 2),
            "Gross Loss": round(gross_loss, 2),

            "Profit Factor": (
                round(profit_factor, 2)
                if profit_factor != float("inf")
                else "Infinity"
            ),

            "Average Win": round(average_win, 2),
            "Average Loss": round(average_loss, 2),

            "Largest Win": round(largest_win, 2),
            "Largest Loss": round(largest_loss, 2),
        }