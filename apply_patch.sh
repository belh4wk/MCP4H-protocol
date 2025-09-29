#!/usr/bin/env bash
set -euo pipefail
PATCH_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="${1:-.}"

echo "Applying CI + requirements patch into $REPO_DIR ..."

mkdir -p "$REPO_DIR/.github/workflows"
mkdir -p "$REPO_DIR/tests"

cp -v "$PATCH_DIR/.github/workflows/ci.yml" "$REPO_DIR/.github/workflows/ci.yml"
cp -v "$PATCH_DIR/requirements.txt" "$REPO_DIR/requirements.txt"
cp -v "$PATCH_DIR/requirements.md" "$REPO_DIR/requirements.md"
cp -v "$PATCH_DIR/tests/test_schema_vectors.py" "$REPO_DIR/tests/test_schema_vectors.py"

echo "Done. Commit and push to trigger GitHub Actions."
