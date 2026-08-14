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
    - H4 Trend Regime

    Also calculates:

    - Stop Loss
    - Take Profit
    """

    def generate_signals(
        self,
        df: pd.DataFrame,
        h4_df: pd.DataFrame | None = None,
    ) -> pd.DataFrame:

        data = df.copy()

        # -------------------------------------------------
        # H4 Trend Regime
        # -------------------------------------------------

        if h4_df is None or h4_df.empty:
            raise ValueError(
                "H4 market data is required for Strategy v5."
            )

        h4_data = h4_df.copy()

        h4_data["H4_EMA_50"] = h4_data["Close"].ewm(
            span=50,
            adjust=False,
        ).mean()

        h4_data["H4_EMA_200"] = h4_data["Close"].ewm(
            span=200,
            adjust=False,
        ).mean()

        h4_data["H4_Bullish"] = (
            h4_data["H4_EMA_50"]
            > h4_data["H4_EMA_200"]
        )

        h4_data["H4_Bearish"] = (
            h4_data["H4_EMA_50"]
            < h4_data["H4_EMA_200"]
        )

        # Use the most recent completed H4 regime
        # for each H1 candle.
        h4_regime = h4_data[
            [
                "Time",
                "H4_EMA_50",
                "H4_EMA_200",
                "H4_Bullish",
                "H4_Bearish",
            ]
        ].copy()

        data = pd.merge_asof(
            data.sort_values("Time"),
            h4_regime.sort_values("Time"),
            on="Time",
            direction="backward",
        )

        data["H4_Bullish"] = (
            data["H4_Bullish"]
            .fillna(False)
        )

        data["H4_Bearish"] = (
            data["H4_Bearish"]
            .fillna(False)
        )

        # -------------------------------------------------
        # Signal Defaults
        # -------------------------------------------------

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
            & data["H4_Bullish"]
            & strong_trend
            & (data["ADX"] > config.ADX_THRESHOLD)
            & (data["RSI"] <= config.RSI_BUY_LEVEL)
        )

        # -------------------------------------------------
        # SELL
        # -------------------------------------------------

        sell = (
            bearish_ema
            & data["H4_Bearish"]
            & strong_trend
            & (data["ADX"] > config.ADX_THRESHOLD)
            & (data["RSI"] >= config.RSI_SELL_LEVEL)
        )

        # -------------------------------------------------
        # BUY Signal
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
        # SELL Signal
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
            hold
            & (~bullish_ema)
            & (~bearish_ema),
            "Reason"
        ] = "EMA direction unavailable"

        # -------------------------------------------------
        # Determine possible BUY / SELL direction
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
        ] = "EMA distance too small"

        # -------------------------------------------------
        # ADX Failure
        # -------------------------------------------------

        data.loc[
            bullish_candidate
            & strong_trend
            & (data["ADX"] <= config.ADX_THRESHOLD),
            "Reason"
        ] = "BUY rejected: ADX below threshold"

        data.loc[
            bearish_candidate
            & strong_trend
            & (data["ADX"] <= config.ADX_THRESHOLD),
            "Reason"
        ] = "SELL rejected: ADX below threshold"

        # -------------------------------------------------
        # RSI Failure
        # -------------------------------------------------

        data.loc[
            bullish_candidate
            & strong_trend
            & (data["ADX"] > config.ADX_THRESHOLD)
            & (data["RSI"] > config.RSI_BUY_LEVEL),
            "Reason"
        ] = "BUY rejected: RSI above buy level"

        data.loc[
            bearish_candidate
            & strong_trend
            & (data["ADX"] > config.ADX_THRESHOLD)
            & (data["RSI"] < config.RSI_SELL_LEVEL),
            "Reason"
        ] = "SELL rejected: RSI below sell level"

        # -------------------------------------------------
        # H4 Regime Rejection Diagnostics
        #
        # Keep this LAST so an H4 rejection is not
        # overwritten by ADX or RSI diagnostics.
        # -------------------------------------------------

        data.loc[
            hold
            & bullish_ema
            & (~data["H4_Bullish"]),
            "Reason"
        ] = "BUY rejected: H4 trend not bullish"

        data.loc[
            hold
            & bearish_ema
            & (~data["H4_Bearish"]),
            "Reason"
        ] = "SELL rejected: H4 trend not bearish"

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

        data["Diagnostic_H4_EMA_50"] = (
            data["H4_EMA_50"]
        )

        data["Diagnostic_H4_EMA_200"] = (
            data["H4_EMA_200"]
        )

        data["Diagnostic_H4_Bullish"] = (
            data["H4_Bullish"]
        )

        data["Diagnostic_H4_Bearish"] = (
            data["H4_Bearish"]
        )

        return data