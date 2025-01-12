#!/bin/bash

# List of models to test
models=("llama3.2" "phi4" "gemma27b-unlocked" "qwen2.5-coder:32b" "llama3.3" "qwen2.5:72b")

# Set environment variables
export OLLAMA_URL="http://localhost:11434"

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed. Please install it to run the test."
    exit 1
fi

# Loop through each model and run the test
for model in "${models[@]}"
do
    export OLLAMA_MODEL="$model"
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