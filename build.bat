@echo off
ECHO =======================================================
ECHO == Dupe-Finder - Build Script (v2 with PyFiglet fix) ==
ECHO =======================================================
ECHO.

REM 
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO ERROR: Python not found. Please ensure it is installed and added to your system's PATH.
    GOTO:EOF
)

ECHO [1/4] Configuring virtual environment (venv)...
IF NOT EXIST venv (
    ECHO      Creating a new environment...
    python -m venv venv
) ELSE (
    ECHO      Environment already exists.
)

ECHO.
ECHO [2/4] Activating environment and installing dependencies...
CALL venv\Scripts\activate.bat
pip install -r requirements.txt
pip install pyinstaller

ECHO.
ECHO [3/4] Building the executable (.exe) with PyInstaller and data files...

REM The --add-data flag tells PyInstaller to include the pyfiglet fonts.
pyinstaller --onefile --name dupe-finder --add-data "venv\Lib\site-packages\pyfiglet\fonts;pyfiglet\fonts" src/main.py

ECHO.
ECHO [4/4] BUILD COMPLETE!
ECHO.
ECHO You can find the final executable file in:
ECHO %cd%\dist\dupe-finder.exe
ECHO.
ECHO =======================================================
PAUSE