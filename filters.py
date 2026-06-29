from config import ADX_MINIMUM


def is_trending(df):
    """
    Returns True if the market is trending.
    """

    last = df.iloc[-2]

    return last["ADX"] >= ADX_MINIMUM


def trend_direction(df):
    """
    Returns:
        BULLISH
        BEARISH
        SIDEWAYS
    """

    last = df.iloc[-2]

    if last["EMA_FAST"] > last["EMA_SLOW"]:
        return "BULLISH"

    if last["EMA_FAST"] < last["EMA_SLOW"]:
        return "BEARISH"

    return "SIDEWAYS"