"""
BTC Trend Trader Professional v4
Application Shutdown
"""

from __future__ import annotations

from application.context import ApplicationContext


class Shutdown:
    """
    Gracefully shuts down the application.

    Responsibilities
    ----------------
    - Disconnect MT5
    - Stop runtime
    - Release resources
    - Clear application context
    """

    def __init__(
        self,
        context: ApplicationContext,
    ) -> None:

        self.context = context

    # ---------------------------------------------------------

    def execute(self) -> None:
        """
        Shutdown application resources.
        """

        runtime = self.context.runtime

        if runtime is not None:

            stop = getattr(runtime, "stop", None)

            if callable(stop):

                try:
                    stop()

                except Exception:
                    pass

        connector = self.context.connector

        if connector is not None:

            disconnect = getattr(
                connector,
                "disconnect",
                None,
            )

            if callable(disconnect):

                try:
                    disconnect()

                except Exception:
                    pass

        self.context.clear()