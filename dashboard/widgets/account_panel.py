"""
Account Panel
"""

from __future__ import annotations

from typing import Any, Dict


class AccountPanel:
    """Read-only account information panel."""

    def __init__(self) -> None:
        self._data: Dict[str, Any] = {}

    def update(self, data: Dict[str, Any] | None) -> None:
        self._data = dict(data or {})

    def render(self) -> None:
        print("\n" + "=" * 60)
        print("ACCOUNT")
        print("=" * 60)

        if not self._data:
            print("No account data available.")
            return

        for key, value in self._data.items():
            print(f"{key:<25}: {value}")

    @property
    def data(self) -> Dict[str, Any]:
        return dict(self._data)