@echo off
title TrackZen RailSync - Dual Dev Mode
echo ======================================================================
echo           TRACKZEN - RAILSYNC DUAL DEV MODE (SIH 2026)
echo ======================================================================
echo.
cd /d "%~dp0"

echo Starting FastAPI Backend on http://localhost:8000 ...
start "TrackZen Backend" cmd /k "cd /d ""%~dp0backend"" && .\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

timeout /t 2 /nobreak >nul

echo Starting Vite Frontend on http://localhost:5173 ...
start "TrackZen Frontend" cmd /k "cd /d ""%~dp0frontend"" && npm.cmd run dev"

timeout /t 3 /nobreak >nul
start "" http://localhost:5173
echo.
echo Both servers started!
