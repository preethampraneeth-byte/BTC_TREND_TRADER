from backtesting.trade_simulator import TradeSimulator
from backtesting.performance_report import PerformanceReport
from dashboard.dashboard import Dashboard

sim = TradeSimulator(10000)

sim.open_trade(
    direction="BUY",
    entry_price=100,
    stop_loss=95,
    take_profit=110,
    lot_size=1,
    entry_time="2025-01-01 00:00",
)

sim.update_trade(
    high=111,
    low=99,
    close=110,
    current_time="2025-01-01 01:00",
)

summary = {
    "Total Candles": 2,
    "BUY Signals": 1,
    "SELL Signals": 0,
    "HOLD Signals": 1,
}

performance = PerformanceReport().generate(
    sim.get_trade_history(),
    10000,
    sim.get_balance(),
)

Dashboard().show_complete_dashboard(
    summary,
    performance,
    sim.get_trade_history(),
)