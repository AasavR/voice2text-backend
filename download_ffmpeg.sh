#!/bin/bash

# Download and extract ffmpeg static build during backend startup

FFMPEG_URL="https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"
FFMPEG_DIR="ffmpeg"

echo "Downloading ffmpeg..."
curl -L $FFMPEG_URL -o ffmpeg-release-amd64-static.tar.xz

echo "Extracting ffmpeg..."
tar -xf ffmpeg-release-amd64-static.tar.xz

# Rename extracted folder to ffmpeg for consistent path
mv ffmpeg-release-amd64-static $FFMPEG_DIR

# Clean up archive
rm ffmpeg-release-amd64-static.tar.xz

echo "ffmpeg downloaded and extracted to $FFMPEG_DIR"
