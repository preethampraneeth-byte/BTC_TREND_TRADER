"""
BTC Trend Trader v1.0
Main Entry Point (Version 4)

Pipeline

1. Connect MT5
2. Load market data (CSV or MT5)
3. Calculate indicators
4. Generate strategy signals
5. Backtest signals
6. Simulate trades
7. Generate performance report
8. Display dashboard
"""

import config

from core.mt5_connector import MT5Connector
from core.market_data import MarketData
from core.indicators import Indicators
from core.strategy import Strategy

from backtesting.backtester import Backtester
from backtesting.performance_report import PerformanceReport

from dashboard.dashboard import Dashboard


def main():

    connector = None

    try:

        market = MarketData()

        # -------------------------------------------------
        # Load historical data
        # -------------------------------------------------

        if config.USE_CSV_DATA:

            print("Loading historical data from CSV...")

            candles = market.load_from_csv(
                config.CSV_DATA_FILE
            )

        else:

            connector = MT5Connector()

            if not connector.connect():
                return

            if not connector.symbol_info(config.SYMBOL):
                return

            print("Downloading historical data from MT5...")

            candles = market.get_candles(
                symbol=config.SYMBOL,
                timeframe=config.TIMEFRAME,
                bars=500,
            )

        # -------------------------------------------------
        # Indicators
        # -------------------------------------------------

        indicators = Indicators()

        candles = indicators.calculate(candles)

        # -------------------------------------------------
        # Strategy
        # -------------------------------------------------

        strategy = Strategy()

        candles = strategy.generate_signals(candles)

        # -------------------------------------------------
        # Strategy Diagnostics
        # -------------------------------------------------

        ema_fast = candles[f"EMA_{config.EMA_FAST}"]
        ema_slow = candles[f"EMA_{config.EMA_SLOW}"]

        ema_distance = (ema_fast - ema_slow).abs()

        strong_trend = (
            ema_distance
            >= candles["ATR"] * config.EMA_DISTANCE_ATR_MULTIPLIER
        )

        adx_ok = candles["ADX"] > config.ADX_THRESHOLD

        rsi_buy = candles["RSI"] > config.RSI_BUY_LEVEL
        rsi_sell = candles["RSI"] < config.RSI_SELL_LEVEL

        # BUY pipeline
        buy_step1 = ema_fast > ema_slow
        buy_step2 = buy_step1 & strong_trend
        buy_step3 = buy_step2 & adx_ok
        buy_step4 = buy_step3 & rsi_buy

        # SELL pipeline
        sell_step1 = ema_fast < ema_slow
        sell_step2 = sell_step1 & strong_trend
        sell_step3 = sell_step2 & adx_ok
        sell_step4 = sell_step3 & rsi_sell

        diagnostics = {

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

        # -------------------------------------------------
        # Performance Report
        # -------------------------------------------------

        performance = PerformanceReport().generate(
            trades=trades,
            starting_balance=statistics["starting_balance"],
            ending_balance=statistics["ending_balance"],
            equity_curve=statistics["equity_curve"],
        )

        # -------------------------------------------------
        # Dashboard
        # -------------------------------------------------

        dashboard = Dashboard()

        dashboard.show_complete_dashboard(
            summary=summary,
            performance=performance,
            trades=trades,
            diagnostics=diagnostics,
        )

    finally:

        if connector is not None:
            connector.disconnect()


if __name__ == "__main__":
    main()