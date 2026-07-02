"""
BTC Trend Trader Professional v4
Milestone M3

Execution Audit

Responsibilities
----------------
- Store execution history
- Track retries
- Track execution time
- Track slippage
- Export execution records

This module performs NO:
- MT5 execution
- Trade management
- Risk calculations
"""

from __future__ import annotations

from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class ExecutionRecord:
    """
    Immutable execution record.
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

    status: str = ""

    message: str = ""

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )


class ExecutionAudit:
    """
    Stores execution history.

    One instance may be shared across the engine.
    """

    def __init__(self):

        self._records: List[ExecutionRecord] = []

    # ----------------------------------------------------
    # Recording
    # ----------------------------------------------------

    def record(
        self,
        *,
        order_id=None,
        ticket=None,
        symbol="",
        side="",
        volume=0.0,
        requested_price=0.0,
        fill_price=0.0,
        stop_loss=None,
        take_profit=None,
        slippage=0.0,
        retry_count=0,
        execution_time_ms=0.0,
        status="",
        message="",
    ) -> ExecutionRecord:
        """
        Store execution record.
        """

        record = ExecutionRecord(
            order_id=order_id,
            ticket=ticket,
            symbol=symbol,
            side=side,
            volume=volume,
            requested_price=requested_price,
            fill_price=fill_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            slippage=slippage,
            retry_count=retry_count,
            execution_time_ms=execution_time_ms,
            status=status,
            message=message,
        )

        self._records.append(record)

        return record

    # ----------------------------------------------------
    # Queries
    # ----------------------------------------------------

    def all(self) -> List[ExecutionRecord]:
        """
        Return all execution records.
        """

        return list(self._records)

    def latest(self) -> Optional[ExecutionRecord]:
        """
        Return latest record.
        """

        if not self._records:
            return None

        return self._records[-1]

    def by_ticket(
        self,
        ticket: int,
    ) -> List[ExecutionRecord]:
        """
        Find records by MT5 ticket.
        """

        return [
            record
            for record in self._records
            if record.ticket == ticket
        ]

    def by_order(
        self,
        order_id: str,
    ) -> List[ExecutionRecord]:
        """
        Find records by order id.
        """

        return [
            record
            for record in self._records
            if record.order_id == order_id
        ]

    def successful(self) -> List[ExecutionRecord]:
        """
        Return successful executions.
        """

        return [
            record
            for record in self._records
            if record.status.upper()
            in (
                "FILLED",
                "CLOSED",
                "PARTIAL",
                "MODIFIED",
            )
        ]

    def failed(self) -> List[ExecutionRecord]:
        """
        Return failed executions.
        """

        return [
            record
            for record in self._records
            if record.status.upper() == "FAILED"
        ]

    # ----------------------------------------------------
    # Statistics
    # ----------------------------------------------------

    def execution_count(self) -> int:

        return len(self._records)

    def average_slippage(self) -> float:

        if not self._records:
            return 0.0

        values = [
            r.slippage
            for r in self._records
        ]

        return sum(values) / len(values)

    def average_execution_time(self) -> float:

        if not self._records:
            return 0.0

        values = [
            r.execution_time_ms
            for r in self._records
        ]

        return sum(values) / len(values)

    def total_retries(self) -> int:

        return sum(
            r.retry_count
            for r in self._records
        )

    # ----------------------------------------------------
    # Export
    # ----------------------------------------------------

    def snapshot(self) -> List[Dict]:
        """
        Export audit history.
        """

        output = []

        for record in self._records:

            item = asdict(record)

            item["timestamp"] = (
                record.timestamp.isoformat()
            )

            output.append(item)

        return output

    # ----------------------------------------------------
    # Reset
    # ----------------------------------------------------

    def clear(self):

        self._records.clear()