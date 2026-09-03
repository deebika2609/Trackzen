@echo off
title TrackZen RailSync - Instant Live Public Tunnel
echo ======================================================================
echo           TRACKZEN - RAILSYNC LIVE PUBLIC TUNNEL (SIH 2026)
echo ======================================================================
echo.
cd /d "%~dp0"

echo [1/2] Launching Backend Unified Server in Background...
start "TrackZen Server (Port 8000)" /min cmd /c "cd /d ""%~dp0backend"" && .\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000"

timeout /t 3 /nobreak >nul

echo [2/2] Generating Instant Live Public HTTPS URL...
echo ======================================================================
echo  Your live public link is being generated below!
echo  Anyone in the world (judges/evaluators) can open this link on any device.
echo ======================================================================
echo.

call npx.cmd -y localtunnel --port 8000 --open
pause
