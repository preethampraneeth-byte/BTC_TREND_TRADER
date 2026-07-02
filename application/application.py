"""
BTC Trend Trader Professional v4
Application
"""

from __future__ import annotations

from application.context import ApplicationContext
from application.shutdown import Shutdown
from application.startup import Startup


class Application:
    """
    Main application coordinator.
    """

    def __init__(self) -> None:

        self.context = ApplicationContext()

        self.startup = Startup(
            self.context,
        )

        self.shutdown = Shutdown(
            self.context,
        )

    # ---------------------------------------------------------

    def initialize(self) -> None:

        self.startup.initialize()

    # ---------------------------------------------------------

    def run(self) -> None:

        runtime = self.context.runtime

        if runtime is None:
            raise RuntimeError(
                "Application runtime has not been initialized."
            )

        runtime.run()

    # ---------------------------------------------------------

    def stop(self) -> None:

        self.shutdown.execute()

    # ---------------------------------------------------------

    def execute(self) -> None:
        """
        Complete application lifecycle.
        """

        try:

            self.initialize()

            self.run()

        finally:

            self.stop()