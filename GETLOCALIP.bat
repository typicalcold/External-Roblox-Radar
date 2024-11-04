@echo off
setlocal EnableDelayedExpansion
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr "IPv4"') do (
    set ip=%%i
    set ip=!ip: =!
)
echo Your local IP address is: !ip!
pause
