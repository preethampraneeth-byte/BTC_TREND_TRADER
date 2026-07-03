"""
BTC Trend Trader Professional v4
Live Trading Runtime

Sprint 9.1
"""

from __future__ import annotations

import time

import config

from core.risk_manager import RiskManager
from live.live_market_feed import LiveMarketFeed
from live.paper_trade_executor import PaperTradeExecutor
from services.live_strategy_service import LiveStrategyService


class LiveRuntime:
    """
    Executes the live paper trading workflow.

    Processes each completed candle only once.
    """

    def __init__(self):

        self.market_feed = LiveMarketFeed()

        self.strategy = LiveStrategyService()

        self.risk_manager = RiskManager()

        self.executor = PaperTradeExecutor()

        self.running = False

        self.last_processed_candle = None

    # -------------------------------------------------

    def initialize(self):

        print()
        print("=" * 60)
        print("BTC TREND TRADER v4")
        print("LIVE PAPER TRADING")
        print("=" * 60)

    # -------------------------------------------------

    def process_market(self):

        candles = self.market_feed.latest()

        if candles is None:

            print("Waiting for market data...")

            return

        candles = self.strategy.generate_signals(candles)

        latest = candles.iloc[-1]

        candle_time = latest["Time"]

        if candle_time == self.last_processed_candle:

            return

        self.last_processed_candle = candle_time

        print()

        print(f"New Candle : {candle_time}")

        #
        # Update existing trade
        #

        closed_trade = self.executor.update(

            high=latest["High"],

            low=latest["Low"],

            close=latest["Close"],

            timestamp=candle_time,

        )

        if closed_trade is not None:

            print()

            print("✓ Paper trade closed.")

            print(f"Result     : {closed_trade['result']}")

            print(f"Profit     : {closed_trade['profit']:.2f}")

            print(f"Balance    : {self.executor.get_balance():.2f}")

            print(f"Equity     : {self.executor.get_equity():.2f}")

        signal = latest["Signal"]

        print(f"Signal     : {signal}")

        if self.executor.has_open_trade():

            print("Position   : OPEN")

            print(f"Balance    : {self.executor.get_balance():.2f}")

            print(f"Equity     : {self.executor.get_equity():.2f}")

            return

        if signal not in ("BUY", "SELL"):

            print(f"Balance    : {self.executor.get_balance():.2f}")

            print(f"Equity     : {self.executor.get_equity():.2f}")

            return

        lot_size = self.risk_manager.calculate_position_size(

            balance=self.executor.get_balance(),

            risk_percent=config.RISK_PER_TRADE,

            entry_price=latest["Close"],

            stop_loss=latest["StopLoss"],

        )

        created = self.executor.execute(

            signal=signal,

            price=latest["Close"],

            stop_loss=latest["StopLoss"],

            take_profit=latest["TakeProfit"],

            lot_size=lot_size,

            timestamp=candle_time,

        )

        if created:

            print("✓ Paper trade created.")

        else:

            print("Trade already exists.")

        print(f"Balance    : {self.executor.get_balance():.2f}")

        print(f"Equity     : {self.executor.get_equity():.2f}")

    # -------------------------------------------------

    def start(self):

        self.initialize()

        print()

        print("Paper trading enabled.")

        print()

        self.running = True

        while self.running:

            self.process_market()

            time.sleep(5)

    # -------------------------------------------------

    def stop(self):

        self.running = False

    # -------------------------------------------------

    def shutdown(self):

        self.market_feed.shutdown()

        print()

        print("Paper trading stopped.")