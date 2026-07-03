"""
BTC Trend Trader Professional v4
Backtest Runtime
"""

from __future__ import annotations

from services.market_data_service import MarketDataService
from services.diagnostics_service import DiagnosticsService
from services.backtest_service import BacktestService
from services.reporting_service import ReportingService
from services.dashboard_service import DashboardService

from analytics.analytics_service import AnalyticsService


class BacktestRuntime:
    """
    Executes the complete backtesting workflow using
    application services.
    """

    def __init__(self) -> None:

        self.name = "BACKTEST"

        self.market_data_service = MarketDataService()

        self.diagnostics_service = DiagnosticsService()

        self.backtest_service = BacktestService()

        self.reporting_service = ReportingService()

        self.dashboard_service = DashboardService()

        self.analytics_service = AnalyticsService()

    # -------------------------------------------------

    def load_market_data(self):

        return self.market_data_service.load()

    # -------------------------------------------------

    def prepare_market(self, candles):

        return self.market_data_service.prepare(candles)

    # -------------------------------------------------

    def build_diagnostics(self, candles):

        return self.diagnostics_service.generate(candles)

    # -------------------------------------------------

    def run_backtest(self, candles):

        return self.backtest_service.run(candles)

    # -------------------------------------------------

    def generate_performance_report(
        self,
        trades,
        statistics,
    ):

        return self.reporting_service.generate(
            trades,
            statistics,
        )

    # -------------------------------------------------

    def generate_analytics(
        self,
        trades,
        starting_balance,
    ):

        return self.analytics_service.generate(
            trades,
            starting_balance,
        )

    # -------------------------------------------------

    def show_dashboard(
        self,
        summary,
        performance,
        trades,
        diagnostics,
        analytics,
    ):

        self.dashboard_service.show(
            summary=summary,
            performance=performance,
            trades=trades,
            diagnostics=diagnostics,
            analytics=analytics,
        )

    # -------------------------------------------------

    def shutdown(self):

        self.market_data_service.shutdown()

    # -------------------------------------------------

    def run(self):

        candles = self.load_market_data()

        candles = self.prepare_market(candles)

        diagnostics = self.build_diagnostics(candles)

        results = self.run_backtest(candles)

        performance = self.generate_performance_report(
            results["trades"],
            results["statistics"],
        )

        analytics = self.generate_analytics(
            results["trades"],
            results["starting_balance"],
        )

        self.show_dashboard(
            summary=results["summary"],
            performance=performance,
            trades=results["trades"],
            diagnostics=diagnostics,
            analytics=analytics,
        )

        self.shutdown()