"""
BTC Trend Trader Professional v4
Dashboard Controller
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


class DashboardController:
    """Read-only integration layer between the trading engine and dashboard."""

    def __init__(
        self,
        trade_executor: Optional[Any] = None,
        risk_manager: Optional[Any] = None,
        trade_storage: Optional[Any] = None,
        execution_audit: Optional[Any] = None,
        event_bus: Optional[Any] = None,
    ) -> None:
        self.trade_executor = trade_executor
        self.risk_manager = risk_manager
        self.trade_storage = trade_storage
        self.execution_audit = execution_audit
        self.event_bus = event_bus

        self._account: Dict[str, Any] = {}
        self._positions: List[Any] = []
        self._orders: List[Any] = []
        self._history: List[Any] = []
        self._events: List[Any] = []
        self._risk: Dict[str, Any] = {}
        self._statistics: Dict[str, Any] = {}

    def refresh(self) -> None:
        self._refresh_account()
        self._refresh_positions()
        self._refresh_orders()
        self._refresh_history()
        self._refresh_events()
        self._refresh_risk()
        self._refresh_statistics()

    def get_account(self) -> Dict[str, Any]:
        return dict(self._account)

    def get_positions(self) -> List[Any]:
        return list(self._positions)

    def get_orders(self) -> List[Any]:
        return list(self._orders)

    def get_history(self) -> List[Any]:
        return list(self._history)

    def get_events(self) -> List[Any]:
        return list(self._events)

    def get_risk(self) -> Dict[str, Any]:
        return dict(self._risk)

    def get_statistics(self) -> Dict[str, Any]:
        return dict(self._statistics)

    def _refresh_account(self) -> None:
        try:
            backend = getattr(self.trade_executor, "backend", None)
            if backend and hasattr(backend, "get_account"):
                data = backend.get_account()
                self._account = data if isinstance(data, dict) else {}
        except Exception as e:
            logger.debug("Dashboard refresh failed", exc_info=e)

    def _refresh_positions(self) -> None:
        try:
            if self.trade_storage and hasattr(self.trade_storage, "load_trade"):
                state = self.trade_storage.load_trade()
                self._positions = [state] if state is not None else []
        except Exception:
            pass

    def _refresh_orders(self) -> None:
        try:
            state = getattr(self.trade_executor, "execution_state", None)
            self._orders = [state] if state is not None else []
        except Exception:
            pass

    def _refresh_history(self) -> None:
        try:
            if self.execution_audit and hasattr(self.execution_audit, "records"):
                self._history = list(self.execution_audit.records)
        except Exception:
            pass

    def _refresh_events(self) -> None:
        try:
            if self.event_bus and hasattr(self.event_bus, "events"):
                self._events = list(self.event_bus.events)
        except Exception:
            pass

    def _refresh_risk(self) -> None:
        try:
            if self.risk_manager and hasattr(self.risk_manager, "snapshot"):
                data = self.risk_manager.snapshot()
                self._risk = data if isinstance(data, dict) else {}
        except Exception:
            pass

    def _refresh_statistics(self) -> None:
        try:
            self._statistics = {
                "positions": len(self._positions),
                "orders": len(self._orders),
                "history": len(self._history),
                "events": len(self._events),
            }
        except Exception:
            pass
