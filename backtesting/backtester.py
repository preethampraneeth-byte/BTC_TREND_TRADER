"""
BTC Trend Trader v3.0
Backtester

Professional execution model

Execution Order
---------------
1. Activate pending orders
2. Update open trades
3. Submit new pending orders
4. Calculate dynamic position size
"""

from __future__ import annotations

import pandas as pd

import config

from core.risk_manager import RiskManager
from backtesting.trade_simulator import TradeSimulator


class Backtester:

    def __init__(self, starting_balance: float = 10000):

        self.starting_balance = starting_balance

    # ---------------------------------------------------------

    def summarize(self, df: pd.DataFrame):

        return {

            "Total Candles": len(df),

            "BUY Signals": int((df["Signal"] == "BUY").sum()),

            "SELL Signals": int((df["Signal"] == "SELL").sum()),

            "HOLD Signals": int((df["Signal"] == "HOLD").sum()),

        }

    # ---------------------------------------------------------

    def simulate(
        self,
        df: pd.DataFrame,
        lot_size: float = 1.0,
    ):

        simulator = TradeSimulator(self.starting_balance)

        # Risk Manager
        risk_manager = RiskManager()

        for _, row in df.iterrows():

            # ---------------------------------------------
            # STEP 1
            # Activate pending order using NEXT candle open
            # ---------------------------------------------

            if simulator.has_pending_trade():

                simulator.process_pending_order(
                    entry_price=row["Open"],
                    entry_time=row["Time"],
                )

            # ---------------------------------------------
            # STEP 2
            # Update open trade
            # ---------------------------------------------

            simulator.update_trade(
                high=row["High"],
                low=row["Low"],
                close=row["Close"],
                current_time=row["Time"],
                atr=row["ATR"],
            )

            # ---------------------------------------------
            # STEP 3
            # Skip if trade still open
            # ---------------------------------------------

            if simulator.has_open_trade():
                continue

            # ---------------------------------------------
            # STEP 4
            # Submit NEW pending order
            # ---------------------------------------------

            signal = row["Signal"]

            if signal not in ("BUY", "SELL"):
                continue

            # ---------------------------------------------
            # Calculate Dynamic Position Size
            # ---------------------------------------------

            calculated_lot = risk_manager.calculate_position_size(
                balance=simulator.get_balance(),
                risk_percent=config.RISK_PER_TRADE,
                entry_price=row["Close"],
                stop_loss=row["StopLoss"],
            )

            simulator.submit_order(
                direction=signal,
                signal_price=row["Close"],
                stop_loss=row["StopLoss"],
                take_profit=row["TakeProfit"],
                lot_size=calculated_lot,
                submit_time=row["Time"],
            )

        # -------------------------------------------------
        # Close final open trade
        # -------------------------------------------------

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