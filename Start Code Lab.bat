@echo off
rem Double-click this file to open the Code Lab on Windows — no typing needed.
cd /d "%~dp0"
echo Starting the Code Lab...  (close this window when you are done)
echo.
where py >nul 2>nul
if %errorlevel%==0 (
    py code_lab\code_lab.py
) else (
    python code_lab\code_lab.py
)
echo.
echo The Code Lab has stopped. You can close this window.
pause
