"""
trade_simulator.py

Trade Simulator v3.4.1

Responsibilities
----------------
- Manage pending orders
- Manage open trades
- Close trades
- Track balance
- Track equity curve
- Calculate PnL
- Prepare for break-even & trailing stop
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


# =========================================================
# Trade Status
# =========================================================

class TradeStatus(Enum):
    PENDING = "PENDING"
    OPEN = "OPEN"
    CLOSED = "CLOSED"


# =========================================================
# Pending Order
# =========================================================

@dataclass
class PendingOrder:
    direction: str
    signal_price: float
    stop_loss: float
    take_profit: float
    lot_size: float
    submit_time: str


# =========================================================
# Simulated Trade
# =========================================================

@dataclass
class SimulatedTrade:

    # -----------------------------
    # Trade Information
    # -----------------------------

    direction: str

    entry_price: float
    stop_loss: float
    take_profit: float

    lot_size: float

    entry_time: str

    # -----------------------------
    # Trade State
    # -----------------------------

    status: TradeStatus = TradeStatus.OPEN

    exit_price: Optional[float] = None
    exit_time: Optional[str] = None

    profit: float = 0.0

    result: Optional[str] = None

    # -----------------------------
    # Trade Management
    # -----------------------------

    initial_stop_loss: Optional[float] = None

    break_even_activated: bool = False

    trailing_stop_activated: bool = False

    highest_price: Optional[float] = None

    lowest_price: Optional[float] = None

    initial_lot_size: float = 0.0

remaining_lot_size: float = 0.0

partial_tp_hits: list = None

partial_exits: list = None

partial_profit: float = 0.0

bars_in_trade: int = 0

entry_bar: int = 0

time_exit_enabled: bool = False

exit_reason: Optional[str] = None


# =========================================================
# Trade Simulator
# =========================================================

class TradeSimulator:

    def __init__(self, starting_balance: float = 10000):

        self.starting_balance = starting_balance
        self.balance = starting_balance

        self.equity_curve = [starting_balance]

        self.pending_trade: Optional[PendingOrder] = None
        self.current_trade: Optional[SimulatedTrade] = None

        self.trade_history = []

    # -----------------------------------------------------

    def has_pending_trade(self):

        return self.pending_trade is not None

    # -----------------------------------------------------

    def has_open_trade(self):

        return self.current_trade is not None

    # -----------------------------------------------------

    def submit_order(
        self,
        direction,
        signal_price,
        stop_loss,
        take_profit,
        lot_size,
        submit_time,
    ):

        if self.pending_trade is not None:
            return False

        if self.current_trade is not None:
            return False

        self.pending_trade = PendingOrder(
            direction=direction,
            signal_price=signal_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            lot_size=lot_size,
            submit_time=submit_time,
        )

        return True

    # -----------------------------------------------------

    def process_pending_order(
        self,
        entry_price,
        entry_time,
    ):

        if self.pending_trade is None:
            return False

        order = self.pending_trade

        self.current_trade = SimulatedTrade(
            direction=order.direction,
            entry_price=entry_price,
            stop_loss=order.stop_loss,
            take_profit=order.take_profit,
            lot_size=order.lot_size,
            entry_time=entry_time,
            status=TradeStatus.OPEN,

            initial_stop_loss=order.stop_loss,

            highest_price=entry_price,

            lowest_price=entry_price,
        )

        self.pending_trade = None

        return True

    # -----------------------------------------------------

    def open_trade(
        self,
        direction,
        entry_price,
        stop_loss,
        take_profit,
        lot_size,
        entry_time,
    ):

        if self.current_trade is not None:
            return False

        self.current_trade = SimulatedTrade(
            direction=direction,
            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            lot_size=lot_size,
            entry_time=entry_time,
            status=TradeStatus.OPEN,

            initial_stop_loss=stop_loss,

            highest_price=entry_price,

            lowest_price=entry_price,
        )

        return True

    # -----------------------------------------------------
    def update_trade(
        self,
        high,
        low,
        close,
        current_time,
    ):

        if self.current_trade is None:
            return None

        trade = self.current_trade

        # ---------------------------------------------
        # Track highest / lowest price reached
        # ---------------------------------------------

        trade.highest_price = max(
            trade.highest_price,
            high,
        )

        trade.lowest_price = min(
            trade.lowest_price,
            low,
        )

        # ---------------------------------------------
        # BUY
        # ---------------------------------------------

        if trade.direction.upper() == "BUY":

            if low <= trade.stop_loss:

                self._close_trade(
                    trade.stop_loss,
                    current_time,
                    "LOSS",
                )

                return "LOSS"

            if high >= trade.take_profit:

                self._close_trade(
                    trade.take_profit,
                    current_time,
                    "WIN",
                )

                return "WIN"

        # ---------------------------------------------
        # SELL
        # ---------------------------------------------

        else:

            if high >= trade.stop_loss:

                self._close_trade(
                    trade.stop_loss,
                    current_time,
                    "LOSS",
                )

                return "LOSS"

            if low <= trade.take_profit:

                self._close_trade(
                    trade.take_profit,
                    current_time,
                    "WIN",
                )

                return "WIN"

        return None

    # -----------------------------------------------------

    def force_close(
        self,
        price,
        current_time,
    ):

        if self.current_trade is None:
            return

        self._close_trade(
            price,
            current_time,
            "FORCED",
        )

    # -----------------------------------------------------

    def _close_trade(
        self,
        exit_price,
        exit_time,
        result,
    ):

        trade = self.current_trade

        trade.exit_price = exit_price
        trade.exit_time = exit_time
        trade.result = result
        trade.status = TradeStatus.CLOSED

        if trade.direction.upper() == "BUY":
            points = exit_price - trade.entry_price
        else:
            points = trade.entry_price - exit_price

        trade.profit = points * trade.lot_size

        self.balance += trade.profit

        self.equity_curve.append(self.balance)

        self.trade_history.append(trade)

        self.current_trade = None

    # -----------------------------------------------------

    def get_balance(self):

        return self.balance

    # -----------------------------------------------------

    def get_trade_history(self):

        return self.trade_history

    # -----------------------------------------------------

    def get_equity_curve(self):

        return self.equity_curve

    # -----------------------------------------------------

    def get_statistics(self):

        total = len(self.trade_history)

        if total == 0:

            return {
                "starting_balance": self.starting_balance,
                "ending_balance": self.balance,
                "net_profit": 0,
                "total_trades": 0,
                "wins": 0,
                "losses": 0,
                "win_rate": 0,
                "equity_curve": self.equity_curve,
            }

        wins = sum(
            1
            for trade in self.trade_history
            if trade.result == "WIN"
        )

        losses = sum(
            1
            for trade in self.trade_history
            if trade.result == "LOSS"
        )

        net_profit = (
            self.balance
            - self.starting_balance
        )

        return {

            "starting_balance": self.starting_balance,

            "ending_balance": self.balance,

            "net_profit": net_profit,

            "total_trades": total,

            "wins": wins,

            "losses": losses,

            "win_rate": round(
                (wins / total) * 100,
                2,
            ),

            "equity_curve": self.equity_curve,

        }