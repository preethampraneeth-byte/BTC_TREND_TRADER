"""
BTC Trend Trader v4.0

Advanced Logging

Centralized logging for the trading engine.

Responsibilities
----------------
- File logging
- Console logging
- Trade lifecycle logging
- Error logging
- Event logging

This module does NOT:
- Execute trades
- Calculate risk
- Manage trade state
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class AdvancedLogger:
    """
    Wrapper around Python logging providing a consistent
    logging interface for the trading engine.
    """

    def __init__(
        self,
        name="BTCTrendTrader",
        log_directory="logs",
        filename="trading.log",
        level=logging.INFO,
        max_bytes=5 * 1024 * 1024,
        backup_count=5,
        console=True,
    ):
        self.log_directory = Path(log_directory)
        self.log_directory.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.propagate = False

        if not self.logger.handlers:

            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s"
            )

            file_handler = RotatingFileHandler(
                self.log_directory / filename,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding="utf-8",
            )

            file_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)

            if console:
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                self.logger.addHandler(console_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def exception(self, message):
        self.logger.exception(message)

    def critical(self, message):
        self.logger.critical(message)

    def log_trade_open(self, trade):
        if trade is None:
            return

        self.info(
            (
                f"TRADE OPENED | "
                f"id={trade.trade_id} | "
                f"{trade.symbol} | "
                f"{trade.side} | "
                f"entry={trade.entry_price} | "
                f"qty={trade.quantity}"
            )
        )

    def log_trade_update(self, trade):
        if trade is None:
            return

        self.info(
            (
                f"TRADE UPDATED | "
                f"id={trade.trade_id} | "
                f"remaining={trade.remaining_quantity} | "
                f"SL={trade.current_stop} | "
                f"UPNL={trade.unrealized_pnl:.2f}"
            )
        )

    def log_partial_exit(
        self,
        trade,
        quantity,
        price,
        reason,
    ):
        if trade is None:
            return

        self.info(
            (
                f"PARTIAL EXIT | "
                f"id={trade.trade_id} | "
                f"qty={quantity} | "
                f"price={price} | "
                f"reason={reason}"
            )
        )

    def log_stop_update(
        self,
        trade,
        new_stop,
    ):
        if trade is None:
            return

        self.info(
            (
                f"STOP UPDATED | "
                f"id={trade.trade_id} | "
                f"new_stop={new_stop}"
            )
        )

    def log_tp_hit(
        self,
        trade,
        tp_level,
    ):
        if trade is None:
            return

        self.info(
            (
                f"TAKE PROFIT HIT | "
                f"id={trade.trade_id} | "
                f"tp={tp_level}"
            )
        )

    def log_trade_close(self, trade):
        if trade is None:
            return

        self.info(
            (
                f"TRADE CLOSED | "
                f"id={trade.trade_id} | "
                f"exit={trade.exit_price} | "
                f"realized_pnl={trade.realized_pnl:.2f} | "
                f"rr={trade.realized_rr:.2f}"
            )
        )

    def log_event(
        self,
        event,
        **kwargs,
    ):
        if kwargs:
            payload = ", ".join(
                f"{k}={v}" for k, v in kwargs.items()
            )
            self.info(f"{event} | {payload}")
        else:
            self.info(event)