"""
Position Panel
"""

from __future__ import annotations

from typing import Any, List


class PositionPanel:
    """Read-only position information panel."""

    def __init__(self) -> None:
        self._positions: List[Any] = []

    def update(self, positions: List[Any] | None) -> None:
        self._positions = list(positions or [])

    def render(self) -> None:
        print("\n" + "=" * 60)
        print("OPEN POSITIONS")
        print("=" * 60)

        if not self._positions:
            print("No open positions.")
            return

        for index, position in enumerate(self._positions, start=1):
            print(f"{index}. {position}")

    @property
    def positions(self) -> List[Any]:
        return list(self._positions)