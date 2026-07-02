"""
BTC Trend Trader Professional v4
Recovery Manager
"""

from __future__ import annotations

import shutil
from pathlib import Path


class RecoveryManager:
    """
    Restores application state from a backup file.
    """

    def restore(
        self,
        backup_file: str,
        destination: str,
    ) -> bool:

        try:

            backup_path = Path(backup_file)
            destination_path = Path(destination)

            destination_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            shutil.copy2(
                backup_path,
                destination_path,
            )

            return True

        except Exception:
            return False