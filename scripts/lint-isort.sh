#!/bin/env bash
set -euo pipefail

if [[ "${CI:=}" == "true" ]]; then
  isort . --check-only --diff
else
  isort .
fi
