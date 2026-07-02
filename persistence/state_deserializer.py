"""
BTC Trend Trader Professional v4
State Deserializer
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class StateDeserializer:
    """
    Deserializes application state from JSON.
    """

    def load(
        self,
        filename: str,
    ) -> Any:

        try:

            with open(
                Path(filename),
                "r",
                encoding="utf-8",
            ) as file:

                return json.load(file)

        except Exception:
            return None