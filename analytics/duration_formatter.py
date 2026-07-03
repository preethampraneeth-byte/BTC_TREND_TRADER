"""
BTC Trend Trader Professional v4
Duration Formatter
"""

from __future__ import annotations


class DurationFormatter:
    """
    Converts duration (seconds) into
    human-readable text.
    """

    # -------------------------------------------------

    def format(
        self,
        seconds: float,
    ) -> str:

        if seconds <= 0:
            return "0m"

        seconds = int(seconds)

        days = seconds // 86400
        seconds %= 86400

        hours = seconds // 3600
        seconds %= 3600

        minutes = seconds // 60

        parts = []

        if days:
            parts.append(f"{days}d")

        if hours:
            parts.append(f"{hours}h")

        if minutes:
            parts.append(f"{minutes}m")

        if not parts:
            return "<1m"

        return " ".join(parts)