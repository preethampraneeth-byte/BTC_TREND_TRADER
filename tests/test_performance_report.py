from backtesting.trade_simulator import TradeSimulator
from backtesting.performance_report import PerformanceReport

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

report = PerformanceReport()

results = report.generate(
    trades=sim.get_trade_history(),
    starting_balance=10000,
    ending_balance=sim.get_balance(),
)

print(results)