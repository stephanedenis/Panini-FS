//! Integration tests for index module

use panini_core::git::repo::PaniniRepo;
use panini_core::index::builder::IndexBuilder;
use panini_core::index::query::QueryEngine;
use panini_core::index::rocks::RocksIndex;
use panini_core::index::tantivy_search::TantivyIndex;
use panini_core::schema::concept::{Concept, ConceptType};
use panini_core::schema::crud::{create_concept, update_concept};
use panini_core::schema::dhatu::Dhatu;
use panini_core::schema::relation::RelationType;
use panini_core::schema::relations::add_relation;
use chrono::Utc;
use tempfile::TempDir;

fn create_test_concept(repo: &PaniniRepo, id: &str, title: &str, body: &str) -> Concept {
    let concept = Concept {
        id: id.to_string(),
        r#type: ConceptType::Concept,
        dhatu: Dhatu::TEXT,
        title: title.to_string(),
        tags: vec!["test".to_string(), "integration".to_string()],
        created: Utc::now(),
        updated: Utc::now(),
        author: None,
        relations: vec![],
        content_refs: vec![],
        metadata: serde_json::Value::Null,
        markdown_body: body.to_string(),
    };
    
    create_concept(repo, &concept).unwrap();
    concept
}

#[test]
fn test_full_index_workflow() {
    let tmp = TempDir::new().unwrap();
    let repo = PaniniRepo::init(tmp.path().join("repo")).unwrap();
    
    // Create concepts
    create_test_concept(&repo, "rust", "Rust Programming", "Rust is a systems programming language.");
    create_test_concept(&repo, "python", "Python Programming", "Python is a high-level language.");
    
    // Add relation
    add_relation(&repo, "rust", RelationType::RelatedTo, "python", Some(0.7)).unwrap();
    
    // Build index
    let builder = IndexBuilder::new(repo.clone(), &tmp.path().join("index/rocks")).unwrap();
    let stats = builder.build().unwrap();
    
    assert_eq!(stats.concepts_indexed, 2);
    assert_eq!(stats.relations_indexed, 1);
    assert!(stats.is_success());
    
    // Verify RocksDB
    let concept = builder.index().get_concept("rust").unwrap();
    assert!(concept.is_some());
    assert_eq!(concept.unwrap().title, "Rust Programming");
    
    let relations = builder.index().get_relations("rust").unwrap();
    assert_eq!(relations.len(), 1);
    assert_eq!(relations[0].target, "python");
}

#[test]
fn test_incremental_index_updates() {
    let tmp = TempDir::new().unwrap();
    let repo = PaniniRepo::init(tmp.path().join("repo")).unwrap();
    
    // Initial concept
    create_test_concept(&repo, "concept1", "Original Title", "Original content");
    
    // Build index
    let builder = IndexBuilder::new(repo.clone(), &tmp.path().join("index/rocks")).unwrap();
    builder.build().unwrap();
    
    // Update concept
    let mut concept = builder.index().get_concept("concept1").unwrap().unwrap();
    concept.title = "Updated Title".to_string();
    update_concept(&repo, &concept).unwrap();
    
    // Incremental update
    builder.update_concept("concept1").unwrap();
    
    // Verify
    let updated = builder.index().get_concept("concept1").unwrap().unwrap();
    assert_eq!(updated.title, "Updated Title");
}

#[test]
fn test_tantivy_fulltext_search() {
    let tmp = TempDir::new().unwrap();
    let repo = PaniniRepo::init(tmp.path().join("repo")).unwrap();
    
    create_test_concept(&repo, "rust", "Rust Programming Language", "Rust provides memory safety without garbage collection.");
    create_test_concept(&repo, "go", "Go Programming Language", "Go is designed for simplicity and concurrency.");
    create_test_concept(&repo, "python", "Python Language", "Python emphasizes code readability.");
    
    // Build Tantivy index
    let mut index = TantivyIndex::open(tmp.path().join("index/tantivy")).unwrap();
    
    for id in &["rust", "go", "python"] {
        let concept = panini_core::schema::crud::read_concept(&repo, id).unwrap();
        index.add_concept(&concept).unwrap();
    }
    
    index.commit().unwrap();
    
    // Search tests
    let results = index.search("memory safety", 10).unwrap();
    assert_eq!(results.len(), 1);
    assert_eq!(results[0].id, "rust");
    
    let results = index.search("Programming", 10).unwrap();
    assert_eq!(results.len(), 3); // All have "Programming" in title
    
    let results = index.search("concurrency", 10).unwrap();
    assert_eq!(results.len(), 1);
    assert_eq!(results[0].id, "go");
}

#[test]
fn test_query_engine_integration() {
    let tmp = TempDir::new().unwrap();
    let repo = PaniniRepo::init(tmp.path().join("repo")).unwrap();
    
    // Create knowledge base
    create_test_concept(&repo, "animal", "Animal", "Living organisms that can move.");
    create_test_concept(&repo, "mammal", "Mammal", "Warm-blooded vertebrates.");
    create_test_concept(&repo, "dog", "Dog", "Domesticated mammal, loyal companion.");
    
    add_relation(&repo, "mammal", RelationType::IsA, "animal", None).unwrap();
    add_relation(&repo, "dog", RelationType::IsA, "mammal", None).unwrap();
    
    // Create query engine
    let engine = QueryEngine::new(repo, &tmp.path().join("index")).unwrap();
    engine.rebuild().unwrap();
    
    // Test concept retrieval
    let concept = engine.get_concept("dog").unwrap();
    assert!(concept.is_some());
    assert_eq!(concept.unwrap().title, "Dog");
    
    // Test relation queries
    let relations = engine.get_relations("dog").unwrap();
    assert_eq!(relations.len(), 1);
    assert_eq!(relations[0].target, "mammal");
    
    // Test fulltext search
    let results = engine.search("companion", 10).unwrap();
    assert_eq!(results.len(), 1);
    assert_eq!(results[0].id, "dog");
    
    // Test statistics
    let stats = engine.stats().unwrap();
    assert_eq!(stats.concepts_indexed, 3);
    assert_eq!(stats.relations_indexed, 2);
    assert_eq!(stats.fulltext_docs, 3);
}

#[test]
fn test_cache_performance() {
    let tmp = TempDir::new().unwrap();
    let repo = PaniniRepo::init(tmp.path().join("repo")).unwrap();
    
    // Create concepts
    for i in 0..10 {
        create_test_concept(&repo, &format!("concept{}", i), &format!("Concept {}", i), "Test content");
    }
    
    let engine = QueryEngine::new(repo, &tmp.path().join("index")).unwrap();
    engine.rebuild().unwrap();
    
    // First pass (cache misses)
    for i in 0..10 {
        let _ = engine.get_concept(&format!("concept{}", i)).unwrap();
    }
    
    // Second pass (cache hits)
    for i in 0..10 {
        let _ = engine.get_concept(&format!("concept{}", i)).unwrap();
    }
    
    let stats = engine.stats().unwrap();
    println!("Cache hits: {}, misses: {}", stats.cache_hits, stats.cache_misses);
    println!("Hit rate: {:.2}%", stats.cache_hit_rate());
    
    assert!(stats.cache_hits > 0);
    assert!(stats.cache_hit_rate() > 40.0); // At least 40% hit rate
}

#[test]
fn test_complex_query_scenario() {
    let tmp = TempDir::new().unwrap();
    let repo = PaniniRepo::init(tmp.path().join("repo")).unwrap();
    
    // Build a complex knowledge base
    let concepts = vec![
        ("cs", "Computer Science", "Study of computation and information."),
        ("ai", "Artificial Intelligence", "Machines that can perform intelligent tasks."),
        ("ml", "Machine Learning", "Subset of AI focused on learning from data."),
        ("dl", "Deep Learning", "Neural networks with multiple layers."),
        ("cv", "Computer Vision", "Teaching computers to understand images."),
    ];
    
    for (id, title, body) in &concepts {
        create_test_concept(&repo, id, title, body);
    }
    
    // Add relations
    add_relation(&repo, "ai", RelationType::PartOf, "cs", Some(0.9)).unwrap();
    add_relation(&repo, "ml", RelationType::PartOf, "ai", Some(1.0)).unwrap();
    add_relation(&repo, "dl", RelationType::IsA, "ml", Some(1.0)).unwrap();
    add_relation(&repo, "cv", RelationType::RelatedTo, "dl", Some(0.8)).unwrap();
    add_relation(&repo, "cv", RelationType::PartOf, "ai", Some(0.9)).unwrap();
    
    let engine = QueryEngine::new(repo, &tmp.path().join("index")).unwrap();
    engine.rebuild().unwrap();
    
    // Test graph building
    let graph = engine.build_graph().unwrap();
    let stats = graph.stats();
    
    assert_eq!(stats.node_count, 5);
    assert_eq!(stats.edge_count, 5);
    
    // Test BFS from root
    let reachable = graph.bfs("cs", None).unwrap();
    assert!(reachable.len() >= 3); // cs -> ai -> ml -> dl, cv
    
    // Test shortest path
    let path = graph.shortest_path("dl", "cs").unwrap();
    assert!(path.is_some());
    let path = path.unwrap();
    assert_eq!(path[0], "dl");
    assert_eq!(path[path.len() - 1], "cs");
    
    // Test search
    let results = engine.search("neural networks", 10).unwrap();
    assert!(results.iter().any(|r| r.id == "dl"));
    
    // Test find by relation
    let part_of_concepts = engine.find_by_relation(RelationType::PartOf).unwrap();
    assert!(part_of_concepts.contains(&"ml".to_string()));
    assert!(part_of_concepts.contains(&"cv".to_string()));
}

#[test]
fn test_large_scale_indexing() {
    let tmp = TempDir::new().unwrap();
    let repo = PaniniRepo::init(tmp.path().join("repo")).unwrap();
    
    // Create 200 concepts
    for i in 0..200 {
        create_test_concept(
            &repo,
            &format!("concept{}", i),
            &format!("Concept Number {}", i),
            &format!("This is the content for concept {}. It contains various keywords for testing fulltext search.", i),
        );
    }
    
    // Add relations (chain)
    for i in 0..199 {
        add_relation(
            &repo,
            &format!("concept{}", i),
            RelationType::Causes,
            &format!("concept{}", i + 1),
            Some(0.5),
        )
        .unwrap();
    }
    
    // Build index
    let start = std::time::Instant::now();
    let engine = QueryEngine::new(repo, &tmp.path().join("index")).unwrap();
    engine.rebuild().unwrap();
    let duration = start.elapsed();
    
    println!("Index build time: {:?}", duration);
    assert!(duration.as_secs() < 10); // Should complete in < 10s
    
    let stats = engine.stats().unwrap();
    assert_eq!(stats.concepts_indexed, 200);
    assert_eq!(stats.relations_indexed, 199);
    assert_eq!(stats.fulltext_docs, 200);
    
    // Test search performance
    let start = std::time::Instant::now();
    let results = engine.search("concept", 10).unwrap();
    let search_time = start.elapsed();
    
    println!("Search time: {:?}", search_time);
    assert!(search_time.as_millis() < 100); // Should search in < 100ms
    assert_eq!(results.len(), 10);
}
