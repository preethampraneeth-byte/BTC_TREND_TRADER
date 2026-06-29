"""
BTC Trend Trader v1.0
Market Data Module
"""

from datetime import datetime
import pandas as pd
import MetaTrader5 as mt5


class MarketData:
    """
    Downloads historical market data from MetaTrader 5.
    """

    # Mapping from our config timeframe names to MT5 constants
    TIMEFRAME_MAP = {
        "M1": mt5.TIMEFRAME_M1,
        "M5": mt5.TIMEFRAME_M5,
        "M15": mt5.TIMEFRAME_M15,
        "M30": mt5.TIMEFRAME_M30,
        "H1": mt5.TIMEFRAME_H1,
        "H4": mt5.TIMEFRAME_H4,
        "D1": mt5.TIMEFRAME_D1,
    }

    def get_candles(self, symbol, timeframe, bars=500):
        """
        Download historical candles.

        Parameters
        ----------
        symbol : str
            Trading symbol (e.g. BTCUSD#)

        timeframe : str
            Timeframe (H1, M15, etc.)

        bars : int
            Number of candles to download

        Returns
        -------
        pandas.DataFrame
        """

        if timeframe not in self.TIMEFRAME_MAP:
            raise ValueError(f"Unsupported timeframe: {timeframe}")

        mt5_timeframe = self.TIMEFRAME_MAP[timeframe]

        rates = mt5.copy_rates_from_pos(
            symbol,
            mt5_timeframe,
            0,
            bars
        )

        if rates is None:
            raise RuntimeError(
                f"Unable to download data for {symbol}"
            )

        df = pd.DataFrame(rates)

        df["time"] = pd.to_datetime(
            df["time"],
            unit="s"
        )

        df = df.rename(
            columns={
                "time": "Time",
                "open": "Open",
                "high": "High",
                "low": "Low",
                "close": "Close",
                "tick_volume": "Volume",
            }
        )

        columns = [
            "Time",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
        ]

        return df[columns]