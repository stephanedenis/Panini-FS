//! Integration tests for schema module

use panini_core::git::repo::PaniniRepo;
use panini_core::schema::concept::{Concept, ConceptType};
use panini_core::schema::crud::{create_concept, delete_concept, list_concepts, read_concept, update_concept};
use panini_core::schema::dhatu::Dhatu;
use panini_core::schema::graph::KnowledgeGraph;
use panini_core::schema::relation::RelationType;
use panini_core::schema::relations::{add_relation, get_relations, get_relation_stats, remove_relation};
use panini_core::schema::taxonomy::Taxonomy;
use chrono::Utc;
use tempfile::TempDir;

fn create_test_concept(repo: &PaniniRepo, id: &str, title: &str) -> Concept {
    let concept = Concept {
        id: id.to_string(),
        r#type: ConceptType::Concept,
        dhatu: Dhatu::TEXT,
        title: title.to_string(),
        tags: vec!["test".to_string()],
        created: Utc::now(),
        updated: Utc::now(),
        author: None,
        relations: vec![],
        content_refs: vec![],
        metadata: serde_json::Value::Null,
        markdown_body: format!("# {}\n\nTest content for {}", title, id),
    };
    
    create_concept(repo, &concept).unwrap();
    concept
}

#[test]
fn test_full_concept_lifecycle() {
    let tmp = TempDir::new().unwrap();
    let repo = PaniniRepo::init(tmp.path()).unwrap();
    
    // Create
    let concept = create_test_concept(&repo, "rust", "Rust Programming");
    assert!(repo.path.join("knowledge/rust.md").exists());
    
    // Read
    let read = read_concept(&repo, "rust").unwrap();
    assert_eq!(read.id, "rust");
    assert_eq!(read.title, "Rust Programming");
    
    // Update
    let mut updated = read.clone();
    updated.title = "Rust Language".to_string();
    update_concept(&repo, &updated).unwrap();
    
    let read2 = read_concept(&repo, "rust").unwrap();
    assert_eq!(read2.title, "Rust Language");
    
    // Delete
    delete_concept(&repo, "rust").unwrap();
    assert!(!repo.path.join("knowledge/rust.md").exists());
}

#[test]
fn test_crud_with_relations() {
    let tmp = TempDir::new().unwrap();
    let repo = PaniniRepo::init(tmp.path()).unwrap();
    
    // Create concepts
    create_test_concept(&repo, "programming", "Programming");
    create_test_concept(&repo, "rust", "Rust");
    
    // Add relation
    add_relation(&repo, "rust", RelationType::IsA, "programming", Some(0.9)).unwrap();
    
    // Verify relation
    let concept = read_concept(&repo, "rust").unwrap();
    assert_eq!(concept.relations.len(), 1);
    assert_eq!(concept.relations[0].rel_type, RelationType::IsA);
    assert_eq!(concept.relations[0].target, "programming");
    assert_eq!(concept.relations[0].confidence, 0.9);
    
    // Remove relation
    remove_relation(&repo, "rust", RelationType::IsA, "programming").unwrap();
    
    let concept2 = read_concept(&repo, "rust").unwrap();
    assert_eq!(concept2.relations.len(), 0);
}

#[test]
fn test_graph_building_from_concepts() {
    let tmp = TempDir::new().unwrap();
    let repo = PaniniRepo::init(tmp.path()).unwrap();
    
    // Create knowledge base
    create_test_concept(&repo, "animal", "Animal");
    create_test_concept(&repo, "mammal", "Mammal");
    create_test_concept(&repo, "dog", "Dog");
    create_test_concept(&repo, "cat", "Cat");
    
    add_relation(&repo, "mammal", RelationType::IsA, "animal", None).unwrap();
    add_relation(&repo, "dog", RelationType::IsA, "mammal", None).unwrap();
    add_relation(&repo, "cat", RelationType::IsA, "mammal", None).unwrap();
    add_relation(&repo, "dog", RelationType::RelatedTo, "cat", Some(0.7)).unwrap();
    
    // Build graph
    let graph = KnowledgeGraph::build(&repo).unwrap();
    
    // Verify structure
    let stats = graph.stats();
    assert_eq!(stats.node_count, 4);
    assert_eq!(stats.edge_count, 4);
    
    // Test neighbors
    let neighbors = graph.neighbors("mammal").unwrap();
    assert_eq!(neighbors.len(), 1); // only animal
    
    // Test shortest path
    let path = graph.shortest_path("dog", "animal").unwrap();
    assert!(path.is_some());
    assert_eq!(path.unwrap().len(), 3); // dog -> mammal -> animal
}

#[test]
fn test_taxonomy_integration() {
    let tmp = TempDir::new().unwrap();
    let repo = PaniniRepo::init(tmp.path()).unwrap();
    
    // Create taxonomy
    create_test_concept(&repo, "vehicle", "Vehicle");
    create_test_concept(&repo, "car", "Car");
    create_test_concept(&repo, "truck", "Truck");
    create_test_concept(&repo, "sedan", "Sedan");
    
    add_relation(&repo, "car", RelationType::IsA, "vehicle", None).unwrap();
    add_relation(&repo, "truck", RelationType::IsA, "vehicle", None).unwrap();
    add_relation(&repo, "sedan", RelationType::IsA, "car", None).unwrap();
    
    // Build taxonomy
    let taxonomy = Taxonomy::build(&repo).unwrap();
    
    // Verify roots
    assert_eq!(taxonomy.roots.len(), 1);
    assert!(taxonomy.roots.contains(&"vehicle".to_string()));
    
    // Verify hierarchy
    let vehicle_children = taxonomy.children("vehicle");
    assert_eq!(vehicle_children.len(), 2);
    
    // Verify depth
    assert_eq!(taxonomy.depth("vehicle"), 0);
    assert_eq!(taxonomy.depth("car"), 1);
    assert_eq!(taxonomy.depth("sedan"), 2);
    
    // Verify ancestors
    let sedan_ancestors = taxonomy.ancestors("sedan");
    assert!(sedan_ancestors.contains(&"car".to_string()));
    assert!(sedan_ancestors.contains(&"vehicle".to_string()));
}

#[test]
fn test_relation_statistics() {
    let tmp = TempDir::new().unwrap();
    let repo = PaniniRepo::init(tmp.path()).unwrap();
    
    create_test_concept(&repo, "concept1", "Concept 1");
    create_test_concept(&repo, "concept2", "Concept 2");
    create_test_concept(&repo, "concept3", "Concept 3");
    
    add_relation(&repo, "concept1", RelationType::IsA, "concept2", Some(0.9)).unwrap();
    add_relation(&repo, "concept1", RelationType::PartOf, "concept3", Some(0.8)).unwrap();
    add_relation(&repo, "concept1", RelationType::Causes, "concept2", Some(0.7)).unwrap();
    
    let stats = get_relation_stats(&repo, "concept1").unwrap();
    
    assert_eq!(stats.total, 3);
    assert_eq!(stats.by_type.get(&RelationType::IsA), Some(&1));
    assert_eq!(stats.by_type.get(&RelationType::PartOf), Some(&1));
    assert_eq!(stats.by_type.get(&RelationType::Causes), Some(&1));
    
    let avg = stats.avg_confidence;
    assert!((avg - 0.8).abs() < 0.01); // (0.9 + 0.8 + 0.7) / 3 = 0.8
}

#[test]
fn test_graph_traversal_depth_limit() {
    let tmp = TempDir::new().unwrap();
    let repo = PaniniRepo::init(tmp.path()).unwrap();
    
    // Create chain: a -> b -> c -> d -> e
    create_test_concept(&repo, "a", "A");
    create_test_concept(&repo, "b", "B");
    create_test_concept(&repo, "c", "C");
    create_test_concept(&repo, "d", "D");
    create_test_concept(&repo, "e", "E");
    
    add_relation(&repo, "a", RelationType::Causes, "b", None).unwrap();
    add_relation(&repo, "b", RelationType::Causes, "c", None).unwrap();
    add_relation(&repo, "c", RelationType::Causes, "d", None).unwrap();
    add_relation(&repo, "d", RelationType::Causes, "e", None).unwrap();
    
    let graph = KnowledgeGraph::build(&repo).unwrap();
    
    // BFS with depth limit
    let result_d2 = graph.bfs("a", Some(2)).unwrap();
    assert!(result_d2.len() <= 3); // a, b, c (depth 0, 1, 2)
    
    let result_d4 = graph.bfs("a", Some(4)).unwrap();
    assert_eq!(result_d4.len(), 5); // all nodes reachable
}

#[test]
fn test_circular_dependency_detection() {
    let tmp = TempDir::new().unwrap();
    let repo = PaniniRepo::init(tmp.path()).unwrap();
    
    // Create cycle: a -> b -> c -> a
    create_test_concept(&repo, "a", "A");
    create_test_concept(&repo, "b", "B");
    create_test_concept(&repo, "c", "C");
    
    add_relation(&repo, "a", RelationType::Causes, "b", None).unwrap();
    add_relation(&repo, "b", RelationType::Causes, "c", None).unwrap();
    add_relation(&repo, "c", RelationType::Causes, "a", None).unwrap();
    
    let graph = KnowledgeGraph::build(&repo).unwrap();
    
    let stats = graph.stats();
    assert!(stats.is_cyclic);
}

#[test]
fn test_complex_knowledge_base() {
    let tmp = TempDir::new().unwrap();
    let repo = PaniniRepo::init(tmp.path()).unwrap();
    
    // Create complex knowledge base
    let concepts = vec![
        ("physics", "Physics"),
        ("mechanics", "Mechanics"),
        ("thermodynamics", "Thermodynamics"),
        ("newton_laws", "Newton's Laws"),
        ("energy", "Energy"),
    ];
    
    for (id, title) in &concepts {
        create_test_concept(&repo, id, title);
    }
    
    // Add relations
    add_relation(&repo, "mechanics", RelationType::PartOf, "physics", Some(1.0)).unwrap();
    add_relation(&repo, "thermodynamics", RelationType::PartOf, "physics", Some(1.0)).unwrap();
    add_relation(&repo, "newton_laws", RelationType::PartOf, "mechanics", Some(0.9)).unwrap();
    add_relation(&repo, "energy", RelationType::RelatedTo, "thermodynamics", Some(0.95)).unwrap();
    add_relation(&repo, "energy", RelationType::RelatedTo, "mechanics", Some(0.85)).unwrap();
    
    // Build graph
    let graph = KnowledgeGraph::build(&repo).unwrap();
    let stats = graph.stats();
    
    assert_eq!(stats.node_count, 5);
    assert_eq!(stats.edge_count, 5);
    assert!(!stats.is_cyclic);
    
    // Build taxonomy
    let taxonomy = Taxonomy::build(&repo).unwrap();
    
    // Physics should be root
    assert!(taxonomy.roots.contains(&"physics".to_string()));
    
    // Check descendants
    let physics_descendants = taxonomy.descendants("physics");
    assert!(physics_descendants.contains(&"mechanics".to_string()));
    assert!(physics_descendants.contains(&"thermodynamics".to_string()));
    
    // List all concepts
    let all = list_concepts(&repo).unwrap();
    assert_eq!(all.len(), 5);
}

#[test]
fn test_performance_large_graph() {
    let tmp = TempDir::new().unwrap();
    let repo = PaniniRepo::init(tmp.path()).unwrap();
    
    // Create 50 concepts
    for i in 0..50 {
        create_test_concept(&repo, &format!("concept{}", i), &format!("Concept {}", i));
    }
    
    // Add relations (chain)
    for i in 0..49 {
        add_relation(
            &repo,
            &format!("concept{}", i),
            RelationType::Causes,
            &format!("concept{}", i + 1),
            None,
        )
        .unwrap();
    }
    
    // Build graph (should be fast)
    let start = std::time::Instant::now();
    let graph = KnowledgeGraph::build(&repo).unwrap();
    let build_time = start.elapsed();
    
    println!("Graph build time: {:?}", build_time);
    assert!(build_time.as_millis() < 1000); // Should build in < 1s
    
    // BFS traversal
    let start = std::time::Instant::now();
    let result = graph.bfs("concept0", None).unwrap();
    let bfs_time = start.elapsed();
    
    println!("BFS time: {:?}", bfs_time);
    assert_eq!(result.len(), 50);
    assert!(bfs_time.as_millis() < 100); // Should traverse in < 100ms
}
