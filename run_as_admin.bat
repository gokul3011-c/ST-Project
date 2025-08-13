@echo off
title USB Physical Security - Administrator Launcher
echo ========================================
echo    USB Physical Security Launcher
echo ========================================
echo.
echo This launcher will start the USB Physical Security
echo application with administrator privileges.
echo.
echo Note: You may be prompted by Windows UAC
echo to allow administrator access.
echo.

REM Check if already running as admin
net session >nul 2>&1
if %errorLevel% equ 0 (
    echo Already running as administrator.
    echo Starting application...
    echo.
    python usb_physical_security.py
) else (
    echo Requesting administrator privileges...
    echo.
    
    REM Try to run the Python script directly with admin rights
    powershell -Command "Start-Process python -ArgumentList 'usb_physical_security.py' -Verb RunAs -WorkingDirectory '%~dp0'"
    
    if %errorLevel% equ 0 (
        echo Application started with administrator privileges.
    ) else (
        echo Failed to start with administrator privileges.
        echo.
        echo Please try one of these alternatives:
        echo 1. Right-click on usb_physical_security.py and select "Run as administrator"
        echo 2. Run PowerShell as administrator and execute: python usb_physical_security.py
        echo.
        pause
    )
)

echo.
echo Launcher completed.
pause
