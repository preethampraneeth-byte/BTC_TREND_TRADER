"""
BTC Trend Trader v1.0
Risk Management Module
"""

from __future__ import annotations

import config


class RiskManager:
    """
    Calculates trade levels and risk information.
    """

    def calculate_trade_levels(self, signal: str, row) -> dict:
        """
        Calculate Entry, Stop Loss and Take Profit.

        Parameters
        ----------
        signal : str
            BUY / SELL / HOLD

        row : pandas.Series

        Returns
        -------
        dict
        """

        entry = float(row["Close"])
        atr = float(row["ATR"])

        sl_distance = atr * config.ATR_SL_MULTIPLIER
        tp_distance = sl_distance * config.RR_RATIO

        trade = {
            "Signal": signal,
            "Reason": row.get("Reason", ""),
            "Entry": round(entry, 2),
            "ATR": round(atr, 2),
            "StopLoss": None,
            "TakeProfit": None,
            "StopDistance": 0.0,
            "RiskPercent": config.RISK_PER_TRADE * 100,
            "RiskReward": config.RR_RATIO,
        }

        if signal == "BUY":

            stop_loss = entry - sl_distance
            take_profit = entry + tp_distance

            trade["StopLoss"] = round(stop_loss, 2)
            trade["TakeProfit"] = round(take_profit, 2)
            trade["StopDistance"] = round(entry - stop_loss, 2)

        elif signal == "SELL":

            stop_loss = entry + sl_distance
            take_profit = entry - tp_distance

            trade["StopLoss"] = round(stop_loss, 2)
            trade["TakeProfit"] = round(take_profit, 2)
            trade["StopDistance"] = round(stop_loss - entry, 2)

        return trade