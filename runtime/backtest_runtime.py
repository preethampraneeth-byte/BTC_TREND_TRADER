"""
BTC Trend Trader Professional v4
Backtest Runtime
"""

from __future__ import annotations

from services.market_data_service import MarketDataService
from services.backtest_service import BacktestService
from services.diagnostics_service import DiagnosticsService

from core.indicators import Indicators
from core.strategy import Strategy

from backtesting.performance_report import PerformanceReport

from dashboard.dashboard import Dashboard


class BacktestRuntime:
    """
    Executes the complete backtesting workflow.

    Current migration status

    ✓ MarketDataService
    ✓ Strategy preparation
    ✓ DiagnosticsService
    ✓ BacktestService
    ✓ Performance reporting
    ✓ Dashboard orchestration
    """

    def __init__(self) -> None:

        self.name = "BACKTEST"

        self.market_data_service = MarketDataService()
        self.backtest_service = BacktestService()
        self.diagnostics_service = DiagnosticsService()

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

        return self.diagnostics_service.build(candles)

    # -------------------------------------------------
    # Backtester
    # -------------------------------------------------

    def run_backtest(self, candles):

        return self.backtest_service.run(candles)

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

        self.market_data_service.shutdown()

    # -------------------------------------------------
    # Runtime
    # -------------------------------------------------

    def run(self) -> None:

        candles = self.market_data_service.load()

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