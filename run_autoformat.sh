#!/bin/bash
set -euo pipefail

uv sync --extra develop
uv run --no-sync black .
uv run --no-sync docformatter -i -r . --exclude venv --exclude .venv
uv run --no-sync isort .
