"""
BTC Trend Trader v1.0
Position Size Module
"""

from __future__ import annotations

import config


class PositionSizer:
    """
    Calculates the trading volume based on
    account balance and risk percentage.
    """

    def calculate(
        self,
        balance: float,
        trade: dict,
        volume_min: float,
        volume_max: float,
        volume_step: float,
    ) -> dict:

        # No trade -> no position size
        if trade["Signal"] == "HOLD":
            trade["LotSize"] = 0.0
            trade["RiskAmount"] = 0.0
            return trade

        risk_amount = balance * config.RISK_PER_TRADE

        stop_distance = abs(
            trade["Entry"] - trade["StopLoss"]
        )

        if stop_distance <= 0:
            trade["LotSize"] = 0.0
            trade["RiskAmount"] = 0.0
            return trade

        # Simple sizing model for v1.0.
        # We'll validate it against MT5 before placing orders.
        lot_size = risk_amount / stop_distance

        # Round down to broker volume step
        lot_size = round(
            lot_size / volume_step
        ) * volume_step

        # Respect broker limits
        lot_size = max(volume_min, lot_size)
        lot_size = min(volume_max, lot_size)

        trade["LotSize"] = round(lot_size, 2)
        trade["RiskAmount"] = round(risk_amount, 2)

        return trade