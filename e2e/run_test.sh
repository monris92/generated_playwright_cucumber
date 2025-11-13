#!/bin/bash
# Simple test runner

cd "$(dirname "$0")"

echo "🚀 Running test: wl_advancesearch_byname_test"
python3 run_test.py
