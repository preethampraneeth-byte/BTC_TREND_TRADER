"""
BTC Trend Trader v1.0
Backtester (Version 2)

Version 1:
- Count BUY / SELL / HOLD signals

Version 2:
- Simulate trades
- Calculate profit/loss
- Return trading statistics
"""

from __future__ import annotations

import pandas as pd

from backtesting.trade_simulator import TradeSimulator


class Backtester:
    """
    Backtests strategy signals using the TradeSimulator.
    """

    def __init__(self, starting_balance: float = 10000):
        self.starting_balance = starting_balance

    # ---------------------------------------------------------
    # Existing functionality
    # ---------------------------------------------------------

    def summarize(self, df: pd.DataFrame) -> dict:

        buy_count = (df["Signal"] == "BUY").sum()
        sell_count = (df["Signal"] == "SELL").sum()
        hold_count = (df["Signal"] == "HOLD").sum()

        total = len(df)

        return {
            "Total Candles": total,
            "BUY Signals": int(buy_count),
            "SELL Signals": int(sell_count),
            "HOLD Signals": int(hold_count),
        }

    # ---------------------------------------------------------
    # New functionality
    # ---------------------------------------------------------

    def simulate(
        self,
        df: pd.DataFrame,
        lot_size: float = 1.0,
    ) -> dict:
        """
        Simulate historical trades.

        Required DataFrame columns:

        Time
        Open
        High
        Low
        Close
        Signal
        StopLoss
        TakeProfit
        """

        simulator = TradeSimulator(self.starting_balance)

        for _, row in df.iterrows():

            # Update existing trade first
            simulator.update_trade(
                high=row["High"],
                low=row["Low"],
                close=row["Close"],
                current_time=row["Time"],
            )

            # Skip if a trade is already open
            if simulator.has_open_trade():
                continue

            signal = row["Signal"]

            if signal not in ("BUY", "SELL"):
                continue

            simulator.open_trade(
                direction=signal,
                entry_price=row["Close"],
                stop_loss=row["StopLoss"],
                take_profit=row["TakeProfit"],
                lot_size=lot_size,
                entry_time=row["Time"],
            )

        # Close any remaining trade at the final candle
        if simulator.has_open_trade():

            last = df.iloc[-1]

            simulator.force_close(
                price=last["Close"],
                current_time=last["Time"],
            )

        return {
            "statistics": simulator.get_statistics(),
            "trades": simulator.get_trade_history(),
        }