use assert_cmd::Command;
use predicates::prelude::*;
use std::fs;
use tempfile::TempDir;

#[test]
fn test_cli_init() {
    let tmp = TempDir::new().unwrap();
    
    Command::cargo_bin("panini-cli").unwrap()
        .arg("init")
        .arg(tmp.path())
        .assert()
        .success()
        .stdout(predicate::str::contains("✅"))
        .stdout(predicate::str::contains("Initialized"));
}

#[test]
fn test_cli_create_read() {
    let tmp = TempDir::new().unwrap();
    
    // Init repo
    Command::cargo_bin("panini-cli").unwrap()
        .arg("init")
        .arg(tmp.path())
        .assert()
        .success();
    
    // Create concept
    Command::cargo_bin("panini-cli").unwrap()
        .current_dir(tmp.path())
        .arg("create")
        .arg("test_concept")
        .arg("--title")
        .arg("Test Concept")
        .assert()
        .success()
        .stdout(predicate::str::contains("✅"))
        .stdout(predicate::str::contains("test_concept"));
    
    // Read concept
    Command::cargo_bin("panini-cli").unwrap()
        .current_dir(tmp.path())
        .arg("read")
        .arg("test_concept")
        .assert()
        .success()
        .stdout(predicate::str::contains("test_concept"))
        .stdout(predicate::str::contains("Test Concept"));
}

#[test]
fn test_cli_create_with_tags() {
    let tmp = TempDir::new().unwrap();
    
    Command::cargo_bin("panini-cli").unwrap()
        .arg("init")
        .arg(tmp.path())
        .assert()
        .success();
    
    Command::cargo_bin("panini-cli").unwrap()
        .current_dir(tmp.path())
        .arg("create")
        .arg("tagged_concept")
        .arg("--title")
        .arg("Tagged")
        .arg("--tags")
        .arg("tag1,tag2,tag3")
        .assert()
        .success();
    
    Command::cargo_bin("panini-cli").unwrap()
        .current_dir(tmp.path())
        .arg("read")
        .arg("tagged_concept")
        .arg("--json")
        .assert()
        .success()
        .stdout(predicate::str::contains("tag1"))
        .stdout(predicate::str::contains("tag2"));
}

#[test]
fn test_cli_update() {
    let tmp = TempDir::new().unwrap();
    
    Command::cargo_bin("panini-cli").unwrap()
        .arg("init")
        .arg(tmp.path())
        .assert()
        .success();
    
    Command::cargo_bin("panini-cli").unwrap()
        .current_dir(tmp.path())
        .arg("create")
        .arg("update_test")
        .arg("--title")
        .arg("Original")
        .assert()
        .success();
    
    Command::cargo_bin("panini-cli").unwrap()
        .current_dir(tmp.path())
        .arg("update")
        .arg("update_test")
        .arg("--title")
        .arg("Updated Title")
        .assert()
        .success()
        .stdout(predicate::str::contains("✅"))
        .stdout(predicate::str::contains("Updated"));
    
    Command::cargo_bin("panini-cli").unwrap()
        .current_dir(tmp.path())
        .arg("read")
        .arg("update_test")
        .assert()
        .stdout(predicate::str::contains("Updated Title"));
}

#[test]
fn test_cli_delete() {
    let tmp = TempDir::new().unwrap();
    
    Command::cargo_bin("panini-cli").unwrap()
        .arg("init")
        .arg(tmp.path())
        .assert()
        .success();
    
    Command::cargo_bin("panini-cli").unwrap()
        .current_dir(tmp.path())
        .arg("create")
        .arg("delete_test")
        .arg("--title")
        .arg("To Delete")
        .assert()
        .success();
    
    Command::cargo_bin("panini-cli").unwrap()
        .current_dir(tmp.path())
        .arg("delete")
        .arg("delete_test")
        .assert()
        .success()
        .stdout(predicate::str::contains("✅"))
        .stdout(predicate::str::contains("Deleted"));
    
    Command::cargo_bin("panini-cli").unwrap()
        .current_dir(tmp.path())
        .arg("read")
        .arg("delete_test")
        .assert()
        .failure();
}

#[test]
fn test_cli_list() {
    let tmp = TempDir::new().unwrap();
    
    Command::cargo_bin("panini-cli").unwrap()
        .arg("init")
        .arg(tmp.path())
        .assert()
        .success();
    
    // Create multiple concepts
    for i in 1..=3 {
        Command::cargo_bin("panini-cli").unwrap()
            .current_dir(tmp.path())
            .arg("create")
            .arg(format!("concept_{}", i))
            .arg("--title")
            .arg(format!("Concept {}", i))
            .assert()
            .success();
    }
    
    Command::cargo_bin("panini-cli").unwrap()
        .current_dir(tmp.path())
        .arg("list")
        .assert()
        .success()
        .stdout(predicate::str::contains("concept_1"))
        .stdout(predicate::str::contains("concept_2"))
        .stdout(predicate::str::contains("concept_3"));
}

#[test]
fn test_cli_list_json() {
    let tmp = TempDir::new().unwrap();
    
    Command::cargo_bin("panini-cli").unwrap()
        .arg("init")
        .arg(tmp.path())
        .assert()
        .success();
    
    Command::cargo_bin("panini-cli").unwrap()
        .current_dir(tmp.path())
        .arg("create")
        .arg("json_test")
        .arg("--title")
        .arg("JSON Test")
        .assert()
        .success();
    
    Command::cargo_bin("panini-cli").unwrap()
        .current_dir(tmp.path())
        .arg("list")
        .arg("--json")
        .assert()
        .success()
        .stdout(predicate::str::contains("["))
        .stdout(predicate::str::contains("]"))
        .stdout(predicate::str::contains("json_test"));
}

#[test]
fn test_cli_add_relation() {
    let tmp = TempDir::new().unwrap();
    
    Command::cargo_bin("panini-cli").unwrap()
        .arg("init")
        .arg(tmp.path())
        .assert()
        .success();
    
    // Create two concepts
    Command::cargo_bin("panini-cli").unwrap()
        .current_dir(tmp.path())
        .arg("create")
        .arg("parent")
        .arg("--title")
        .arg("Parent")
        .assert()
        .success();
    
    Command::cargo_bin("panini-cli").unwrap()
        .current_dir(tmp.path())
        .arg("create")
        .arg("child")
        .arg("--title")
        .arg("Child")
        .assert()
        .success();
    
    // Add relation
    Command::cargo_bin("panini-cli").unwrap()
        .current_dir(tmp.path())
        .arg("add-relation")
        .arg("child")
        .arg("--rel-type")
        .arg("is_a")
        .arg("parent")
        .assert()
        .success()
        .stdout(predicate::str::contains("✅"))
        .stdout(predicate::str::contains("-->"));
}

#[test]
fn test_cli_add_relation_with_confidence() {
    let tmp = TempDir::new().unwrap();
    
    Command::cargo_bin("panini-cli").unwrap()
        .arg("init")
        .arg(tmp.path())
        .assert()
        .success();
    
    Command::cargo_bin("panini-cli").unwrap()
        .current_dir(tmp.path())
        .arg("create")
        .arg("a")
        .arg("--title")
        .arg("A")
        .assert()
        .success();
    
    Command::cargo_bin("panini-cli").unwrap()
        .current_dir(tmp.path())
        .arg("create")
        .arg("b")
        .arg("--title")
        .arg("B")
        .assert()
        .success();
    
    Command::cargo_bin("panini-cli").unwrap()
        .current_dir(tmp.path())
        .arg("add-relation")
        .arg("a")
        .arg("--rel-type")
        .arg("related_to")
        .arg("b")
        .arg("--confidence")
        .arg("0.85")
        .assert()
        .success();
}

#[test]
fn test_cli_relations() {
    let tmp = TempDir::new().unwrap();
    
    Command::cargo_bin("panini-cli").unwrap()
        .arg("init")
        .arg(tmp.path())
        .assert()
        .success();
    
    Command::cargo_bin("panini-cli").unwrap()
        .current_dir(tmp.path())
        .arg("create")
        .arg("source")
        .arg("--title")
        .arg("Source")
        .assert()
        .success();
    
    Command::cargo_bin("panini-cli").unwrap()
        .current_dir(tmp.path())
        .arg("create")
        .arg("target")
        .arg("--title")
        .arg("Target")
        .assert()
        .success();
    
    Command::cargo_bin("panini-cli").unwrap()
        .current_dir(tmp.path())
        .arg("add-relation")
        .arg("source")
        .arg("--rel-type")
        .arg("causes")
        .arg("target")
        .assert()
        .success();
    
    Command::cargo_bin("panini-cli").unwrap()
        .current_dir(tmp.path())
        .arg("relations")
        .arg("source")
        .assert()
        .success()
        .stdout(predicate::str::contains("target"))
        .stdout(predicate::str::contains("Causes"));
}

#[test]
#[ignore] // FIXME: Status command not implemented (todo!)
fn test_cli_status() {
    let tmp = TempDir::new().unwrap();
    
    Command::cargo_bin("panini-cli").unwrap()
        .arg("init")
        .arg(tmp.path())
        .assert()
        .success();
    
    Command::cargo_bin("panini-cli").unwrap()
        .current_dir(tmp.path())
        .arg("status")
        .assert()
        .success()
        .stdout(predicate::str::contains("Status"));
}

#[test]
fn test_cli_invalid_relation_type() {
    let tmp = TempDir::new().unwrap();
    
    Command::cargo_bin("panini-cli").unwrap()
        .arg("init")
        .arg(tmp.path())
        .assert()
        .success();
    
    Command::cargo_bin("panini-cli").unwrap()
        .current_dir(tmp.path())
        .arg("create")
        .arg("a")
        .arg("--title")
        .arg("A")
        .assert()
        .success();
    
    Command::cargo_bin("panini-cli").unwrap()
        .current_dir(tmp.path())
        .arg("create")
        .arg("b")
        .arg("--title")
        .arg("B")
        .assert()
        .success();
    
    Command::cargo_bin("panini-cli").unwrap()
        .current_dir(tmp.path())
        .arg("add-relation")
        .arg("a")
        .arg("--rel-type")
        .arg("invalid_type")
        .arg("b")
        .assert()
        .failure()
        .stderr(predicate::str::contains("invalid"));
}

#[test]
fn test_cli_read_json() {
    let tmp = TempDir::new().unwrap();
    
    Command::cargo_bin("panini-cli").unwrap()
        .arg("init")
        .arg(tmp.path())
        .assert()
        .success();
    
    Command::cargo_bin("panini-cli").unwrap()
        .current_dir(tmp.path())
        .arg("create")
        .arg("json_read")
        .arg("--title")
        .arg("JSON Read Test")
        .arg("--tags")
        .arg("test,json")
        .assert()
        .success();
    
    Command::cargo_bin("panini-cli").unwrap()
        .current_dir(tmp.path())
        .arg("read")
        .arg("json_read")
        .arg("--json")
        .assert()
        .success()
        .stdout(predicate::str::contains("{"))
        .stdout(predicate::str::contains("\"id\""))
        .stdout(predicate::str::contains("\"title\""))
        .stdout(predicate::str::contains("\"tags\""));
}
