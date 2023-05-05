#!/bin/bash

# Check if a subreddit argument was provided
if [ -z "$1" ]; then
    echo "Error: Please provide a subreddit name"
    exit 1
fi

# Run the Python script with the provided subreddit name as an argument
python main.py $1