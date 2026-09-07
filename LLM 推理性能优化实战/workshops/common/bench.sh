#!/usr/bin/env bash
# Shared bench_client.py wrapper. Run this against a server started by
# serve.sh, once per config (baseline/optimized), then diff the two reports
# with compare.py.
#
# Usage (called from a workshop dir):
#   MODEL=... LABEL=baseline REQUESTS_FILE=requests.jsonl bash ../common/bench.sh
set -euo pipefail

MODEL="${MODEL:?set MODEL}"
LABEL="${LABEL:?set LABEL, e.g. baseline or optimized}"
REQUESTS_FILE="${REQUESTS_FILE:-requests.jsonl}"
REQUESTS="${REQUESTS:-32}"
CONCURRENCY="${CONCURRENCY:-8}"
BASE_URL="${BASE_URL:-http://127.0.0.1:8000/v1}"
CONFIG_NOTE="${CONFIG_NOTE:-}"
OUTPUT="${OUTPUT:-${LABEL}.json}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 "$SCRIPT_DIR/bench_client.py" \
  --base-url "$BASE_URL" \
  --model "$MODEL" \
  --requests-file "$REQUESTS_FILE" \
  --requests "$REQUESTS" \
  --concurrency "$CONCURRENCY" \
  --label "$LABEL" \
  --config-note "$CONFIG_NOTE" \
  --output "$OUTPUT"

echo "wrote $OUTPUT" >&2
