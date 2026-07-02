"""
BTC Trend Trader Professional v4
Paper Trade Executor
"""

from __future__ import annotations

from typing import Optional

from paper_trading.paper_account import PaperAccount
from paper_trading.paper_order_book import PaperOrderBook
from paper_trading.paper_position import PaperPosition


class PaperTradeExecutor:
    """
    Executes simulated trades without sending
    orders to MetaTrader 5.
    """

    def __init__(
        self,
        account: Optional[PaperAccount] = None,
        order_book: Optional[PaperOrderBook] = None,
    ) -> None:

        self.account = account or PaperAccount()

        self.order_book = order_book or PaperOrderBook()

    def open_position(
        self,
        symbol: str,
        direction: str,
        volume: float,
        entry_price: float,
        stop_loss: float,
        take_profit: float,
        entry_time: str,
        margin: float = 0.0,
    ) -> Optional[PaperPosition]:

        if not self.account.reserve_margin(margin):
            return None

        return self.order_book.create_position(
            symbol=symbol,
            direction=direction,
            volume=volume,
            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            entry_time=entry_time,
        )

    def update_market_price(
        self,
        symbol: str,
        price: float,
    ) -> None:

        self.order_book.update_market_price(
            symbol,
            price,
        )

        unrealized = 0.0

        for position in self.order_book.get_open_positions():

            unrealized += position.unrealized_profit

        self.account.update_unrealized(
            unrealized,
        )

    def close_position(
        self,
        ticket: int,
        exit_price: float,
        exit_time: str,
        margin: float = 0.0,
    ) -> bool:

        profit = self.order_book.close_position(
            ticket=ticket,
            price=exit_price,
            exit_time=exit_time,
        )

        if profit is None:
            return False

        self.account.release_margin(
            margin,
        )

        self.account.apply_profit(
            profit,
        )

        return True

    def get_account(self) -> PaperAccount:

        return self.account

    def get_open_positions(self):

        return self.order_book.get_open_positions()

    def get_all_positions(self):

        return self.order_book.get_all_positions()

    def reset(self) -> None:

        self.order_book.clear()

        self.account.reset()