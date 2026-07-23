"""
Application startup validation.

This service validates the application configuration
before execution begins.
"""

from __future__ import annotations

import config


class StartupValidator:
    """
    Validates application startup requirements.
    """

    def validate(self):
        """Validate application configuration."""

        self._validate_backtest_balance()
        self._validate_paper_balance()
        self._validate_risk()
        self._validate_rr_ratio()
        self._validate_atr_settings()
        self._validate_partial_profit()

        return True

    # -------------------------------------------------

    def _validate_backtest_balance(self):

        if config.INITIAL_BALANCE <= 0:
            raise ValueError(
                "INITIAL_BALANCE must be greater than 0."
            )

    # -------------------------------------------------

    def _validate_paper_balance(self):

        if config.PAPER_STARTING_BALANCE <= 0:
            raise ValueError(
                "PAPER_STARTING_BALANCE must be greater than 0."
            )

    # -------------------------------------------------

    def _validate_risk(self):

        if not 0 < config.RISK_PER_TRADE <= 1:
            raise ValueError(
                "RISK_PER_TRADE must be between 0 and 1."
            )

    # -------------------------------------------------

    def _validate_rr_ratio(self):

        if config.RR_RATIO <= 0:
            raise ValueError(
                "RR_RATIO must be greater than 0."
            )

    # -------------------------------------------------

    def _validate_atr_settings(self):

        if config.ATR_PERIOD <= 0:
            raise ValueError(
                "ATR_PERIOD must be greater than 0."
            )

        if config.ATR_SL_MULTIPLIER <= 0:
            raise ValueError(
                "ATR_SL_MULTIPLIER must be greater than 0."
            )

        if config.TRAILING_STOP_ATR <= 0:
            raise ValueError(
                "TRAILING_STOP_ATR must be greater than 0."
            )

    # -------------------------------------------------

    def _validate_partial_profit(self):

        if not config.ENABLE_PARTIAL_TP:
            return

        if len(config.PARTIAL_TP_LEVELS) != len(config.PARTIAL_TP_PERCENTAGES):
            raise ValueError(
                "PARTIAL_TP_LEVELS and PARTIAL_TP_PERCENTAGES must have the same length."
            )

        if len(config.PARTIAL_TP_LEVELS) == 0:
            raise ValueError(
                "At least one partial take-profit level is required."
            )

        total_percentage = sum(config.PARTIAL_TP_PERCENTAGES)

        if total_percentage != 100:
            raise ValueError(
                "PARTIAL_TP_PERCENTAGES must total exactly 100."
            )

        for level in config.PARTIAL_TP_LEVELS:
            if level <= 0:
                raise ValueError(
                    "All PARTIAL_TP_LEVELS must be greater than 0."
                )

        for percentage in config.PARTIAL_TP_PERCENTAGES:
            if percentage <= 0:
                raise ValueError(
                    "All PARTIAL_TP_PERCENTAGES must be greater than 0."
                )