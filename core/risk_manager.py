"""
BTC Trend Trader v4.0
Risk Manager

Responsible for risk calculations only.

Responsibilities
----------------
- Position sizing
- Stop loss validation
- Break-even calculation
- Trailing stop calculation

This module does NOT:
- Maintain trade state
- Execute orders
- Track statistics
"""

from typing import Optional


class RiskManager:
    """
    Handles risk-related calculations.
    """

    def calculate_position_size(
        self,
        balance,
        risk_percent,
        entry_price,
        stop_loss,
    ):
        """
        Calculate position size using a fixed-risk model.

        Backward compatible with previous versions.
        """

        risk_amount = balance * risk_percent

        stop_distance = abs(entry_price - stop_loss)

        if stop_distance == 0:
            return 0.0

        lot_size = risk_amount / stop_distance

        return round(lot_size, 2)

    def calculate_break_even_stop(
        self,
        entry_price: float,
        current_stop: float,
        current_price: float,
        side: str,
        trigger_price: Optional[float] = None,
        lock_in: float = 0.0,
    ) -> float:
        """
        Calculate a break-even stop.

        Returns the new stop if the trigger has been reached,
        otherwise returns the existing stop.

        This method performs no trade management.
        """

        side = side.upper()

        if trigger_price is None:
            trigger_price = entry_price

        if side == "BUY":
            if current_price >= trigger_price:
                return max(current_stop, entry_price + lock_in)
            return current_stop

        if current_price <= trigger_price:
            return min(current_stop, entry_price - lock_in)

        return current_stop

    def calculate_trailing_stop(
        self,
        current_stop: float,
        current_price: float,
        trail_distance: float,
        side: str,
    ) -> float:
        """
        Calculate a trailing stop.

        Returns the updated stop while never loosening
        the existing stop.
        """

        if trail_distance <= 0:
            return current_stop

        side = side.upper()

        if side == "BUY":
            proposed = current_price - trail_distance
            return max(current_stop, proposed)

        proposed = current_price + trail_distance
        return min(current_stop, proposed)

    def validate_stop_loss(
        self,
        entry_price: float,
        stop_loss: float,
        side: str,
    ) -> bool:
        """
        Validate stop placement.
        """

        side = side.upper()

        if side == "BUY":
            return stop_loss < entry_price

        return stop_loss > entry_price

    def calculate_risk_amount(
        self,
        balance: float,
        risk_percent: float,
    ) -> float:
        """
        Calculate currency risk amount.
        """

        return balance * risk_percent

    def calculate_reward_risk_ratio(
        self,
        entry_price: float,
        stop_loss: float,
        target_price: float,
        side: str,
    ) -> float:
        """
        Calculate reward-to-risk ratio.
        """

        risk = abs(entry_price - stop_loss)

        if risk == 0:
            return 0.0

        side = side.upper()

        if side == "BUY":
            reward = target_price - entry_price
        else:
            reward = entry_price - target_price

        return reward / risk