#!/bin/bash                               # Run with bash (consistent with the rest of the repo)
set -euo pipefail                         # Fail fast: -e stop on error, -u error on unset vars, pipefail propagate pipeline failures

uv sync --extra develop                   # Ensure the uv environment exists and all dev tools are installed

uv run --no-sync ruff format --check .    # Check formatting without modifying files (CI-style formatting gate)
uv run --no-sync ruff check .             # Run Ruff lint checks without autofixing (CI-style lint gate)
uv run --no-sync ty check                 # Run ty static type checking
uv run --no-sync pytest tests/            # Run unit tests in tests/ only
