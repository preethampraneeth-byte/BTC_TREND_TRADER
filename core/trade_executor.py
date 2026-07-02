
"""
BTC Trend Trader v4.0
Trade Executor
"""

from typing import Any, Callable, Optional

from core.execution_state import ExecutionState, OrderStatus
from core.execution_retry import RetryEngine
from core.execution_audit import ExecutionAudit
from core.execution_lifecycle import OrderLifecycle
from core.execution_partial import PartialCloseEngine
from core.trade_storage import TradeStorage
from core.event_bus import global_event_bus, Events


class TradeExecutor:
    """Backend-agnostic trade execution wrapper."""

    def __init__(
        self,
        backend: Optional[Any] = None,
        max_retries: int = 3,
        retry_delay: float = 0.5,
    ):
        self.backend = backend
        self.max_retries = max(1, int(max_retries))
        self.retry_delay = retry_delay

        self.execution_state = ExecutionState()
        self.retry_engine = RetryEngine(
            max_retries=self.max_retries,
            retry_delay=self.retry_delay,
        )
        self.audit = ExecutionAudit()
        self.lifecycle = OrderLifecycle()
        self.partial_engine = PartialCloseEngine()
        self.storage = TradeStorage()

    def set_backend(self, backend: Any):
        self.backend = backend

    def _publish_event(self, event, **payload):
        """
        Publish an event without interrupting trading.
        """
        try:
            global_event_bus.publish(
                event,
                **payload,
            )
        except Exception:
            pass




    def _persist_trade(self):
        """
        Persist current execution state.
        Persistence failures must never interrupt trading.
        """
        try:
            self.storage.save_trade(
                self.execution_state
            )
        except Exception:
            pass

    def _retry(self, func: Callable, *args, **kwargs):
        result = self.retry_engine.execute(func, *args, **kwargs)
        self.execution_state.retry_count = result.retries
        if result.success:
            return result.result
        raise RuntimeError(result.error)

    def open_order(
        self,
        symbol,
        side,
        volume,
        price=None,
        stop_loss=None,
        take_profit=None,
        **kwargs,
    ) -> Any:
        if self.backend is None:
            raise RuntimeError("Execution backend not configured.")
        if not hasattr(self.backend, "open_order"):
            raise NotImplementedError("Backend does not implement open_order().")

        self.lifecycle.reset()
        self.lifecycle.mark_sent()

        self._publish_event(
            Events.ORDER_SENT,
            symbol=symbol,
            side=side,
            volume=volume,
        )

        self.execution_state.symbol = symbol
        self.execution_state.side = side
        self.execution_state.volume = volume
        self.execution_state.requested_price = price or 0.0
        self.execution_state.stop_loss = stop_loss
        self.execution_state.take_profit = take_profit

        try:
            result = self._retry(
                self.backend.open_order,
                symbol=symbol,
                side=side,
                volume=volume,
                price=price,
                stop_loss=stop_loss,
                take_profit=take_profit,
                **kwargs,
            )

            if hasattr(result, "ticket"):
                self.execution_state.ticket = result.ticket

            if hasattr(result, "fill_price"):
                self.execution_state.fill_price = result.fill_price

            if hasattr(result, "slippage"):
                self.execution_state.slippage = result.slippage

            self.lifecycle.mark_filled()

            self._publish_event(
                Events.ORDER_FILLED,
                symbol=symbol,
                side=side,
                volume=volume,
            )
            self.execution_state.set_status(OrderStatus.FILLED)

            self._record_success(
                status="FILLED",
                message="Order opened successfully.",
                symbol=symbol,
                side=side,
                volume=volume,
                requested_price=price or 0.0,
                stop_loss=stop_loss,
                take_profit=take_profit,
            )
            return result

        except Exception:
            self._record_failure(
                "Order execution failed.",
                symbol=symbol,
                side=side,
                volume=volume,
                requested_price=price or 0.0,
                stop_loss=stop_loss,
                take_profit=take_profit,
                reason="Order execution failed.",
            )
            raise



    def _record_success(
        self,
        *,
        status: str,
        message: str,
        **fields,
    ) -> None:
        """
        Common success bookkeeping.
        Keeps all audit/persistence logic in one place.
        """

        self.audit.record(
            retry_count=self.execution_state.retry_count,
            status=status,
            message=message,
            **fields,
        )

        self._persist_trade()

    def _record_failure(
        self,
        message: str,
        **fields,
    ) -> None:
        """
        Common failure bookkeeping.
        """

        self.lifecycle.mark_failed()
        self.execution_state.record_failure(message)

        self._publish_event(
            Events.ORDER_FAILED,
            **fields,
        )

        self.audit.record(
            retry_count=self.execution_state.retry_count,
            status="FAILED",
            message=message,
            **fields,
        )

        self._persist_trade()

    def close_order(self, position_id, volume=None, **kwargs) -> Any:
        if self.backend is None:
            raise RuntimeError("Execution backend not configured.")
        if not hasattr(self.backend, "close_order"):
            raise NotImplementedError("Backend does not implement close_order().")

        try:
            result = self._retry(
                self.backend.close_order,
                position_id=position_id,
                volume=volume,
                **kwargs,
            )
            self.lifecycle.mark_closed()

            self._publish_event(
                Events.ORDER_CLOSED,
                position_id=position_id,
                volume=volume,
            )
            self.execution_state.set_status(OrderStatus.CLOSED)
            self._record_success(
                status="CLOSED",
                message="Position closed.",
                ticket=position_id,
                volume=volume,
            )
            return result
        except Exception:
            self._record_failure(
                "Position close failed.",
                ticket=position_id,
                volume=volume,
            )
            raise

    
    def partial_close(self, position_id, volume, **kwargs) -> Any:
        if self.backend is None:
            raise RuntimeError("Execution backend not configured.")

        result = self.partial_engine.close_quantity(
            current_volume=kwargs.get("current_volume", volume),
            quantity=volume,
        )
        if not result.valid:
            raise ValueError(result.reason)

        close_volume = result.close_volume

        try:
            if hasattr(self.backend, "partial_close"):
                backend_result = self._retry(
                    self.backend.partial_close,
                    position_id=position_id,
                    volume=close_volume,
                    **kwargs,
                )
            elif hasattr(self.backend, "close_order"):
                backend_result = self._retry(
                    self.backend.close_order,
                    position_id=position_id,
                    volume=close_volume,
                    **kwargs,
                )
            else:
                raise NotImplementedError("Backend does not support partial_close().")

            self.lifecycle.mark_partial()

            self._publish_event(
                Events.ORDER_PARTIAL,
                position_id=position_id,
                volume=close_volume,
            )
            self.execution_state.set_status(OrderStatus.PARTIAL)
            self._record_success(
                status="PARTIAL",
                message="Partial position close.",
                volume=close_volume,
            )
            return backend_result
        except Exception:
            self._record_failure(
                "Partial close failed.",
                position_id=position_id,
                volume=close_volume,
            )
            raise


    
    def modify_stop_loss(self, position_id, new_stop_loss, **kwargs) -> Any:
        if self.backend is None:
            raise RuntimeError("Execution backend not configured.")
        if not hasattr(self.backend, "modify_stop_loss"):
            raise NotImplementedError("Backend does not implement modify_stop_loss().")
        try:
            result = self._retry(
                self.backend.modify_stop_loss,
                position_id=position_id,
                stop_loss=new_stop_loss,
                **kwargs,
            )
            self.lifecycle.mark_modified()

            self._publish_event(
                Events.ORDER_MODIFIED,
                position_id=position_id,
                stop_loss=new_stop_loss,
            )

            self.execution_state.set_status(OrderStatus.MODIFIED)
            self.execution_state.stop_loss = new_stop_loss
            self._record_success(
                status="MODIFIED",
                message="Stop loss updated.",
                stop_loss=new_stop_loss,
            )
            return result
        except Exception:
            self._record_failure(
                "Stop loss modification failed.",
                position_id=position_id,
                stop_loss=new_stop_loss,
            )
            raise


    
    def modify_take_profit(self, position_id, take_profit, **kwargs) -> Any:
        if self.backend is None:
            raise RuntimeError("Execution backend not configured.")
        if not hasattr(self.backend, "modify_take_profit"):
            raise NotImplementedError("Backend does not implement modify_take_profit().")
        try:
            result = self._retry(
                self.backend.modify_take_profit,
                position_id=position_id,
                take_profit=take_profit,
                **kwargs,
            )
            self.lifecycle.mark_modified()

            self._publish_event(
                Events.ORDER_MODIFIED,
                position_id=position_id,
                take_profit=take_profit,
            )

            self.execution_state.set_status(OrderStatus.MODIFIED)
            self.execution_state.take_profit = take_profit
            self._record_success(
                status="MODIFIED",
                message="Take profit updated.",
                take_profit=take_profit,
            )
            return result
        except Exception:
            self._record_failure(
                "Take profit modification failed.",
                position_id=position_id,
                take_profit=take_profit,
            )
            raise


    def restore_execution_state(self) -> None:
        """
        Restore the last persisted execution state.
        """

        try:

            state = self.storage.load_trade()

            if state is not None:
                self.execution_state = state

        except Exception:
            pass


    def cancel_order(self, order_id, **kwargs) -> Any:
        if self.backend is None:
            raise RuntimeError("Execution backend not configured.")
        if not hasattr(self.backend, "cancel_order"):
            raise NotImplementedError("Backend does not implement cancel_order().")

        return self._retry(
            self.backend.cancel_order,
            order_id=order_id,
            **kwargs,
        )