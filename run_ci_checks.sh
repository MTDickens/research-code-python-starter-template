#!/bin/bash
set -euo pipefail

./run_autoformat.sh
uv run --no-sync mypy .
uv run --no-sync pytest . --pylint -m pylint --pylint-rcfile=.pylintrc
uv run --no-sync pytest tests/
