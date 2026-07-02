"""
BTC Trend Trader Professional v4
Milestone M3

Execution State

Responsibilities
----------------
- Maintain order execution state
- Track execution metadata
- Store execution statistics

This module performs NO:
- MT5 execution
- Retry logic
- Order management
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Optional


class OrderStatus(str, Enum):
    """
    Order lifecycle.
    """

    NEW = "NEW"

    SENT = "SENT"

    FILLED = "FILLED"

    PARTIAL = "PARTIAL"

    MODIFIED = "MODIFIED"

    CLOSED = "CLOSED"

    FAILED = "FAILED"


@dataclass
class ExecutionState:
    """
    Runtime execution state.

    Stores execution information only.
    """

    order_id: Optional[str] = None

    ticket: Optional[int] = None

    symbol: str = ""

    side: str = ""

    volume: float = 0.0

    requested_price: float = 0.0

    fill_price: float = 0.0

    stop_loss: Optional[float] = None

    take_profit: Optional[float] = None

    slippage: float = 0.0

    retry_count: int = 0

    execution_time_ms: float = 0.0

    status: OrderStatus = OrderStatus.NEW

    opened_at: Optional[datetime] = None

    updated_at: Optional[datetime] = None

    closed_at: Optional[datetime] = None

    last_error: Optional[str] = None

    metadata: Dict = field(default_factory=dict)

    # ---------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------

    def set_status(
        self,
        status: OrderStatus,
    ):

        self.status = status

        self.updated_at = datetime.utcnow()

        if (
            status == OrderStatus.FILLED
            and self.opened_at is None
        ):
            self.opened_at = self.updated_at

        if status == OrderStatus.CLOSED:
            self.closed_at = self.updated_at

    # ---------------------------------------------------

    def record_fill(
        self,
        ticket: int,
        fill_price: float,
        slippage: float = 0.0,
    ):

        self.ticket = ticket

        self.fill_price = fill_price

        self.slippage = slippage

        self.set_status(OrderStatus.FILLED)

    # ---------------------------------------------------

    def record_failure(
        self,
        error: str,
    ):

        self.last_error = error

        self.set_status(OrderStatus.FAILED)

    # ---------------------------------------------------

    def increment_retry(self):

        self.retry_count += 1

        self.updated_at = datetime.utcnow()

    # ---------------------------------------------------

    def update_execution_time(
        self,
        milliseconds: float,
    ):

        self.execution_time_ms = milliseconds

        self.updated_at = datetime.utcnow()

    # ---------------------------------------------------

    def reset(self):

        self.order_id = None

        self.ticket = None

        self.symbol = ""

        self.side = ""

        self.volume = 0.0

        self.requested_price = 0.0

        self.fill_price = 0.0

        self.stop_loss = None

        self.take_profit = None

        self.slippage = 0.0

        self.retry_count = 0

        self.execution_time_ms = 0.0

        self.status = OrderStatus.NEW

        self.opened_at = None

        self.updated_at = None

        self.closed_at = None

        self.last_error = None

        self.metadata.clear()

    # ---------------------------------------------------

    def snapshot(self):
        """
        Export execution state.
        """

        return {

            "order_id": self.order_id,

            "ticket": self.ticket,

            "symbol": self.symbol,

            "side": self.side,

            "volume": self.volume,

            "requested_price": self.requested_price,

            "fill_price": self.fill_price,

            "stop_loss": self.stop_loss,

            "take_profit": self.take_profit,

            "slippage": self.slippage,

            "retry_count": self.retry_count,

            "execution_time_ms": self.execution_time_ms,

            "status": self.status.value,

            "opened_at": (
                self.opened_at.isoformat()
                if self.opened_at
                else None
            ),

            "updated_at": (
                self.updated_at.isoformat()
                if self.updated_at
                else None
            ),

            "closed_at": (
                self.closed_at.isoformat()
                if self.closed_at
                else None
            ),

            "last_error": self.last_error,

            "metadata": dict(self.metadata),
        }