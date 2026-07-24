"""
Trade Audit Service

Provides a central location for recording
trade lifecycle events.
"""

from __future__ import annotations


class TradeAuditService:
    """
    Records trade audit events.

    This initial implementation is intentionally
    lightweight. Future phases will add logging
    to files and structured audit records.
    """

    def log(self, event, trade, message=""):
        """
        Record an audit event.

        Parameters
        ----------
        event : str
            Event name.

        trade : object
            Trade instance.

        message : str
            Optional description.
        """

        return