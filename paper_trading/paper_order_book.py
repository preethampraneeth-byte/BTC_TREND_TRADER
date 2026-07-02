"""
BTC Trend Trader Professional v4
Paper Trading Order Book
"""

from __future__ import annotations

from typing import Dict, List, Optional

from paper_trading.paper_position import PaperPosition


class PaperOrderBook:
    """
    Maintains simulated paper trading positions.
    """

    def __init__(self) -> None:

        self._positions: Dict[int, PaperPosition] = {}

        self._next_ticket = 1

    def create_position(
        self,
        symbol: str,
        direction: str,
        volume: float,
        entry_price: float,
        stop_loss: float,
        take_profit: float,
        entry_time: str,
    ) -> PaperPosition:

        position = PaperPosition(
            ticket=self._next_ticket,
            symbol=symbol,
            direction=direction,
            volume=volume,
            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            entry_time=entry_time,
            current_price=entry_price,
        )

        self._positions[position.ticket] = position

        self._next_ticket += 1

        return position

    def get_position(
        self,
        ticket: int,
    ) -> Optional[PaperPosition]:

        return self._positions.get(ticket)

    def get_open_positions(self) -> List[PaperPosition]:

        return [
            position
            for position in self._positions.values()
            if position.is_open()
        ]

    def get_all_positions(self) -> List[PaperPosition]:

        return list(self._positions.values())

    def close_position(
        self,
        ticket: int,
        price: float,
        exit_time: str,
    ) -> Optional[float]:

        position = self.get_position(ticket)

        if position is None:
            return None

        if not position.is_open():
            return position.realized_profit

        return position.close(
            price=price,
            exit_time=exit_time,
        )

    def update_market_price(
        self,
        symbol: str,
        price: float,
    ) -> None:

        for position in self.get_open_positions():

            if position.symbol == symbol:
                position.update_price(price)

    def clear(self) -> None:

        self._positions.clear()

        self._next_ticket = 1