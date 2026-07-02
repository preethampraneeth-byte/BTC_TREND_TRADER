"""
BTC Trend Trader Professional v4
Paper Trading Account
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class PaperAccount:
    """
    Simulated trading account for paper trading.
    """

    starting_balance: float = 10000.0
    balance: float = 10000.0
    equity: float = 10000.0
    margin: float = 0.0
    free_margin: float = 10000.0
    unrealized_profit: float = 0.0
    realized_profit: float = 0.0

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            return

        self.balance += amount
        self.equity += amount
        self.free_margin += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            return

        if amount > self.balance:
            return

        self.balance -= amount
        self.equity -= amount
        self.free_margin = max(
            0.0,
            self.free_margin - amount,
        )

    def apply_profit(self, profit: float) -> None:
        self.realized_profit += profit
        self.balance += profit
        self.equity = self.balance + self.unrealized_profit
        self.free_margin = self.equity - self.margin

    def update_unrealized(self, profit: float) -> None:
        self.unrealized_profit = profit
        self.equity = self.balance + profit
        self.free_margin = self.equity - self.margin

    def reserve_margin(self, margin: float) -> bool:
        if margin <= 0:
            return True

        if margin > self.free_margin:
            return False

        self.margin += margin
        self.free_margin -= margin
        return True

    def release_margin(self, margin: float) -> None:
        if margin <= 0:
            return

        self.margin = max(
            0.0,
            self.margin - margin,
        )

        self.free_margin = self.equity - self.margin

    def reset(self) -> None:
        self.balance = self.starting_balance
        self.equity = self.starting_balance
        self.margin = 0.0
        self.free_margin = self.starting_balance
        self.unrealized_profit = 0.0
        self.realized_profit = 0.0

    def snapshot(self) -> Dict:
        return asdict(self)
