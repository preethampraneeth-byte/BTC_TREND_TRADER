"""
BTC Trend Trader v2.2
Backtester

Responsibilities
----------------
- Count BUY / SELL / HOLD signals
- Simulate historical trades
- Prepare for pending-order execution
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
    # Market Summary
    # ---------------------------------------------------------

    def summarize(self, df: pd.DataFrame) -> dict:

        buy_count = (df["Signal"] == "BUY").sum()
        sell_count = (df["Signal"] == "SELL").sum()
        hold_count = (df["Signal"] == "HOLD").sum()

        return {
            "Total Candles": len(df),
            "BUY Signals": int(buy_count),
            "SELL Signals": int(sell_count),
            "HOLD Signals": int(hold_count),
        }

    # ---------------------------------------------------------
    # Internal Helpers
    # ---------------------------------------------------------

    def _update_open_trade(
        self,
        simulator,
        row,
    ):

        simulator.update_trade(
            high=row["High"],
            low=row["Low"],
            close=row["Close"],
            current_time=row["Time"],
        )

    # ---------------------------------------------------------

    def _process_signal(
        self,
        simulator,
        row,
        lot_size,
    ):

        signal = row["Signal"]

        if signal not in ("BUY", "SELL"):
            return

        simulator.open_trade(
            direction=signal,
            entry_price=row["Close"],
            stop_loss=row["StopLoss"],
            take_profit=row["TakeProfit"],
            lot_size=lot_size,
            entry_time=row["Time"],
        )

    # ---------------------------------------------------------
    # Simulation
    # ---------------------------------------------------------

    def simulate(
        self,
        df: pd.DataFrame,
        lot_size: float = 1.0,
    ) -> dict:

        simulator = TradeSimulator(self.starting_balance)

        for _, row in df.iterrows():

            # Step 1
            self._update_open_trade(
                simulator,
                row,
            )

            # Step 2
            if simulator.has_open_trade():
                continue

            # Step 3
            self._process_signal(
                simulator,
                row,
                lot_size,
            )

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