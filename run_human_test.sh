#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install it to run the test."
    exit 1
fi

# Run the human decoding game script
echo "Starting the Human Babel Game..."
python3 test/human_babel_test.py

# Check if the test ran successfully
if [ $? -eq 0 ]; then
    echo "Test completed successfully."
else
    echo "Test failed. Check the logs for more information."
    exit 1
fi

# Print the final scores
if [ -f "results/final_scores.csv" ]; then
    echo "Final scores recorded in final_scores.csv:"
    tail -n 5 results/final_scores.csv
else
    echo "Error: final_scores.csv not found."
fi

exit 0