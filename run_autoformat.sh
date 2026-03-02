#!/bin/bash                              # Run with bash (consistent with the rest of the repo)
set -euo pipefail                        # Fail fast: -e stop on error, -u error on unset vars, pipefail propagate pipeline failures

uv sync --extra develop                  # Create/sync the uv environment and install dev tools (ruff/ty/pytest) via the "develop" extra

uv run --no-sync ruff check --fix .      # Run Ruff lint and apply safe autofixes (including import sorting); --no-sync avoids re-syncing
uv run --no-sync ruff format .           # Run Ruff formatter (Black replacement) to format code consistently; --no-sync avoids re-syncing
