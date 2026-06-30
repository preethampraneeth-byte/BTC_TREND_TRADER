"""
trade_simulator.py

Simulates trade execution during backtesting.

Responsibilities:
- Open simulated trades
- Monitor TP / SL
- Close trades
- Track equity
- Calculate PnL
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

class TradeStatus(Enum):
    PENDING = "PENDING"
    OPEN = "OPEN"
    CLOSED = "CLOSED"


@dataclass
class SimulatedTrade:
    direction: str
    entry_price: float
    stop_loss: float
    take_profit: float
    lot_size: float

    entry_time: str

    status: TradeStatus = TradeStatus.PENDING

    exit_price: Optional[float] = None
    exit_time: Optional[str] = None

    profit: float = 0.0
    result: Optional[str] = None


class TradeSimulator:

    def __init__(self, starting_balance: float = 10000):

        self.starting_balance = starting_balance
        self.balance = starting_balance

        self.current_trade: Optional[SimulatedTrade] = None

        self.trade_history = []

    # ---------------------------------------------------------

    def has_open_trade(self):

        return self.current_trade is not None

    # ---------------------------------------------------------

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
        )

        return True

    # ---------------------------------------------------------

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

        if trade.direction.upper() == "BUY":

            # Stop Loss
            if low <= trade.stop_loss:

                self._close_trade(
                    trade.stop_loss,
                    current_time,
                    "LOSS",
                )

                return "LOSS"

            # Take Profit
            if high >= trade.take_profit:

                self._close_trade(
                    trade.take_profit,
                    current_time,
                    "WIN",
                )

                return "WIN"

        elif trade.direction.upper() == "SELL":

            # Stop Loss
            if high >= trade.stop_loss:

                self._close_trade(
                    trade.stop_loss,
                    current_time,
                    "LOSS",
                )

                return "LOSS"

            # Take Profit
            if low <= trade.take_profit:

                self._close_trade(
                    trade.take_profit,
                    current_time,
                    "WIN",
                )

                return "WIN"

        return None

    # ---------------------------------------------------------

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

    # ---------------------------------------------------------

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

        if trade.direction.upper() == "BUY":

            points = exit_price - trade.entry_price

        else:

            points = trade.entry_price - exit_price

        trade.profit = points * trade.lot_size

        self.balance += trade.profit

        self.trade_history.append(trade)

        self.current_trade = None

    # ---------------------------------------------------------

    def get_balance(self):

        return self.balance

    # ---------------------------------------------------------

    def get_trade_history(self):

        return self.trade_history

    # ---------------------------------------------------------

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
            }

        wins = sum(
            1 for t in self.trade_history
            if t.result == "WIN"
        )

        losses = sum(
            1 for t in self.trade_history
            if t.result == "LOSS"
        )

        net_profit = self.balance - self.starting_balance

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
        }