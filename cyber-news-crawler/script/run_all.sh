#!/bin/bash

SCRIPT_DIR="$(cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P)"
PROJECT_DIR="${SCRIPT_DIR}/.."

cd ${PROJECT_DIR} && ./script/run.sh "crawler/github/trending/github_trending_crawler.py"
cd ${PROJECT_DIR} && ./script/run.sh "crawler/github/event/github_event_crawler.py"
