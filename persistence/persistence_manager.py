"""
BTC Trend Trader Professional v4
Persistence Manager
"""

from __future__ import annotations

from typing import Any

from persistence.state_serializer import StateSerializer
from persistence.state_deserializer import StateDeserializer
from persistence.backup_manager import BackupManager
from persistence.recovery_manager import RecoveryManager


class PersistenceManager:
    """
    Central persistence coordinator.
    """

    def __init__(self) -> None:
        self.serializer = StateSerializer()
        self.deserializer = StateDeserializer()
        self.backup_manager = BackupManager()
        self.recovery_manager = RecoveryManager()

    def save(self, state: Any, filename: str) -> bool:
        return self.serializer.save(state, filename)

    def load(self, filename: str) -> Any:
        return self.deserializer.load(filename)

    def backup(self, source: str, destination: str) -> bool:
        return self.backup_manager.create_backup(
            source,
            destination,
        )

    def recover(self, backup_file: str, destination: str) -> bool:
        return self.recovery_manager.restore(
            backup_file,
            destination,
        )