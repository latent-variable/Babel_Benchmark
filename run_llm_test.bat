@echo off
REM List of models to test
setlocal enabledelayedexpansion
set models="meta-llama/llama-3.1-405b-instruct" "mistralai/mistral-large-2411" "google/gemma-2-27b-it" "openai/gpt-4o-mini" "openai/gpt-4o-2024-11-20" "anthropic/claude-3.5-sonnet" "deepseek/deepseek-chat" "llama3.2" "phi4" "gemma27b-unlocked" "qwen2.5-coder:32b" "llama3.3" "qwen2.5:72b"

REM Load the .env file if it exists
if exist .env (
    for /f "tokens=1,* delims==" %%i in ('findstr /v "^#" .env') do (
        set %%i=%%j
    )
)

REM Check if required environment variables are set
if "%OPENROUTER_API_KEY%"=="" (
    echo Error: OPENROUTER_API_KEY is not set. Please set it in your .env file.
    exit /b 1
)

REM Set default environment variables
set OLLAMA_URL=http://localhost:11434
set USE_OLLAMA=False

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install it to run the test.
    exit /b 1
)

REM Loop through each model and run the test
for %%m in (%models%) do (
    set MODEL=%%m
    echo Running test\llm_babel_test.py with model: %%m...
    python test\llm_babel_test.py

    REM Check if the test ran successfully
    if errorlevel 1 (
        echo Test failed for model: %%m. Check the logs for more information.
        exit /b 1
    ) else (
        echo Test completed successfully for model: %%m.
    )

    REM Print final score
    if exist results\final_scores.csv (
        echo Final score for model %%m recorded in final_scores.csv:
        type results\final_scores.csv | more +%LAST%
    ) else (
        echo Error: final_scores.csv not found for model %%m.
    )
)

exit /b 0
