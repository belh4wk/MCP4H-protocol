#!/usr/bin/env bash
set -euo pipefail
PATCH_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="${1:-.}"
REMOVE_OLD="${2:-}"

echo "Merging CI workflows into $REPO_DIR/.github/workflows/ci.yml ..."

mkdir -p "$REPO_DIR/.github/workflows"
cp -v "$PATCH_DIR/.github/workflows/ci.yml" "$REPO_DIR/.github/workflows/ci.yml"

if [ "$REMOVE_OLD" = "--remove-old" ]; then
  if [ -f "$REPO_DIR/.github/workflows/validate.yml" ]; then
    rm -v "$REPO_DIR/.github/workflows/validate.yml"
    echo "Removed old validate.yml"
  fi
fi

echo "Done. Commit and push to trigger the merged CI."
