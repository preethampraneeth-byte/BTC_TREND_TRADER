"""
BTC Trend Trader v3.0
Risk Manager

Calculates position size based on
account balance and risk percentage.
"""


class RiskManager:
    """
    Handles position sizing.
    """

    def calculate_position_size(
        self,
        balance,
        risk_percent,
        entry_price,
        stop_loss,
    ):
        """
        Calculate lot size using fixed-risk model.
        """

        risk_amount = balance * risk_percent

        stop_distance = abs(entry_price - stop_loss)

        if stop_distance == 0:
            return 0.0

        lot_size = risk_amount / stop_distance

        return round(lot_size, 2)