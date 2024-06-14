#!/bin/bash

# Ensure the script is being run from the project root
PROJECT_DIR="$(pwd)"

# Install the Python package
pip install .

echo "Dev-Craft installed successfully. You can now use the 'dev-craft' command."
