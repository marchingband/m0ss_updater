#!/usr/bin/env bash
set -e  # exit if any command fails

# === Pyapp build environment ===
export PYAPP_PROJECT_NAME="m0ss_updater"
export PYAPP_PROJECT_VERSION="0.0.1"
export PYAPP_PROJECT_DEPENDENCY_FILE="./requirements.txt"
export PYAPP_EXEC_SCRIPT="./m0ss_updater.py"
export PYAPP_DISTRIBUTION_EMBED="true"
export PYAPP_IS_GUI="true"

# === Run build ===
cargo build --release