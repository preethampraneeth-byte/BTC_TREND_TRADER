"""
BTC Trend Trader Professional v4
Milestone M3

Event Bus

Responsibilities
----------------
- Publish/Subscribe communication
- Loose coupling between modules
- Safe event dispatch
- Callback registration

This module performs NO:
- Trading
- Risk calculations
- MT5 execution
- Persistence
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from threading import Lock
from typing import Any, Callable, DefaultDict, Dict, List


# ============================================================
# Event
# ============================================================


@dataclass(frozen=True)
class Event:
    """
    Immutable event object.
    """

    name: str
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


# ============================================================
# Event Bus
# ============================================================


class EventBus:
    """
    Thread-safe publish/subscribe event bus.

    Subscribers are isolated from each other.
    Exceptions inside callbacks never interrupt
    trading or other subscribers.
    """

    def __init__(self):

        self._subscribers: DefaultDict[
            str,
            List[Callable[[Event], None]]
        ] = defaultdict(list)

        self._lock = Lock()

    # --------------------------------------------------------
    # Subscribe
    # --------------------------------------------------------

    def subscribe(
        self,
        event_name: str,
        callback: Callable[[Event], None],
    ):
        """
        Register callback.
        """

        with self._lock:

            if callback not in self._subscribers[event_name]:
                self._subscribers[event_name].append(callback)

    # --------------------------------------------------------

    def unsubscribe(
        self,
        event_name: str,
        callback: Callable[[Event], None],
    ):
        """
        Remove callback.
        """

        with self._lock:

            if callback in self._subscribers[event_name]:
                self._subscribers[event_name].remove(callback)

    # --------------------------------------------------------

    def clear(
        self,
        event_name: str = None,
    ):
        """
        Remove subscribers.
        """

        with self._lock:

            if event_name is None:
                self._subscribers.clear()
            else:
                self._subscribers.pop(event_name, None)

    # --------------------------------------------------------
    # Publish
    # --------------------------------------------------------

    def publish(
        self,
        event_name: str,
        **payload,
    ):
        """
        Publish event.

        Callback failures are ignored to
        avoid interrupting trading.
        """

        event = Event(
            name=event_name,
            payload=payload,
        )

        with self._lock:
            callbacks = list(
                self._subscribers.get(event_name, [])
            )

        for callback in callbacks:

            try:
                callback(event)

            except Exception:
                pass

    # --------------------------------------------------------
    # Query
    # --------------------------------------------------------

    def subscribers(
        self,
        event_name: str,
    ) -> List[Callable]:
        """
        Return subscribers.
        """

        with self._lock:

            return list(
                self._subscribers.get(event_name, [])
            )

    def has_subscribers(
        self,
        event_name: str,
    ) -> bool:
        """
        Returns True if event has listeners.
        """

        return len(
            self.subscribers(event_name)
        ) > 0


# ============================================================
# Standard Events
# ============================================================


class Events:
    """
    Standard event names used by the engine.
    """

    TRADE_OPENED = "trade_opened"

    TRADE_UPDATED = "trade_updated"

    TRADE_CLOSED = "trade_closed"

    PARTIAL_EXIT = "partial_exit"

    TP_HIT = "tp_hit"

    SL_HIT = "sl_hit"

    BREAK_EVEN = "break_even"

    TRAIL_UPDATED = "trail_updated"

    STOP_UPDATED = "stop_updated"

    ORDER_NEW = "order_new"

    ORDER_SENT = "order_sent"

    ORDER_FILLED = "order_filled"

    ORDER_PARTIAL = "order_partial"

    ORDER_MODIFIED = "order_modified"

    ORDER_CLOSED = "order_closed"

    ORDER_FAILED = "order_failed"

    RISK_APPROVED = "risk_approved"

    RISK_REJECTED = "risk_rejected"

    ENGINE_STARTED = "engine_started"

    ENGINE_STOPPED = "engine_stopped"

    PERSISTENCE_SAVED = "persistence_saved"

    PERSISTENCE_LOADED = "persistence_loaded"

    DASHBOARD_UPDATED = "dashboard_updated"


# ============================================================
# Global Event Bus
# ============================================================

global_event_bus = EventBus()