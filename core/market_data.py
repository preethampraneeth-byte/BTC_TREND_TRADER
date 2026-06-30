"""
BTC Trend Trader v1.0
Market Data Module
"""

import pandas as pd
import MetaTrader5 as mt5


class MarketData:
    """
    Downloads and loads historical market data.
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

    # ---------------------------------------------------------

    def get_candles(self, symbol, timeframe, bars=500):
        """
        Download historical candles from MetaTrader 5.

        Parameters
        ----------
        symbol : str
            Trading symbol (e.g. BTCUSD)

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
            bars,
        )

        if rates is None:
            raise RuntimeError(
                f"Unable to download data for {symbol}"
            )

        df = pd.DataFrame(rates)

        df["time"] = pd.to_datetime(
            df["time"],
            unit="s",
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

    # ---------------------------------------------------------

    def save_to_csv(self, df, filename):
        """
        Save market data to CSV.
        """

        df.to_csv(
            filename,
            index=False,
        )

    # ---------------------------------------------------------

    def load_from_csv(self, filename):
        """
        Load market data from CSV.
        """

        return pd.read_csv(
            filename,
            parse_dates=["Time"],
        )