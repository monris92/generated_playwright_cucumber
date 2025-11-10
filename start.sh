#!/bin/bash

# Quick Start Script
# Activates virtual environment and runs the generator

echo "🚀 Quick Start - Playwright to Cucumber BDD Generator"
echo "======================================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found! Run setup first"
    echo "   Command: ./setup_env.sh"
    exit 1
fi

# Check if script exists
if [ ! -f "cucumber_generator.py" ]; then
    echo "❌ cucumber_generator.py not found!"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if playwright is available
if ! command -v playwright &> /dev/null; then
    echo "❌ Playwright not found in virtual environment!"
    echo "🔧 Installing..."
    pip install playwright
    playwright install
fi

echo "🎭 Starting Playwright to Cucumber Generator..."
echo ""
echo "💡 Using Python: $(which python)"
echo ""
python cucumber_generator.py
