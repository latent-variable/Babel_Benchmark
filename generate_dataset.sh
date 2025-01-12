#!/bin/bash

# Set environment variables
export OPENAI_API_KEY="your_openai_api_key_here"
export OLLAMA_HOST="http://localhost:11434"
export USE_OLLAMA=true
export MODEL="llama3.2"
export NUM_SENTENCES=100

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed. Please install Python3 to run this script."
    exit 1
fi

# Run generate_sentence.py to generate random sentences
echo "Running generate_sentence.py..."
python3 src/generate_sentence.py
if [ $? -ne 0 ]; then
    echo "Error running generate_sentence.py."
    exit 1
fi

# Run babel_encoding.py to encode the sentences
echo "Running babel_encoding.py..."
python3 src/babel_encoding.py
if [ $? -ne 0 ]; then
    echo "Error running babel_encoding.py."
    exit 1
fi

echo "All tasks completed successfully."
