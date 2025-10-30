#!/bin/bash
# Fix libclang.so symlink and build Panini-FS
# Run this script with: bash fix_and_build.sh

echo "=== Panini-FS Final Build Script ==="
echo "Date: $(date '+%Y-%m-%d %H:%M:%S')"
echo

# Step 1: Create libclang.so symlink
echo "Step 1/3: Creating libclang.so symlink..."
if [ ! -e /usr/lib64/libclang.so ]; then
    sudo ln -sf /usr/lib64/libclang.so.21.1.4 /usr/lib64/libclang.so
    if [ $? -eq 0 ]; then
        echo "✅ Symlink created: /usr/lib64/libclang.so -> libclang.so.21.1.4"
    else
        echo "❌ Failed to create symlink (need sudo)"
        exit 1
    fi
else
    echo "✅ libclang.so already exists"
fi

# Verify symlink
ls -la /usr/lib64/libclang.so* | head -5
echo

# Step 2: Build Panini-FS
echo "Step 2/3: Building Panini-FS (release mode)..."
echo "This will take 8-12 minutes..."
echo

cd /home/stephane/GitHub/Panini-FS || exit 1

# Clean previous failed build
rm -rf target/release/build/clang-sys-*

# Start build with timestamp
BUILD_START=$(date +%s)
cargo build --release 2>&1 | tee build_final.log

BUILD_END=$(date +%s)
BUILD_DURATION=$((BUILD_END - BUILD_START))
BUILD_MINUTES=$((BUILD_DURATION / 60))
BUILD_SECONDS=$((BUILD_DURATION % 60))

echo
echo "Build completed in ${BUILD_MINUTES}m ${BUILD_SECONDS}s"
echo

# Step 3: Verify binaries
echo "Step 3/3: Verifying binaries..."
echo

if [ -f target/release/panini ] && [ -f target/release/panini-server ]; then
    echo "✅ Binaries created successfully!"
    echo
    ls -lh target/release/panini target/release/panini-server
    echo
    echo "Testing panini CLI..."
    ./target/release/panini --version
    echo
    echo "Testing panini-server..."
    ./target/release/panini-server --version 2>&1 || echo "(server version check may not be implemented)"
    echo
    echo "=== 🎉 BUILD SUCCESSFUL! ==="
    echo
    echo "Next steps:"
    echo "  1. Run tests: cargo test --all"
    echo "  2. Try CLI: ./target/release/panini init test-repo"
    echo "  3. Install: cargo install --path crates/panini-cli"
    echo
else
    echo "❌ Build failed - binaries not found"
    echo "Check build_final.log for errors"
    exit 1
fi
