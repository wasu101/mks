@echo off
setlocal

REM Get the computer name from the argument
set COMPUTER_NAME=%1

REM Check if COMPUTER_NAME is provided
if "%COMPUTER_NAME%"=="" (
    echo Error: Computer name not provided.
    exit /b 1
)

REM Define the predefined HOST
set HOST=W240303NN

REM Path to TightVNC executable
set VNC_PATH="C:\Program Files\TightVNC\tvnviewer.exe"

REM Set the password
set PASSWORD=admin*

REM Copy the COMPUTER_NAME to the clipboard
echo %COMPUTER_NAME% | clip

REM Launch TightVNC with the HOST and provided COMPUTER_NAME
start "" %VNC_PATH% %HOST%:%COMPUTER_NAME% -password %PASSWORD%

endlocal
