#!/usr/bin/env bash
# start_server.sh
set -euo pipefail
# activate venv if present
if [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
fi
export PYTHONUNBUFFERED=1
python -m app.server
