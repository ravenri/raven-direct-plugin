#!/usr/bin/env bash
# Usage: build.sh draft.md /mnt/user-data/outputs/Industry_Overview_<Deal>.docx
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
pandoc "$1" -f markdown+pipe_tables+fenced_divs -o "$2" --reference-doc="$here/assets/industry-overview-template.docx"
python3 "$here/scripts/check.py" "$2"
