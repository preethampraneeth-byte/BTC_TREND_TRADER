"""
BTC Trend Trader v1.0
MT5 Connection Module
"""

import MetaTrader5 as mt5
import config


class MT5Connector:
    """Handles connection to MetaTrader 5."""

    def __init__(self):
        self.connected = False

    def connect(self):
        """Initialize and log in to MetaTrader 5."""

        # Initialize MT5
        if config.MT5_PATH:
            initialized = mt5.initialize(path=config.MT5_PATH)
        else:
            initialized = mt5.initialize()

        if not initialized:
            print("❌ Failed to initialize MetaTrader 5")
            print("Error:", mt5.last_error())
            return False

        # Login
        authorized = mt5.login(
            login=config.LOGIN,
            password=config.PASSWORD,
            server=config.SERVER
        )

        if not authorized:
            print("❌ Login failed")
            print("Error:", mt5.last_error())
            mt5.shutdown()
            return False

        self.connected = True

        print("✅ Connected to MetaTrader 5")

        return True

    def account_info(self):
        """Print account information."""

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

    def symbol_info(self, symbol):
        """Verify the trading symbol exists."""

        info = mt5.symbol_info(symbol)

        if info is None:
            print(f"❌ Symbol '{symbol}' not found.")
            return False

        if not info.visible:
            mt5.symbol_select(symbol, True)

        print(f"✅ Symbol '{symbol}' is available.")

        return True

    def disconnect(self):
        """Close MT5 connection."""

        mt5.shutdown()
        self.connected = False

        print("Disconnected from MetaTrader 5.")