"""
BTC Trend Trader Professional v4
Backtest Runtime
"""

from __future__ import annotations

import config

from core.market_data import MarketData
from core.mt5_connector import MT5Connector
from core.indicators import Indicators
from core.strategy import Strategy

from backtesting.backtester import Backtester
from backtesting.performance_report import PerformanceReport

from dashboard.dashboard import Dashboard


class BacktestRuntime:
    """
    Executes the existing backtesting workflow.

    Migration is intentionally incremental.

    Current migration status:

    ✓ Historical market data loading
    ✓ Indicator calculation
    ✓ Strategy signal generation
    ✓ Strategy diagnostics
    ✓ Backtester orchestration
    ✓ Performance report orchestration
    ✓ Dashboard orchestration

    Remaining work:
    - Collapse into a single execute() workflow
    - Integrate with Application.execute()
    """

    def __init__(self) -> None:

        self.name = "BACKTEST"

        self.connector: MT5Connector | None = None

    # -------------------------------------------------
    # Market Data
    # -------------------------------------------------

    def load_market_data(self):

        market = MarketData()

        if config.USE_CSV_DATA:

            print("Loading historical data from CSV...")

            return market.load_from_csv(
                config.CSV_DATA_FILE
            )

        self.connector = MT5Connector()

        if not self.connector.connect():
            raise RuntimeError("Failed to connect to MT5.")

        if not self.connector.symbol_info(config.SYMBOL):
            raise RuntimeError(
                f"Unable to access symbol '{config.SYMBOL}'."
            )

        print("Downloading historical data from MT5...")

        return market.get_candles(
            symbol=config.SYMBOL,
            timeframe=config.TIMEFRAME,
            bars=500,
        )

    # -------------------------------------------------
    # Indicator + Strategy
    # -------------------------------------------------

    def prepare_market(self, candles):

        indicators = Indicators()

        candles = indicators.calculate(candles)

        strategy = Strategy()

        candles = strategy.generate_signals(candles)

        return candles

    # -------------------------------------------------
    # Diagnostics
    # -------------------------------------------------

    def build_diagnostics(self, candles):

        ema_fast = candles[f"EMA_{config.EMA_FAST}"]

        ema_slow = candles[f"EMA_{config.EMA_SLOW}"]

        ema_distance = (ema_fast - ema_slow).abs()

        strong_trend = (
            ema_distance
            >= candles["ATR"]
            * config.EMA_DISTANCE_ATR_MULTIPLIER
        )

        adx_ok = candles["ADX"] > config.ADX_THRESHOLD

        rsi_buy = candles["RSI"] > config.RSI_BUY_LEVEL

        rsi_sell = candles["RSI"] < config.RSI_SELL_LEVEL

        buy_step1 = ema_fast > ema_slow
        buy_step2 = buy_step1 & strong_trend
        buy_step3 = buy_step2 & adx_ok
        buy_step4 = buy_step3 & rsi_buy

        sell_step1 = ema_fast < ema_slow
        sell_step2 = sell_step1 & strong_trend
        sell_step3 = sell_step2 & adx_ok
        sell_step4 = sell_step3 & rsi_sell

        return {

            "BUY: EMA > Slow": int(buy_step1.sum()),
            "BUY: + Strong Trend": int(buy_step2.sum()),
            "BUY: + ADX": int(buy_step3.sum()),
            "BUY: + RSI": int(buy_step4.sum()),

            "SELL: EMA < Slow": int(sell_step1.sum()),
            "SELL: + Strong Trend": int(sell_step2.sum()),
            "SELL: + ADX": int(sell_step3.sum()),
            "SELL: + RSI": int(sell_step4.sum()),

        }

    # -------------------------------------------------
    # Backtester
    # -------------------------------------------------

    def run_backtest(self, candles):

        backtester = Backtester(
            starting_balance=config.INITIAL_BALANCE
        )

        summary = backtester.summarize(candles)

        simulation = backtester.simulate(
            candles,
            lot_size=1.0,
        )

        statistics = simulation["statistics"]

        trades = simulation["trades"]

        return {
            "summary": summary,
            "statistics": statistics,
            "trades": trades,
        }

    # -------------------------------------------------
    # Performance Report
    # -------------------------------------------------

    def generate_performance_report(
        self,
        trades,
        statistics,
    ):

        return PerformanceReport().generate(
            trades=trades,
            starting_balance=statistics["starting_balance"],
            ending_balance=statistics["ending_balance"],
            equity_curve=statistics["equity_curve"],
        )

    # -------------------------------------------------
    # Dashboard
    # -------------------------------------------------

    def show_dashboard(
        self,
        summary,
        performance,
        trades,
        diagnostics,
    ):

        dashboard = Dashboard()

        dashboard.show_complete_dashboard(
            summary=summary,
            performance=performance,
            trades=trades,
            diagnostics=diagnostics,
        )

    # -------------------------------------------------
    # Cleanup
    # -------------------------------------------------

    def shutdown(self) -> None:

        if self.connector is not None:
            self.connector.disconnect()

    # -------------------------------------------------
    # Runtime
    # -------------------------------------------------

    def run(self) -> None:

        candles = self.load_market_data()

        candles = self.prepare_market(candles)

        diagnostics = self.build_diagnostics(candles)

        results = self.run_backtest(candles)

        performance = self.generate_performance_report(
            results["trades"],
            results["statistics"],
        )

        self.show_dashboard(
            results["summary"],
            performance,
            results["trades"],
            diagnostics,
        )

        self.shutdown()