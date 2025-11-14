#!/bin/bash
# Simple test runner

cd "$(dirname "$0")"

echo "🚀 Running test: wl_advancesearch_deceased_in_cemetery"
python3 run_test.py
