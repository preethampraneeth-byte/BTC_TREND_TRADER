"""
BTC Trend Trader Professional v4
Milestone M3

Execution Lifecycle

Responsibilities
----------------
- Order lifecycle management
- State transition validation
- Lifecycle history
- Current execution status

This module performs NO:
- MT5 execution
- Retry logic
- Risk calculations
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional


class OrderState(str, Enum):
    """
    Valid execution states.
    """

    NEW = "NEW"

    SENT = "SENT"

    FILLED = "FILLED"

    PARTIAL = "PARTIAL"

    MODIFIED = "MODIFIED"

    CLOSED = "CLOSED"

    FAILED = "FAILED"


@dataclass
class LifecycleEvent:
    """
    Represents one lifecycle transition.
    """

    previous_state: Optional[OrderState]

    new_state: OrderState

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )

    message: str = ""


class OrderLifecycle:
    """
    Controls legal order state transitions.
    """

    VALID_TRANSITIONS = {

        OrderState.NEW: {
            OrderState.SENT,
            OrderState.FAILED,
        },

        OrderState.SENT: {
            OrderState.FILLED,
            OrderState.FAILED,
        },

        OrderState.FILLED: {
            OrderState.PARTIAL,
            OrderState.MODIFIED,
            OrderState.CLOSED,
        },

        OrderState.PARTIAL: {
            OrderState.PARTIAL,
            OrderState.MODIFIED,
            OrderState.CLOSED,
        },

        OrderState.MODIFIED: {
            OrderState.MODIFIED,
            OrderState.PARTIAL,
            OrderState.CLOSED,
        },

        OrderState.CLOSED: set(),

        OrderState.FAILED: set(),
    }

    def __init__(self):

        self._state = OrderState.NEW

        self._history: List[LifecycleEvent] = [

            LifecycleEvent(
                previous_state=None,
                new_state=OrderState.NEW,
                message="Lifecycle created.",
            )
        ]

    # --------------------------------------------------
    # State
    # --------------------------------------------------

    @property
    def state(self):

        return self._state

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    def can_transition(
        self,
        new_state: OrderState,
    ) -> bool:

        return (
            new_state
            in self.VALID_TRANSITIONS[self._state]
        )

    # --------------------------------------------------
    # Transition
    # --------------------------------------------------

    def transition(
        self,
        new_state: OrderState,
        message: str = "",
    ) -> bool:
        """
        Attempt lifecycle transition.

        Returns True on success.
        """

        if not self.can_transition(
            new_state
        ):
            return False

        previous = self._state

        self._state = new_state

        self._history.append(

            LifecycleEvent(
                previous_state=previous,
                new_state=new_state,
                message=message,
            )
        )

        return True

    # --------------------------------------------------
    # Convenience
    # --------------------------------------------------

    def mark_sent(self):

        return self.transition(
            OrderState.SENT
        )

    def mark_filled(self):

        return self.transition(
            OrderState.FILLED
        )

    def mark_partial(self):

        return self.transition(
            OrderState.PARTIAL
        )

    def mark_modified(self):

        return self.transition(
            OrderState.MODIFIED
        )

    def mark_closed(self):

        return self.transition(
            OrderState.CLOSED
        )

    def mark_failed(self):

        return self.transition(
            OrderState.FAILED
        )

    # --------------------------------------------------
    # Queries
    # --------------------------------------------------

    def is_open(self):

        return self._state in (

            OrderState.NEW,

            OrderState.SENT,

            OrderState.FILLED,

            OrderState.PARTIAL,

            OrderState.MODIFIED,
        )

    def is_closed(self):

        return self._state == OrderState.CLOSED

    def is_failed(self):

        return self._state == OrderState.FAILED

    # --------------------------------------------------
    # History
    # --------------------------------------------------

    def history(self):

        return list(self._history)

    # --------------------------------------------------
    # Reset
    # --------------------------------------------------

    def reset(self):

        self._state = OrderState.NEW

        self._history = [

            LifecycleEvent(

                previous_state=None,

                new_state=OrderState.NEW,

                message="Lifecycle reset.",
            )
        ]

    # --------------------------------------------------
    # Export
    # --------------------------------------------------

    def snapshot(self):

        return {

            "current_state": self._state.value,

            "history": [

                {

                    "previous_state": (
                        item.previous_state.value
                        if item.previous_state
                        else None
                    ),

                    "new_state": item.new_state.value,

                    "timestamp": item.timestamp.isoformat(),

                    "message": item.message,

                }

                for item in self._history
            ],
        }