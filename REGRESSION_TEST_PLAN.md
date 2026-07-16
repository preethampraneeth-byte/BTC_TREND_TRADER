# BTC Trend Trader Professional

# Regression Test Plan

## Purpose

This document defines the regression tests that must be completed before creating a Release Candidate.

The objective is to verify that every major feature continues to function correctly after code changes while ensuring that trading behaviour remains unchanged.

---

# Test Environment

## Python

* Virtual Environment Enabled

## Platform

* Windows
* MetaTrader 5

## Broker

* XM

## Symbol

* BTCUSD#

## Trading Mode

* Paper Trading

---

# RT-001 — Application Startup

## Objective

Verify successful application startup.

### Command

```bash
python main.py paper
```

### Expected Result

* Application starts successfully.
* Startup banner displayed.
* Startup diagnostics displayed.
* No exceptions.

Status

* [ ] PASS
* [ ] FAIL

---

# RT-002 — Invalid Mode

## Command

```bash
python main.py invalid
```

### Expected Result

* Invalid execution mode message displayed.
* Application exits cleanly.
* Exit code 1 returned.

Status

* [ ] PASS
* [ ] FAIL

---

# RT-003 — Configuration Validation

Temporarily set an invalid configuration.

Example:

```python
TIMEFRAME = "M2"
```

### Expected Result

* Configuration validation fails.
* Clear error message displayed.
* Application exits before connecting to MT5.

Restore the original configuration after testing.

Status

* [ ] PASS
* [ ] FAIL

---

# RT-004 — Backtest Execution

## Command

```bash
python main.py
```

### Verify

* Historical data loads.
* Strategy executes.
* Trades generated.
* Performance report displayed.
* Analytics displayed.
* No exceptions.

Status

* [ ] PASS
* [ ] FAIL

---

# RT-005 — MT5 Connection

Verify:

* MT5 initializes successfully.
* Login succeeds.
* Symbol is available.
* No connection errors.

Status

* [ ] PASS
* [ ] FAIL

---

# RT-006 — Market Processing

Verify:

* New candles detected.
* Duplicate candles ignored.
* Signals generated correctly.
* Runtime continues operating.

Status

* [ ] PASS
* [ ] FAIL

---

# RT-007 — Heartbeat

Run paper trading for at least two minutes.

Verify:

* Heartbeat printed every 60 seconds.
* Balance displayed.
* Equity displayed.
* Open trades displayed.
* Last processed candle displayed.
* Uptime increases correctly.

Status

* [ ] PASS
* [ ] FAIL

---

# RT-008 — Position Sizing

Verify that different stop-loss distances produce different calculated lot sizes while maintaining the configured risk percentage.

Status

* [ ] PASS
* [ ] FAIL

---

# RT-009 — Break-even

Verify:

* Break-even activates at the configured threshold.
* Stop loss moves correctly.
* Trade remains valid.

Status

* [ ] PASS
* [ ] FAIL

---

# RT-010 — ATR Trailing Stop

Verify:

* Trailing stop activates.
* Stop follows favourable price movement.
* Stop never moves backwards.

Status

* [ ] PASS
* [ ] FAIL

---

# RT-011 — Partial Profit Taking

Verify:

* Partial exits occur at configured R levels.
* Remaining position size is correct.
* Final position closes correctly.

Status

* [ ] PASS
* [ ] FAIL

---

# RT-012 — Time Exit

Verify:

* Trade closes after the configured maximum number of bars.
* Exit reason is recorded correctly.

Status

* [ ] PASS
* [ ] FAIL

---

# RT-013 — Analytics

Verify:

* Session summary is correct.
* Exit reasons are recorded.
* Bars held statistics are correct.
* Trade duration statistics are correct.
* Profit factor is calculated.
* Recovery factor is calculated.
* Drawdown statistics are correct.

Status

* [ ] PASS
* [ ] FAIL

---

# RT-014 — CSV Logging

Verify that completed trades are written correctly.

Check:

* Entry time
* Exit time
* Direction
* Prices
* Profit
* Exit reason
* Bars held
* Trade duration

Status

* [ ] PASS
* [ ] FAIL

---

# RT-015 — Clean Shutdown

Stop the application using Ctrl+C.

Verify:

* Shutdown message displayed.
* Session summary printed once.
* MT5 disconnected.
* Application exits normally.

Status

* [ ] PASS
* [ ] FAIL

---

# Long-Run Validation

Run paper trading continuously.

Minimum duration:

* 2 hours

Verify:

* No crashes.
* No unexpected exceptions.
* Stable heartbeat.
* Stable MT5 connection.
* Stable memory usage.

Status

* [ ] PASS
* [ ] FAIL

---

# Pre-Release Validation

Before Sprint 12 begins:

* Complete at least 100 paper trades.
* Review all analytics.
* Review CSV output.
* Confirm no unexpected runtime behaviour.
* Freeze trading logic.

Status

* [ ] PASS
* [ ] FAIL

---

# Release Approval

The Release Candidate may be created only if:

* All regression tests pass.
* No critical defects remain.
* Documentation is current.
* Git working tree is clean.
* Latest changes are pushed to the remote repository.

Release Candidate Tag:

```
v4.5-rc1
```

Approved By:

---

Date:

---
