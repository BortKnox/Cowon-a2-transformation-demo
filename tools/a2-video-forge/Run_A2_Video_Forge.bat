@echo off
setlocal
title A2 Video Forge
cd /d "%~dp0"

where pyw >nul 2>nul
if %errorlevel%==0 (
    start "" pyw -3 "%~dp0a2_video_forge.pyw"
    exit /b 0
)

where pythonw >nul 2>nul
if %errorlevel%==0 (
    start "" pythonw "%~dp0a2_video_forge.pyw"
    exit /b 0
)

echo Python for Windows was not found.
echo Install Python 3.10 or newer, then run this launcher again.
pause
