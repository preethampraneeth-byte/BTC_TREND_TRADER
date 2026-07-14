"""
BTC Trend Trader Professional v4
Paper Trade Executor

Sprint 10.4 Stable
Architecture Refactor Base
"""

from __future__ import annotations

from typing import Any, Dict, List

import csv
import os

import config
from core.risk_manager import RiskManager


class PaperTradeExecutor:
    """
    Executes and manages paper trades.

    Features
    --------
    - Single open position
    - Duplicate candle protection
    - TP monitoring
    - SL monitoring
    - Balance tracking
    - Equity tracking
    - Trade history
    """

    def __init__(self):

        self.starting_balance = config.PAPER_STARTING_BALANCE

        self.balance = self.starting_balance

        self.equity = self.starting_balance

        self.open_trade: Dict[str, Any] | None = None

        self.trade_history: List[Dict[str, Any]] = []

        self.last_trade_time = None

        self.risk_manager = RiskManager()

        os.makedirs(config.LOG_FOLDER, exist_ok=True)

    # -------------------------------------------------

    def execute(
        self,
        signal: str,
        price: float,
        stop_loss: float,
        take_profit: float,
        lot_size: float,
        timestamp,
    ) -> bool:

        if self.last_trade_time == timestamp:
            return False

        if self.open_trade is not None:
            return False

        self.open_trade = {

            "signal": signal,

            "entry_price": float(price),

            "stop_loss": float(stop_loss),

            "initial_stop_loss": float(stop_loss),

            "take_profit": float(take_profit),

            "lot_size": float(lot_size),

            "initial_lot_size": float(lot_size),

            "remaining_lot_size": float(lot_size),

            "entry_time": timestamp,

            "exit_price": None,

            "exit_time": None,

            "profit": 0.0,

            "status": "OPEN",

            "result": None,

            "break_even_activated": False,

            "trailing_stop_activated": False,

            "highest_price": float(price),

            "lowest_price": float(price),

            "partial_tp_hits": [
                False
                for _ in config.PARTIAL_TP_LEVELS
            ],

            "partial_exits": [],

            "partial_profit": 0.0,

            "bars_in_trade": 0,

            "entry_bar": 0,

            "time_exit_enabled": config.ENABLE_TIME_EXIT,

            "exit_reason": None,

        }

        self.last_trade_time = timestamp

        return True

    # -------------------------------------------------

    def update(
        self,
        high: float,
        low: float,
        close: float,
        timestamp,
        atr: float | None = None,
    ):

        if self.open_trade is None:
            self.equity = self.balance
            return None

        trade = self.open_trade

        signal = trade["signal"]

        trade["bars_in_trade"] += 1

        # 1. Break-even
        self._update_break_even(trade, high, low, signal)

        # 2. ATR Trailing
        self._update_trailing_stop(trade, high, low, atr, signal)

        # 3. Partial Profit
        self._update_partial_profit(trade, high, low, timestamp, signal)

        # 4. Normal Exit

        exit_price = self._check_exit_conditions(
            trade,
            high,
            low,
            signal,
        )

        # 5. Time Exit

        if exit_price is None:

            exit_price = self._check_time_exit(
                trade,
                close,
            )

        # 6. Floating Equity
        self._update_equity(trade, close, signal)

        # Still Open
        if exit_price is None:
            return None

        # 7. Close Trade
        return self._close_trade(trade, exit_price, timestamp, signal)

    # -------------------------------------------------

    def _update_break_even(self, trade, high, low, signal):

        #
        # Break-even Management
        #

        if (
            config.ENABLE_BREAK_EVEN
            and not trade["break_even_activated"]
        ):

            initial_risk = abs(
                trade["entry_price"]
                - trade["initial_stop_loss"]
            )

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

            if new_stop != trade["stop_loss"]:

                trade["stop_loss"] = new_stop

                trade["break_even_activated"] = True

                print()

                print("✓ Break-even activated")

                print(
                    f"Trigger Price : "
                    f"{trigger_price:.2f}"
                )

                print(
                    f"Entry Price   : "
                    f"{trade['entry_price']:.2f}"
                )

                print(
                    f"New Stop Loss : "
                    f"{new_stop:.2f}"
                )

    # -------------------------------------------------

    def _update_trailing_stop(self, trade, high, low, atr, signal):

        #
        # ATR Trailing Stop Management
        #

        trade["highest_price"] = max(
            trade["highest_price"],
            float(high),
        )

        trade["lowest_price"] = min(
            trade["lowest_price"],
            float(low),
        )

        if (
            config.ENABLE_TRAILING_STOP
            and atr is not None
        ):

            initial_risk = abs(
                trade["entry_price"]
                - trade["initial_stop_loss"]
            )

            trail_distance = (
                float(atr)
                * config.TRAILING_STOP_ATR
            )

            if (
                initial_risk > 0
                and trail_distance > 0
            ):

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

                if trailing_ready:

                    new_stop = self.risk_manager.calculate_trailing_stop(

                        current_stop=trade["stop_loss"],

                        current_price=trailing_price,

                        trail_distance=trail_distance,

                        side=signal,

                    )

                    if new_stop != trade["stop_loss"]:

                        trade["stop_loss"] = new_stop

                        trade["trailing_stop_activated"] = True

                        print()

                        print("Trailing stop updated")

                        print(
                            f"Trigger Price : "
                            f"{trigger_price:.2f}"
                        )

                        print(
                            f"Trail Price   : "
                            f"{trailing_price:.2f}"
                        )

                        print(
                            f"ATR Distance  : "
                            f"{trail_distance:.2f}"
                        )

                        print(
                            f"New Stop Loss : "
                            f"{new_stop:.2f}"
                        )

    # -------------------------------------------------

    def _update_partial_profit(self, trade, high, low, timestamp, signal):

        #
        # Partial Profit Taking
        #

        if config.ENABLE_PARTIAL_TP:

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

                if signal == "BUY":

                    partial_price = (
                        trade["entry_price"]
                        + (
                            initial_risk
                            * level
                        )
                    )

                    partial_hit = high >= partial_price

                else:

                    partial_price = (
                        trade["entry_price"]
                        - (
                            initial_risk
                            * level
                        )
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

                self.balance += partial_profit

                trade["partial_exits"].append(
                    {
                        "level": float(level),
                        "percentage": float(
                            config.PARTIAL_TP_PERCENTAGES[index]
                        ),
                        "exit_price": partial_price,
                        "lot_size": close_lot,
                        "profit": partial_profit,
                        "exit_time": timestamp,
                    }
                )

                print()

                print("Partial profit taken")

                print(
                    f"Level       : "
                    f"{level:.2f}R"
                )

                print(
                    f"Exit Price  : "
                    f"{partial_price:.2f}"
                )

                print(
                    f"Closed Lot  : "
                    f"{close_lot:.2f}"
                )

                print(
                    f"Remaining   : "
                    f"{trade['lot_size']:.2f}"
                )

                print(
                    f"Profit      : "
                    f"{partial_profit:.2f}"
                )

    # -------------------------------------------------

    def _check_time_exit(self, trade, close):

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

        print()

        print("Time Exit triggered")

        print(
            f"Bars Held  : "
            f"{trade['bars_in_trade']}"
        )

        print(
            f"Exit Price : "
            f"{close:.2f}"
        )

        return float(close)

    # -------------------------------------------------

    def _check_exit_conditions(self, trade, high, low, signal):

        exit_price = None

        #
        # BUY
        #

        if trade["lot_size"] <= 0:

            exit_price = trade["partial_exits"][-1]["exit_price"]

        elif signal == "BUY":

            if low <= trade["stop_loss"]:

                exit_price = trade["stop_loss"]

            elif high >= trade["take_profit"]:

                exit_price = trade["take_profit"]

        #
        # SELL
        #

        else:

            if high >= trade["stop_loss"]:

                exit_price = trade["stop_loss"]

            elif low <= trade["take_profit"]:

                exit_price = trade["take_profit"]

        return exit_price

    # -------------------------------------------------

    def _update_equity(self, trade, close, signal):

        #
        # Floating Equity
        #
        if signal == "BUY":

            floating = (
                close - trade["entry_price"]
            ) * trade["lot_size"]

        else:

            floating = (
                trade["entry_price"] - close
            ) * trade["lot_size"]

        self.equity = self.balance + floating

    # -------------------------------------------------

    def _close_trade(self, trade, exit_price, timestamp, signal):

        #
        # Close Trade
        #

        if signal == "BUY":

            closing_profit = (
                exit_price - trade["entry_price"]
            ) * trade["lot_size"]

        else:

            closing_profit = (
                trade["entry_price"] - exit_price
            ) * trade["lot_size"]

        profit = trade["profit"] + closing_profit

        trade["exit_price"] = exit_price

        trade["exit_time"] = timestamp

        trade["profit"] = profit

        trade["remaining_lot_size"] = 0.0

        trade["lot_size"] = 0.0

        trade["status"] = "CLOSED"

        if profit > 0:

            trade["result"] = "WIN"

        elif profit < 0:

            trade["result"] = "LOSS"

        else:

            trade["result"] = "BREAKEVEN"

        self.balance += closing_profit

        self.equity = self.balance

        self.trade_history.append(trade.copy())

        self.log_trade_to_csv(trade)

        self.open_trade = None

        return trade

    # -------------------------------------------------

    def has_open_trade(self) -> bool:

        return self.open_trade is not None

    # -------------------------------------------------

    def get_open_trades(self):

        if self.open_trade is None:
            return []

        return [self.open_trade.copy()]

    # -------------------------------------------------

    def get_trade_history(self):

        return list(self.trade_history)

    # -------------------------------------------------

    def get_balance(self):

        return self.balance

    # -------------------------------------------------

    def get_equity(self):

        return self.equity


    # -------------------------------------------------

    def get_statistics(self):

        profits = [

            trade["profit"]

            for trade in self.trade_history

        ]

        wins = [

            p

            for p in profits

            if p > 0

        ]

        losses = [

            p

            for p in profits

            if p < 0

        ]

        gross_profit = sum(wins)

        gross_loss = abs(sum(losses))

        total_trades = len(profits)

        net_profit = self.balance - self.starting_balance

        return {

            "starting_balance": self.starting_balance,

            "ending_balance": self.balance,

            "equity": self.equity,

            "net_profit": net_profit,

            "total_trades": total_trades,

            "wins": len(wins),

            "losses": len(losses),

            "win_rate": (

                round((len(wins) / total_trades) * 100, 2)

                if total_trades

                else 0.0

            ),

            "gross_profit": gross_profit,

            "gross_loss": gross_loss,

            "profit_factor": (

                round(gross_profit / gross_loss, 2)

                if gross_loss > 0

                else 0.0

            ),

            "average_win": (

                round(gross_profit / len(wins), 2)

                if wins

                else 0.0

            ),

            "average_loss": (

                round(gross_loss / len(losses), 2)

                if losses

                else 0.0

            ),

            "largest_win": max(wins) if wins else 0.0,

            "largest_loss": min(losses) if losses else 0.0,

        }

    # -------------------------------------------------

    def print_summary(self):

        stats = self.get_statistics()

        print()

        print("=" * 60)

        print("PAPER TRADING SESSION SUMMARY")

        print("=" * 60)

        print(f"Starting Balance : {stats['starting_balance']:.2f}")

        print(f"Ending Balance   : {stats['ending_balance']:.2f}")

        print(f"Net Profit       : {stats['net_profit']:.2f}")

        print(f"Total Trades     : {stats['total_trades']}")

        print(f"Wins             : {stats['wins']}")

        print(f"Losses           : {stats['losses']}")

        print(f"Win Rate         : {stats['win_rate']:.2f}%")

        print(f"Gross Profit     : {stats['gross_profit']:.2f}")

        print(f"Gross Loss       : {stats['gross_loss']:.2f}")

        print(f"Profit Factor    : {stats['profit_factor']}")

        print(f"Average Win      : {stats['average_win']:.2f}")

        print(f"Average Loss     : {stats['average_loss']:.2f}")

        print(f"Largest Win      : {stats['largest_win']:.2f}")

        print(f"Largest Loss     : {stats['largest_loss']:.2f}")

        print("=" * 60)

        # -------------------------------------------------

    def log_trade_to_csv(self, trade):

        if not config.LOG_TO_CSV:
            return

        file_exists = os.path.exists(config.TRADE_LOG)

        with open(
            config.TRADE_LOG,
            "a",
            newline="",
            encoding="utf-8",
        ) as csvfile:

            writer = csv.writer(csvfile)

            if not file_exists:

                writer.writerow([
                    "Entry Time",
                    "Exit Time",
                    "Signal",
                    "Entry Price",
                    "Exit Price",
                    "Initial Lot",
                    "Remaining Lot",
                    "Stop Loss",
                    "Take Profit",
                    "Break-even",
                    "Trailing",
                    "Partial Count",
                    "Partial Profit",
                    "Total Profit",
                    "Result",
                    "Balance",
                ])

            writer.writerow([
                trade["entry_time"],
                trade["exit_time"],
                trade["signal"],
                round(trade["entry_price"], 2),
                round(trade["exit_price"], 2),
                round(trade["initial_lot_size"], 4),
                round(trade["remaining_lot_size"], 4),
                round(trade["stop_loss"], 2),
                round(trade["take_profit"], 2),
                trade["break_even_activated"],
                trade["trailing_stop_activated"],
                len(trade["partial_exits"]),
                round(trade["partial_profit"], 2),
                round(trade["profit"], 2),
                trade["result"],
                round(self.balance, 2),
            ])

    # -------------------------------------------------

    def reset(self):

        self.balance = self.starting_balance

        self.equity = self.starting_balance

        self.open_trade = None

        self.trade_history.clear()

        self.last_trade_time = None
