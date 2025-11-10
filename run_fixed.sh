#!/bin/bash

# Quick Start Script - Run the Cucumber Generator with Virtual Environment
# Use this if you get "playwright not found" errors

echo "🎭 Playwright to Cucumber BDD Generator"
echo "========================================"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📍 Working directory: $SCRIPT_DIR"

# Check for virtual environment
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "🔧 Running setup..."
    if [ -f "setup_env.sh" ]; then
        ./setup_env.sh
    else
        echo "❌ setup_env.sh not found!"
        echo "💡 Please run: pip install -r requirements.txt && playwright install"
        exit 1
    fi
fi

# Set paths
VENV_PYTHON="$SCRIPT_DIR/venv/bin/python"

echo "🔍 Using Python: $VENV_PYTHON"

# Verify Python exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo "❌ Python not found in virtual environment!"
    exit 1
fi

# Verify Playwright is available
if ! "$VENV_PYTHON" -m playwright --help > /dev/null 2>&1; then
    echo "❌ Playwright not found!"
    echo "🔧 Installing Playwright..."
    "$VENV_PYTHON" -m pip install playwright
    "$VENV_PYTHON" -m playwright install

    if "$VENV_PYTHON" -m playwright --help > /dev/null 2>&1; then
        echo "✅ Playwright installed successfully!"
    else
        echo "❌ Failed to install Playwright. Check your internet connection."
        exit 1
    fi
fi

# Run the generator
echo ""
echo "🚀 Starting Cucumber Generator..."
echo ""
"$VENV_PYTHON" cucumber_generator.py

echo ""
echo "✅ Generator finished! Check your project folder for generated tests."
