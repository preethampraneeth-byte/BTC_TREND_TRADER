"""
BTC Trend Trader Professional v4
Configuration Validator

Sprint 11.2.1
"""

from __future__ import annotations

import config


SUPPORTED_TIMEFRAMES = {
    "M1",
    "M5",
    "M15",
    "M30",
    "H1",
    "H4",
    "D1",
}


def validate() -> None:
    """
    Validate application configuration.

    Raises
    ------
    ValueError
        If any configuration value is invalid.
    """

    # -------------------------------------------------
    # Symbol
    # -------------------------------------------------

    if not config.SYMBOL.strip():

        raise ValueError(
            "SYMBOL cannot be empty."
        )

    # -------------------------------------------------
    # Timeframe
    # -------------------------------------------------

    if config.TIMEFRAME.upper() not in SUPPORTED_TIMEFRAMES:

        raise ValueError(
            f"Unsupported timeframe: {config.TIMEFRAME}"
        )

    # -------------------------------------------------
    # Risk
    # -------------------------------------------------

    #
    # RISK_PER_TRADE is stored as a decimal fraction.
    #
    # Examples:
    #
    # 0.01 = 1%
    # 0.02 = 2%
    # 0.005 = 0.5%
    #

    if not (0 < config.RISK_PER_TRADE <= 1):

        raise ValueError(
            "RISK_PER_TRADE must be between 0 and 1."
        )

    # -------------------------------------------------
    # Balances
    # -------------------------------------------------

    if config.INITIAL_BALANCE <= 0:

        raise ValueError(
            "INITIAL_BALANCE must be positive."
        )

    if config.PAPER_STARTING_BALANCE <= 0:

        raise ValueError(
            "PAPER_STARTING_BALANCE must be positive."
        )

    # -------------------------------------------------
    # Magic Number
    # -------------------------------------------------

    if config.MAGIC_NUMBER <= 0:

        raise ValueError(
            "MAGIC_NUMBER must be positive."
        )

    # -------------------------------------------------
    # Time Exit
    # -------------------------------------------------

    if config.MAX_BARS_IN_TRADE <= 0:

        raise ValueError(
            "MAX_BARS_IN_TRADE must be greater than zero."
        )

    # -------------------------------------------------
    # Partial Profit Validation
    # -------------------------------------------------

    if len(config.PARTIAL_TP_LEVELS) != len(
        config.PARTIAL_TP_PERCENTAGES
    ):

        raise ValueError(
            "PARTIAL_TP_LEVELS and "
            "PARTIAL_TP_PERCENTAGES must have "
            "the same length."
        )

    if sum(config.PARTIAL_TP_PERCENTAGES) != 100:

        raise ValueError(
            "PARTIAL_TP_PERCENTAGES must total 100."
        )