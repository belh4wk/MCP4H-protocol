#!/usr/bin/env bash
set -euo pipefail
PATCH_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="${1:-.}"

echo "Applying citation patch into $REPO_DIR ..."

cp -v "$PATCH_DIR/CITATION.cff" "$REPO_DIR/CITATION.cff"
cp -v "$PATCH_DIR/CITATIONS.bib" "$REPO_DIR/CITATIONS.bib"
mkdir -p "$REPO_DIR/docs"
cp -v "$PATCH_DIR/docs/README_citation_additions.md" "$REPO_DIR/docs/README_citation_additions.md"

echo "Done. Consider pasting the README snippet from docs/README_citation_additions.md into your README.md."
