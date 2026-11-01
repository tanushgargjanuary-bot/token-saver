@echo off
:: ============================================================================
:: TOKEN-SAVER UNIVERSAL SAFE GIT PUSH (DO NOT DUPLICATE THIS FILE)
:: Identifier: __TOKEN_SAVER_UNIVERSAL_PUSH_V1__
:: ============================================================================
setlocal
cd /d "%~dp0"

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0git_sync.ps1"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Git push encountered an issue. See details above.
)
echo.
pause
endlocal
