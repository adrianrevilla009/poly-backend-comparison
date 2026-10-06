use axum::{extract::Path, http::StatusCode, routing::get, Json, Router};
use serde::Serialize;
use serde_json::{json, Value};

#[derive(Serialize)]
struct Order {
    id: i64,
    customer: String,
    total: f64,
    status: &'static str,
}

async fn order(Path(id): Path<i64>) -> Result<Json<Order>, StatusCode> {
    if id < 0 {
        return Err(StatusCode::BAD_REQUEST);
    }
    Ok(Json(Order { id, customer: format!("c-{}", id % 100), total: (id % 1000) as f64 + 0.5, status: "NEW" }))
}

async fn health() -> Json<Value> {
    Json(json!({ "status": "UP" }))
}

#[tokio::main]
async fn main() {
    let port = std::env::var("PORT").unwrap_or_else(|_| "8080".into());
    let app = Router::new().route("/health", get(health)).route("/orders/:id", get(order));
    let listener = tokio::net::TcpListener::bind(format!("0.0.0.0:{port}")).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
