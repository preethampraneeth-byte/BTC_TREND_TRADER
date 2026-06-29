import pandas_ta as ta

from config import (
    FAST_EMA,
    SLOW_EMA,
    ATR_PERIOD,
    ADX_PERIOD,
    RSI_PERIOD
)


def calculate_indicators(df):
    """
    Calculate all indicators.
    """

    # EMA
    df["EMA_FAST"] = ta.ema(
        df["close"],
        length=FAST_EMA
    )

    df["EMA_SLOW"] = ta.ema(
        df["close"],
        length=SLOW_EMA
    )

    # ATR
    df["ATR"] = ta.atr(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        length=ATR_PERIOD
    )

    # ADX
    adx = ta.adx(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        length=ADX_PERIOD
    )

    df["ADX"] = adx[f"ADX_{ADX_PERIOD}"]

    # RSI
    df["RSI"] = ta.rsi(
        df["close"],
        length=RSI_PERIOD
    )

    return df