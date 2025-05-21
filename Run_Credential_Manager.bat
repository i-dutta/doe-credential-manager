@echo off
REM Set working directory to the batch file location
cd /d %~dp0

REM Launch the app using portable Python
portable_python\python\python.exe -m streamlit run app\main.py
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo ERROR: Failed to launch the Streamlit app.
    echo Please ensure that the portable_python folder contains all required packages.
    echo Refer to the README for setup instructions.
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b %ERRORLEVEL%
)

echo.
echo Streamlit app closed successfully.
echo Press any key to exit...
pause >nul
