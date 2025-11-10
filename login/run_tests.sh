#!/bin/bash

# Enhanced Test Runner for Generated Project
# This script handles virtual environment automatically

echo "🎭 Enhanced Test Runner"
echo "======================"

# Get the directory where this script is located
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$PROJECT_DIR")"
VENV_PYTHON="$PARENT_DIR/venv/bin/python"

echo "📍 Project directory: $PROJECT_DIR"
echo "🐍 Looking for Python at: $VENV_PYTHON"

# Check if parent virtual environment exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo "❌ Virtual environment not found at: $VENV_PYTHON"
    echo "💡 Please run the generator from the parent directory first:"
    echo "   cd '$PARENT_DIR'"
    echo "   ./run_fixed.sh"
    exit 1
fi

# Get feature name from command line or detect from directory
if [ $# -eq 0 ]; then
    # Try to detect feature name from directory structure
    FEATURE_NAME=$(basename "$PROJECT_DIR")
    echo "🔍 Auto-detected feature: $FEATURE_NAME"
else
    FEATURE_NAME="$1"
    echo "🎯 Running feature: $FEATURE_NAME"
fi

# Change to project directory
cd "$PROJECT_DIR"

echo "🚀 Running tests with virtual environment Python..."
echo ""

# Run the Python test runner with the correct Python executable
"$VENV_PYTHON" run_tests.py "$FEATURE_NAME"

echo ""
echo "✅ Test runner finished!"
echo "📊 Check reports/report_${FEATURE_NAME}.html for detailed results"
