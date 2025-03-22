#!/bin/bash

# Exit on error
set -e

echo "===== LMMS-Claude-MCP Installer ====="
echo "This script will install LMMS-Claude-MCP and its dependencies."

# Check if Python is installed
if command -v python3 &>/dev/null; then
    PYTHON="python3"
elif command -v python &>/dev/null; then
    PYTHON="python"
else
    echo "Error: Python 3 is required but not found. Please install Python 3 first."
    exit 1
fi

echo "Using Python: $($PYTHON --version)"

# Check for uv or pip
if command -v uv &>/dev/null; then
    echo "uv found, using uv for installation"
    INSTALLER="uv pip"
elif command -v pip3 &>/dev/null; then
    echo "pip3 found, using pip3 for installation"
    INSTALLER="pip3"
elif command -v pip &>/dev/null; then
    echo "pip found, using pip for installation"
    INSTALLER="pip"
else
    echo "Error: Neither uv nor pip is installed. Please install either package manager."
    exit 1
fi

# Install in development mode
echo "Installing LMMS-Claude-MCP..."
$INSTALLER install -e .

# Verify installation
echo "Verifying installation..."
if command -v lmms-mcp &>/dev/null; then
    echo "✅ Installation successful! You can now use lmms-mcp"
    echo ""
    echo "Basic usage: lmms-mcp"
    echo "For help: lmms-mcp --help"
    echo ""
    echo "Next steps:"
    echo "1. Configure Claude or Cursor to use LMMS-MCP (see README.md)"
    echo "2. Launch LMMS before interacting with Claude"
else
    echo "⚠️ Installation may have succeeded, but lmms-mcp command was not found in PATH."
    echo "You may need to:"
    echo "1. Add your Python bin directory to PATH"
    echo "2. Use python -m lmms_mcp.cli instead of lmms-mcp"
fi