#!/bin/bash
# Build script for Panini-FS
set -e

cd "$(dirname "$0")"
echo "Building in: $(pwd)"
echo "Time: $(date '+%H:%M:%S')"

cargo build --release 2>&1 | tee build.log

echo ""
echo "Build complete at: $(date '+%H:%M:%S')"
echo "Binaries in: ./target/release/"
ls -lh target/release/panini* 2>/dev/null || echo "Binaries not found (build may have failed)"
