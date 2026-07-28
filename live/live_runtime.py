"""
BTC Trend Trader Professional v4
Live Trading Runtime

Sprint 11.1.4
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

        self.shutdown_complete = False

        self.start_time = time.time()

        self.last_heartbeat = time.time()

    # -------------------------------------------------

    def initialize(self):

        print()
        print("=" * 60)
        print("BTC TREND TRADER v4")
        print("LIVE PAPER TRADING")
        print("=" * 60)

        self.print_startup_diagnostics()

    # -------------------------------------------------

    def print_startup_diagnostics(self):

        print()
        print("=" * 60)
        print("STARTUP DIAGNOSTICS")
        print("=" * 60)

        print(f"Mode            : PAPER")
        print(f"Symbol          : {config.SYMBOL}")
        print(f"Timeframe       : {config.TIMEFRAME}")
        print(
        f"Risk / Trade    : "
        f"{config.RISK_PER_TRADE * 100:.2f}%"
        )
        print(
            f"Initial Balance : "
            f"{self.executor.get_balance():.2f}"
        )

        print("=" * 60)

    # -------------------------------------------------

    def print_heartbeat(self):

        now = time.time()

        if now - self.last_heartbeat < config.HEARTBEAT_INTERVAL_SECONDS:

            return

        self.last_heartbeat = now

        uptime = int(now - self.start_time)

        hours = uptime // 3600

        minutes = (uptime % 3600) // 60

        seconds = uptime % 60

        print()

        print("-" * 60)

        print("HEARTBEAT")

        print("-" * 60)

        print("Status        : RUNNING")

        print("Mode          : PAPER")

        print(
            f"Balance       : "
            f"{self.executor.get_balance():.2f}"
        )

        print(
            f"Equity        : "
            f"{self.executor.get_equity():.2f}"
        )

        print(
            f"Open Trades   : "
            f"{len(self.executor.get_open_trades())}"
        )

        if self.last_processed_candle is None:

            print("Last Candle   : None")

        else:

            print(
                f"Last Candle   : "
                f"{self.last_processed_candle}"
            )

        print(
            f"Uptime        : "
            f"{hours:02}:{minutes:02}:{seconds:02}"
        )

        print("-" * 60)

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

        ema_distance = abs(
            latest[f"EMA_{config.EMA_FAST}"] -
            latest[f"EMA_{config.EMA_SLOW}"]
        )

        strong_trend = (
            ema_distance >=
            latest["ATR"] * config.EMA_DISTANCE_ATR_MULTIPLIER
        )

        print(
            f"Signal={latest['Signal']} | "
            f"Fast>Slow={latest[f'EMA_{config.EMA_FAST}'] > latest[f'EMA_{config.EMA_SLOW}']} | "
            f"StrongTrend={strong_trend} | "
            f"ADX_OK={latest['ADX'] > config.ADX_THRESHOLD} | "
            f"BUY_RSI_OK={latest['RSI'] <= config.RSI_BUY_LEVEL} | "
            f"SELL_RSI_OK={latest['RSI'] >= config.RSI_SELL_LEVEL}"
        )

        print()
        print(f"New Candle : {candle_time}")

        #
        # -------------------------------------------------
        # Update Existing Position
        # -------------------------------------------------
        #
        
        closed_trade = self.executor.update(

            high=float(latest["High"]),

            low=float(latest["Low"]),

            close=float(latest["Close"]),

            atr=float(latest["ATR"]),

            timestamp=candle_time,

        )

        if closed_trade is not None:

            print()

            print("✓ Paper trade closed.")

            print(f"Result     : {closed_trade['result']}")

            print(f"Profit     : {closed_trade['profit']:.2f}")

            print(f"Balance    : {self.executor.get_balance():.2f}")

            print(f"Equity     : {self.executor.get_equity():.2f}")

        #
        # -------------------------------------------------
        # Existing Position
        # -------------------------------------------------
        #

        if self.executor.has_open_trade():

            trade = self.executor.get_open_trades()[0]

            print("Position   : OPEN")
            print(f"Balance    : {self.executor.get_balance():.2f}")
            print(f"Equity     : {self.executor.get_equity():.2f}")
            print(f"Stop Loss  : {trade['stop_loss']:.2f}")
            print(f"Take Profit: {trade['take_profit']:.2f}")
            print(f"Lot Size   : {trade['lot_size']:.2f}")
            print(
                f"Partials   : "
                f"{len(trade['partial_exits'])}/"
                f"{len(trade['partial_tp_hits'])}"
            )
            print(
                f"Break-even : "
                f"{'YES' if trade['break_even_activated'] else 'NO'}"
            )

            print(
                f"Trailing   : "
                f"{'YES' if trade['trailing_stop_activated'] else 'NO'}"
            )

            return

        #
        # -------------------------------------------------
        # Strategy Signal
        # -------------------------------------------------
        #

        signal = latest["Signal"]

        if signal not in ("BUY", "SELL"):

            print(f"Signal     : {signal}")

            print(f"Balance    : {self.executor.get_balance():.2f}")

            print(f"Equity     : {self.executor.get_equity():.2f}")

            return

        print(f"Signal     : {signal}")

        #
        # -------------------------------------------------
        # Position Size
        # -------------------------------------------------
        #

        lot_size = self.risk_manager.calculate_position_size(

            balance=self.executor.get_balance(),

            risk_percent=config.RISK_PER_TRADE,

            entry_price=float(latest["Close"]),

            stop_loss=float(latest["StopLoss"]),

        )

        #
        # -------------------------------------------------
        # Create Paper Trade
        # -------------------------------------------------
        #

        created = self.executor.execute(

            signal=signal,

            price=float(latest["Close"]),

            stop_loss=float(latest["StopLoss"]),

            take_profit=float(latest["TakeProfit"]),

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

        try:

            while self.running:

                self.process_market()

                self.print_heartbeat()

                time.sleep(5)

        except KeyboardInterrupt:

            print()

            print("Stopping paper trading...")

            self.stop()

        finally:

            self.shutdown()

    # -------------------------------------------------

    def stop(self):

        self.running = False

    # -------------------------------------------------

    def shutdown(self):

        if self.shutdown_complete:

            return

        self.shutdown_complete = True

        self.running = False

        print()

        self.executor.print_summary()

        self.market_feed.shutdown()

        print()

        print("Paper trading stopped.")