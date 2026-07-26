@echo off

echo Starting XM Global MT5...
start "" "C:\Program Files\XM Global MT5\terminal64.exe"

timeout /t 15 /nobreak >nul

echo Starting BTC Trend Trader...
"C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe" "C:\Users\Administrator\Desktop\BTC_TREND_TRADER\main.py"

pause