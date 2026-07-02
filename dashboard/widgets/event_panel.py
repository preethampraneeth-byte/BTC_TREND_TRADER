"""
Event Panel
"""

from __future__ import annotations

from typing import Any, List


class EventPanel:
    """Read-only event log panel."""

    def __init__(self) -> None:
        self._events: List[Any] = []

    def update(self, events: List[Any] | None) -> None:
        self._events = list(events or [])

    def render(self) -> None:
        print("\n" + "=" * 60)
        print("EVENT LOG")
        print("=" * 60)

        if not self._events:
            print("No events available.")
            return

        for index, event in enumerate(self._events, start=1):
            print(f"{index}. {event}")

    @property
    def events(self) -> List[Any]:
        return list(self._events)