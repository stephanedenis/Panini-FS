# Rust Configuration for PaniniFS-2

## Installing Rust on openSUSE

```bash
# Installation via rustup (recommended method)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env

# Or via zypper
sudo zypper install rustup
rustup default stable
```

## Required System Dependencies

```bash
# For FUSE (userspace filesystem)
sudo zypper install fuse3-devel libfuse3-3

# For Git (if not already installed)
sudo zypper install git2-devel libgit2-devel

# Development tools
sudo zypper install gcc pkg-config
```

## PaniniFS-2 Project Structure

- **Core**: Semantic engine and Git management
- **VFS**: Virtual file system (FUSE)
- **Semantic**: Semantic models and atoms
- **Storage**: Interface with Git repositories
- **Interface**: CLI and conversational API

## Useful Rust Crates

- `fuser`: Modern FUSE interface for Rust
- `git2`: Git bindings for Rust
- `serde`: Serialization/deserialization
- `tokio`: Async runtime
- `clap`: CLI interface
- `log` and `env_logger`: Logging
- `sqlite` or `rocksdb`: Fast local cache
