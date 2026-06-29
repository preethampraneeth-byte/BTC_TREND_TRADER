"""
BTC Trend Trader v1.0
Indicators Module

Calculates:
- EMA
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

        data[f"EMA_{config.EMA_FAST}"] = ta.ema(
            data["Close"],
            length=config.EMA_FAST
        )

        data[f"EMA_{config.EMA_SLOW}"] = ta.ema(
            data["Close"],
            length=config.EMA_SLOW
        )

        # ==========================
        # ATR
        # ==========================

        data["ATR"] = ta.atr(
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
            length=config.ATR_PERIOD
        )

        # ==========================
        # RSI
        # ==========================

        data["RSI"] = ta.rsi(
            data["Close"],
            length=config.RSI_PERIOD
        )

        # ==========================
        # ADX
        # ==========================

        adx = ta.adx(
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
            length=config.ADX_PERIOD
        )

        data["ADX"] = adx[f"ADX_{config.ADX_PERIOD}"]

        return data