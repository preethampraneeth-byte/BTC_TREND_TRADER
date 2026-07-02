"""
BTC Trend Trader Professional v4
Event Bus Tests
"""

import unittest

from core.event_bus import EventBus


class TestEventBus(unittest.TestCase):

    def setUp(self):

        self.event_bus = EventBus()
        self.received = []

    def listener(self, event):

        self.received.append(event)

    def test_subscribe(self):

        self.event_bus.subscribe(
            "TEST_EVENT",
            self.listener,
        )

        self.assertTrue(
            self.event_bus.has_subscribers(
                "TEST_EVENT"
            )
        )

    def test_publish(self):

        self.event_bus.subscribe(
            "TEST_EVENT",
            self.listener,
        )

        self.event_bus.publish(
            "TEST_EVENT",
            value=100,
        )

        self.assertEqual(
            len(self.received),
            1,
        )

        self.assertEqual(
            self.received[0].payload["value"],
            100,
        )

    def test_multiple_subscribers(self):

        second = []

        def listener_two(event):
            second.append(event)

        self.event_bus.subscribe(
            "TEST_EVENT",
            self.listener,
        )

        self.event_bus.subscribe(
            "TEST_EVENT",
            listener_two,
        )

        self.event_bus.publish(
            "TEST_EVENT",
            price=50000,
        )

        self.assertEqual(
            len(self.received),
            1,
        )

        self.assertEqual(
            len(second),
            1,
        )

        self.assertEqual(
            second[0].payload["price"],
            50000,
        )

    def test_publish_without_subscribers(self):

        self.event_bus.publish(
            "UNKNOWN_EVENT",
            value=1,
        )

        self.assertEqual(
            len(self.received),
            0,
        )


if __name__ == "__main__":
    unittest.main()