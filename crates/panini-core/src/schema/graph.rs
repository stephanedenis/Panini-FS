//! Graph operations using petgraph

use crate::error::{Error, Result};
use crate::git::repo::PaniniRepo;
use crate::schema::crud::{list_concepts, read_concept};
use crate::schema::relation::RelationType;
use petgraph::graph::{DiGraph, NodeIndex};
use petgraph::visit::EdgeRef;
use petgraph::Direction;
use std::collections::HashMap;

/// Knowledge graph
#[derive(Clone)]
pub struct KnowledgeGraph {
    graph: DiGraph<String, RelationType>,
    node_map: HashMap<String, NodeIndex>,
}

impl KnowledgeGraph {
    /// Build graph from repository
    pub fn build(repo: &PaniniRepo) -> Result<Self> {
        let mut graph = DiGraph::new();
        let mut node_map = HashMap::new();
        
        // Get all concepts
        let concept_ids = list_concepts(repo)?;
        
        // Add nodes
        for id in &concept_ids {
            let idx = graph.add_node(id.clone());
            node_map.insert(id.clone(), idx);
        }
        
        // Add edges (relations)
        for id in &concept_ids {
            let concept = read_concept(repo, id)?;
            let source_idx = node_map[id];
            
            for relation in &concept.relations {
                if let Some(&target_idx) = node_map.get(&relation.target) {
                    graph.add_edge(source_idx, target_idx, relation.rel_type);
                }
            }
        }
        
        Ok(Self { graph, node_map })
    }
    
    /// Get node index by concept ID
    pub fn get_node(&self, id: &str) -> Option<NodeIndex> {
        self.node_map.get(id).copied()
    }
    
    /// Get concept ID by node index
    pub fn get_concept_id(&self, idx: NodeIndex) -> Option<&str> {
        self.graph.node_weight(idx).map(|s| s.as_str())
    }
    
    /// Get neighbors (outgoing edges)
    pub fn neighbors(&self, id: &str) -> Result<Vec<String>> {
        let idx = self.get_node(id)
            .ok_or_else(|| Error::NotFound(format!("Concept not found: {}", id)))?;
        
        Ok(self.graph
            .neighbors(idx)
            .filter_map(|n| self.graph.node_weight(n).cloned())
            .collect())
    }
    
    /// Get neighbors by relation type
    pub fn neighbors_by_type(&self, id: &str, rel_type: RelationType) -> Result<Vec<String>> {
        let idx = self.get_node(id)
            .ok_or_else(|| Error::NotFound(format!("Concept not found: {}", id)))?;
        
        Ok(self.graph
            .edges(idx)
            .filter(|e| *e.weight() == rel_type)
            .filter_map(|e| self.graph.node_weight(e.target()).cloned())
            .collect())
    }
    
    /// Get predecessors (incoming edges)
    pub fn predecessors(&self, id: &str) -> Result<Vec<String>> {
        let idx = self.get_node(id)
            .ok_or_else(|| Error::NotFound(format!("Concept not found: {}", id)))?;
        
        Ok(self.graph
            .neighbors_directed(idx, Direction::Incoming)
            .filter_map(|n| self.graph.node_weight(n).cloned())
            .collect())
    }
    
    /// Shortest path between two concepts
    pub fn shortest_path(&self, from: &str, to: &str) -> Result<Option<Vec<String>>> {
        let from_idx = self.get_node(from)
            .ok_or_else(|| Error::NotFound(format!("Concept not found: {}", from)))?;
        let to_idx = self.get_node(to)
            .ok_or_else(|| Error::NotFound(format!("Concept not found: {}", to)))?;
        
        // Use Dijkstra for shortest path
        let path_map = petgraph::algo::dijkstra(&self.graph, from_idx, Some(to_idx), |_| 1);
        
        if !path_map.contains_key(&to_idx) {
            return Ok(None); // No path found
        }
        
        // Reconstruct path
        let mut path = Vec::new();
        let mut current = to_idx;
        path.push(self.get_concept_id(current).unwrap().to_string());
        
        while current != from_idx {
            // Find predecessor
            let mut found = false;
            for pred in self.graph.neighbors_directed(current, Direction::Incoming) {
                if path_map.contains_key(&pred) && path_map[&pred] + 1 == path_map[&current] {
                    current = pred;
                    path.push(self.get_concept_id(current).unwrap().to_string());
                    found = true;
                    break;
                }
            }
            
            if !found {
                break;
            }
        }
        
        path.reverse();
        Ok(Some(path))
    }
    
    /// Breadth-first traversal from node
    pub fn bfs(&self, start: &str, max_depth: Option<usize>) -> Result<Vec<String>> {
        let start_idx = self.get_node(start)
            .ok_or_else(|| Error::NotFound(format!("Concept not found: {}", start)))?;
        
        let mut visited = Vec::new();
        let mut queue = std::collections::VecDeque::new();
        let mut visited_set = std::collections::HashSet::new();
        
        queue.push_back((start_idx, 0));
        visited_set.insert(start_idx);
        
        while let Some((idx, depth)) = queue.pop_front() {
            if let Some(max) = max_depth {
                if depth > max {
                    continue;
                }
            }
            
            if let Some(id) = self.get_concept_id(idx) {
                visited.push(id.to_string());
            }
            
            for neighbor in self.graph.neighbors(idx) {
                if !visited_set.contains(&neighbor) {
                    visited_set.insert(neighbor);
                    queue.push_back((neighbor, depth + 1));
                }
            }
        }
        
        Ok(visited)
    }
    
    /// Depth-first traversal from node
    pub fn dfs(&self, start: &str, max_depth: Option<usize>) -> Result<Vec<String>> {
        let start_idx = self.get_node(start)
            .ok_or_else(|| Error::NotFound(format!("Concept not found: {}", start)))?;
        
        let mut visited = Vec::new();
        let mut stack = vec![(start_idx, 0)];
        let mut visited_set = std::collections::HashSet::new();
        
        while let Some((idx, depth)) = stack.pop() {
            if visited_set.contains(&idx) {
                continue;
            }
            
            if let Some(max) = max_depth {
                if depth > max {
                    continue;
                }
            }
            
            visited_set.insert(idx);
            
            if let Some(id) = self.get_concept_id(idx) {
                visited.push(id.to_string());
            }
            
            for neighbor in self.graph.neighbors(idx) {
                if !visited_set.contains(&neighbor) {
                    stack.push((neighbor, depth + 1));
                }
            }
        }
        
        Ok(visited)
    }
    
    /// Detect cycles in graph
    pub fn has_cycle(&self) -> bool {
        petgraph::algo::is_cyclic_directed(&self.graph)
    }
    
    /// Find strongly connected components
    pub fn strongly_connected_components(&self) -> Vec<Vec<String>> {
        let sccs = petgraph::algo::tarjan_scc(&self.graph);
        
        sccs.into_iter()
            .map(|component| {
                component
                    .into_iter()
                    .filter_map(|idx| self.get_concept_id(idx).map(|s| s.to_string()))
                    .collect()
            })
            .collect()
    }
    
    /// Get graph statistics
    pub fn stats(&self) -> GraphStats {
        GraphStats {
            node_count: self.graph.node_count(),
            edge_count: self.graph.edge_count(),
            is_cyclic: self.has_cycle(),
            avg_degree: if self.graph.node_count() > 0 {
                self.graph.edge_count() as f32 / self.graph.node_count() as f32
            } else {
                0.0
            },
        }
    }
    
    /// Get node degree (in + out)
    pub fn degree(&self, id: &str) -> Result<(usize, usize)> {
        let idx = self.get_node(id)
            .ok_or_else(|| Error::NotFound(format!("Concept not found: {}", id)))?;
        
        let in_degree = self.graph.neighbors_directed(idx, Direction::Incoming).count();
        let out_degree = self.graph.neighbors_directed(idx, Direction::Outgoing).count();
        
        Ok((in_degree, out_degree))
    }
}

/// Graph statistics
#[derive(Debug, Clone)]
pub struct GraphStats {
    pub node_count: usize,
    pub edge_count: usize,
    pub is_cyclic: bool,
    pub avg_degree: f32,
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::schema::concept::{Concept, ConceptType};
    use crate::schema::crud::create_concept;
    use crate::schema::dhatu::Dhatu;
    use crate::schema::relations::add_relation;
    use chrono::Utc;
    use tempfile::TempDir;
    
    fn create_test_concept(repo: &PaniniRepo, id: &str) -> Concept {
        let concept = Concept {
            id: id.to_string(),
            r#type: ConceptType::Concept,
            dhatu: Dhatu::TEXT,
            title: format!("Test {}", id),
            tags: vec![],
            created: Utc::now(),
            updated: Utc::now(),
            author: None,
            relations: vec![],
            content_refs: vec![],
            metadata: serde_json::Value::Null,
            markdown_body: format!("# Test {}", id),
        };
        
        create_concept(repo, &concept).unwrap();
        concept
    }
    
    #[test]
    fn test_build_graph() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        create_test_concept(&repo, "a");
        create_test_concept(&repo, "b");
        create_test_concept(&repo, "c");
        
        add_relation(&repo, "a", RelationType::IsA, "b", None).unwrap();
        add_relation(&repo, "b", RelationType::IsA, "c", None).unwrap();
        
        let graph = KnowledgeGraph::build(&repo).unwrap();
        let stats = graph.stats();
        
        assert_eq!(stats.node_count, 3);
        assert_eq!(stats.edge_count, 2);
    }
    
    #[test]
    fn test_neighbors() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        create_test_concept(&repo, "a");
        create_test_concept(&repo, "b");
        create_test_concept(&repo, "c");
        
        add_relation(&repo, "a", RelationType::IsA, "b", None).unwrap();
        add_relation(&repo, "a", RelationType::PartOf, "c", None).unwrap();
        
        let graph = KnowledgeGraph::build(&repo).unwrap();
        let neighbors = graph.neighbors("a").unwrap();
        
        assert_eq!(neighbors.len(), 2);
        assert!(neighbors.contains(&"b".to_string()));
        assert!(neighbors.contains(&"c".to_string()));
    }
    
    #[test]
    fn test_shortest_path() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        create_test_concept(&repo, "a");
        create_test_concept(&repo, "b");
        create_test_concept(&repo, "c");
        create_test_concept(&repo, "d");
        
        add_relation(&repo, "a", RelationType::IsA, "b", None).unwrap();
        add_relation(&repo, "b", RelationType::IsA, "c", None).unwrap();
        add_relation(&repo, "c", RelationType::IsA, "d", None).unwrap();
        
        let graph = KnowledgeGraph::build(&repo).unwrap();
        let path = graph.shortest_path("a", "d").unwrap().unwrap();
        
        assert_eq!(path, vec!["a", "b", "c", "d"]);
    }
    
    #[test]
    fn test_bfs() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        create_test_concept(&repo, "a");
        create_test_concept(&repo, "b");
        create_test_concept(&repo, "c");
        
        add_relation(&repo, "a", RelationType::IsA, "b", None).unwrap();
        add_relation(&repo, "a", RelationType::IsA, "c", None).unwrap();
        
        let graph = KnowledgeGraph::build(&repo).unwrap();
        let visited = graph.bfs("a", None).unwrap();
        
        assert_eq!(visited.len(), 3);
        assert_eq!(visited[0], "a"); // Start node first
    }
    
    #[test]
    fn test_has_cycle() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        create_test_concept(&repo, "a");
        create_test_concept(&repo, "b");
        create_test_concept(&repo, "c");
        
        // Create cycle: a -> b -> c -> a
        add_relation(&repo, "a", RelationType::IsA, "b", None).unwrap();
        add_relation(&repo, "b", RelationType::IsA, "c", None).unwrap();
        add_relation(&repo, "c", RelationType::IsA, "a", None).unwrap();
        
        let graph = KnowledgeGraph::build(&repo).unwrap();
        
        assert!(graph.has_cycle());
    }
    
    #[test]
    fn test_degree() {
        let tmp = TempDir::new().unwrap();
        let repo = PaniniRepo::init(tmp.path()).unwrap();
        
        create_test_concept(&repo, "a");
        create_test_concept(&repo, "b");
        create_test_concept(&repo, "c");
        
        add_relation(&repo, "a", RelationType::IsA, "b", None).unwrap();
        add_relation(&repo, "c", RelationType::IsA, "b", None).unwrap();
        
        let graph = KnowledgeGraph::build(&repo).unwrap();
        let (in_deg, out_deg) = graph.degree("b").unwrap();
        
        assert_eq!(in_deg, 2); // a -> b, c -> b
        assert_eq!(out_deg, 0);
    }
}
