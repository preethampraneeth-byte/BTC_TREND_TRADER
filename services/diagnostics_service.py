"""
BTC Trend Trader Professional v4
Diagnostics Service
"""

from __future__ import annotations

import config


class DiagnosticsService:
    """
    Generates strategy diagnostics.
    """

    def __init__(self) -> None:
        pass

    # -------------------------------------------------

    def generate(self, candles):

        ema_fast = candles[
            f"EMA_{config.EMA_FAST}"
        ]

        ema_slow = candles[
            f"EMA_{config.EMA_SLOW}"
        ]

        ema_distance = (ema_fast - ema_slow).abs()

        strong_trend = (
            ema_distance
            >= candles["ATR"]
            * config.EMA_DISTANCE_ATR_MULTIPLIER
        )

        adx_ok = (
            candles["ADX"]
            > config.ADX_THRESHOLD
        )

        rsi_buy = (
            candles["RSI"]
            <= config.RSI_BUY_LEVEL
        )

        rsi_sell = (
            candles["RSI"]
            >= config.RSI_SELL_LEVEL
        )

        buy_step1 = ema_fast > ema_slow
        buy_step2 = buy_step1 & strong_trend
        buy_step3 = buy_step2 & adx_ok
        buy_step4 = buy_step3 & rsi_buy

        sell_step1 = ema_fast < ema_slow
        sell_step2 = sell_step1 & strong_trend
        sell_step3 = sell_step2 & adx_ok
        sell_step4 = sell_step3 & rsi_sell

        return {

            "BUY: EMA > Slow": int(buy_step1.sum()),
            "BUY: + Strong Trend": int(buy_step2.sum()),
            "BUY: + ADX": int(buy_step3.sum()),
            "BUY: + RSI": int(buy_step4.sum()),

            "SELL: EMA < Slow": int(sell_step1.sum()),
            "SELL: + Strong Trend": int(sell_step2.sum()),
            "SELL: + ADX": int(sell_step3.sum()),
            "SELL: + RSI": int(sell_step4.sum()),

        }