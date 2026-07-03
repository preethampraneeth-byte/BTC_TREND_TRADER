"""
BTC Trend Trader Professional v4
Application Entry Point
"""

from __future__ import annotations

import sys

from runtime.application_runtime import ApplicationRuntime


def main() -> None:

    mode = "backtest"

    if len(sys.argv) > 1:

        mode = sys.argv[1]

    app = ApplicationRuntime()

    app.run(mode)


if __name__ == "__main__":

    main()