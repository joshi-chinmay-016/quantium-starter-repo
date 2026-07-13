#!/bin/bash
# Activate virtual environment (checks both venv and .venv)
if [ -d "./venv" ]; then
  source ./venv/Scripts/activate
elif [ -d "./.venv" ]; then
  source ./.venv/Scripts/activate
else
  echo "Virtual environment not found. Exiting."
  exit 1
fi

# Run pytest and capture exit code
pytest
TEST_RESULT=$?

# Deactivate virtual environment (optional)
if command -v deactivate >/dev/null 2>&1; then
  deactivate
fi

# Exit with appropriate code
if [ $TEST_RESULT -eq 0 ]; then
  exit 0
else
  exit 1
fi
