"""
BTC Trend Trader Professional v4
State Serializer
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class StateSerializer:
    """
    Serializes application state to JSON.
    """

    def save(
        self,
        state: Any,
        filename: str,
    ) -> bool:

        try:

            data = (
                state.to_dict()
                if hasattr(state, "to_dict")
                else state
            )

            with open(
                Path(filename),
                "w",
                encoding="utf-8",
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4,
                    default=str,
                )

            return True

        except Exception:
            return False