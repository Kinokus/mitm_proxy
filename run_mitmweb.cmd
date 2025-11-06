@echo off
REM Run mitmweb with awesome_cache.py script
REM Web interface will be available at http://127.0.0.1:8081
REM Proxy will listen on 127.0.0.1:8080

echo Starting mitmweb...
echo Web interface: http://127.0.0.1:8081
echo Proxy listening on: 127.0.0.1:8080
echo.

"%APPDATA%\Python\Python312\Scripts\mitmweb.exe" -s awesome_cache.py --set stream_large_bodies=0 --listen-host 127.0.0.1 --listen-port 8080

