@echo off
echo Attempting to enable USB storage devices...
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script requires administrator privileges.
    echo Please run as administrator.
    pause
    exit /b 1
)

REM Enable USB storage devices
REG ADD "HKLM\SYSTEM\CurrentControlSet\Services\USBSTOR" /v Start /t REG_DWORD /d 3 /f >nul 2>&1
if %errorLevel% equ 0 (
    echo SUCCESS: USB storage devices have been enabled.
    echo.
    echo Note: USB storage devices should now be accessible.
    echo You may need to reconnect USB devices for changes to take effect.
    echo.
    echo To disable USB storage again, run the block_usb.bat file.
    echo.
    echo Operation completed successfully!
    echo.
    echo Press any key to close this window...
    pause >nul
    exit /b 0
) else (
    echo ERROR: Failed to enable USB storage devices.
    echo Error code: %errorLevel%
    echo.
    echo Possible causes:
    echo - Insufficient permissions
    echo - Registry key not accessible
    echo - System policy restrictions
)

echo.
pause
