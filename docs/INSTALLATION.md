# Installation Guide - Panini-FS v2.0

Complete installation instructions for all platforms.

---

## System Requirements

- **Rust**: 1.75+ (MSRV)
- **Git**: 2.40+
- **OpenSSL**: 1.1.1+ or 3.0+ (dev packages)
- **OS**: Linux, macOS, Windows

---

## Prerequisites

### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install -y build-essential pkg-config libssl-dev git
```

### Fedora/RHEL/CentOS

```bash
sudo dnf install -y gcc pkg-config openssl-devel git
```

### Arch Linux

```bash
sudo pacman -Sy base-devel pkg-config openssl git
```

### macOS (Homebrew)

```bash
brew install pkg-config openssl git
```

### Windows

1. Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)
2. Install [Git for Windows](https://git-scm.com/download/win)
3. Install [OpenSSL](https://slproweb.com/products/Win32OpenSSL.html) or use `vcpkg`:
   ```powershell
   vcpkg install openssl:x64-windows
   ```

---

## Install Rust

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
rustc --version  # Should show 1.75+
```

---

## Clone Repository

```bash
git clone https://github.com/stephanedenis/Panini-FS.git
cd Panini-FS
```

---

## Build

### Standard Build

```bash
cargo build --release
```

**Expected output:**
```
   Compiling panini-core v2.0.0-alpha
   Compiling panini-cli v2.0.0-alpha
   Compiling panini-server v2.0.0-alpha
    Finished `release` profile [optimized] target(s) in X.XXs
```

**Binaries created:**
- `./target/release/panini` - CLI tool
- `./target/release/panini-server` - REST API server

---

## Troubleshooting

### OpenSSL Not Found

**Symptom:**
```
error: failed to run custom build command for `openssl-sys v0.9.110`
Could not find directory of OpenSSL installation
```

**Solution 1: Install OpenSSL dev packages** (recommended)

**Ubuntu/Debian:**
```bash
sudo apt-get install libssl-dev pkg-config
```

**Fedora/RHEL:**
```bash
sudo dnf install openssl-devel pkg-config
```

**Arch Linux:**
```bash
sudo pacman -S openssl pkg-config
```

**macOS:**
```bash
brew install openssl@3 pkg-config
export PKG_CONFIG_PATH="/opt/homebrew/opt/openssl@3/lib/pkgconfig"
```

**Solution 2: Use vendored OpenSSL** (fallback)

Add to `crates/panini-core/Cargo.toml`:
```toml
[dependencies]
git2 = { version = "0.18", features = ["vendored-openssl"] }
```

Then rebuild:
```bash
cargo build --release
```

**Solution 3: Manual OpenSSL path**

If OpenSSL is installed in non-standard location:
```bash
export OPENSSL_DIR=/path/to/openssl
export PKG_CONFIG_PATH=/path/to/openssl/lib/pkgconfig
cargo build --release
```

---

### pkg-config Not Found

**Symptom:**
```
error: pkg-config not found
```

**Solution:**

**Ubuntu/Debian:**
```bash
sudo apt-get install pkg-config
```

**Fedora/RHEL:**
```bash
sudo dnf install pkgconf-pkg-config
```

**Arch Linux:**
```bash
sudo pacman -S pkgconf
```

**macOS:**
```bash
brew install pkg-config
```

---

### Git Clone HTTPS Errors

**Symptom:**
```
fatal: unable to access 'https://...': SSL certificate problem
```

**Solution:**

Use SSH instead:
```bash
git clone git@github.com:stephanedenis/Panini-FS.git
```

Or configure Git to use system certificates:
```bash
git config --global http.sslBackend schannel  # Windows
git config --global http.sslBackend openssl   # Linux/macOS
```

---

### Compilation Takes Too Long

**Solution: Parallel compilation**

```bash
cargo build --release -j$(nproc)  # Linux/macOS
cargo build --release -j%NUMBER_OF_PROCESSORS%  # Windows
```

**Reduce debug info for faster compile:**
```bash
# Add to Cargo.toml
[profile.release]
debug = 0
```

---

### Insufficient RAM

**Symptom:**
```
error: linking failed: memory exhausted
```

**Solution: Increase codegen units**

Add to `Cargo.toml`:
```toml
[profile.release]
codegen-units = 256
incremental = true
```

Or reduce parallelism:
```bash
cargo build --release -j1
```

---

### Test Failures

**Symptom:**
```
test result: FAILED. X passed; Y failed; Z ignored
```

**Note**: Some tests require Git configuration:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

To skip failing tests:
```bash
cargo build --release  # Skip tests entirely
```

---

## Installation

### Install CLI globally

```bash
cargo install --path crates/panini-cli
```

**Verify:**
```bash
panini --version
# Output: panini 2.0.0-alpha
```

**Add to PATH** (if not already):
```bash
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

### Install Server

```bash
cargo install --path crates/panini-server
```

**Verify:**
```bash
panini-server --version
# Output: panini-server 2.0.0-alpha
```

---

## Docker Installation (Alternative)

### Build Docker Image

```dockerfile
# Dockerfile
FROM rust:1.75 as builder

# Install dependencies
RUN apt-get update && \
    apt-get install -y libssl-dev pkg-config git && \
    rm -rf /var/lib/apt/lists/*

# Build
WORKDIR /app
COPY . .
RUN cargo build --release

# Runtime image
FROM debian:bookworm-slim
RUN apt-get update && \
    apt-get install -y libssl3 ca-certificates git && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/target/release/panini /usr/local/bin/
COPY --from=builder /app/target/release/panini-server /usr/local/bin/

EXPOSE 3000
CMD ["panini-server"]
```

**Build:**
```bash
docker build -t panini-fs:2.0.0-alpha .
```

**Run CLI:**
```bash
docker run --rm panini-fs:2.0.0-alpha panini --version
```

**Run Server:**
```bash
docker run -p 3000:3000 panini-fs:2.0.0-alpha
```

---

## Verification

### Test CLI

```bash
panini init test-repo
cd test-repo
panini create test_concept --title "Test Concept"
panini list
```

**Expected output:**
```
✅ Repository initialized: test-repo
✅ Created: test_concept
📚 Concepts (1):
  - test_concept
```

### Test Server

```bash
# Terminal 1: Start server
panini-server

# Terminal 2: Test health
curl http://localhost:3000/health
# Output: OK

# Test concepts endpoint
curl http://localhost:3000/concepts
# Output: []
```

---

## Uninstall

```bash
# Remove binaries
cargo uninstall panini-cli panini-server

# Or manually
rm ~/.cargo/bin/panini
rm ~/.cargo/bin/panini-server

# Remove repository
rm -rf ~/path/to/Panini-FS
```

---

## Next Steps

- Read [CLI Guide](CLI_GUIDE.md) for usage examples
- Read [API Documentation](API.md) for REST API reference
- Read [Architecture](constitution_v2.md) for system design
- Join [Discussions](https://github.com/stephanedenis/Panini-FS/discussions) for support

---

## Platform-Specific Notes

### Linux (Arch Linux)

Known issue: OpenSSL dev package may not be installed by default.

**Fix:**
```bash
sudo pacman -S openssl pkg-config
```

### macOS (Apple Silicon)

May require Rosetta 2 for some dependencies:
```bash
softwareupdate --install-rosetta
```

Set OpenSSL path:
```bash
export PKG_CONFIG_PATH="/opt/homebrew/opt/openssl@3/lib/pkgconfig"
```

### Windows (WSL)

Recommended for best experience:
```bash
# In WSL
sudo apt-get update
sudo apt-get install build-essential libssl-dev pkg-config git
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### Windows (Native)

Use PowerShell as Administrator:
```powershell
# Install Rust
winget install Rustlang.Rustup

# Install OpenSSL via vcpkg
git clone https://github.com/Microsoft/vcpkg.git
cd vcpkg
.\bootstrap-vcpkg.bat
.\vcpkg integrate install
.\vcpkg install openssl:x64-windows

# Set environment variable
$env:VCPKG_ROOT = "C:\path\to\vcpkg"
```

---

## Support

- **GitHub Issues**: [Report bugs](https://github.com/stephanedenis/Panini-FS/issues)
- **Discussions**: [Ask questions](https://github.com/stephanedenis/Panini-FS/discussions)
- **Email**: support@panini-fs.dev

---

**Last Updated**: 2025-10-29  
**Version**: 2.0.0-alpha
