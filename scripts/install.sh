#!/bin/bash
# Quick installation script for SaaS Planz MVP

set -e

echo "=========================================="
echo "SaaS Planz MVP - Installation"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version || { echo "Python 3 not found. Please install Python 3.10+"; exit 1; }
echo "✅ Python 3 found"
echo ""

# Install dependencies
echo "Installing dependencies..."
echo "This may take a few minutes..."
echo ""

pip3 install pandas==2.1.4 ortools==9.8.3296 streamlit==1.31.1 pytest==7.4.4 pytest-cov==4.1.0

echo ""
echo "=========================================="
echo "✅ Installation Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Test models: python3 test_models_only.py"
echo "2. Test parser: python3 manual_test.py"
echo "3. Launch app: streamlit run app.py"
echo ""
echo "For more info, see README.md"
echo ""
