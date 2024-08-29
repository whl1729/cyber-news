SCRIPT_DIR="$(cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P)"
PROJECT_DIR="${SCRIPT_DIR}/.."

for ((i = 1; i <= 10; i++)); do
    result=$(${SCRIPT_DIR}/run.sh crawler/github/github_device_verification.py)
    if [[ ${result} =~ "verify device ok" ]]; then
        echo "The ${i}th try succeed"
    else
        echo "The ${i}th try fails"
        break
    fi
done
