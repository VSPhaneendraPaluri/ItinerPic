@echo off
setlocal

REM ItinerPic local helper script
REM Creates a fresh virtual environment, reinstalls dependencies, and starts the app.

set "PROJECT_ROOT=%~dp0"
set "VENV_DIR=%PROJECT_ROOT%.venv"
set "REQ_FILE=%PROJECT_ROOT%requirements.txt"
set "START_SCRIPT=%PROJECT_ROOT%scripts\run_server.py"

cd /d "%PROJECT_ROOT%"

echo.
echo [1/4] Preparing project folder...
echo Project root: %PROJECT_ROOT%

REM Clean previous environment if it exists.
if exist "%VENV_DIR%" (
    echo [2/4] Removing previous virtual environment...
    rmdir /s /q "%VENV_DIR%"
) else (
    echo [2/4] No previous virtual environment found.
)

REM Create a new environment.
echo [3/4] Creating a fresh virtual environment...
python -m venv "%VENV_DIR%"
if errorlevel 1 (
    echo Failed to create virtual environment.
    exit /b 1
)

REM Activate and install dependencies.
echo [4/4] Installing dependencies and launching app...
call "%VENV_DIR%\Scripts\activate.bat"
python -m pip install --upgrade pip
python -m pip install -r "%REQ_FILE%"
if errorlevel 1 (
    echo Failed to install dependencies.
    exit /b 1
)

echo Starting ItinerPic...
python "%START_SCRIPT%"
if errorlevel 1 (
    echo Failed to start app.
    exit /b 1
)

endlocal
