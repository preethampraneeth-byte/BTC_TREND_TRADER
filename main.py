"""
BTC Trend Trader Professional v4
Main Entry Point
"""

from application.application import Application


def main() -> None:
    """
    Bootstrap the application.

    The complete execution workflow is delegated to the
    configured runtime via Application.execute().
    """

    Application().execute()


if __name__ == "__main__":
    main()