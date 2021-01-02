use std::env;
use actix_web::{get, web, App, HttpRequest, HttpResponse, HttpServer, Responder};
use r2d2_postgres::{postgres::NoTls, r2d2, PostgresConnectionManager};
type DbPool = web::Data<r2d2::Pool<PostgresConnectionManager<NoTls>>>;

#[get("/apikeys")]
async fn auth(req: HttpRequest, pool: DbPool) -> impl Responder {
    let api_key_header = req.headers().get("x-api-key");
    match api_key_header {
        Some(api_key) => {
            // Verify api_key
            if api_key == "123" {
                HttpResponse::Ok()
            } else {
                // Check database:
                let hashed_key = api_key.to_str().unwrap().to_owned();
                let res = web::block(move || {
                    let mut conn = pool.get().unwrap();
                    conn.query_one(
                        "SELECT * FROM api_key WHERE hash = $1 AND expiration_date > CURRENT_TIMESTAMP;",
                        &[&hashed_key],
                    )
                })
                .await;
                match res {
                    Ok(_) => HttpResponse::Ok(),
                    Err(_) => HttpResponse::Forbidden(),
                }
            }
        }
        _ => HttpResponse::Unauthorized(),
    }
}

#[get("/health")]
async fn health() -> impl Responder {
    HttpResponse::Ok()
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let max_con = env::var("MAX_CON").unwrap_or("10".to_string()).parse::<u32>().unwrap_or(10);
    let min_con = env::var("MIN_CON").unwrap_or("1".to_string()).parse::<u32>().unwrap_or(1);
    let port = env::var("PORT").unwrap_or("8000".to_string()).parse::<u32>().unwrap_or(8000);
    // Connect to db
    let manager = PostgresConnectionManager::new(
        "host=localhost user=postgres password=docker"
            .parse()
            .unwrap(),
        NoTls,
    );
    let pool = r2d2::Pool::builder()
        .max_size(max_con)
        .min_idle(Some(min_con))
        .build(manager)
        .unwrap();
    let bind_address = format!("0.0.0.0:{}", port);
    let server = HttpServer::new(move || App::new().data(pool.clone()).service(auth).service(health))
        .bind(bind_address.clone()).expect("Failed to start server")
        .workers(1)
        .run();
    println!("Server ready on {}", bind_address.clone());
    server.await
}
