"""
BTC Trend Trader Professional v4
Application Startup
"""

from __future__ import annotations

import config

from application.context import ApplicationContext
from runtime.execution_router import ExecutionRouter


class Startup:
    """
    Initializes the application.

    Responsibilities
    ----------------
    - Load configuration
    - Create execution runtime
    - Register shared services
    """

    def __init__(
        self,
        context: ApplicationContext,
    ) -> None:

        self.context = context

    # ---------------------------------------------------------

    def initialize(self) -> ApplicationContext:
        """
        Initialize application services.
        """

        self.context.config = config

        router = ExecutionRouter()

        runtime = router.runtime()

        self.context.runtime = runtime

        self.context.register(
            "execution_router",
            router,
        )

        self.context.register(
            "runtime",
            runtime,
        )

        return self.context