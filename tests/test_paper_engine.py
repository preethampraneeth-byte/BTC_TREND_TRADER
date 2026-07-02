"""
BTC Trend Trader Professional v4
Paper Engine Tests
"""

import unittest

from paper_trading.paper_engine import PaperEngine


class TestPaperEngine(unittest.TestCase):

    def setUp(self):

        self.engine = PaperEngine()

        self.engine.start()

    def tearDown(self):

        self.engine.stop()

    def test_engine_start(self):

        self.assertTrue(
            self.engine.session.is_active()
        )

    def test_process_signal(self):

        signal = {
            "symbol": "BTCUSD",
            "direction": "BUY",
            "volume": 1.0,
            "entry_price": 50000.0,
            "stop_loss": 49500.0,
            "take_profit": 51000.0,
            "entry_time": "2026-01-01 00:00",
        }

        result = self.engine.process_signal(
            signal
        )

        self.assertTrue(result)

        self.assertEqual(
            len(self.engine.open_positions()),
            1,
        )

    def test_update_price(self):

        signal = {
            "symbol": "BTCUSD",
            "direction": "BUY",
            "volume": 1.0,
            "entry_price": 50000.0,
            "stop_loss": 49500.0,
            "take_profit": 51000.0,
            "entry_time": "2026-01-01 00:00",
        }

        self.engine.process_signal(signal)

        self.engine.update_price(
            "BTCUSD",
            50500.0,
        )

        position = self.engine.open_positions()[0]

        self.assertGreater(
            position.unrealized_profit,
            0.0,
        )

    def test_close_position(self):

        signal = {
            "symbol": "BTCUSD",
            "direction": "BUY",
            "volume": 1.0,
            "entry_price": 50000.0,
            "stop_loss": 49500.0,
            "take_profit": 51000.0,
            "entry_time": "2026-01-01 00:00",
        }

        self.engine.process_signal(signal)

        position = self.engine.open_positions()[0]

        result = self.engine.close_position(
            ticket=position.ticket,
            price=50500.0,
            exit_time="2026-01-01 01:00",
        )

        self.assertTrue(result)

        self.assertEqual(
            position.status,
            "CLOSED",
        )

    def test_history(self):

        signal = {
            "symbol": "BTCUSD",
            "direction": "BUY",
            "volume": 1.0,
            "entry_price": 50000.0,
            "stop_loss": 49500.0,
            "take_profit": 51000.0,
            "entry_time": "2026-01-01 00:00",
        }

        self.engine.process_signal(signal)

        self.assertEqual(
            len(self.engine.history()),
            1,
        )

    def test_reset(self):

        signal = {
            "symbol": "BTCUSD",
            "direction": "BUY",
            "volume": 1.0,
            "entry_price": 50000.0,
            "stop_loss": 49500.0,
            "take_profit": 51000.0,
            "entry_time": "2026-01-01 00:00",
        }

        self.engine.process_signal(signal)

        self.engine.reset()

        self.assertEqual(
            len(self.engine.open_positions()),
            0,
        )

        self.assertEqual(
            len(self.engine.history()),
            0,
        )


if __name__ == "__main__":
    unittest.main()