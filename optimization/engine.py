"""
BTC Trend Trader v3.2.2
Optimization Engine

Runs parameter optimization using the existing
strategy, backtester and performance report.
"""

from __future__ import annotations

import config

from core.market_data import MarketData
from core.indicators import Indicators
from core.strategy import Strategy

from backtesting.backtester import Backtester
from backtesting.performance_report import PerformanceReport


class Optimizer:

    def __init__(self):

        self.market = MarketData()
        self.indicators = Indicators()
        self.strategy = Strategy()

        self.results = []

    # -------------------------------------------------

    def load_data(self):

        print("\nLoading historical data...")

        data = self.market.load_from_csv(
            config.CSV_DATA_FILE
        )

        print(f"Loaded {len(data)} candles.")

        return data

    # -------------------------------------------------

    def prepare_data(self):

        data = self.load_data()

        print("Calculating indicators...")

        data = self.indicators.calculate(data)

        print("Indicators calculated.")

        return data

    # -------------------------------------------------

    def run_single_test(
        self,
        candles,
        adx_threshold,
    ):

        config.ADX_THRESHOLD = adx_threshold

        data = candles.copy(deep=True)

        data = self.strategy.generate_signals(data)

        backtester = Backtester(
            starting_balance=config.INITIAL_BALANCE
        )

        simulation = backtester.simulate(data)

        statistics = simulation["statistics"]

        trades = simulation["trades"]

        performance = PerformanceReport().generate(
            trades=trades,
            starting_balance=statistics["starting_balance"],
            ending_balance=statistics["ending_balance"],
            equity_curve=statistics["equity_curve"],
        )

        self.results.append({

            "ADX": adx_threshold,

            "Profit Factor":
                performance["Profit Factor"],

            "Return":
                performance["Return (%)"],

            "Drawdown":
                performance["Maximum Drawdown (%)"],

            "Win Rate":
                performance["Win Rate (%)"],

            "Trades":
                performance["Total Trades"],

        })

    # -------------------------------------------------

    def print_results(self):

        print("\n")
        print("=" * 70)
        print("OPTIMIZATION RESULTS")
        print("=" * 70)

        print(
            f"{'ADX':<8}"
            f"{'PF':<10}"
            f"{'Return':<12}"
            f"{'DD':<10}"
            f"{'Win%':<10}"
            f"{'Trades':<10}"
        )

        print("-" * 70)

        for result in self.results:

            print(

                f"{result['ADX']:<8}"

                f"{str(result['Profit Factor']):<10}"

                f"{result['Return']:<12}"

                f"{result['Drawdown']:<10}"

                f"{result['Win Rate']:<10}"

                f"{result['Trades']:<10}"

            )

    # -------------------------------------------------

    def run(self):

        print("=" * 70)
        print("BTC TREND TRADER PARAMETER OPTIMIZER")
        print("=" * 70)

        candles = self.prepare_data()

        original_adx = config.ADX_THRESHOLD

        total = len(config.OPTIMIZE_ADX_VALUES)

        try:

            for index, adx in enumerate(
                config.OPTIMIZE_ADX_VALUES,
                start=1,
            ):

                print(
                    f"\n[{index}/{total}] "
                    f"Testing ADX_THRESHOLD = {adx}"
                )

                self.run_single_test(
                    candles,
                    adx,
                )

        finally:

            config.ADX_THRESHOLD = original_adx

        self.print_results()