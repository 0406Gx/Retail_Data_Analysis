@echo off
setlocal EnableExtensions
pushd "%~dp0"

chcp 65001 >nul

echo ==============================================
echo   Retail Sales Data Analysis
echo ==============================================
echo.

set "VENV_PYTHON=%~dp0..\.venv\Scripts\python.exe"

if not exist "%VENV_PYTHON%" (
    echo Error: Virtual environment not found at %VENV_PYTHON%
    echo Please create the virtual environment first.
    pause
    popd
    exit /b 1
)

echo Using Python: %VENV_PYTHON%
echo.

echo Running analysis...
echo.
cd code
"%VENV_PYTHON%" sales_analysis.py

echo.
echo ==============================================
echo   Analysis completed! Results saved to img folder.
echo ==============================================
echo.
pause
popd
