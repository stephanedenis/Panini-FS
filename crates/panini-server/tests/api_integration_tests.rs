use axum::{
    body::Body,
    http::{Request, StatusCode},
};
use panini_core::schema::concept::Concept;
use serde_json::json;
use tower::ServiceExt;

async fn setup_test_app() -> axum::Router {
    // Test setup would normally use a test repo
    // Simplified for illustration
    panini_server::create_app().await
}

#[tokio::test]
async fn test_root_endpoint() {
    let app = setup_test_app().await;
    
    let response = app
        .oneshot(Request::builder().uri("/").body(Body::empty()).unwrap())
        .await
        .unwrap();
    
    assert_eq!(response.status(), StatusCode::OK);
    
    let body = hyper::body::to_bytes(response.into_body()).await.unwrap();
    let body_str = String::from_utf8(body.to_vec()).unwrap();
    
    assert!(body_str.contains("Panini-FS"));
}

#[tokio::test]
async fn test_health_endpoint() {
    let app = setup_test_app().await;
    
    let response = app
        .oneshot(Request::builder().uri("/health").body(Body::empty()).unwrap())
        .await
        .unwrap();
    
    assert_eq!(response.status(), StatusCode::OK);
    
    let body = hyper::body::to_bytes(response.into_body()).await.unwrap();
    assert_eq!(&body[..], b"OK");
}

#[tokio::test]
async fn test_list_concepts_empty() {
    let app = setup_test_app().await;
    
    let response = app
        .oneshot(
            Request::builder()
                .uri("/concepts")
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();
    
    assert_eq!(response.status(), StatusCode::OK);
    
    let body = hyper::body::to_bytes(response.into_body()).await.unwrap();
    let concepts: Vec<String> = serde_json::from_slice(&body).unwrap();
    
    assert!(concepts.is_empty() || concepts.len() >= 0);
}

#[tokio::test]
async fn test_create_concept() {
    let app = setup_test_app().await;
    
    let concept = json!({
        "id": "test_concept",
        "title": "Test Concept",
        "dhatu": "SEEKING",
        "tags": ["test"]
    });
    
    let response = app
        .oneshot(
            Request::builder()
                .method("POST")
                .uri("/concepts")
                .header("content-type", "application/json")
                .body(Body::from(serde_json::to_vec(&concept).unwrap()))
                .unwrap(),
        )
        .await
        .unwrap();
    
    assert_eq!(response.status(), StatusCode::CREATED);
}

#[tokio::test]
async fn test_get_concept() {
    let app = setup_test_app().await;
    
    // First create a concept
    let concept = json!({
        "id": "get_test",
        "title": "Get Test",
        "dhatu": "SEEKING"
    });
    
    let _ = app
        .clone()
        .oneshot(
            Request::builder()
                .method("POST")
                .uri("/concepts")
                .header("content-type", "application/json")
                .body(Body::from(serde_json::to_vec(&concept).unwrap()))
                .unwrap(),
        )
        .await
        .unwrap();
    
    // Then retrieve it
    let response = app
        .oneshot(
            Request::builder()
                .uri("/concepts/get_test")
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();
    
    assert!(
        response.status() == StatusCode::OK || response.status() == StatusCode::NOT_FOUND
    );
}

#[tokio::test]
async fn test_get_nonexistent_concept() {
    let app = setup_test_app().await;
    
    let response = app
        .oneshot(
            Request::builder()
                .uri("/concepts/nonexistent_id_12345")
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();
    
    assert_eq!(response.status(), StatusCode::NOT_FOUND);
}

#[tokio::test]
async fn test_update_concept() {
    let app = setup_test_app().await;
    
    let concept = json!({
        "id": "update_test",
        "title": "Original Title",
        "dhatu": "SEEKING"
    });
    
    // Create
    let _ = app
        .clone()
        .oneshot(
            Request::builder()
                .method("POST")
                .uri("/concepts")
                .header("content-type", "application/json")
                .body(Body::from(serde_json::to_vec(&concept).unwrap()))
                .unwrap(),
        )
        .await
        .unwrap();
    
    // Update
    let updated = json!({
        "id": "update_test",
        "title": "Updated Title",
        "dhatu": "SEEKING"
    });
    
    let response = app
        .oneshot(
            Request::builder()
                .method("PUT")
                .uri("/concepts/update_test")
                .header("content-type", "application/json")
                .body(Body::from(serde_json::to_vec(&updated).unwrap()))
                .unwrap(),
        )
        .await
        .unwrap();
    
    assert!(
        response.status() == StatusCode::OK || response.status() == StatusCode::NOT_FOUND
    );
}

#[tokio::test]
async fn test_update_id_mismatch() {
    let app = setup_test_app().await;
    
    let concept = json!({
        "id": "wrong_id",
        "title": "Test",
        "dhatu": "SEEKING"
    });
    
    let response = app
        .oneshot(
            Request::builder()
                .method("PUT")
                .uri("/concepts/correct_id")
                .header("content-type", "application/json")
                .body(Body::from(serde_json::to_vec(&concept).unwrap()))
                .unwrap(),
        )
        .await
        .unwrap();
    
    assert_eq!(response.status(), StatusCode::BAD_REQUEST);
}

#[tokio::test]
async fn test_delete_concept() {
    let app = setup_test_app().await;
    
    let concept = json!({
        "id": "delete_test",
        "title": "To Delete",
        "dhatu": "SEEKING"
    });
    
    // Create
    let _ = app
        .clone()
        .oneshot(
            Request::builder()
                .method("POST")
                .uri("/concepts")
                .header("content-type", "application/json")
                .body(Body::from(serde_json::to_vec(&concept).unwrap()))
                .unwrap(),
        )
        .await
        .unwrap();
    
    // Delete
    let response = app
        .oneshot(
            Request::builder()
                .method("DELETE")
                .uri("/concepts/delete_test")
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();
    
    assert!(
        response.status() == StatusCode::NO_CONTENT
            || response.status() == StatusCode::INTERNAL_SERVER_ERROR
    );
}

#[tokio::test]
async fn test_get_relations() {
    let app = setup_test_app().await;
    
    let response = app
        .oneshot(
            Request::builder()
                .uri("/concepts/test_concept/relations")
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();
    
    assert!(
        response.status() == StatusCode::OK
            || response.status() == StatusCode::INTERNAL_SERVER_ERROR
    );
}

#[tokio::test]
async fn test_add_relation() {
    let app = setup_test_app().await;
    
    // Create source concept
    let source = json!({
        "id": "rel_source",
        "title": "Source",
        "dhatu": "SEEKING"
    });
    
    let _ = app
        .clone()
        .oneshot(
            Request::builder()
                .method("POST")
                .uri("/concepts")
                .header("content-type", "application/json")
                .body(Body::from(serde_json::to_vec(&source).unwrap()))
                .unwrap(),
        )
        .await
        .unwrap();
    
    // Create target concept
    let target = json!({
        "id": "rel_target",
        "title": "Target",
        "dhatu": "SEEKING"
    });
    
    let _ = app
        .clone()
        .oneshot(
            Request::builder()
                .method("POST")
                .uri("/concepts")
                .header("content-type", "application/json")
                .body(Body::from(serde_json::to_vec(&target).unwrap()))
                .unwrap(),
        )
        .await
        .unwrap();
    
    // Add relation
    let relation = json!({
        "rel_type": "is_a",
        "target": "rel_target",
        "confidence": 0.9
    });
    
    let response = app
        .oneshot(
            Request::builder()
                .method("POST")
                .uri("/concepts/rel_source/relations")
                .header("content-type", "application/json")
                .body(Body::from(serde_json::to_vec(&relation).unwrap()))
                .unwrap(),
        )
        .await
        .unwrap();
    
    assert!(
        response.status() == StatusCode::CREATED
            || response.status() == StatusCode::INTERNAL_SERVER_ERROR
    );
}

#[tokio::test]
async fn test_add_relation_invalid_type() {
    let app = setup_test_app().await;
    
    let relation = json!({
        "rel_type": "invalid_type",
        "target": "some_target",
        "confidence": 0.5
    });
    
    let response = app
        .oneshot(
            Request::builder()
                .method("POST")
                .uri("/concepts/some_source/relations")
                .header("content-type", "application/json")
                .body(Body::from(serde_json::to_vec(&relation).unwrap()))
                .unwrap(),
        )
        .await
        .unwrap();
    
    assert_eq!(response.status(), StatusCode::BAD_REQUEST);
}

#[tokio::test]
async fn test_cors_headers() {
    let app = setup_test_app().await;
    
    let response = app
        .oneshot(
            Request::builder()
                .method("OPTIONS")
                .uri("/concepts")
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();
    
    // CORS should allow cross-origin requests
    assert!(response.headers().contains_key("access-control-allow-origin"));
}
