import os
from typing import Optional
import asyncpg

from fastapi import FastAPI, Header, Response


max_con = int(os.getenv("MAX_CON", 10))
min_con = int(os.getenv("MIN_CON", 1))

db_pool = None

app = FastAPI()

@app.on_event("startup")
async def startup():
    global db_pool
    db_pool = await asyncpg.create_pool(database='postgres', user='postgres', password="docker", min_size=min_con, max_size=max_con)

@app.get("/apikeys")
async def auth(x_api_key: Optional[str] = Header(None)):
    if x_api_key == "123":
        return Response(status_code=200)
    elif x_api_key:
        hashed_key = x_api_key
        async with db_pool.acquire() as connection:
            # Open a transaction.
            async with connection.transaction():
                # Run the query passing the request argument.
                if len(await connection.fetch("SELECT * FROM api_key WHERE hash = $1 AND expiration_date > CURRENT_TIMESTAMP;", hashed_key)) == 1:
                    return Response(status_code=200)
                else:
                    return Response(status_code=403)
    return Response(status_code=401)

@app.get("/health")
async def health():
    return Response(status_code=200)
