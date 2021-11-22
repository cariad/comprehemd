#!/bin/env bash
set -euo pipefail

# This script is never run in CI. This is just a convenience for humans.

./scripts/lint-shell.sh

./scripts/lint-black.sh
./scripts/lint-flake8.sh
./scripts/lint-isort.sh
./scripts/lint-package-types.sh
./scripts/lint-test-types.sh
./scripts/lint-yaml.sh
