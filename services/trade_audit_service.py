"""
Trade Audit Service

Provides a central location for recording
trade lifecycle events.
"""

from __future__ import annotations

from datetime import datetime


class TradeAuditService:
    """
    Records trade audit events.
    """

    def __init__(self):
        self.events = []

    def log(self, event, trade, message=""):
        """
        Record an audit event.
        """

        self.events.append(
            {
                "timestamp": datetime.now(),
                "event": event,
                "trade": trade,
                "message": message,
            }
        )

    def get_events(self):
        """
        Return all recorded audit events.
        """

        return list(self.events)