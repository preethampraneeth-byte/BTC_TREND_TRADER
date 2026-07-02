"""
BTC Trend Trader Professional v4
Paper Trading Tests
"""

import unittest

from paper_trading.paper_session import PaperSession


class TestPaperTrading(unittest.TestCase):

    def setUp(self):

        self.session = PaperSession()

        self.session.start()

        self.executor = self.session.get_executor()

    def tearDown(self):

        self.session.stop()

    def test_session_start(self):

        self.assertTrue(
            self.session.is_active()
        )

    def test_open_position(self):

        position = self.executor.open_position(
            symbol="BTCUSD",
            direction="BUY",
            volume=1.0,
            entry_price=50000.0,
            stop_loss=49500.0,
            take_profit=51000.0,
            entry_time="2026-01-01 00:00",
        )

        self.assertIsNotNone(position)

        self.assertEqual(
            len(self.executor.get_open_positions()),
            1,
        )

    def test_price_update(self):

        position = self.executor.open_position(
            symbol="BTCUSD",
            direction="BUY",
            volume=1.0,
            entry_price=50000.0,
            stop_loss=49500.0,
            take_profit=51000.0,
            entry_time="2026-01-01 00:00",
        )

        self.executor.update_market_price(
            "BTCUSD",
            50500.0,
        )

        self.assertGreater(
            position.unrealized_profit,
            0.0,
        )

    def test_close_position(self):

        position = self.executor.open_position(
            symbol="BTCUSD",
            direction="BUY",
            volume=1.0,
            entry_price=50000.0,
            stop_loss=49500.0,
            take_profit=51000.0,
            entry_time="2026-01-01 00:00",
        )

        result = self.executor.close_position(
            ticket=position.ticket,
            exit_price=50500.0,
            exit_time="2026-01-01 01:00",
        )

        self.assertTrue(result)

        self.assertEqual(
            position.status,
            "CLOSED",
        )

    def test_reset(self):

        self.executor.open_position(
            symbol="BTCUSD",
            direction="BUY",
            volume=1.0,
            entry_price=50000.0,
            stop_loss=49500.0,
            take_profit=51000.0,
            entry_time="2026-01-01 00:00",
        )

        self.session.reset()

        self.assertFalse(
            self.session.is_active()
        )

        self.assertEqual(
            len(self.executor.get_open_positions()),
            0,
        )


if __name__ == "__main__":
    unittest.main()