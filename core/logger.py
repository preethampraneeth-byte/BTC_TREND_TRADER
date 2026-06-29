"""
BTC Trend Trader v1.0
CSV Logger
"""

from __future__ import annotations

from pathlib import Path
import csv


class TradeLogger:
    """
    Logs every trade decision to a CSV file.
    """

    def __init__(self, filename: str = "logs/trade_log.csv"):

        self.file = Path(filename)

        # Create logs folder if it doesn't exist
        self.file.parent.mkdir(parents=True, exist_ok=True)

        # Create CSV with header if it doesn't exist
        if not self.file.exists():
            with open(self.file, "w", newline="") as f:
                writer = csv.writer(f)

                writer.writerow([
                    "Signal",
                    "Reason",
                    "Entry",
                    "StopLoss",
                    "TakeProfit",
                    "LotSize",
                    "RiskPercent",
                ])

    def log(self, trade: dict):

        with open(self.file, "a", newline="") as f:

            writer = csv.writer(f)

            writer.writerow([
                trade.get("Signal"),
                trade.get("Reason"),
                trade.get("Entry"),
                trade.get("StopLoss"),
                trade.get("TakeProfit"),
                trade.get("LotSize"),
                trade.get("RiskPercent"),
            ])