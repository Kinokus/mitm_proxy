@echo off
REM Run mitmdump with awesome_cache.py script (command-line mode, no UI)
REM Proxy will listen on 127.0.0.1:8080

echo Starting mitmdump...
echo Proxy listening on: 127.0.0.1:8080
echo Press Ctrl+C to stop
echo.

"%APPDATA%\Python\Python312\Scripts\mitmdump.exe" -s awesome_cache.py --set stream_large_bodies=0 --listen-host 127.0.0.1 --listen-port 8080

