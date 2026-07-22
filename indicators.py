import pandas_ta as ta

from config import (
    EMA_FAST,
    EMA_SLOW,
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
        length=EMA_FAST
    )

    df["EMA_SLOW"] = ta.ema(
        df["close"],
        length=EMA_SLOW
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