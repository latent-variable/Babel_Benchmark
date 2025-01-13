@echo off
REM Check if Python is installed
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python is not installed. Please install it to run the test.
    exit /b 1
)

REM Run the human decoding game script
echo Starting the Human Babel Game...
python test\human_babel_test.py

REM Check if the test ran successfully
IF ERRORLEVEL 1 (
    echo Test failed. Check the logs for more information.
    exit /b 1
) ELSE (
    echo Test completed successfully.
)

REM Print the final scores
IF EXIST results\final_scores.csv (
    echo Final scores recorded in final_scores.csv:
    type results\final_scores.csv | more +%LAST%
) ELSE (
    echo Error: final_scores.csv not found.
)

exit /b 0
