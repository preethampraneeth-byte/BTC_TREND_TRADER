"""
History Panel
"""

from __future__ import annotations

from typing import Any, List


class HistoryPanel:
    """Read-only trade history panel."""

    def __init__(self) -> None:
        self._history: List[Any] = []

    def update(self, history: List[Any] | None) -> None:
        self._history = list(history or [])

    def render(self) -> None:
        print("\n" + "=" * 60)
        print("TRADE HISTORY")
        print("=" * 60)

        if not self._history:
            print("No trade history available.")
            return

        for index, trade in enumerate(self._history, start=1):
            print(f"{index}. {trade}")

    @property
    def history(self) -> List[Any]:
        return list(self._history)