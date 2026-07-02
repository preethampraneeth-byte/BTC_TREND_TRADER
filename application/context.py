"""
BTC Trend Trader Professional v4
Application Context
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ApplicationContext:
    """
    Shared application context.

    Holds references shared throughout the
    application lifecycle.
    """

    config: Optional[Any] = None

    execution_router: Optional[Any] = None

    runtime: Optional[Any] = None

    connector: Optional[Any] = None

    dashboard: Optional[Any] = None

    analytics: Optional[Any] = None

    persistence: Optional[Any] = None

    services: Dict[str, Any] = field(
        default_factory=dict
    )

    # ---------------------------------------------------------

    def register(
        self,
        name: str,
        service: Any,
    ) -> None:

        self.services[name] = service

    # ---------------------------------------------------------

    def resolve(
        self,
        name: str,
    ) -> Optional[Any]:

        return self.services.get(name)

    # ---------------------------------------------------------

    def clear(self) -> None:

        self.services.clear()

        self.execution_router = None

        self.runtime = None

        self.connector = None

        self.dashboard = None

        self.analytics = None

        self.persistence = None