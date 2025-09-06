#!/bin/bash

# Test and validation script for PaniniFS-2

set -e

echo "🔧 Testing and validating PaniniFS-2"
echo "===================================="

# Check that Rust is installed
if ! command -v cargo &> /dev/null; then
    echo "❌ Rust/Cargo is not installed. See Copilotage/setup-rust.md"
    exit 1
fi

echo "✅ Rust/Cargo detected: $(cargo --version)"

# Navigate to project directory
cd "$(dirname "$0")/../PaniniFS-2"

echo ""
echo "🧹 Cleaning previous artifacts..."
cargo clean

echo ""
echo "🔍 Checking code formatting..."
cargo fmt --check || {
    echo "⚠️  Code not formatted. Auto-formatting..."
    cargo fmt
    echo "✅ Code formatted"
}

echo ""
echo "🕵️  Static analysis with Clippy..."
cargo clippy -- -D warnings

echo ""
echo "🧪 Running unit tests..."
cargo test

echo ""
echo "🏗️  Building in debug mode..."
cargo build

echo ""
echo "🏗️  Building in release mode..."
cargo build --release

echo ""
echo "📋 Checking examples..."
cargo build --examples

echo ""
echo "📚 Generating documentation..."
cargo doc --no-deps

echo ""
echo "🎯 Running basic example..."
if cargo run --example basic_usage; then
    echo "✅ Example ran successfully"
else
    echo "❌ Example failed"
    exit 1
fi

echo ""
echo "📊 Project statistics:"
echo "  - Lines of Rust code: $(find src -name "*.rs" -exec wc -l {} + | tail -1 | awk '{print $1}')"
echo "  - Source files: $(find src -name "*.rs" | wc -l)"
echo "  - Tests: $(grep -r "#\[test\]" src | wc -l)"

echo ""
echo "🎉 All tests pass! PaniniFS-2 is ready for development."
echo ""
echo "Suggested next steps:"
echo "  1. Install system dependencies: sudo zypper install fuse3-devel libgit2-devel"
echo "  2. Check the roadmap: cat Copilotage/roadmap.md"
echo "  3. Start by implementing complete GitStorage"
echo "  4. Create persistent RocksDB index"
