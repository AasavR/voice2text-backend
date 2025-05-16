#!/bin/bash

# Download and extract FFmpeg for Render
curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz -o ffmpeg-release-amd64-static.tar.xz
mkdir -p ffmpeg
tar -xf ffmpeg-release-amd64-static.tar.xz --strip-components=1 -C ffmpeg
rm ffmpeg-release-amd64-static.tar.xz

# Export path
export PATH="$(pwd)/ffmpeg:$PATH"
