"""
Application startup validation.

This service validates the application configuration
before execution begins.
"""

from __future__ import annotations

from services.configuration_manager import ConfigurationManager


class StartupValidator:
    """
    Validates application startup requirements.
    """

    def __init__(self):
        self.config = ConfigurationManager()

    def validate(self):
        """
        Validate application configuration.
        Raises ValueError if a configuration value is invalid.
        """

        self._validate_backtest_balance()
        self._validate_paper_balance()
        self._validate_risk()
        self._validate_rr_ratio()
        self._validate_atr_settings()
        self._validate_partial_profit()
        self._validate_time_exit()

        return True

    # -------------------------------------------------

    def _validate_backtest_balance(self):
        """Ensure the backtest starting balance is valid."""

        if self.config.get("INITIAL_BALANCE") <= 0:
            raise ValueError(
                "INITIAL_BALANCE must be greater than 0."
            )

    # -------------------------------------------------

    def _validate_paper_balance(self):
        """Ensure the paper trading starting balance is valid."""

        if self.config.get("PAPER_STARTING_BALANCE") <= 0:
            raise ValueError(
                "PAPER_STARTING_BALANCE must be greater than 0."
            )

    # -------------------------------------------------

    def _validate_risk(self):
        """Ensure risk per trade is within a valid range."""

        risk = self.config.get("RISK_PER_TRADE")

        if not 0 < risk <= 1:
            raise ValueError(
                "RISK_PER_TRADE must be between 0 and 1."
            )

    # -------------------------------------------------

    def _validate_rr_ratio(self):
        """Ensure the reward-to-risk ratio is valid."""

        if self.config.get("RR_RATIO") <= 0:
            raise ValueError(
                "RR_RATIO must be greater than 0."
            )

    # -------------------------------------------------

    def _validate_atr_settings(self):
        """Ensure ATR-related settings are valid."""

        if self.config.get("ATR_PERIOD") <= 0:
            raise ValueError(
                "ATR_PERIOD must be greater than 0."
            )

        if self.config.get("ATR_SL_MULTIPLIER") <= 0:
            raise ValueError(
                "ATR_SL_MULTIPLIER must be greater than 0."
            )

        if self.config.get("TRAILING_STOP_ATR") <= 0:
            raise ValueError(
                "TRAILING_STOP_ATR must be greater than 0."
            )

    # -------------------------------------------------

    def _validate_partial_profit(self):
        """Ensure partial profit configuration is valid."""

        if not self.config.get("ENABLE_PARTIAL_TP"):
            return

        levels = self.config.get("PARTIAL_TP_LEVELS")
        percentages = self.config.get("PARTIAL_TP_PERCENTAGES")

        if len(levels) != len(percentages):
            raise ValueError(
                "PARTIAL_TP_LEVELS and PARTIAL_TP_PERCENTAGES must have the same length."
            )

        if len(levels) == 0:
            raise ValueError(
                "At least one partial take-profit level is required."
            )

        if sum(percentages) != 100:
            raise ValueError(
                "PARTIAL_TP_PERCENTAGES must total exactly 100."
            )

        for level in levels:
            if level <= 0:
                raise ValueError(
                    "All PARTIAL_TP_LEVELS must be greater than 0."
                )

        for percentage in percentages:
            if percentage <= 0:
                raise ValueError(
                    "All PARTIAL_TP_PERCENTAGES must be greater than 0."
                )

    # -------------------------------------------------

    def _validate_time_exit(self):
        """Ensure time exit configuration is valid."""

        if not self.config.get("ENABLE_TIME_EXIT"):
            return

        if self.config.get("MAX_BARS_IN_TRADE") <= 0:
            raise ValueError(
                "MAX_BARS_IN_TRADE must be greater than 0."
            )