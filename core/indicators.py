"""
BTC Trend Trader v1.0
Indicators Module

Calculates:
- EMA 20
- EMA Fast
- EMA Slow
- ATR
- RSI
- ADX

Uses pandas-ta for reliable indicator calculations.
"""

from __future__ import annotations

import pandas as pd
import pandas_ta as ta

import config


class Indicators:
    """
    Calculates all technical indicators required by the strategy.
    """

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add technical indicators to the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame

        Returns
        -------
        pandas.DataFrame
        """

        data = df.copy()

        # ==========================
        # EMA
        # ==========================

        # EMA 20
        # Used later by Strategy v5
        # for pullback / entry timing.
        data["EMA_20"] = ta.ema(
            data["Close"],
            length=20,
        )

        # Fast EMA
        data[f"EMA_{config.EMA_FAST}"] = ta.ema(
            data["Close"],
            length=config.EMA_FAST,
        )

        # Slow EMA
        data[f"EMA_{config.EMA_SLOW}"] = ta.ema(
            data["Close"],
            length=config.EMA_SLOW,
        )

        # ==========================
        # ATR
        # ==========================

        data["ATR"] = ta.atr(
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
            length=config.ATR_PERIOD,
        )

        # ==========================
        # RSI
        # ==========================

        data["RSI"] = ta.rsi(
            data["Close"],
            length=config.RSI_PERIOD,
        )

        # ==========================
        # ADX
        # ==========================

        adx = ta.adx(
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
            length=config.ADX_PERIOD,
        )

        data["ADX"] = adx[
            f"ADX_{config.ADX_PERIOD}"
        ]

        return data