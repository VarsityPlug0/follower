#!/bin/bash

# Instagram Automation Tool Runner
# This script runs the Instagram automation tool with common parameters

echo "Instagram Automation Tool"
echo "========================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.7 or higher and try again"
    exit 1
fi

# Check if required files exist
if [ ! -f "instagram_automation.py" ]; then
    echo "Error: instagram_automation.py not found"
    echo "Please run this script from the project directory"
    exit 1
fi

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Install/update dependencies
echo "Installing/updating dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Warning: Failed to install dependencies"
    echo "Continuing with execution..."
fi

# Run the automation tool
echo "Starting Instagram automation..."
python3 instagram_automation.py "$@"

echo ""
echo "Automation completed."