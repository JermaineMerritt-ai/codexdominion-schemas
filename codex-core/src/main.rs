use actix_web::{web, App, HttpResponse, HttpServer, Responder};
use std::sync::{Arc, Mutex};
use std::time::{Duration, Instant};

// Simple circuit breaker state
struct CircuitBreaker {
    failures: u32,
    last_failure: Option<Instant>,
    open: bool,
}

impl CircuitBreaker {
    fn new() -> Self {
        Self { failures: 0, last_failure: None, open: false }
    }
    fn record_failure(&mut self) {
        self.failures += 1;
        self.last_failure = Some(Instant::now());
        if self.failures >= 3 {
            self.open = true;
        }
    }
    fn reset(&mut self) {
        self.failures = 0;
        self.open = false;
        self.last_failure = None;
    }
    fn is_open(&self) -> bool {
        if self.open {
            if let Some(last) = self.last_failure {
                if last.elapsed() > Duration::from_secs(30) {
                    return false;
                }
            }
            return true;
        }
        false
    }
}

async fn health() -> impl Responder {
    HttpResponse::Ok().body("OK")
}

async fn orchestrate(
    cb: web::Data<Arc<Mutex<CircuitBreaker>>>,
) -> impl Responder {
    let mut cb = cb.lock().unwrap();
    if cb.is_open() {
        return HttpResponse::ServiceUnavailable().body("Circuit breaker open");
    }
    // Simulate downstream call with retry
    let mut attempts = 0;
    let max_attempts = 3;
    let mut success = false;
    while attempts < max_attempts {
        attempts += 1;
        // Simulate a failure on first two attempts
        if attempts < 3 {
            cb.record_failure();
        } else {
            cb.reset();
            success = true;
            break;
        }
    }
    if success {
        HttpResponse::Ok().body("Orchestration succeeded")
    } else {
        HttpResponse::InternalServerError().body("Orchestration failed")
    }
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let cb = Arc::new(Mutex::new(CircuitBreaker::new()));
    HttpServer::new(move || {
        App::new()
            .app_data(web::Data::new(cb.clone()))
            .route("/health", web::get().to(health))
            .route("/orchestrate", web::post().to(orchestrate))
    })
    .bind(("0.0.0.0", 8081))?
    .run()
    .await
}
