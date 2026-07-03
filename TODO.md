# BTC Trend Trader Professional v4

## Pending Fixes

### Analytics

- Fix TradeDuration analytics.
  - Current output always returns zero durations.
  - Verify duration calculation from entry_time and exit_time.
  - Add unit tests covering pandas.Timestamp values.