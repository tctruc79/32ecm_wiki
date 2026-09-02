#!/bin/bash
# Dong bo wiki/ tu course root vao content/ cua Quartz. Chay lai script nay +
# `git add -A && git commit && git push` moi khi wiki duoc cap nhat va muon publish ban moi.
set -euo pipefail

SRC="/Volumes/DATA/.CloudStorage/Data/OneDrive2-Personal/MAE/STUDY/MODULE1/5. [32_ECM] - ECONOMETRICS/wiki"
DEST="$(cd "$(dirname "$0")" && pwd)/content"

rm -rf "$DEST"
mkdir -p "$DEST"

for d in sources concepts people synthesis assets; do
  if [ -d "$SRC/$d" ]; then
    cp -R "$SRC/$d" "$DEST/$d"
  fi
done

# index.md la trang hub cua wiki ECM (khac DBC/DAS dung overview.md) -> copy thang, khong can alias
cp "$SRC/index.md" "$DEST/index.md"

echo "Synced. Files in content/:"
find "$DEST" -name "*.md" | wc -l
