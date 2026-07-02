"""
BTC Trend Trader Professional v4
Paper Trading Session
"""

from __future__ import annotations

from typing import Optional

from paper_trading.paper_account import PaperAccount
from paper_trading.paper_order_book import PaperOrderBook
from paper_trading.paper_trade_executor import PaperTradeExecutor


class PaperSession:
    """
    Coordinates a complete paper trading session.

    This class owns the simulated account,
    order book and trade executor.
    """

    def __init__(
        self,
        account: Optional[PaperAccount] = None,
        order_book: Optional[PaperOrderBook] = None,
    ) -> None:

        self.account = account or PaperAccount()

        self.order_book = order_book or PaperOrderBook()

        self.executor = PaperTradeExecutor(
            account=self.account,
            order_book=self.order_book,
        )

        self.active = False

    def start(self) -> None:
        """
        Start a paper trading session.
        """

        self.active = True

    def stop(self) -> None:
        """
        Stop a paper trading session.
        """

        self.active = False

    def reset(self) -> None:
        """
        Reset session state.
        """

        self.executor.reset()

        self.active = False

    def is_active(self) -> bool:
        """
        Returns True when the session is active.
        """

        return self.active

    def get_executor(self) -> PaperTradeExecutor:
        """
        Return the paper trade executor.
        """

        return self.executor

    def get_account(self) -> PaperAccount:
        """
        Return the simulated account.
        """

        return self.account

    def get_order_book(self) -> PaperOrderBook:
        """
        Return the simulated order book.
        """

        return self.order_book