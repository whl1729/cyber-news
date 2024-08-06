#!/bin/bash

SCRIPT_DIR="$(cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P)"
PROJECT_DIR="${SCRIPT_DIR}/.."
CRAWLER_DIR="${PROJECT_DIR}/crawler"
CRAWLER_PATH=""
LOG_LEVEL="info"
REMOVE_LOG=0

function show_usage() {
  echo "Usage: $0 path [options]"
  echo "Arguments:"
  echo "  path             Specify a script path to run, such as \"crawler/github/github_login.py\""

  echo "Options:"
  echo "  -h, --help       Show this help message"
  echo "  -l, --log-level LEVEL  Specify log level. Value: debug, info, warn or error"
}

function parse_args() {
  if [[ "$1" != *.py ]]; then
    show_usage
    exit 1
  fi

  CRAWLER_PATH="$1"
  shift

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

  export PYTHONPATH=${PROJECT_DIR}:${CRAWLER_DIR}:${PYTHONPATH}
  python "${PROJECT_DIR}/${CRAWLER_PATH}" -l "${LOG_LEVEL}"
}

main "$@"
