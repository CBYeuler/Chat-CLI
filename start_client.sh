#!/usr/bin/env bash
# start_client.sh
set -euo pipefail
if [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
fi
python -m client.cli
