"""
BTC Trend Trader Professional v4
Trade Management Service

Shared trade-management logic for all execution modes.

Responsibilities
----------------
- Break-even management
- Trailing stop management
- Partial profit management
- Time exit evaluation

This service does NOT:
- Execute trades
- Maintain balances
- Submit orders
- Calculate position size
"""

from __future__ import annotations

import config


class TradeManagementService:
    """
    Shared trade-management service.

    Both the backtester and paper trader will use this
    service so that trade-management behaviour remains
    consistent across execution modes.
    """

    def __init__(self, risk_manager):

        self.risk_manager = risk_manager

    # -------------------------------------------------

    def update_break_even(self, trade, high, low):

        if (
            not config.ENABLE_BREAK_EVEN
            or trade["break_even_activated"]
        ):
            return False

        initial_risk = abs(
            trade["entry_price"]
            - trade["initial_stop_loss"]
        )

        signal = trade["signal"]

        if signal == "BUY":

            trigger_price = (
                trade["entry_price"]
                + (
                    initial_risk
                    * config.BREAK_EVEN_R
                )
            )

            current_price = high

        else:

            trigger_price = (
                trade["entry_price"]
                - (
                    initial_risk
                    * config.BREAK_EVEN_R
                )
            )

            current_price = low

        new_stop = self.risk_manager.calculate_break_even_stop(
            entry_price=trade["entry_price"],
            current_stop=trade["stop_loss"],
            current_price=current_price,
            side=signal,
            trigger_price=trigger_price,
            lock_in=config.BREAK_EVEN_OFFSET,
        )

        if new_stop == trade["stop_loss"]:
            return False

        trade["stop_loss"] = new_stop
        trade["break_even_activated"] = True

        return True

    # -------------------------------------------------

    def update_trailing_stop(self, trade, high, low, atr):

        trade["highest_price"] = max(
            trade["highest_price"],
            float(high),
        )

        trade["lowest_price"] = min(
            trade["lowest_price"],
            float(low),
        )

        if (
            not config.ENABLE_TRAILING_STOP
            or atr is None
        ):
            return False

        initial_risk = abs(
            trade["entry_price"]
            - trade["initial_stop_loss"]
        )

        trail_distance = (
            float(atr)
            * config.TRAILING_STOP_ATR
        )

        if (
            initial_risk <= 0
            or trail_distance <= 0
        ):
            return False

        signal = trade["signal"]

        if signal == "BUY":

            trigger_price = (
                trade["entry_price"]
                + (
                    initial_risk
                    * config.TRAILING_START_R
                )
            )

            trailing_price = trade["highest_price"]

            trailing_ready = (
                trailing_price >= trigger_price
            )

        else:

            trigger_price = (
                trade["entry_price"]
                - (
                    initial_risk
                    * config.TRAILING_START_R
                )
            )

            trailing_price = trade["lowest_price"]

            trailing_ready = (
                trailing_price <= trigger_price
            )

        if not trailing_ready:
            return False

        new_stop = self.risk_manager.calculate_trailing_stop(
            current_stop=trade["stop_loss"],
            current_price=trailing_price,
            trail_distance=trail_distance,
            side=signal,
        )

        if new_stop == trade["stop_loss"]:
            return False

        trade["stop_loss"] = new_stop
        trade["trailing_stop_activated"] = True

        return True

    # -------------------------------------------------

    def update_partial_profit(
        self,
        trade,
        high,
        low,
        timestamp,
    ):

        if not config.ENABLE_PARTIAL_TP:
            return None

        initial_risk = abs(
            trade["entry_price"]
            - trade["initial_stop_loss"]
        )

        for index, level in enumerate(config.PARTIAL_TP_LEVELS):

            if index >= len(config.PARTIAL_TP_PERCENTAGES):
                continue

            if index >= len(trade["partial_tp_hits"]):
                continue

            if trade["partial_tp_hits"][index]:
                continue

            if trade["lot_size"] <= 0:
                continue

            if initial_risk <= 0:
                continue

            signal = trade["signal"]

            if signal == "BUY":

                partial_price = (
                    trade["entry_price"]
                    + initial_risk * level
                )

                partial_hit = high >= partial_price

            else:

                partial_price = (
                    trade["entry_price"]
                    - initial_risk * level
                )

                partial_hit = low <= partial_price

            if not partial_hit:
                continue

            close_lot = (
                trade["initial_lot_size"]
                * (
                    config.PARTIAL_TP_PERCENTAGES[index]
                    / 100
                )
            )

            close_lot = min(
                close_lot,
                trade["lot_size"],
            )

            if close_lot <= 0:
                continue

            if signal == "BUY":

                partial_profit = (
                    partial_price
                    - trade["entry_price"]
                ) * close_lot

            else:

                partial_profit = (
                    trade["entry_price"]
                    - partial_price
                ) * close_lot

            trade["lot_size"] -= close_lot

            if trade["lot_size"] < 0:
                trade["lot_size"] = 0.0

            trade["remaining_lot_size"] = trade["lot_size"]

            trade["partial_tp_hits"][index] = True

            trade["partial_profit"] += partial_profit

            trade["profit"] += partial_profit

            partial_exit = {
                "level": float(level),
                "percentage": float(
                    config.PARTIAL_TP_PERCENTAGES[index]
                ),
                "exit_price": partial_price,
                "lot_size": close_lot,
                "profit": partial_profit,
                "exit_time": timestamp,
            }

            trade["partial_exits"].append(
                partial_exit
            )

            return {
                "level": level,
                "exit_price": partial_price,
                "close_lot": close_lot,
                "profit": partial_profit,
            }

        return None

    # -------------------------------------------------

    def check_time_exit(
        self,
        trade,
        close,
    ):

        if not config.ENABLE_TIME_EXIT:
            return None

        if not trade["time_exit_enabled"]:
            return None

        if trade["break_even_activated"]:
            return None

        if trade["trailing_stop_activated"]:
            return None

        if trade["bars_in_trade"] < config.MAX_BARS_IN_TRADE:
            return None

        trade["exit_reason"] = "TIME_EXIT"

        return float(close)