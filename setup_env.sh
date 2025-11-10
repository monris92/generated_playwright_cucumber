#!/bin/bash

# Environment Setup Script
# Sets up virtual environment and installs all dependencies

echo "🎭 Playwright to Cucumber BDD Generator - Environment Setup"
echo "==========================================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_warning "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        print_success "Virtual environment created"
    else
        print_error "Failed to create virtual environment"
        exit 1
    fi
else
    print_success "Virtual environment already exists"
fi

# Activate virtual environment
print_success "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_success "Upgrading pip..."
pip install --upgrade pip

# Install requirements
if [ -f "requirements.txt" ]; then
    print_success "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt

    if [ $? -eq 0 ]; then
        print_success "Dependencies installed successfully"
    else
        print_error "Failed to install dependencies"
        exit 1
    fi
else
    print_error "requirements.txt not found"
    exit 1
fi

# Install Playwright browsers
print_success "Installing Playwright browsers..."
playwright install

# Check for system dependencies
print_warning "Checking system dependencies..."
echo "If you see errors about missing dependencies, run:"
echo "sudo playwright install-deps"

print_success "Setup completed!"
echo ""
echo "📋 How to use:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run generator: python cucumber_generator.py"
echo "3. Or use quick start: ./run_fixed.sh"
echo ""
echo "🎉 Happy Testing!"
