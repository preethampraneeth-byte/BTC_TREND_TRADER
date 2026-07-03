"""
BTC Trend Trader Professional v4
MT5 Connection Module
"""

from __future__ import annotations

import MetaTrader5 as mt5
import pandas as pd

import config


class MT5Connector:
    """
    Handles connection to MetaTrader 5.
    """

    def __init__(self):

        self.connected = False

    # -------------------------------------------------

    def connect(self):

        if config.MT5_PATH:

            initialized = mt5.initialize(
                path=config.MT5_PATH
            )

        else:

            initialized = mt5.initialize()

        if not initialized:

            print("❌ Failed to initialize MetaTrader 5")
            print("Error:", mt5.last_error())

            return False

        authorized = mt5.login(

            login=config.LOGIN,

            password=config.PASSWORD,

            server=config.SERVER,

        )

        if not authorized:

            print("❌ Login failed")
            print("Error:", mt5.last_error())

            mt5.shutdown()

            return False

        self.connected = True

        print("✅ Connected to MetaTrader 5")

        return True

    # -------------------------------------------------

    def account_info(self):

        if not self.connected:

            print("Not connected.")

            return

        info = mt5.account_info()

        if info is None:

            print("Could not retrieve account information.")

            return

        print("\n===== ACCOUNT INFORMATION =====")

        print(f"Login      : {info.login}")
        print(f"Server     : {info.server}")
        print(f"Balance    : {info.balance}")
        print(f"Equity     : {info.equity}")
        print(f"Leverage   : {info.leverage}")
        print(f"Currency   : {info.currency}")

    # -------------------------------------------------

    def symbol_info(
        self,
        symbol,
    ):

        info = mt5.symbol_info(symbol)

        if info is None:

            print(f"❌ Symbol '{symbol}' not found.")

            return False

        if not info.visible:

            mt5.symbol_select(symbol, True)

        print(f"✅ Symbol '{symbol}' is available.")

        return True

    # -------------------------------------------------

    def get_latest_candles(
        self,
        symbol,
        timeframe,
        bars=500,
    ):
        """
        Retrieve the latest candles from MT5.

        Accepts either:

            M1
            M5
            M15
            M30
            H1
            H4
            D1

        or MT5 timeframe constants.
        """

        timeframe_map = {

            "M1": mt5.TIMEFRAME_M1,

            "M5": mt5.TIMEFRAME_M5,

            "M15": mt5.TIMEFRAME_M15,

            "M30": mt5.TIMEFRAME_M30,

            "H1": mt5.TIMEFRAME_H1,

            "H4": mt5.TIMEFRAME_H4,

            "D1": mt5.TIMEFRAME_D1,

        }

        if isinstance(timeframe, str):

            timeframe = timeframe.upper()

            if timeframe not in timeframe_map:

                raise ValueError(
                    f"Unsupported timeframe: {timeframe}"
                )

            timeframe = timeframe_map[timeframe]

        rates = mt5.copy_rates_from_pos(

            symbol,

            timeframe,

            0,

            bars,

        )

        if rates is None:

            print("MT5 Error:", mt5.last_error())

            return None

        candles = pd.DataFrame(rates)

        if candles.empty:

            return None

        candles["Time"] = pd.to_datetime(

            candles["time"],

            unit="s",

        )

        candles.rename(

            columns={

                "open": "Open",

                "high": "High",

                "low": "Low",

                "close": "Close",

                "tick_volume": "Volume",

            },

            inplace=True,

        )

        return candles[
            [
                "Time",
                "Open",
                "High",
                "Low",
                "Close",
                "Volume",
            ]
        ]

    # -------------------------------------------------

    def disconnect(self):

        mt5.shutdown()

        self.connected = False

        print("Disconnected from MetaTrader 5.")