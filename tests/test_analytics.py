"""
BTC Trend Trader Professional v4
Analytics Tests
"""

import unittest

from analytics.analytics_engine import AnalyticsEngine


class DummyTrade:

    def __init__(self, profit):

        self.profit = profit


class TestAnalyticsEngine(unittest.TestCase):

    def setUp(self):

        self.engine = AnalyticsEngine()

        self.trades = [
            DummyTrade(100),
            DummyTrade(-50),
            DummyTrade(200),
            DummyTrade(-25),
        ]

    def test_generate(self):

        report = self.engine.generate(self.trades)

        self.assertIn("performance", report)
        self.assertIn("trade_statistics", report)
        self.assertIn("risk_statistics", report)
        self.assertIn("equity_curve", report)

    def test_performance_metrics(self):

        report = self.engine.generate(self.trades)

        performance = report["performance"]

        self.assertEqual(
            performance["total_trades"],
            4,
        )

        self.assertEqual(
            performance["winning_trades"],
            2,
        )

        self.assertEqual(
            performance["losing_trades"],
            2,
        )


if __name__ == "__main__":
    unittest.main()