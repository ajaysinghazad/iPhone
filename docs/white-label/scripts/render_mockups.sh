#!/usr/bin/env bash
# Prefer Pillow generator (reliable in CI). Optional Chrome pass if CHROME_SCREENSHOT=1.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT/scripts/generate_mockups.py"
if [[ "${CHROME_SCREENSHOT:-0}" != "1" ]]; then
  exit 0
fi
MOCK="$ROOT/mockups"
OUT="$ROOT/images"
mkdir -p "$OUT"
CHROME="${CHROME:-/usr/local/bin/google-chrome}"

cp -f /home/ubuntu/.cursor/projects/workspace/assets/1a68c17b-ac8e-453d-96c1-19578d785121.png "$OUT/00-reference-dashboard.png"
cp -f /home/ubuntu/.cursor/projects/workspace/assets/ee1cd86a-07c2-4fbf-9cd7-0e73aba52420.jpg "$OUT/00-reference-login.jpg"

render() {
  local html="$1"
  local png="$2"
  local w="${3:-390}"
  local h="${4:-920}"
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars \
    --user-data-dir="/tmp/chrome-headless-$$" \
    --window-size="${w},${h}" \
    --screenshot="$png" \
    "file://${html}" 2>/dev/null || true
  rm -rf "/tmp/chrome-headless-$$"
}

render "$MOCK/01-select-organisation.html" "$OUT/01-select-organisation.png"
render "$MOCK/02-login-org-a.html" "$OUT/02-login-org-a-vha.png"
render "$MOCK/03-login-org-b.html" "$OUT/03-login-org-b-memorial.png"
render "$MOCK/04-dashboard-branded.html" "$OUT/04-dashboard-branded.png"
render "$MOCK/05-change-organisation.html" "$OUT/05-change-organisation.png"
render "$MOCK/06-flow-diagram.html" "$OUT/06-flow-diagram.png" 940 1100

echo "Rendered PNGs in $OUT"
