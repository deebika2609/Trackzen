@echo off
title TrackZen RailSync - Unified Server
echo ======================================================================
echo           TRACKZEN - RAILSYNC PROTOTYPE (SIH 2026)
echo ======================================================================
echo Starting unified server (Frontend Dashboard + Backend API + Swagger Docs)...
echo.

cd /d "%~dp0"

echo [1/2] Checking Frontend Build...
if not exist "frontend\dist\index.html" (
    echo Building React Frontend...
    cd frontend
    call npm.cmd run build
    cd ..
)

echo [2/2] Launching Unified FastAPI Server on http://localhost:8000 ...
echo.
echo ======================================================================
echo  1. Frontend Dashboard:       http://localhost:8000
echo  2. Interactive API Docs:     http://localhost:8000/docs
echo  3. Backend API Base:         http://localhost:8000/api
echo  4. Health Check:             http://localhost:8000/api/health
echo ======================================================================
echo.
echo Opening browser in 3 seconds...
start "" http://localhost:8000

cd backend
call .\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause
