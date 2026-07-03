"""
BTC Trend Trader Professional v4
Analytics Module Registry
"""

from __future__ import annotations

from typing import Any, Dict


class AnalyticsModuleRegistry:
    """
    Stores registered analytics modules.
    """

    def __init__(self):

        self._modules: Dict[str, Any] = {}

    # -------------------------------------------------

    def register(
        self,
        name: str,
        module: Any,
    ) -> None:

        self._modules[name] = module

    # -------------------------------------------------

    def modules(self):

        return self._modules.items()