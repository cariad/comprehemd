#!/bin/env bash
set -euo pipefail

pytest -vv

if [[ "${CI:=}" == "true" ]]; then
  echo "Skipping documentation press in CI."
else
  python -m edition docs/source.md README.md       --press markdown
  python -m edition docs/source.md docs/index.html --press html
fi
