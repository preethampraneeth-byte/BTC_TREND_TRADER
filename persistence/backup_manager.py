"""
BTC Trend Trader Professional v4
Backup Manager
"""

from __future__ import annotations

import shutil
from pathlib import Path


class BackupManager:
    """
    Creates backup copies of persistence files.
    """

    def create_backup(
        self,
        source: str,
        destination: str,
    ) -> bool:

        try:

            source_path = Path(source)
            destination_path = Path(destination)

            destination_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            shutil.copy2(
                source_path,
                destination_path,
            )

            return True

        except Exception:
            return False