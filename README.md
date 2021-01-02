# API KEY Verification endpoint

This is to create a basic speedtest comparing different languages

## The API
The api has two endpoints.
- `GET /health`. This endpoint always returns HTTP status code 200. It is used to check when the service is ready so that the performance testing can begin.

- `GET /apikeys`. This enpoint expects a x-api-key HTTP header containing the api-key.
    ```
    curl -H "x-api-key: 123" localhost:8000/apikeys
    ```

  Possible return values:
  - 200: The header was found in the db and is not expired
  - 401: The header is missing or empty
  - 403: The header was not found in the DB

Implementations should use a connection pool to a Postgres DB where the MAX and MIN connections can be specified with the environment variables. `MAX_CON` defaults to `10` and `MIN_CON` defaults to `1`.

Frameworks that can start multiple workers should be set to start only one worker.

## Current implementations
- Rust v1.49.0
  - install [Rust](https://www.rust-lang.org/tools/install)
    ```
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
    ```
- Python v3.8.0
  - It is recommended to use a virtual environment like [pyenv](https://github.com/pyenv/pyenv) with [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)
  - Install dependencies with `pip install -r requirements.txt`

## Performance tests
### Machine:
- MacBook Pro (15-inch, 2018)
- 2,2 GHz 6-Core Intel Core i7
- 16 GB 2400 MHz DDR4

The machine was running on battery.

### Postgres:
Run in docker:
```
docker run --name some-postgres -dti -p 5432:5432 -e POSTGRES_PASSWORD=docker postgres
```
SQL:
```SQL
CREATE TABLE api_key (
	"id" varchar(512) NOT NULL,
	"hash" varchar(512) NOT NULL,
	"expiration_date" timestamptz NOT NULL,
	CONSTRAINT api_key_pk PRIMARY KEY ("id"),
	CONSTRAINT api_key_un UNIQUE ("hash")
);

INSERT INTO api_key
("id", "hash", "expiration_date")
VALUES
('1234', '4321', CURRENT_TIMESTAMP + interval '1 day')
;
```
---
### Results:
MAX_CON=10 MIN_CON=1
```
RUST - Actix Web - r2d2_postgres:
Running 1m test @ http://localhost:8000/apikeys
  10 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    63.10ms   37.17ms 432.45ms   84.89%
    Req/Sec   165.90     29.66   282.00     70.40%
  99240 requests in 1.00m, 7.10MB read
Requests/sec:   1652.38
Transfer/sec:    121.02KB
```
```
PYTHON - FastAPI - psycopg2:
Running 1m test @ http://localhost:8000/apikeys
  10 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   380.58ms   43.71ms 670.70ms   72.42%
    Req/Sec    32.68     23.64    90.00     63.09%
  15719 requests in 1.00m, 1.59MB read
Requests/sec:    261.83
Transfer/sec:     27.10KB
```
```
PYTHON - FastAPI - asyncpg:
Running 1m test @ http://localhost:8000/apikeys
  10 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    91.20ms   25.62ms 387.08ms   68.28%
    Req/Sec   110.25     17.61   181.00     64.70%
  65942 requests in 1.00m, 6.67MB read
Requests/sec:   1097.33
Transfer/sec:    113.59KB
```
---
MAX_CON=50 MIN_CON=1
```
RUST - Actix Web - r2d2_postgres:
Running 1m test @ http://localhost:8000/apikeys
  10 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    42.49ms   15.57ms 232.21ms   75.18%
    Req/Sec   237.90     50.84   610.00     64.78%
  142189 requests in 1.00m, 10.17MB read
Requests/sec:   2365.85
Transfer/sec:    173.28KB
```
```
PYTHON - FastAPI - psycopg2:
Running 1m test @ http://localhost:8000/apikeys
  10 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   437.73ms   57.41ms 809.38ms   80.04%
    Req/Sec    30.09     21.91    90.00     73.82%
  13679 requests in 1.00m, 1.38MB read
Requests/sec:    227.64
Transfer/sec:     23.56KB
```
```
PYTHON - FastAPI - asyncpg:
Running 1m test @ http://localhost:8000/apikeys
  10 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    91.20ms   25.62ms 387.08ms   68.28%
    Req/Sec   110.25     17.61   181.00     64.70%
  65942 requests in 1.00m, 6.67MB read
Requests/sec:   1097.33
Transfer/sec:    113.59KB
```
