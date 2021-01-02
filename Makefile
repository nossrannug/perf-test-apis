max_con:=50
min_con:=1
warmup:=5
duration:=60

threads:=4 # Make sure that postgres has some cores
connections:=500 # Number of concurrent connections

run: 
	@make run-rust
	@make run-python

build-rust:
	@cd rust && cargo build --release

run-rust:
	@make build-rust # Need to make sure that the code has been built
	@echo "🦀 RUST"
	@cd rust && MAX_CON=$(max_con) MIN_CON=$(min_con) ./target/release/auth-api > /dev/null &
	@make perf-test title="🦀 RUST - Actix Web - r2d2_postgres"
	@make stop-api

stop-api:
	@lsof -t -i :8000 | xargs kill

run-python:
	@echo "⚡ PYTHON:"
	@make run-psycopg
	@sleep 5 # Need some delay
	@make run-asyncpg

run-psycopg:
	@echo "PSYCOPG:"
	@cd py && MAX_CON=$(max_con) MIN_CON=$(min_con) uvicorn run_psycopg2:app --port 8000 --workers 1 --no-access-log --log-level critical &
	@make perf-test title="Python - psycopg2"
	@make stop-api

run-asyncpg:
	@cd py && MAX_CON=$(max_con) MIN_CON=$(min_con) uvicorn run_asyncpg:app --port 8000 --workers 1 --no-access-log --log-level critical &
	@make perf-test title="Python - Async pg"
	@make stop-api

perf-test:
	@./wait-for-api.sh
	@echo "### $(title) - $(shell date)\n" >> report.md
	@echo "Pool size - max_con: $(max_con), min_con: $(min_con)\n" >> report.md
	@echo "\`\`\`" >> report.md
	@echo "🔥 - Warmup for $(warmup)s"
	@wrk -H "x-api-key: 4321" http://localhost:8000/apikeys -c$(connections) -t$(threads) -d$(warmup)s > /dev/null
	@echo "🚀 - Perf test for $(duration)s"
	@wrk -H "x-api-key: 4321" http://localhost:8000/apikeys -c$(connections) -t$(threads) -d$(duration)s >> report.md
	@echo "\`\`\`" >> report.md
	@echo "---" >> report.md

wait:
	@./wait-for-api.sh