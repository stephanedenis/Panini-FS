//! Panini-FS Mount Command
//!
//! Mount Panini-FS as a FUSE filesystem

use anyhow::Result;
use clap::Parser;
use panini_fuse::{mount, MountConfig};
use std::path::PathBuf;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

#[derive(Parser, Debug)]
#[command(name = "panini-mount")]
#[command(about = "Mount Panini-FS as a FUSE filesystem", long_about = None)]
struct Args {
    /// Storage directory containing Panini-FS data
    #[arg(short, long, env = "PANINI_STORAGE")]
    storage: PathBuf,
    
    /// Mount point directory
    #[arg(short, long)]
    mount: PathBuf,
    
    /// Enable time-travel features
    #[arg(long, default_value = "true")]
    time_travel: bool,
    
    /// Enable concept navigation
    #[arg(long, default_value = "true")]
    concepts: bool,
    
    /// Enable debug logging
    #[arg(short, long)]
    debug: bool,
}

fn main() -> Result<()> {
    let args = Args::parse();
    
    // Initialize logging
    let log_level = if args.debug {
        tracing::Level::DEBUG
    } else {
        tracing::Level::INFO
    };
    
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| format!("panini_fuse={}", log_level).into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();
    
    // Validate paths
    if !args.storage.exists() {
        anyhow::bail!("Storage directory does not exist: {:?}", args.storage);
    }
    
    if !args.mount.exists() {
        tracing::info!("Creating mount point: {:?}", args.mount);
        std::fs::create_dir_all(&args.mount)?;
    }
    
    // Create mount configuration
    let mut config = MountConfig::new(args.storage.clone(), args.mount.clone());
    config.enable_time_travel = args.time_travel;
    config.enable_concepts = args.concepts;
    
    tracing::info!("🗂️  Panini-FS Mount");
    tracing::info!("Storage: {:?}", config.storage_path);
    tracing::info!("Mount point: {:?}", config.mount_point);
    tracing::info!("Time-travel: {}", config.enable_time_travel);
    tracing::info!("Concepts: {}", config.enable_concepts);
    tracing::info!("");
    tracing::info!("🔐 Mounting in READ-ONLY mode (immutable filesystem)");
    tracing::info!("Press Ctrl+C to unmount");
    tracing::info!("");
    
    // Mount the filesystem
    mount(config)?;
    
    Ok(())
}
