"""
BTC Trend Trader Professional v4
Strategy Module

Step 1:
Add detailed entry diagnostics without changing
the existing trading logic.
"""

from __future__ import annotations

from enum import Enum

import numpy as np
import pandas as pd

import config


class Signal(Enum):
    HOLD = 0
    BUY = 1
    SELL = -1


class Strategy:
    """
    Trend-following strategy using:

    - EMA Fast
    - EMA Slow
    - EMA Distance Filter
    - ADX
    - RSI

    Also calculates:

    - Stop Loss
    - Take Profit

    Step 1:
    Adds detailed diagnostic information for rejected
    entry conditions without changing signal behavior.
    """

    def generate_signals(
        self,
        df: pd.DataFrame,
        h4_df: pd.DataFrame | None = None,
    ) -> pd.DataFrame:

        data = df.copy()

        data["Signal"] = Signal.HOLD.name
        data["Reason"] = ""

        data["StopLoss"] = np.nan
        data["TakeProfit"] = np.nan

        # -------------------------------------------------
        # EMA Distance Filter
        # -------------------------------------------------

        ema_distance = abs(
            data[f"EMA_{config.EMA_FAST}"]
            - data[f"EMA_{config.EMA_SLOW}"]
        )

        required_ema_distance = (
            data["ATR"]
            * config.EMA_DISTANCE_ATR_MULTIPLIER
        )

        strong_trend = (
            ema_distance >= required_ema_distance
        )

        # -------------------------------------------------
        # Trend Direction
        # -------------------------------------------------

        bullish_ema = (
            data[f"EMA_{config.EMA_FAST}"]
            > data[f"EMA_{config.EMA_SLOW}"]
        )

        bearish_ema = (
            data[f"EMA_{config.EMA_FAST}"]
            < data[f"EMA_{config.EMA_SLOW}"]
        )

        # -------------------------------------------------
        # BUY
        # -------------------------------------------------

        buy = (
            bullish_ema
            & strong_trend
            & (data["ADX"] > config.ADX_THRESHOLD)
            & (data["RSI"] <= config.RSI_BUY_LEVEL)
        )

        # -------------------------------------------------
        # SELL
        # -------------------------------------------------

        sell = (
            bearish_ema
            & strong_trend
            & (data["ADX"] > config.ADX_THRESHOLD)
            & (data["RSI"] >= config.RSI_SELL_LEVEL)
        )

        # -------------------------------------------------
        # BUY
        # -------------------------------------------------

        data.loc[buy, "Signal"] = Signal.BUY.name

        data.loc[
            buy,
            "Reason"
        ] = "Strong bullish trend"

        data.loc[buy, "StopLoss"] = (
            data.loc[buy, "Close"]
            - data.loc[buy, "ATR"]
            * config.ATR_SL_MULTIPLIER
        )

        risk = (
            data.loc[buy, "Close"]
            - data.loc[buy, "StopLoss"]
        )

        data.loc[buy, "TakeProfit"] = (
            data.loc[buy, "Close"]
            + risk * config.RR_RATIO
        )

        # -------------------------------------------------
        # SELL
        # -------------------------------------------------

        data.loc[sell, "Signal"] = Signal.SELL.name

        data.loc[
            sell,
            "Reason"
        ] = "Strong bearish trend"

        data.loc[sell, "StopLoss"] = (
            data.loc[sell, "Close"]
            + data.loc[sell, "ATR"]
            * config.ATR_SL_MULTIPLIER
        )

        risk = (
            data.loc[sell, "StopLoss"]
            - data.loc[sell, "Close"]
        )

        data.loc[sell, "TakeProfit"] = (
            data.loc[sell, "Close"]
            - risk * config.RR_RATIO
        )

        # -------------------------------------------------
        # HOLD Diagnostics
        # -------------------------------------------------

        hold = data["Signal"] == Signal.HOLD.name

        # Start with the most fundamental failure.
        data.loc[
            hold & (~bullish_ema) & (~bearish_ema),
            "Reason"
        ] = "EMA direction unavailable"

        # -------------------------------------------------
        # Determine possible BUY/SELL direction
        # -------------------------------------------------

        bullish_candidate = (
            hold
            & bullish_ema
        )

        bearish_candidate = (
            hold
            & bearish_ema
        )

        # -------------------------------------------------
        # EMA Distance Failure
        # -------------------------------------------------

        data.loc[
            hold & (~strong_trend),
            "Reason"
        ] = (
            "EMA distance too small"
        )

        # -------------------------------------------------
        # ADX Failure
        # -------------------------------------------------

        data.loc[
            bullish_candidate
            & strong_trend
            & (data["ADX"] <= config.ADX_THRESHOLD),
            "Reason"
        ] = (
            "BUY rejected: ADX below threshold"
        )

        data.loc[
            bearish_candidate
            & strong_trend
            & (data["ADX"] <= config.ADX_THRESHOLD),
            "Reason"
        ] = (
            "SELL rejected: ADX below threshold"
        )

        # -------------------------------------------------
        # RSI Failure
        # -------------------------------------------------

        data.loc[
            bullish_candidate
            & strong_trend
            & (data["ADX"] > config.ADX_THRESHOLD)
            & (data["RSI"] > config.RSI_BUY_LEVEL),
            "Reason"
        ] = (
            "BUY rejected: RSI above buy level"
        )

        data.loc[
            bearish_candidate
            & strong_trend
            & (data["ADX"] > config.ADX_THRESHOLD)
            & (data["RSI"] < config.RSI_SELL_LEVEL),
            "Reason"
        ] = (
            "SELL rejected: RSI below sell level"
        )

        # -------------------------------------------------
        # Diagnostic Columns
        # -------------------------------------------------

        data["Diagnostic_EMA_Distance"] = ema_distance
        data["Diagnostic_Required_EMA_Distance"] = (
            required_ema_distance
        )

        data["Diagnostic_Bullish_EMA"] = bullish_ema
        data["Diagnostic_Bearish_EMA"] = bearish_ema

        data["Diagnostic_ADX_Pass"] = (
            data["ADX"] > config.ADX_THRESHOLD
        )

        data["Diagnostic_RSI_Buy_Pass"] = (
            data["RSI"] <= config.RSI_BUY_LEVEL
        )

        data["Diagnostic_RSI_Sell_Pass"] = (
            data["RSI"] >= config.RSI_SELL_LEVEL
        )

        return data