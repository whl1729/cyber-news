#!/bin/bash

SCRIPT_DIR="$(cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P)"
PROJECT_DIR="${SCRIPT_DIR}/.."
VENV_DIR="${PROJECT_DIR}/venv"

# Create virtual environment if it doesn't exist
if [ ! -d "${VENV_DIR}" ]; then
    echo "Creating virtual environment..."
    python3.14 -m venv "${VENV_DIR}"
fi

# Activate virtual environment
source "${VENV_DIR}/bin/activate"

# Install Python libraries and tools
pip install -r "${PROJECT_DIR}/requirements.txt"

# Initialize pre-commit (skip if it fails due to network issues)
if command -v pre-commit &> /dev/null; then
    pre-commit install || echo "Warning: pre-commit install failed, skipping..."
    pre-commit install -t commit-msg || true
    pre-commit install --install-hooks || true
fi

echo "Installation complete. To activate the virtual environment, run:"
echo "source venv/bin/activate"
