"""
BTC Trend Trader v1.0
Main Entry Point (Version 3)

Pipeline

1. Connect MT5
2. Download market data
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

    connector = MT5Connector()

    if not connector.connect():
        return

    try:

        # -------------------------------------------------
        # Verify trading symbol
        # -------------------------------------------------

        if not connector.symbol_info(config.SYMBOL):
            return

        # -------------------------------------------------
        # Download historical data
        # -------------------------------------------------

        market = MarketData()

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
        )

        # -------------------------------------------------
        # Dashboard
        # -------------------------------------------------

        dashboard = Dashboard()

        dashboard.show_complete_dashboard(
            summary=summary,
            performance=performance,
            trades=trades,
        )

    finally:

        connector.disconnect()


if __name__ == "__main__":
    main()