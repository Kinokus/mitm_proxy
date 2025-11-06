@echo off
REM Open Firefox certificate settings directly
echo Opening Firefox certificate settings...
echo.
echo If Firefox doesn't open automatically, manually go to:
echo about:preferences#privacy
echo.
echo Then scroll to "Certificates" and click "View Certificates"
echo.

start firefox "about:preferences#privacy"

