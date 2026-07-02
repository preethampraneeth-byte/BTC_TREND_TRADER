"""
BTC Trend Trader Professional v4
Paper Trading Engine
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from paper_trading.paper_session import PaperSession


class PaperEngine:
    """
    Coordinates paper trading execution.

    Responsibilities
    ----------------
    - Receive strategy signals
    - Execute simulated trades
    - Update paper account
    - Maintain paper positions

    This engine NEVER communicates with MT5.
    """

    def __init__(
        self,
        session: Optional[PaperSession] = None,
    ) -> None:

        self.session = session or PaperSession()

        self.executor = self.session.get_executor()

        self._history: List[Any] = []

    # ---------------------------------------------------------

    def start(self) -> None:

        self.session.start()

    # ---------------------------------------------------------

    def stop(self) -> None:

        self.session.stop()

    # ---------------------------------------------------------

    def process_signal(
        self,
        signal: Dict[str, Any],
    ) -> bool:
        """
        Execute one strategy signal.

        Expected keys:

            symbol
            direction
            volume
            entry_price
            stop_loss
            take_profit
            entry_time
        """

        if not self.session.is_active():
            return False

        position = self.executor.open_position(
            symbol=signal["symbol"],
            direction=signal["direction"],
            volume=signal["volume"],
            entry_price=signal["entry_price"],
            stop_loss=signal["stop_loss"],
            take_profit=signal["take_profit"],
            entry_time=signal["entry_time"],
        )

        if position is None:
            return False

        self._history.append(position)

        return True

    # ---------------------------------------------------------

    def update_price(
        self,
        symbol: str,
        price: float,
    ) -> None:

        self.executor.update_market_price(
            symbol,
            price,
        )

    # ---------------------------------------------------------

    def close_position(
        self,
        ticket: int,
        price: float,
        exit_time: str,
    ) -> bool:

        return self.executor.close_position(
            ticket=ticket,
            exit_price=price,
            exit_time=exit_time,
        )

    # ---------------------------------------------------------

    def account(self):

        return self.executor.get_account()

    # ---------------------------------------------------------

    def open_positions(self):

        return self.executor.get_open_positions()

    # ---------------------------------------------------------

    def history(self):

        return list(self._history)

    # ---------------------------------------------------------

    def reset(self) -> None:

        self.executor.reset()

        self._history.clear()