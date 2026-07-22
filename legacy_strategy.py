from config import (
    ADX_THRESHOLD,
    RSI_BUY_LEVEL,
    RSI_SELL_LEVEL,
    EMA_DISTANCE_ATR_MULTIPLIER
)


def check_signal(df):
    print("Using strategy.py")
    """
    Trend Continuation Strategy

    BUY:
        EMA_FAST > EMA_SLOW
        ADX > ADX_THRESHOLD
        RSI < RSI_BUY_LEVEL
        Close > EMA_FAST

    SELL:
        EMA_FAST < EMA_SLOW
        ADX > ADX_THRESHOLD
        RSI > RSI_SELL_LEVEL
        Close < EMA_FAST
    """

    current = df.iloc[-2]

    trend = "SIDEWAYS"
    signal = "NO SIGNAL"

    # -------------------------
    # Trend Direction
    # -------------------------

    if current["EMA_FAST"] > current["EMA_SLOW"]:
        trend = "BULLISH"

    elif current["EMA_FAST"] < current["EMA_SLOW"]:
        trend = "BEARISH"

    # -------------------------
    # Trend Strength
    # -------------------------

    trending = current["ADX"] >= ADX_THRESHOLD
    ema_distance = abs(current["EMA_FAST"] - current["EMA_SLOW"])
    minimum_distance = current["ATR"] * EMA_DISTANCE_ATR_MULTIPLIER

    # -------------------------
    # BUY
    # -------------------------

    if (
        trend == "BULLISH"
        and trending
    #   and current["RSI"] <= RSI_BUY_LEVEL
        and current["close"] > current["EMA_FAST"]
    #   and ema_distance >= minimum_distance
    ):
        signal = "BUY"

    # -------------------------
    # SELL
    # -------------------------

    elif (
        trend == "BEARISH"
        and trending
        and current["RSI"] >= RSI_SELL_LEVEL
        and current["close"] < current["EMA_FAST"]
    ):
        signal = "SELL"

    return {
        "signal": signal,
        "trend": trend,
        "trending": trending,
        "close": round(current["close"], 2),
        "ema_fast": round(current["EMA_FAST"], 2),
        "ema_slow": round(current["EMA_SLOW"], 2),
        "adx": round(current["ADX"], 2),
        "atr": round(current["ATR"], 2),
        "rsi": round(current["RSI"], 2)
    }