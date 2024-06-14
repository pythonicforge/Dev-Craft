#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Ensure the script is being run from the project root
PROJECT_DIR="$(pwd)"

echo "Installing Dev-Craft from $PROJECT_DIR..."

# Install the Python package
pip install . || { echo "Failed to install Dev-Craft. Please check for errors."; exit 1; }

echo "Dev-Craft installed successfully."
echo "You can now use the 'dev-craft' command."

# Verify installation
if command -v dev-craft &> /dev/null
then
    echo "'dev-craft' command is available."
else
    echo "Installation completed, but 'dev-craft' command is not found in PATH."
    echo "You may need to adjust your PATH environment variable."
fi
