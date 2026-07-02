"""
Performance Panel
"""

from __future__ import annotations

from typing import Any, Dict


class PerformancePanel:
    """Read-only performance statistics panel."""

    def __init__(self) -> None:
        self._statistics: Dict[str, Any] = {}

    def update(self, statistics: Dict[str, Any] | None) -> None:
        self._statistics = dict(statistics or {})

    def render(self) -> None:
        print("\n" + "=" * 60)
        print("PERFORMANCE")
        print("=" * 60)

        if not self._statistics:
            print("No performance statistics available.")
            return

        for key, value in self._statistics.items():
            print(f"{key:<25}: {value}")

    @property
    def statistics(self) -> Dict[str, Any]:
        return dict(self._statistics)