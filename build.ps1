# Exit if any command fails
$ErrorActionPreference = "Stop"

# === Pyapp build environment ===
$env:PYAPP_PROJECT_NAME = "m0ss_updater"
$env:PYAPP_PROJECT_VERSION = "0.0.1"
$env:PYAPP_PROJECT_DEPENDENCY_FILE = ".\requirements.txt"
$env:PYAPP_EXEC_SCRIPT = ".\m0ss_updater.py"
$env:PYAPP_DISTRIBUTION_EMBED = "true"
$env:PYAPP_IS_GUI = "true"

# === Run build ===
cargo build --release