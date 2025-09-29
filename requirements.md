# MCP4H™ Requirements

This project uses Python tooling for schema validation, CBOR encoding, and developer quality checks.

## Core
- **jsonschema** – validate MCP4H™ JSON messages against schemas
- **cbor2** – generate/parse CBOR equivalents of MCP4H™ messages

## Development / QA
- **pytest** – run unit tests and regression checks
- **flake8** – enforce code style / linting
- **mypy** – type checker for cleaner SDK tooling

## Install
```bash
# Linux / macOS
python3 -m pip install -r requirements.txt

# Windows (PowerShell)
python -m pip install -r requirements.txt
```
