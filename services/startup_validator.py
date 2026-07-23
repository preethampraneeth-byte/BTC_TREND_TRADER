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

        self._validate_backtest_balance()
        self._validate_paper_balance()
        self._validate_risk()

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