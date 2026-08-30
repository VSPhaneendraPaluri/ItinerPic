@echo off
SETLOCAL
IF "%~1"=="" (
  set VENV=venv
) ELSE (
  set VENV=%~1
)

echo Creating virtual environment in .\%VENV%...
python -m venv "%VENV%"
IF ERRORLEVEL 1 (
  echo Failed to create virtual environment.
  EXIT /B 1
)

echo Activating venv and installing requirements...
call "%VENV%\Scripts\activate.bat"
python -m pip install --upgrade pip
pip install -r ..\requirements.txt

echo.
echo Done. To activate the venv run:
echo    call "%VENV%\Scripts\activate.bat"
ENDLOCAL
