"""
BTC Trend Trader Professional v4
Milestone M3

Trade Storage

Responsibilities
----------------
- Persist Trade State
- Persist Risk State
- Persist Execution State
- Restore engine state
- JSON storage backend

Future
------
- SQLite backend
- Cloud storage
- Encryption

This module performs NO:
- Trading
- Risk calculations
- Order execution
"""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class TradeStorage:
    """
    Unified storage for the trading engine.

    Stores:

    - Trade State
    - Risk State
    - Execution State
    """

    def __init__(self, filename="engine_state.json"):

        self.path = Path(filename)

    # --------------------------------------------------------
    # Serialization
    # --------------------------------------------------------

    def _serialize(self, obj):

        if obj is None:
            return None

        if isinstance(obj, datetime):
            return obj.isoformat()

        if is_dataclass(obj):
            obj = asdict(obj)

        if isinstance(obj, dict):

            return {
                k: self._serialize(v)
                for k, v in obj.items()
            }

        if isinstance(obj, list):

            return [
                self._serialize(v)
                for v in obj
            ]

        return obj

    # --------------------------------------------------------

    def _deserialize(self, obj):

        if isinstance(obj, dict):

            return {
                k: self._deserialize(v)
                for k, v in obj.items()
            }

        if isinstance(obj, list):

            return [
                self._deserialize(v)
                for v in obj
            ]

        if isinstance(obj, str):

            try:
                return datetime.fromisoformat(obj)
            except Exception:
                return obj

        return obj

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    def save(
        self,
        trade_state=None,
        risk_state=None,
        execution_state=None,
    ):
        """
        Persist complete engine state.
        """

        payload = {

            "version": "4.0",

            "saved_at": datetime.utcnow().isoformat(),

            "trade_state": self._serialize(
                trade_state
            ),

            "risk_state": self._serialize(
                risk_state
            ),

            "execution_state": self._serialize(
                execution_state
            ),
        }

        with open(
            self.path,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                payload,
                f,
                indent=4,
                ensure_ascii=False,
            )

        return True

    # --------------------------------------------------------
    # Load
    # --------------------------------------------------------

    def load(self):
        """
        Restore engine state.
        """

        if not self.path.exists():
            return None

        with open(
            self.path,
            "r",
            encoding="utf-8",
        ) as f:

            payload = json.load(f)

        return self._deserialize(payload)

    # --------------------------------------------------------
    # State Helpers
    # --------------------------------------------------------

    def load_trade_state(self):

        data = self.load()

        if not data:
            return None

        return data.get("trade_state")

    def load_risk_state(self):

        data = self.load()

        if not data:
            return None

        return data.get("risk_state")

    def load_execution_state(self):

        data = self.load()

        if not data:
            return None

        return data.get("execution_state")

    # --------------------------------------------------------
    # File Operations
    # --------------------------------------------------------

    def exists(self):

        return self.path.exists()

    def clear(self):

        if self.path.exists():
            self.path.unlink()

    # --------------------------------------------------------
    # Metadata
    # --------------------------------------------------------

    def metadata(self):

        if not self.exists():
            return None

        data = self.load()

        return {

            "version": data.get("version"),

            "saved_at": data.get("saved_at"),
        }

    # --------------------------------------------------------
    # Snapshot
    # --------------------------------------------------------

    def snapshot(
        self,
        trade_state=None,
        risk_state=None,
        execution_state=None,
    ):
        """
        Returns storage payload without saving.

        Useful for testing and debugging.
        """

        return {

            "version": "4.0",

            "saved_at": datetime.utcnow(),

            "trade_state": self._serialize(
                trade_state
            ),

            "risk_state": self._serialize(
                risk_state
            ),

            "execution_state": self._serialize(
                execution_state
            ),
        }