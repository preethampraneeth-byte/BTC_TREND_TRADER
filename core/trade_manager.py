"""
BTC Trend Trader
Version 4.0

Trade Manager

This module maintains the complete state of an active trade.

Version 4.0 (Milestone M2)
--------------------------
✓ Active trade lifecycle
✓ Trade identity
✓ Metadata
✓ Position tracking
✓ Partial exit history
✓ Trade statistics
✓ Trade events
✓ Multi-TP tracking
✓ Enhanced summary

Responsibilities
----------------
TradeManager is responsible only for maintaining trade state.

It does NOT calculate:
- ATR
- Position sizing
- Risk
- Trailing stop logic
- Break-even logic

It does NOT execute orders.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Dict, List, Optional
from uuid import uuid4


@dataclass
class PartialExit:
    quantity: float
    price: float
    reason: str
    timestamp: datetime


@dataclass
class TradeState:
    """
    Stores information about one active trade.
    """

    symbol: str
    side: str

    entry_price: float
    quantity: float

    entry_time: datetime

    initial_stop: float
    current_stop: float

    take_profit_levels: List[float] = field(default_factory=list)
    tp_hit: List[bool] = field(default_factory=list)

    highest_price: float = 0.0
    lowest_price: float = 0.0

    bars_in_trade: int = 0

    break_even_enabled: bool = False
    trailing_enabled: bool = False

    is_open: bool = True

    exit_price: Optional[float] = None
    exit_time: Optional[datetime] = None
    exit_reason: Optional[str] = None

    realized_rr: float = 0.0

    # M2 additions

    trade_id: str = field(default_factory=lambda: str(uuid4()))
    last_updated: datetime = field(default_factory=datetime.utcnow)

    metadata: Dict = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)

    original_quantity: float = 0.0
    remaining_quantity: float = 0.0
    realized_quantity: float = 0.0

    partial_exits: List[PartialExit] = field(default_factory=list)

    unrealized_pnl: float = 0.0
    realized_pnl: float = 0.0

    mfe: float = 0.0
    mae: float = 0.0


class TradeManager:
    """
    Maintains the lifecycle of one active trade.
    """

    def __init__(self):
        self.trade: Optional[TradeState] = None

        self._callbacks: Dict[str, List[Callable]] = {
            "trade_opened": [],
            "trade_updated": [],
            "stop_loss_updated": [],
            "tp_hit": [],
            "partial_exit": [],
            "trade_closed": [],
        }

    @property
    def has_position(self):
        """
        Returns True if there is an active trade.
        """
        return self.trade is not None and self.trade.is_open

    def register_callback(self, event: str, callback: Callable):
        if event not in self._callbacks:
            self._callbacks[event] = []

        self._callbacks[event].append(callback)

    def _emit(self, event: str):
        callbacks = self._callbacks.get(event, [])

        for cb in callbacks:
            try:
                cb(self.trade)
            except Exception:
                pass

    def open_trade(
        self,
        symbol,
        side,
        entry_price,
        quantity,
        stop_loss,
        take_profit_levels=None,
    ):
        """
        Creates a new trade state.
        """

        if take_profit_levels is None:
            take_profit_levels = []

        now = datetime.utcnow()

        self.trade = TradeState(
            symbol=symbol,
            side=side,
            entry_price=entry_price,
            quantity=quantity,
            entry_time=now,
            initial_stop=stop_loss,
            current_stop=stop_loss,
            take_profit_levels=list(take_profit_levels),
            tp_hit=[False] * len(take_profit_levels),
            highest_price=entry_price,
            lowest_price=entry_price,
            original_quantity=quantity,
            remaining_quantity=quantity,
            realized_quantity=0.0,
            last_updated=now,
        )

        self._emit("trade_opened")

    def update_price(self, high, low):
        """
        Update trade statistics once per completed candle.
        """

        if not self.has_position:
            return

        trade = self.trade

        trade.highest_price = max(trade.highest_price, high)
        trade.lowest_price = min(trade.lowest_price, low)

        trade.bars_in_trade += 1

        if trade.side.upper() == "BUY":
            trade.mfe = max(trade.mfe, trade.highest_price - trade.entry_price)
            trade.mae = min(trade.mae, trade.lowest_price - trade.entry_price)
            trade.unrealized_pnl = (
                (low - trade.entry_price) * trade.remaining_quantity
            )
        else:
            trade.mfe = max(trade.mfe, trade.entry_price - trade.lowest_price)
            trade.mae = min(trade.mae, trade.entry_price - trade.highest_price)
            trade.unrealized_pnl = (
                (trade.entry_price - high) * trade.remaining_quantity
            )

        for idx, tp in enumerate(trade.take_profit_levels):
            if trade.tp_hit[idx]:
                continue

            hit = (
                high >= tp
                if trade.side.upper() == "BUY"
                else low <= tp
            )

            if hit:
                trade.tp_hit[idx] = True
                self._emit("tp_hit")

        trade.last_updated = datetime.utcnow()

        self._emit("trade_updated")

    def update_stop_loss(self, new_stop):
        """
        Update stop-loss value.
        """

        if not self.has_position:
            return

        self.trade.current_stop = new_stop
        self.trade.last_updated = datetime.utcnow()

        self._emit("stop_loss_updated")

    def record_partial_exit(
        self,
        quantity,
        price,
        reason="Partial Exit",
    ):
        if not self.has_position:
            return

        trade = self.trade

        quantity = min(quantity, trade.remaining_quantity)

        if quantity <= 0:
            return

        trade.remaining_quantity -= quantity
        trade.realized_quantity += quantity

        if trade.side.upper() == "BUY":
            pnl = (price - trade.entry_price) * quantity
        else:
            pnl = (trade.entry_price - price) * quantity

        trade.realized_pnl += pnl

        trade.partial_exits.append(
            PartialExit(
                quantity=quantity,
                price=price,
                reason=reason,
                timestamp=datetime.utcnow(),
            )
        )

        trade.last_updated = datetime.utcnow()

        self._emit("partial_exit")

    def close_trade(self, exit_price, reason="Unknown"):
        """
        Close the active trade.
        """

        if not self.has_position:
            return

        trade = self.trade

        if trade.remaining_quantity > 0:

            if trade.side.upper() == "BUY":
                pnl = (
                    exit_price - trade.entry_price
                ) * trade.remaining_quantity
            else:
                pnl = (
                    trade.entry_price - exit_price
                ) * trade.remaining_quantity

            trade.realized_pnl += pnl
            trade.realized_quantity += trade.remaining_quantity
            trade.remaining_quantity = 0.0

        trade.exit_price = exit_price
        trade.exit_time = datetime.utcnow()
        trade.exit_reason = reason
        trade.last_updated = trade.exit_time
        trade.is_open = False

        risk = abs(trade.entry_price - trade.initial_stop)

        if risk > 0:
            if trade.side.upper() == "BUY":
                trade.realized_rr = (
                    exit_price - trade.entry_price
                ) / risk
            else:
                trade.realized_rr = (
                    trade.entry_price - exit_price
                ) / risk

        self._emit("trade_closed")

    def reset(self):
        """
        Completely clear trade state.
        """

        self.trade = None

    def get_trade(self):
        """
        Return current trade object.
        """

        return self.trade

    def summary(self):
        """
        Return trade information as a dictionary.
        Useful for dashboard and logging.
        """

        if self.trade is None:
            return None

        t = self.trade

        return {
            "trade_id": t.trade_id,
            "symbol": t.symbol,
            "side": t.side,
            "entry_price": t.entry_price,
            "quantity": t.quantity,
            "remaining_quantity": t.remaining_quantity,
            "realized_quantity": t.realized_quantity,
            "current_stop": t.current_stop,
            "highest_price": t.highest_price,
            "lowest_price": t.lowest_price,
            "bars_in_trade": t.bars_in_trade,
            "is_open": t.is_open,
            "entry_time": t.entry_time,
            "last_updated": t.last_updated,
            "exit_price": t.exit_price,
            "exit_time": t.exit_time,
            "exit_reason": t.exit_reason,
            "mfe": t.mfe,
            "mae": t.mae,
            "unrealized_pnl": t.unrealized_pnl,
            "realized_pnl": t.realized_pnl,
            "realized_rr": t.realized_rr,
            "tp_levels": t.take_profit_levels,
            "tp_status": t.tp_hit,
            "metadata": t.metadata,
            "tags": t.tags,
            "partial_exits": [
                {
                    "quantity": p.quantity,
                    "price": p.price,
                    "reason": p.reason,
                    "timestamp": p.timestamp,
                }
                for p in t.partial_exits
            ],
        }