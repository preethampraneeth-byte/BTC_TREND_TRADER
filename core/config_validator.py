"""
BTC Trend Trader Professional v4
Configuration Validator

Sprint 11.2.1
"""

from __future__ import annotations

from services.configuration_manager import ConfigurationManager


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

    config = ConfigurationManager()

    # -------------------------------------------------
    # Symbol
    # -------------------------------------------------

    if not config.get("SYMBOL").strip():

        raise ValueError(
            "SYMBOL cannot be empty."
        )

    # -------------------------------------------------
    # Timeframe
    # -------------------------------------------------

    timeframe = config.get("TIMEFRAME")

    if timeframe.upper() not in SUPPORTED_TIMEFRAMES:

        raise ValueError(
            f"Unsupported timeframe: {timeframe}"
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

    if not (0 < config.get("RISK_PER_TRADE") <= 1):

        raise ValueError(
            "RISK_PER_TRADE must be between 0 and 1."
        )

    # -------------------------------------------------
    # Balances
    # -------------------------------------------------

    if config.get("INITIAL_BALANCE") <= 0:

        raise ValueError(
            "INITIAL_BALANCE must be positive."
        )

    if config.get("PAPER_STARTING_BALANCE") <= 0:

        raise ValueError(
            "PAPER_STARTING_BALANCE must be positive."
        )

    # -------------------------------------------------
    # Magic Number
    # -------------------------------------------------

    if config.get("MAGIC_NUMBER") <= 0:

        raise ValueError(
            "MAGIC_NUMBER must be positive."
        )

    # -------------------------------------------------
    # Time Exit
    # -------------------------------------------------

    if config.get("MAX_BARS_IN_TRADE") <= 0:

        raise ValueError(
            "MAX_BARS_IN_TRADE must be greater than zero."
        )

    # -------------------------------------------------
    # Partial Profit Validation
    # -------------------------------------------------

    partial_tp_levels = config.get("PARTIAL_TP_LEVELS")
    partial_tp_percentages = config.get("PARTIAL_TP_PERCENTAGES")

    if len(partial_tp_levels) != len(partial_tp_percentages):

        raise ValueError(
            "PARTIAL_TP_LEVELS and "
            "PARTIAL_TP_PERCENTAGES must have "
            "the same length."
        )

    if sum(partial_tp_percentages) != 100:

        raise ValueError(
            "PARTIAL_TP_PERCENTAGES must total 100."
        )