@echo off
echo Attempting to disable USB storage devices...
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script requires administrator privileges.
    echo Please run as administrator.
    pause
    exit /b 1
)

REM Disable USB storage devices
REG ADD "HKLM\SYSTEM\CurrentControlSet\Services\USBSTOR" /v Start /t REG_DWORD /d 4 /f >nul 2>&1
if %errorLevel% equ 0 (
    echo SUCCESS: USB storage devices have been disabled.
    echo.
    echo Note: This change affects all USB storage devices.
    echo USB keyboards and mice will continue to work normally.
    echo.
    echo To re-enable USB storage, run the unblock_usb.bat file.
    echo.
    echo Operation completed successfully!
    echo.
    echo Press any key to close this window...
    pause >nul
    exit /b 0
) else (
    echo ERROR: Failed to disable USB storage devices.
    echo Error code: %errorLevel%
    echo.
    echo Possible causes:
    echo - Insufficient permissions
    echo - Registry key not accessible
    echo - System policy restrictions
)

echo.
pause
