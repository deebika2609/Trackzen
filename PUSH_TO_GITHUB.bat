@echo off
setlocal enabledelayedexpansion
title Push TrackZen to GitHub (Automatic 1-Click)
echo ======================================================================
echo           PUSH TRACKZEN RAILSYNC PROTOTYPE TO GITHUB
echo ======================================================================
echo.
cd /d "%~dp0"

echo [1/3] Preparing git commits...
git add .
git commit -m "TrackZen RailSync Prototype SIH 2026 Ready" >nul 2>&1
git branch -M main

echo.
echo [2/3] If you haven't created an empty repository on GitHub yet:
echo       Opening https://github.com/new in your browser now...
start "" https://github.com/new

echo.
echo ======================================================================
echo Instructions on GitHub:
echo  1. Type repository name (e.g. railsync-prototype)
echo  2. Leave it Public
echo  3. Do NOT check "Add a README file" or .gitignore
echo  4. Click "Create repository"
echo  5. Copy the repository URL (e.g. https://github.com/iamdeebika/railsync-prototype.git)
echo ======================================================================
echo.
set /p REPO_URL="Paste your GitHub Repository URL here and press Enter: "

if "%REPO_URL%"=="" (
    echo [ERROR] No URL provided. Please re-run this script when ready.
    pause
    exit /b
)

echo.
echo [3/3] Pushing all code to GitHub (%REPO_URL%)...
git remote remove origin >nul 2>&1
git remote add origin %REPO_URL%
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ======================================================================
    echo  [SUCCESS] All code has been pushed to GitHub successfully!
    echo ======================================================================
    echo  Next Step: Go to https://render.com and deploy in 1 click!
    echo ======================================================================
) else (
    echo.
    echo [NOTE] If GitHub asked you to log in, please complete the sign-in in your browser window.
)

pause
