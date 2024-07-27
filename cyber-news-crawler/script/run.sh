#!/bin/bash

SCRIPT_DIR="$(cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P)"
PROJECT_DIR="${SCRIPT_DIR}/.."
CRAWLER_DIR="${PROJECT_DIR}/crawler"
CRAWLER_PATH=""
NAME=""

function show_usage() {
  echo "Usage: $0 path [options]"
  echo "Arguments:"
  echo "  path             Specify a script path to run, such as \"crawler/github/github_login.py\""

  echo "Options:"
  echo "  -h, --help       Show this help message"
  echo "  -n, --name NAME  Specify a name"
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
      -n|--name)
        NAME="$2"
        shift
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

  if [[ -d "${PROJECT_DIR}/.venv" ]]; then
    source "${PROJECT_DIR}/.venv/Scripts/activate"
  fi

  export PYTHONPATH=${PROJECT_DIR}:${CRAWLER_DIR}:${PYTHONPATH}
  python "${PROJECT_DIR}/${CRAWLER_PATH}"
}

main "$@"
