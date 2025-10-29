# Panini-FS Build Requirements

This document lists system dependencies required to build Panini-FS from source.

## Core Dependencies

### 1. Rust Toolchain

**Required**: Rust 1.75 or later

```bash
# Install rustup (if not already installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Verify installation
rustc --version  # Should be >= 1.75
cargo --version
```

### 2. LLVM/Clang (for RocksDB bindings)

**Required**: libclang for bindgen to generate C++ bindings

#### Arch Linux / Manjaro

```bash
sudo pacman -S clang
```

#### Ubuntu / Debian

```bash
sudo apt-get update
sudo apt-get install libclang-dev llvm-dev
```

#### Fedora / RHEL / CentOS

```bash
sudo dnf install clang-devel llvm-devel
```

#### macOS

```bash
# Using Homebrew
brew install llvm

# Add to PATH (add to ~/.zshrc or ~/.bash_profile)
export PATH="/usr/local/opt/llvm/bin:$PATH"
export LDFLAGS="-L/usr/local/opt/llvm/lib"
export CPPFLAGS="-I/usr/local/opt/llvm/include"
```

#### Windows

```powershell
# Using chocolatey
choco install llvm

# Or download from: https://releases.llvm.org/
```

### 3. Build Tools

#### Linux

```bash
# Arch Linux
sudo pacman -S base-devel

# Ubuntu/Debian
sudo apt-get install build-essential

# Fedora
sudo dnf groupinstall "Development Tools"
```

#### macOS

```bash
xcode-select --install
```

#### Windows

- Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)
- Or install [MinGW-w64](https://www.mingw-w64.org/)

---

## Optional Dependencies

### Git (for repository operations)

```bash
# Usually pre-installed on most systems
git --version

# If not installed:
# Arch: sudo pacman -S git
# Ubuntu: sudo apt-get install git
# macOS: brew install git
```

### OpenSSL (optional - we use vendored version)

Panini-FS uses `vendored-openssl` feature by default, so system OpenSSL is **not required**.

However, if you prefer using system OpenSSL:

```bash
# Arch Linux
sudo pacman -S openssl

# Ubuntu/Debian
sudo apt-get install libssl-dev

# Fedora
sudo dnf install openssl-devel

# macOS
brew install openssl
```

Then modify `Cargo.toml`:
```toml
git2 = { version = "0.18", features = ["https", "ssh"] }  # Remove vendored-openssl
```

---

## Verification

After installing dependencies, verify everything is ready:

```bash
# Check Rust
rustc --version
cargo --version

# Check LLVM/Clang
clang --version
llvm-config --version

# Check build tools
gcc --version  # or clang --version
make --version
```

---

## Troubleshooting

### Error: "couldn't find any valid shared libraries matching: ['libclang.so']"

**Cause**: libclang not installed or not in library path.

**Solution**:

1. Install clang (see above)
2. Set `LIBCLANG_PATH` environment variable:

```bash
# Find libclang location
find /usr -name "libclang.so*" 2>/dev/null

# Set environment variable (example paths)
export LIBCLANG_PATH=/usr/lib/libclang.so.15      # Arch
export LIBCLANG_PATH=/usr/lib/llvm-14/lib         # Ubuntu
export LIBCLANG_PATH=/usr/local/opt/llvm/lib      # macOS

# Then build
cargo build --release
```

### Error: "could not find directory of OpenSSL installation"

**Cause**: System OpenSSL not found (shouldn't happen with vendored-openssl).

**Solution**:

1. Verify `Cargo.toml` has `vendored-openssl` feature:
```toml
git2 = { version = "0.18", features = ["https", "ssh", "vendored-openssl"] }
```

2. Or install system OpenSSL (see Optional Dependencies above)

### Error: "zstd-safe" compilation errors

**Cause**: Incompatible zstd versions (resolved in Tantivy 0.22+).

**Solution**: Ensure `Cargo.toml` uses:
```toml
tantivy = { version = "0.22", default-features = false }
```

### Build is very slow

**Tip**: Use more CPU cores:

```bash
# Set number of parallel jobs (adjust based on your CPU)
export CARGO_BUILD_JOBS=8

# Or
cargo build --release -j8
```

**Tip**: Use `sccache` for caching:

```bash
# Install sccache
cargo install sccache

# Configure Cargo to use it
export RUSTC_WRAPPER=sccache

# Build
cargo build --release
```

---

## Quick Start (TL;DR)

### Arch Linux

```bash
sudo pacman -S base-devel clang rust
cd /path/to/Panini-FS
cargo build --release
```

### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install build-essential libclang-dev curl
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
cd /path/to/Panini-FS
cargo build --release
```

### macOS

```bash
xcode-select --install
brew install llvm rust
cd /path/to/Panini-FS
cargo build --release
```

---

## Build Times

Expected build times (first build, release mode):

| Hardware | Time |
|----------|------|
| 4-core CPU, 8GB RAM | ~15-20 min |
| 8-core CPU, 16GB RAM | ~8-12 min |
| 16-core CPU, 32GB RAM | ~4-6 min |

Subsequent builds (incremental) are much faster: 10-30 seconds.

---

## CI/CD Notes

For automated builds (GitHub Actions, GitLab CI, etc.), see `.github/workflows/` for examples.

Key points:
- Cache `~/.cargo/registry` and `target/` directories
- Use `sccache` for faster builds
- Install dependencies in setup step
- Run with `cargo build --release --locked`

---

**Last Updated**: 2025-10-29  
**Applies To**: Panini-FS v2.0.0+
