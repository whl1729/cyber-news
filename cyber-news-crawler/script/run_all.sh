#!/bin/bash

SCRIPT_DIR="$(cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P)"
PROJECT_DIR="${SCRIPT_DIR}/.."

cd ${PROJECT_DIR} && ./script/run.sh "crawler/github/github_trending_crawler.py"
