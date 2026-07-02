"""
Risk Panel
"""

from __future__ import annotations

from typing import Any, Dict


class RiskPanel:
    """Read-only risk information panel."""

    def __init__(self) -> None:
        self._risk: Dict[str, Any] = {}

    def update(self, risk: Dict[str, Any] | None) -> None:
        self._risk = dict(risk or {})

    def render(self) -> None:
        print("\n" + "=" * 60)
        print("RISK")
        print("=" * 60)

        if not self._risk:
            print("No risk data available.")
            return

        for key, value in self._risk.items():
            print(f"{key:<25}: {value}")

    @property
    def data(self) -> Dict[str, Any]:
        return dict(self._risk)