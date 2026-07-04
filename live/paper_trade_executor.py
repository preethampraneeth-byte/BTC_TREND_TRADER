"""
BTC Trend Trader Professional v4
Paper Trade Executor

Sprint 9.1
"""

from __future__ import annotations

from typing import Any, Dict, List

import config


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

            "take_profit": float(take_profit),

            "lot_size": float(lot_size),

            "entry_time": timestamp,

            "exit_price": None,

            "exit_time": None,

            "profit": 0.0,

            "status": "OPEN",

            "result": None,

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
    ):

        if self.open_trade is None:
            self.equity = self.balance
            return None

        trade = self.open_trade

        signal = trade["signal"]

        exit_price = None

        result = None

        #
        # BUY
        #

        if signal == "BUY":

            if low <= trade["stop_loss"]:

                exit_price = trade["stop_loss"]

                result = "LOSS"

            elif high >= trade["take_profit"]:

                exit_price = trade["take_profit"]

                result = "WIN"

        #
        # SELL
        #

        else:

            if high >= trade["stop_loss"]:

                exit_price = trade["stop_loss"]

                result = "LOSS"

            elif low <= trade["take_profit"]:

                exit_price = trade["take_profit"]

                result = "WIN"

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

        #
        # Still Open
        #

        if exit_price is None:
            return None

        #
        # Close Trade
        #

        if signal == "BUY":

            profit = (
                exit_price - trade["entry_price"]
            ) * trade["lot_size"]

        else:

            profit = (
                trade["entry_price"] - exit_price
            ) * trade["lot_size"]

        trade["exit_price"] = exit_price

        trade["exit_time"] = timestamp

        trade["profit"] = profit

        trade["status"] = "CLOSED"

        trade["result"] = result

        self.balance += profit

        self.equity = self.balance

        self.trade_history.append(trade.copy())

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

    def reset(self):

        self.balance = self.starting_balance

        self.equity = self.starting_balance

        self.open_trade = None

        self.trade_history.clear()

        self.last_trade_time = None