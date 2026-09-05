#!/usr/bin/env bash
# fetch_assets.sh — (re)downloads the raw font/KaTeX assets that
# embed_fonts.py turns into self-hosted, base64-inlined CSS for the
# Mindmap Artifact. Run this once before embed_fonts.py if assets/ is
# missing or you're reconstructing this pipeline from scratch again.
#
# Network note: in a Claude Code sandbox, plain `curl` from Bash may be
# blocked; re-run with the tool's dangerouslyDisableSandbox option, or run
# this script in an environment with normal network access.
#
# KaTeX version: check the current release first --
#   curl -s https://api.github.com/repos/KaTeX/KaTeX/releases/latest | grep tag_name
# (was v0.18.5 as of 2026-09-05; update KATEX_VERSION below if it has moved on).

set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ASSETS="$HERE/assets"
mkdir -p "$ASSETS/plexfonts"

KATEX_VERSION="v0.18.5"

echo "== KaTeX $KATEX_VERSION =="
curl -sL --max-time 60 -o "$ASSETS/katex.tar.gz" \
  "https://github.com/KaTeX/KaTeX/releases/download/${KATEX_VERSION}/katex.tar.gz"
tar -xzf "$ASSETS/katex.tar.gz" -C "$ASSETS"
echo "KaTeX fonts: $(ls "$ASSETS/katex/fonts"/*.woff2 | wc -l)"

echo "== IBM Plex Sans / Plex Mono (via Google Fonts CSS2 API, VI-subset aware) =="
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
curl -sL --max-time 30 -A "$UA" \
  "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&family=IBM+Plex+Mono:wght@400;500;700&display=swap" \
  -o "$ASSETS/plex.css"
grep -oE 'https://fonts\.gstatic\.com/[^)]+\.woff2' "$ASSETS/plex.css" | sort -u > "$ASSETS/plex_urls.txt"
while read -r url; do
  curl -sL --max-time 20 -o "$ASSETS/plexfonts/$(basename "$url")" "$url"
done < "$ASSETS/plex_urls.txt"
echo "Plex font files: $(ls "$ASSETS/plexfonts" | wc -l)"

echo "== Done. Now run: python3 embed_fonts.py =="
