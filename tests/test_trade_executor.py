import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import MetaTrader5 as mt5
import config

from core.mt5_connector import MT5Connector
from core.market_data import MarketData
from core.indicators import Indicators
from core.strategy import Strategy
from core.risk_manager import RiskManager
from core.position_size import PositionSizer
from core.trade_executor import TradeExecutor


def main():

    connector = MT5Connector()

    if not connector.connect():
        return

    account = mt5.account_info()
    symbol = mt5.symbol_info(config.SYMBOL)

    market = MarketData()

    df = market.get_candles(
        symbol=config.SYMBOL,
        timeframe=config.TIMEFRAME,
        bars=300,
    )

    df = Indicators().calculate(df)
    df = Strategy().generate_signals(df)

    latest = df.iloc[-1]

    trade = RiskManager().calculate_trade_levels(
        latest["Signal"],
        latest,
    )

    trade = PositionSizer().calculate(
        balance=account.balance,
        trade=trade,
        volume_min=symbol.volume_min,
        volume_max=symbol.volume_max,
        volume_step=symbol.volume_step,
    )

    executor = TradeExecutor()

    request = executor.build_request(trade)

    executor.preview(request)

    connector.disconnect()


if __name__ == "__main__":
    main()