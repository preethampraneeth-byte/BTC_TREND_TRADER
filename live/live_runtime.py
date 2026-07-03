"""
BTC Trend Trader Professional v4
Live Trading Runtime

Sprint 8.4
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

    No broker orders are placed.
    """

    def __init__(self):

        self.market_feed = LiveMarketFeed()

        self.strategy = LiveStrategyService()

        self.risk_manager = RiskManager()

        self.executor = PaperTradeExecutor()

        self.running = False

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

        candles = self.strategy.generate_signals(
            candles
        )

        latest = candles.iloc[-1]

        signal = latest["Signal"]

        print()

        print(f"Candle : {latest['Time']}")

        print(f"Signal : {signal}")

        if signal not in ("BUY", "SELL"):

            return

        lot_size = self.risk_manager.calculate_position_size(

            balance=config.INITIAL_BALANCE,

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

            timestamp=latest["Time"],

        )

        if created:

            print("Paper trade created.")

        else:

            print("Trade already exists for this candle.")

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