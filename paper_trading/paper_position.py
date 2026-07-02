"""
BTC Trend Trader Professional v4
Paper Trading Position
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Optional


@dataclass
class PaperPosition:
    """
    Represents a simulated open position.
    """

    ticket: int
    symbol: str
    direction: str

    volume: float

    entry_price: float

    stop_loss: float

    take_profit: float

    entry_time: str

    status: str = "OPEN"

    current_price: float = 0.0

    unrealized_profit: float = 0.0

    exit_price: Optional[float] = None

    exit_time: Optional[str] = None

    realized_profit: float = 0.0

    def update_price(
        self,
        price: float,
    ) -> None:
        """
        Update current market price.
        """

        self.current_price = price

        if self.direction.upper() == "BUY":

            self.unrealized_profit = (
                price - self.entry_price
            ) * self.volume

        else:

            self.unrealized_profit = (
                self.entry_price - price
            ) * self.volume

    def close(
        self,
        price: float,
        exit_time: str,
    ) -> float:
        """
        Close the simulated position.
        """

        self.update_price(price)

        self.exit_price = price
        self.exit_time = exit_time

        self.realized_profit = self.unrealized_profit

        self.status = "CLOSED"

        return self.realized_profit

    def is_open(self) -> bool:
        return self.status == "OPEN"

    def snapshot(self) -> Dict:
        return asdict(self)