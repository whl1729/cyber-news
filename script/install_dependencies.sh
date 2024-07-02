#!/bin/bash

SCRIPT_DIR="$(cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P)"
PROJECT_DIR="${SCRIPT_DIR}/.."
CRAWLER_DIR="${PROJECT_DIR}/cyber-news-crawler/"

# Install Python libraries and tools
pip install -r "${CRAWLER_DIR}/requirements.txt"

# Initialize pre-commit
cd "${PROJECT_DIR}"

pre-commit install
pre-commit install -t commit-msg
pre-commit install --install-hooks
