#!/bin/bash

# List of models to test
models=("deepseek/deepseek-chat" "llama3.2" "phi4" "gemma27b-unlocked" "qwen2.5-coder:32b" "llama3.3" "qwen2.5:72b")

# Load the .env file if it exists
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Check if required environment variables are set
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "Error: OPENROUTER_API_KEY is not set. Please set it in your .env file."
    exit 1
fi

# Set default environment variables
export OLLAMA_URL="http://localhost:11434"
export USE_OLLAMA="False"


# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install it to run the test."
    exit 1
fi

# Loop through each model and run the test
for model in "${models[@]}"; do
    export MODEL="$model"
    echo "Running test_babel.py with model: $model..."
    python3 test/test_babel.py

    # Check if the test ran successfully
    if [ $? -eq 0 ]; then
        echo "Test completed successfully for model: $model."
    else
        echo "Test failed for model: $model. Check the logs for more information."
        exit 1
    fi

    # Print final score
    if [ -f "results/final_scores.csv" ]; then
        echo "Final score for model $model recorded in final_scores.csv:"
        tail -n 1 results/final_scores.csv
    else
        echo "Error: final_scores.csv not found for model $model."
    fi
done

exit 0
