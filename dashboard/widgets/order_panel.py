"""
Order Panel
"""

from __future__ import annotations

from typing import Any, List


class OrderPanel:
    """Read-only order information panel."""

    def __init__(self) -> None:
        self._orders: List[Any] = []

    def update(self, orders: List[Any] | None) -> None:
        self._orders = list(orders or [])

    def render(self) -> None:
        print("\n" + "=" * 60)
        print("OPEN ORDERS")
        print("=" * 60)

        if not self._orders:
            print("No open orders.")
            return

        for index, order in enumerate(self._orders, start=1):
            print(f"{index}. {order}")

    @property
    def orders(self) -> List[Any]:
        return list(self._orders)