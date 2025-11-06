@echo off
REM Install mitmproxy certificate for Chrome, Edge, and other Windows browsers
echo.
echo ========================================
echo  Install mitmproxy Certificate 
echo  for Chrome/Edge/Windows Browsers
echo ========================================
echo.

set CERT_FILE=%USERPROFILE%\.mitmproxy\mitmproxy-ca-cert.cer

if not exist "%CERT_FILE%" (
    echo ERROR: Certificate file not found!
    echo Please run mitmweb at least once to generate the certificate.
    echo.
    pause
    exit /b 1
)

echo Installing certificate to Windows Trusted Root CA store...
echo.
echo You will see a security warning - click YES to install.
echo.
pause

certutil -addstore -user Root "%CERT_FILE%"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo  SUCCESS! Certificate installed.
    echo ========================================
    echo.
    echo Chrome, Edge, and other browsers should now trust mitmproxy.
    echo Please restart your browser if it's already open.
    echo.
) else (
    echo.
    echo ========================================
    echo  FAILED to install certificate.
    echo ========================================
    echo.
    echo Try running this script as Administrator.
    echo.
)

pause

