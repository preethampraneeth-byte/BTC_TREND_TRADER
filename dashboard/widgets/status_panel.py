"""
Status Panel
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict


class StatusPanel:
    """Read-only system status panel."""

    def __init__(self) -> None:
        self._status: Dict[str, Any] = {}

    def update(self, status: Dict[str, Any] | None) -> None:
        self._status = dict(status or {})

        if "Last Update" not in self._status:
            self._status["Last Update"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

    def render(self) -> None:
        print("\n" + "=" * 60)
        print("SYSTEM STATUS")
        print("=" * 60)

        if not self._status:
            print("No system status available.")
            return

        for key, value in self._status.items():
            print(f"{key:<25}: {value}")

    @property
    def status(self) -> Dict[str, Any]:
        return dict(self._status)