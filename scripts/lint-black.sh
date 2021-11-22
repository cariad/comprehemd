#!/bin/env bash
set -euo pipefail

if [[ "${CI:=}" == "true" ]]; then
  black . --check --diff
else
  black .
fi
