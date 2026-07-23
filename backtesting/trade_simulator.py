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
from core.risk_manager import RiskManager
from core.trade_management_service import TradeManagementService

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

        self.risk_manager = RiskManager()

        self.trade_management = TradeManagementService(
            self.risk_manager
        )

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

            initial_lot_size=order.lot_size,

            remaining_lot_size=order.lot_size,

            partial_tp_hits=[],

            partial_exits=[],

            partial_profit=0.0,

            bars_in_trade=0,

            entry_bar=0,

            time_exit_enabled=False,

            exit_reason=None,
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

            initial_lot_size=lot_size,

            remaining_lot_size=lot_size,

            partial_tp_hits=[],

            partial_exits=[],

            partial_profit=0.0,

            bars_in_trade=0,

            entry_bar=0,

            time_exit_enabled=False,

            exit_reason=None,
            )

        return True

    def _trade_to_dict(self, trade):
        return {
            "signal": trade.direction,
            "entry_price": trade.entry_price,
            "stop_loss": trade.stop_loss,
            "initial_stop_loss": trade.initial_stop_loss,
            "take_profit": trade.take_profit,
            "lot_size": trade.lot_size,
            "initial_lot_size": trade.initial_lot_size,
            "remaining_lot_size": trade.remaining_lot_size,
            "break_even_activated": trade.break_even_activated,
            "highest_price": trade.highest_price,
            "lowest_price": trade.lowest_price,
            "partial_tp_hits": trade.partial_tp_hits,
            "partial_exits": trade.partial_exits,
            "partial_profit": trade.partial_profit,
            "bars_in_trade": trade.bars_in_trade,
            "entry_bar": trade.entry_bar,
            "time_exit_enabled": trade.time_exit_enabled,
            "exit_reason": trade.exit_reason,
        }

    def _update_trade_from_dict(self, trade, trade_dict):
        trade.stop_loss = trade_dict["stop_loss"]
        trade.break_even_activated = trade_dict["break_even_activated"]
        trade.highest_price = trade_dict["highest_price"]
        trade.lowest_price = trade_dict["lowest_price"]
        trade.remaining_lot_size = trade_dict["remaining_lot_size"]
        trade.partial_tp_hits = trade_dict["partial_tp_hits"]
        trade.partial_exits = trade_dict["partial_exits"]
        trade.partial_profit = trade_dict["partial_profit"]
        trade.bars_in_trade = trade_dict["bars_in_trade"]
        trade.entry_bar = trade_dict["entry_bar"]
        trade.time_exit_enabled = trade_dict["time_exit_enabled"]
        trade.exit_reason = trade_dict["exit_reason"]

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

        trade.bars_in_trade += 1

        trade_dict = self._trade_to_dict(trade)

        self._update_trade_from_dict(
            trade,
            trade_dict,
        )

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
        trade.exit_reason = result

        if trade.direction.upper() == "BUY":
            points = exit_price - trade.entry_price
        else:
            points = trade.entry_price - exit_price

        trade.profit = points * trade.lot_size

        trade.remaining_lot_size = 0.0

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