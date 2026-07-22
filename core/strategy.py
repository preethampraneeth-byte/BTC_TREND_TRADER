"""
BTC Trend Trader v1.2
Strategy Module
"""

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
    """

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:

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

        strong_trend = (
            ema_distance
            >= (
                data["ATR"]
                * config.EMA_DISTANCE_ATR_MULTIPLIER
            )
        )

        # -------------------------------------------------
        # BUY
        # -------------------------------------------------

        buy = (

            (data[f"EMA_{config.EMA_FAST}"]
             > data[f"EMA_{config.EMA_SLOW}"])

            & strong_trend

            & (data["ADX"] > config.ADX_THRESHOLD)

            & (data["RSI"] <= config.RSI_BUY_LEVEL)

        )

        # -------------------------------------------------
        # SELL
        # -------------------------------------------------

        sell = (

            (data[f"EMA_{config.EMA_FAST}"]
             < data[f"EMA_{config.EMA_SLOW}"])

            & strong_trend

            & (data["ADX"] > config.ADX_THRESHOLD)

            & (data["RSI"] >= config.RSI_SELL_LEVEL)

        )

        # -------------------------------------------------
        # BUY
        # -------------------------------------------------

        data.loc[buy, "Signal"] = Signal.BUY.name
        data.loc[buy, "Reason"] = "Strong bullish trend"

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
        data.loc[sell, "Reason"] = "Strong bearish trend"

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
        # HOLD Reasons
        # -------------------------------------------------

        weak = data["Signal"] == Signal.HOLD.name

        data.loc[
            weak & (~strong_trend),
            "Reason"
        ] = "EMA distance too small"

        data.loc[
            weak
            & strong_trend
            & (data["ADX"] <= config.ADX_THRESHOLD),
            "Reason"
        ] = "Weak trend (ADX)"

        return data