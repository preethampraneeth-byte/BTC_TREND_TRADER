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
        """
        Validate application configuration.
        Raises ValueError if a configuration value is invalid.
        """

        self._validate_backtest_balance()
        self._validate_paper_balance()
        self._validate_risk()
        self._validate_rr_ratio()
        self._validate_atr_settings()

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