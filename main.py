"""
BTC Trend Trader Professional v4
Application Entry Point
"""

from __future__ import annotations

import sys
import traceback

from runtime.application_runtime import ApplicationRuntime
from core.config_validator import validate

VALID_MODES = {
    "backtest",
    "paper",
    "live",
}


def main() -> None:
    """
    Application entry point.

    Responsibilities
    ----------------
    • Validate startup mode
    • Display startup information
    • Catch startup failures
    • Exit cleanly
    """

    mode = "backtest"

    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()

    if mode not in VALID_MODES:

        print()

        print("========================================")
        print(" Invalid execution mode")
        print("========================================")
        print(f"Mode: {mode}")
        print()
        print("Valid modes:")
        print("  backtest")
        print("  paper")
        print("  live")
        print()

        sys.exit(1)

    print()
    print("========================================")
    print(" BTC Trend Trader Professional v4")
    print("========================================")
    print(f"Starting in {mode.upper()} mode...")
    print()

    try:

        validate()
        
        app = ApplicationRuntime()

        app.run(mode)

        print()
        print("Application exited normally.")

        sys.exit(0)

    except KeyboardInterrupt:

        print()
        print("Shutdown requested by user.")
        sys.exit(0)

    except Exception as ex:

        print()
        print("========================================")
        print(" STARTUP FAILED")
        print("========================================")
        print(type(ex).__name__)
        print(str(ex))
        print()

        traceback.print_exc()

        sys.exit(2)


if __name__ == "__main__":
    main()