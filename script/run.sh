#!/bin/bash

WORKING_DIR="$(pwd -P)"
SCRIPT_DIR="$(cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P)"
PROJECT_DIR="${SCRIPT_DIR}/.."
NEWS_DIR="${PROJECT_DIR}/news"
INPUT_PATH=""
LOG_LEVEL="info"
REMOVE_LOG=0

function show_usage() {
  echo "Usage: $0 path [options]"
  echo "Options:"
  echo "  -h, --help             Show this help message"
  echo "  -l, --log-level LEVEL  Specify log level. Value: debug, info, warn or error. Default: info"
  echo "  -p, --path PATH        Specify a relative script path to run, such as \"news/crawler/news_crawler.py\""
  echo "  -r, --remove-log       Specify whether to remove log before running input script. 0: don't remove; 1: remove. Default: 0"
}

function parse_args() {
  while [[ "$#" -gt 0 ]]; do
    case $1 in
      -h|--help)
        show_usage
        exit
        ;;
      -l|--log-level)
        LOG_LEVEL="$2"
        shift
        ;;
      -p|--path)
        INPUT_PATH="$2"
        shift
        ;;
      -r|--remove-log)
        REMOVE_LOG=1
        ;;
      *)
        echo "Unknown parameter passed: $1"
        show_usage
        exit 1
        ;;
    esac
    shift
  done
}

function main() {
  parse_args "$@"

  if ((${REMOVE_LOG} == 1)); then
    rm ${LOG_PATH}
    echo "Successfully removed log"
  fi

  if [[ -d "${PROJECT_DIR}/.venv/bin" ]]; then
    source "${PROJECT_DIR}/.venv/bin/activate"
  fi

  export PYTHONPATH=${NEWS_DIR}:${PROJECT_DIR}:${PYTHONPATH}
  if [[ "${INPUT_PATH}" != "" ]]; then
    python "${WORKING_DIR}/${INPUT_PATH}" -l "${LOG_LEVEL}"
  else
    python "${PROJECT_DIR}/news/crawler/news_crawler.py" -l "${LOG_LEVEL}"
  fi
}

main "$@"
