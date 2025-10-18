#!/bin/bash
# Sync diagrams from motia-output to drakon-viewer

SOURCE_DIR="/home/vokov/motia-drn/motia-output/steps"
TARGET_DIR="/home/vokov/motia-drn/tools/drakon-viewer/public/diagrams"

echo "Syncing diagrams from $SOURCE_DIR to $TARGET_DIR..."

# Create target directory if it doesn't exist
mkdir -p "$TARGET_DIR"

# Copy all JSON files
cp -v "$SOURCE_DIR"/*.json "$TARGET_DIR/"

echo "Done! Diagrams synchronized."
