#!/bin/bash

# This script downloads the workflows directory from the galaxyproject/iwc repository
# with minimal data transfer using git sparse-checkout.

set -e

# Check if the parent directory is provided
if [ -z "$1" ]; then
  echo "Error: Parent directory not provided."
  echo "Usage: $0 <parent_directory>"
  exit 1
fi

PARENT_DIR="$1"
echo "Parent directory: $PARENT_DIR"

# Create a temporary directory
TMP_DIR=$(mktemp -d)
echo "Created temporary directory: $TMP_DIR"

# Ensure cleanup on exit
trap 'echo "Cleaning up temporary directory..."; rm -rf "$TMP_DIR"' EXIT

# Change to the temporary directory
cd "$TMP_DIR"

# Initialize a git repository
echo "Initializing git repository..."
git init

# Add the remote repository
echo "Adding remote repository..."
git remote add -f origin https://github.com/galaxyproject/iwc.git

# Enable sparse checkout
echo "Enabling sparse checkout..."
git config core.sparseCheckout true

# Define the directory to checkout
echo "workflows" > .git/info/sparse-checkout
echo "Configured sparse checkout for 'workflows' directory."

# Pull the data from the main branch
echo "Pulling data from remote..."
git pull --depth=1 origin main

# Move the workflows directory to the parent directory
echo "Moving 'workflows' directory to $PARENT_DIR"
mv workflows "$PARENT_DIR"

# The trap will handle the cleanup.
echo "Script finished successfully."