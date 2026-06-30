"""
BTC Trend Trader v3.2
Parameter Optimizer

Milestone 3.2.1

Tests optimization framework only.
No backtesting yet.
"""

import config

from core.market_data import MarketData
from core.indicators import Indicators


def main():

    print("=" * 60)
    print("      BTC TREND TRADER PARAMETER OPTIMIZER")
    print("=" * 60)

    # -------------------------------------------------
    # Load Data
    # -------------------------------------------------

    print("\nLoading historical data...")

    market = MarketData()

    candles = market.load_from_csv(
        config.CSV_DATA_FILE
    )

    print(f"Loaded {len(candles)} candles.")

    # -------------------------------------------------
    # Calculate Indicators
    # -------------------------------------------------

    print("\nCalculating indicators...")

    indicators = Indicators()

    candles = indicators.calculate(candles)

    print("Indicators calculated successfully.")

    # -------------------------------------------------
    # Save Original Setting
    # -------------------------------------------------

    original_adx = config.ADX_THRESHOLD

    print("\nTesting ADX values...\n")

    # -------------------------------------------------
    # Optimization Loop
    # -------------------------------------------------

    for adx in config.OPTIMIZE_ADX_VALUES:

        config.ADX_THRESHOLD = adx

        print(f"Testing ADX_THRESHOLD = {adx}")

    # -------------------------------------------------
    # Restore Original Setting
    # -------------------------------------------------

    config.ADX_THRESHOLD = original_adx

    print("\nOptimization framework test completed.")
    print(f"ADX_THRESHOLD restored to {config.ADX_THRESHOLD}")


if __name__ == "__main__":
    main()