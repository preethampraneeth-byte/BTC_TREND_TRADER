"""
BTC Trend Trader Professional v4
Dashboard Tests
"""

import unittest

from dashboard.dashboard import Dashboard
from dashboard.dashboard_controller import DashboardController


class TestDashboardController(unittest.TestCase):

    def setUp(self):

        self.controller = DashboardController()

    def test_refresh(self):

        self.controller.refresh()

        self.assertIsInstance(
            self.controller.get_account(),
            dict,
        )

        self.assertIsInstance(
            self.controller.get_positions(),
            list,
        )

        self.assertIsInstance(
            self.controller.get_orders(),
            list,
        )

        self.assertIsInstance(
            self.controller.get_history(),
            list,
        )

        self.assertIsInstance(
            self.controller.get_events(),
            list,
        )

        self.assertIsInstance(
            self.controller.get_risk(),
            dict,
        )

        self.assertIsInstance(
            self.controller.get_statistics(),
            dict,
        )


class TestDashboard(unittest.TestCase):

    def setUp(self):

        self.dashboard = Dashboard()

    def test_refresh(self):

        self.dashboard.refresh()

    def test_render(self):

        self.dashboard.render()

    def test_run(self):

        self.dashboard.run()


if __name__ == "__main__":
    unittest.main()