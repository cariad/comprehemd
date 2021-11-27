#!/bin/env bash
set -euo pipefail

find . -name "*.sh" -not -path "*/.venv/*" -exec shellcheck -o all --severity style -x {} +
