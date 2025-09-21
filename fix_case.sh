#!/bin/bash
set -e

# Force Git to register case-only renames by using an intermediate name first

# Docs -> docs
if [ -d "Docs" ]; then
  echo "Renaming Docs -> docs_tmp ..."
  git mv Docs docs_tmp
  git commit -m "chore(structure): intermediate rename Docs -> docs_tmp"
  echo "Renaming docs_tmp -> docs ..."
  git mv docs_tmp docs
  git commit -m "chore(structure): finalize rename docs_tmp -> docs"
else
  echo "Docs/ not found, skipping."
fi

# Code -> code
if [ -d "Code" ]; then
  echo "Renaming Code -> code_tmp ..."
  git mv Code code_tmp
  git commit -m "chore(structure): intermediate rename Code -> code_tmp"
  echo "Renaming code_tmp -> code ..."
  git mv code_tmp code
  git commit -m "chore(structure): finalize rename code_tmp -> code"
else
  echo "Code/ not found, skipping."
fi

echo "All done! Push with: git push origin main"
