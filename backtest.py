from core.mt5_connector import connect, disconnect, get_candles
from indicators import calculate_indicators
from strategy import check_signal

from config import (
    TIMEFRAME,
    CANDLE_COUNT
)


def run_backtest():

    if not connect():
        return

    candles = get_candles(
        TIMEFRAME,
        CANDLE_COUNT
    )

    candles = calculate_indicators(candles)

    buy_signals = 0
    sell_signals = 0

    print("\nRunning Backtest...\n")

    for i in range(250, len(candles)):

        sample = candles.iloc[:i + 1]

        result = check_signal(sample)

        if result["signal"] == "BUY":
            buy_signals += 1

        elif result["signal"] == "SELL":
            sell_signals += 1

    print("=" * 40)
    print("BACKTEST SUMMARY")
    print("=" * 40)
    print(f"Candles Tested : {len(candles)}")
    print(f"BUY Signals    : {buy_signals}")
    print(f"SELL Signals   : {sell_signals}")
    print(f"Total Signals  : {buy_signals + sell_signals}")
    print("=" * 40)

    disconnect()


if __name__ == "__main__":
    run_backtest()