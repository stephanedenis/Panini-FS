//! Panini CLI - Complete command-line interface

use clap::{Parser, Subcommand};
use colored::*;
use panini_core::error::Result;
use panini_core::git::repo::PaniniRepo;
use panini_core::schema::concept::{Concept, ConceptType};
use panini_core::schema::crud::*;
use panini_core::schema::dhatu::Dhatu;
use panini_core::schema::relation::RelationType;
use panini_core::schema::relations::*;
use panini_core::git::sync::ConflictStrategy;
use std::path::PathBuf;

#[derive(Parser)]
#[command(name = "panini")]
#[command(version = "2.0.0")]
#[command(about = "Git-native distributed knowledge graph", long_about = None)]
struct Cli {
    /// Repository path
    #[arg(short, long, default_value = ".")]
    repo: PathBuf,
    
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Initialize a new repository
    Init {
        path: Option<PathBuf>,
    },
    
    /// Create a new concept
    Create {
        id: String,
        #[arg(short, long)]
        title: String,
        #[arg(short = 'T', long)]
        tags: Option<String>,
        #[arg(short, long, default_value = "TEXT")]
        dhatu: String,
    },
    
    /// Read a concept
    Read {
        id: String,
        #[arg(short, long)]
        json: bool,
    },
    
    /// Update a concept
    Update {
        id: String,
        #[arg(short, long)]
        title: Option<String>,
        #[arg(short = 'T', long)]
        tags: Option<String>,
    },
    
    /// Delete a concept
    Delete {
        id: String,
    },
    
    /// List all concepts
    List {
        #[arg(short, long)]
        json: bool,
    },
    
    /// Add a relation
    AddRelation {
        source: String,
        #[arg(short, long)]
        rel_type: String,
        target: String,
        #[arg(short, long)]
        confidence: Option<f32>,
    },
    
    /// Get relations
    Relations {
        id: String,
    },
    
    /// Sync with remote
    Sync,
    
    /// Show status
    Status,
}

fn main() -> Result<()> {
    let cli = Cli::parse();
    
    match cli.command {
        Commands::Init { path } => {
            let repo_path = path.unwrap_or_else(|| PathBuf::from("."));
            PaniniRepo::init(&repo_path)?;
            println!("{} Initialized at {}", "✅".green(), repo_path.display());
            Ok(())
        }
        
        Commands::Create { id, title, tags, dhatu } => {
            let repo = PaniniRepo::open(&cli.repo)?;
            let dhatu_type = match dhatu.to_uppercase().as_str() {
                "TEXT" => Dhatu::TEXT,
                "IMAGE" => Dhatu::IMAGE,
                "AUDIO" => Dhatu::AUDIO,
                "VIDEO" => Dhatu::VIDEO,
                "CODE" => Dhatu::CODE,
                _ => Dhatu::TEXT,
            };
            
            let tag_list = tags.map(|t| t.split(',').map(|s| s.trim().to_string()).collect()).unwrap_or_default();
            
            let concept = Concept {
                id: id.clone(),
                r#type: ConceptType::Concept,
                dhatu: dhatu_type,
                title: title.clone(),
                tags: tag_list,
                created: chrono::Utc::now(),
                updated: chrono::Utc::now(),
                author: None,
                relations: vec![],
                content_refs: vec![],
                metadata: serde_json::Value::Null,
                markdown_body: format!("# {}\n\n", title),
            };
            
            create_concept(&repo, &concept)?;
            println!("{} Created: {}", "✅".green(), id);
            Ok(())
        }
        
        Commands::Read { id, json } => {
            let repo = PaniniRepo::open(&cli.repo)?;
            let concept = read_concept(&repo, &id)?;
            
            if json {
                println!("{}", serde_json::to_string_pretty(&concept)?);
            } else {
                println!("{} {}", "�".cyan(), concept.title.bold());
                println!("ID: {}", concept.id);
                println!("Tags: {}", concept.tags.join(", "));
                println!("\n{}", concept.markdown_body);
            }
            Ok(())
        }
        
        Commands::Update { id, title, tags } => {
            let repo = PaniniRepo::open(&cli.repo)?;
            let mut concept = read_concept(&repo, &id)?;
            
            if let Some(t) = title { concept.title = t; }
            if let Some(t) = tags {
                concept.tags.extend(t.split(',').map(|s| s.trim().to_string()));
                concept.tags.sort();
                concept.tags.dedup();
            }
            
            concept.updated = chrono::Utc::now();
            update_concept(&repo, &concept)?;
            println!("{} Updated: {}", "✅".green(), id);
            Ok(())
        }
        
        Commands::Delete { id } => {
            let repo = PaniniRepo::open(&cli.repo)?;
            delete_concept(&repo, &id)?;
            println!("{} Deleted: {}", "✅".green(), id);
            Ok(())
        }
        
        Commands::List { json } => {
            let repo = PaniniRepo::open(&cli.repo)?;
            let ids = list_concepts(&repo)?;
            
            if json {
                println!("{}", serde_json::to_string_pretty(&ids)?);
            } else {
                println!("{} Concepts ({}):", "📚".cyan(), ids.len());
                for id in ids { println!("  - {}", id); }
            }
            Ok(())
        }
        
        Commands::AddRelation { source, rel_type, target, confidence } => {
            let repo = PaniniRepo::open(&cli.repo)?;
            let rt = parse_relation_type(&rel_type)?;
            add_relation(&repo, &source, rt, &target, confidence)?;
            println!("{} {} --{:?}--> {}", "✅".green(), source, rt, target);
            Ok(())
        }
        
        Commands::Relations { id } => {
            let repo = PaniniRepo::open(&cli.repo)?;
            let relations = get_relations(&repo, &id)?;
            println!("{} Relations ({}):", "🔗".cyan(), relations.len());
            for rel in relations {
                println!("  {:?} --> {}", rel.rel_type, rel.target);
            }
            Ok(())
        }
        
        Commands::Sync => {
            todo!("Sync not yet implemented");
        }
        
        Commands::Status => {
            todo!("Status not yet implemented");
        }
    }
}

fn parse_relation_type(s: &str) -> Result<RelationType> {
    match s.to_lowercase().as_str() {
        "is_a" | "isa" => Ok(RelationType::IsA),
        "part_of" | "partof" => Ok(RelationType::PartOf),
        "causes" => Ok(RelationType::Causes),
        "contradicts" => Ok(RelationType::Contradicts),
        "supports" => Ok(RelationType::Supports),
        "derives_from" => Ok(RelationType::DerivesFrom),
        "used_by" => Ok(RelationType::UsedBy),
        "related_to" => Ok(RelationType::RelatedTo),
        _ => Err(panini_core::error::Error::Validation(format!("Invalid relation: {}", s))),
    }
}
