#!/usr/bin/env bash
# One-time macOS setup. Safe to re-run.
set -euo pipefail
cd "$(dirname "$0")/.."

if ! xcode-select -p >/dev/null 2>&1; then
  echo "Xcode Command Line Tools missing. Run: xcode-select --install"
  echo "Then re-run this script."
  exit 1
fi

if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew missing. Install it from https://brew.sh, then re-run."
  exit 1
fi

brew install verilator icarus-verilog yosys python@3.12

PY="$(brew --prefix python@3.12)/bin/python3.12"
if [ ! -d .venv ]; then
  "$PY" -m venv .venv
fi
.venv/bin/pip install --upgrade pip >/dev/null
.venv/bin/pip install -r requirements.txt

echo
verilator --version
iverilog -V 2>&1 | head -1
yosys -V
echo
make test
echo
echo "Setup complete. Read NEXT.md for what to do next."
