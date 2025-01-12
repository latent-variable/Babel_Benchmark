@echo off

REM Set environment variables
set OPENAI_API_KEY=your_openai_api_key_here
set OLLAMA_HOST=http://localhost:11434
set USE_OLLAMA=true
set MODEL="llama-3.3-abliterated"
set NUM_SENTENCES=100

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python to run this script.
    exit /b
)

REM Run generate_sentence.py to generate random sentences
echo Running generate_sentence.py...
python src/generate_sentence.py
if %ERRORLEVEL% NEQ 0 (
    echo Error running generate_sentence.py.
    exit /b
)

REM Run babel_encoding.py to translate the sentences
echo Running babel_encoding.py...
python scr/babel_translation.py
if %ERRORLEVEL% NEQ 0 (
    echo Error running babel_encoding.py.
    exit /b
)

echo All tasks completed successfully.
pause
