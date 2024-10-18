@echo off
REM Check if the application is running
tasklist /FI "IMAGENAME eq open_vnc_installer_master.exe" | find /I "open_vnc_installer_master.exe" >nul

if errorlevel 1 (
    REM If the application is not running, delete the lock file
    del "C:\MKS Support Center\lock_file.lock" /Q
)
