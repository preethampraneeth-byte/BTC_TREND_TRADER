"""
BTC Trend Trader Professional v4
Milestone M3

Structured Logger

Responsibilities
----------------
- Trade logging
- Execution logging
- Risk logging
- Performance logging
- Error logging
- Event logging
- Console logging
- Rotating file logging

Future
------
- JSON logging
- Remote logging
- Database logging
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class EngineLogger:
    """
    Central logger used throughout the trading engine.
    """

    def __init__(
        self,
        log_directory: str = "logs",
        level: int = logging.INFO,
        console: bool = True,
        max_bytes: int = 5 * 1024 * 1024,
        backup_count: int = 5,
    ):

        self.log_directory = Path(log_directory)
        self.log_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.level = level

        self._trade = self._create_logger(
            "trade",
            "trade.log",
            console,
            max_bytes,
            backup_count,
        )

        self._risk = self._create_logger(
            "risk",
            "risk.log",
            console,
            max_bytes,
            backup_count,
        )

        self._execution = self._create_logger(
            "execution",
            "execution.log",
            console,
            max_bytes,
            backup_count,
        )

        self._performance = self._create_logger(
            "performance",
            "performance.log",
            console,
            max_bytes,
            backup_count,
        )

        self._event = self._create_logger(
            "event",
            "event.log",
            console,
            max_bytes,
            backup_count,
        )

        self._error = self._create_logger(
            "error",
            "error.log",
            console,
            max_bytes,
            backup_count,
        )

    # --------------------------------------------------
    # Internal
    # --------------------------------------------------

    def _create_logger(
        self,
        name: str,
        filename: str,
        console: bool,
        max_bytes: int,
        backup_count: int,
    ) -> logging.Logger:

        logger = logging.getLogger(
            f"BTCTrendTrader.{name}"
        )

        logger.setLevel(self.level)
        logger.propagate = False

        if logger.handlers:
            return logger

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        handler = RotatingFileHandler(
            self.log_directory / filename,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )

        handler.setFormatter(formatter)

        logger.addHandler(handler)

        if console:

            console_handler = logging.StreamHandler()

            console_handler.setFormatter(formatter)

            logger.addHandler(console_handler)

        return logger

    # --------------------------------------------------
    # Payload Formatting
    # --------------------------------------------------

    def _format_payload(
        self,
        **payload,
    ) -> str:
        if not payload:
            return ""

        return ", ".join(
            f"{k}={v}"
            for k, v in payload.items()
        )

    # --------------------------------------------------
    # Generic
    # --------------------------------------------------

    def info(
        self,
        message: str,
    ):
        self._event.info(message)

    def warning(
        self,
        message: str,
    ):
        self._event.warning(message)

    def error(
        self,
        message: str,
        **payload,
    ):
        items = self._format_payload(**payload)

        if items:
            message = f"{message} | {items}"

        self._error.error(message)

    def exception(
        self,
        message: str,
    ):
        self._error.exception(message)

    # --------------------------------------------------
    # Trade
    # --------------------------------------------------

    def trade(
        self,
        message: str,
    ):
        self._trade.info(message)

    # --------------------------------------------------
    # Risk
    # --------------------------------------------------

    def risk(
        self,
        message: str,
    ):
        self._risk.info(message)

    # --------------------------------------------------
    # Execution
    # --------------------------------------------------

    def execution(
        self,
        message: str,
        **payload,
    ):
        items = self._format_payload(**payload)

        if items:
            message = f"{message} | {items}"

        self._execution.info(message)

    # --------------------------------------------------
    # Performance
    # --------------------------------------------------

    def performance(
        self,
        message: str,
    ):
        self._performance.info(message)

    # --------------------------------------------------
    # Event
    # --------------------------------------------------

    def event(
        self,
        message: str,
    ):
        self._event.info(message)

    # --------------------------------------------------
    # Structured Helpers
    # --------------------------------------------------

    def log_trade_open(
        self,
        trade_id: str,
        symbol: str,
        side: str,
        entry: float,
        quantity: float,
    ):

        self.trade(
            f"OPEN | "
            f"id={trade_id} | "
            f"symbol={symbol} | "
            f"side={side} | "
            f"entry={entry} | "
            f"qty={quantity}"
        )

    def log_trade_close(
        self,
        trade_id: str,
        pnl: float,
        rr: float,
    ):

        self.trade(
            f"CLOSE | "
            f"id={trade_id} | "
            f"pnl={pnl:.2f} | "
            f"rr={rr:.2f}"
        )

    def log_partial_exit(
        self,
        trade_id: str,
        quantity: float,
        price: float,
    ):

        self.trade(
            f"PARTIAL | "
            f"id={trade_id} | "
            f"qty={quantity} | "
            f"price={price}"
        )

    def log_stop_update(
        self,
        trade_id: str,
        stop: float,
    ):

        self.trade(
            f"STOP | "
            f"id={trade_id} | "
            f"stop={stop}"
        )

    def log_order(
        self,
        ticket,
        status,
        symbol,
    ):

        self.execution(
            f"ORDER | "
            f"ticket={ticket} | "
            f"status={status} | "
            f"symbol={symbol}"
        )

    def log_risk_rejected(
        self,
        reason,
    ):

        self.risk(
            f"REJECTED | {reason}"
        )

    def log_risk_approved(
        self,
        risk: float,
    ):

        self.risk(
            f"APPROVED | "
            f"risk={risk}"
        )

    def log_event(
        self,
        event_name: str,
        **payload,
    ):

        if payload:

            items = ", ".join(
                f"{k}={v}"
                for k, v in payload.items()
            )

            self.event(
                f"{event_name} | {items}"
            )

        else:

            self.event(event_name)

    def log_performance(
        self,
        metric: str,
        value,
    ):

        self.performance(
            f"{metric}={value}"
        )


# ------------------------------------------------------
# Global Logger
# ------------------------------------------------------

logger = EngineLogger()