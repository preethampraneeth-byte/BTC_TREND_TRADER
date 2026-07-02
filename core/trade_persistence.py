"""
BTC Trend Trader v4.0

Trade Persistence

Responsible for saving and restoring TradeManager state.

Responsibilities
----------------
- Serialize trade state
- Deserialize trade state
- Save to disk
- Load from disk

This module does NOT:
- Execute trades
- Calculate risk
- Modify trade logic
"""

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from core.trade_manager import PartialExit, TradeState


class TradePersistence:
    """
    Handles persistence of TradeState objects.
    """

    def __init__(self, filepath="trade_state.json"):
        self.filepath = Path(filepath)

    @staticmethod
    def _serialize_datetime(value):
        if isinstance(value, datetime):
            return value.isoformat()
        return value

    @staticmethod
    def _deserialize_datetime(value):
        if value is None:
            return None
        return datetime.fromisoformat(value)

    def save(self, trade):
        """
        Save a TradeState object.

        Returns True on success.
        """

        if trade is None:
            return False

        data = asdict(trade)

        data["entry_time"] = self._serialize_datetime(data["entry_time"])
        data["last_updated"] = self._serialize_datetime(data["last_updated"])
        data["exit_time"] = self._serialize_datetime(data["exit_time"])

        partials = []

        for p in data["partial_exits"]:
            p["timestamp"] = self._serialize_datetime(p["timestamp"])
            partials.append(p)

        data["partial_exits"] = partials

        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        return True

    def load(self):
        """
        Restore TradeState from disk.

        Returns:
            TradeState or None
        """

        if not self.filepath.exists():
            return None

        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        data["entry_time"] = self._deserialize_datetime(data["entry_time"])
        data["last_updated"] = self._deserialize_datetime(data["last_updated"])
        data["exit_time"] = self._deserialize_datetime(data["exit_time"])

        partials = []

        for item in data.get("partial_exits", []):
            partials.append(
                PartialExit(
                    quantity=item["quantity"],
                    price=item["price"],
                    reason=item["reason"],
                    timestamp=self._deserialize_datetime(item["timestamp"]),
                )
            )

        data["partial_exits"] = partials

        trade = TradeState(**data)

        return trade

    def clear(self):
        """
        Remove persisted trade state.
        """

        if self.filepath.exists():
            self.filepath.unlink()

    def exists(self):
        """
        Check whether a persisted trade exists.
        """

        return self.filepath.exists()