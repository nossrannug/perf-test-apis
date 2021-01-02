import os
from typing import Optional
from psycopg2.pool import ThreadedConnectionPool
from threading import Semaphore


class QueuePool(ThreadedConnectionPool):
    def __init__(self, minconn, maxconn, *args, **kwargs):
        self._semaphore = Semaphore(maxconn)
        super().__init__(minconn, maxconn, *args, **kwargs)

    def getconn(self, *args, **kwargs):
        self._semaphore.acquire()
        return super().getconn(*args, **kwargs)

    def putconn(self, *args, **kwargs):
        super().putconn(*args, **kwargs)
        self._semaphore.release()

from fastapi import FastAPI, Header, Response


max_con = int(os.getenv("MAX_CON", 10))
min_con = int(os.getenv("MIN_CON", 1))

db_pool = QueuePool(
    database="postgres",
    host="localhost",
    user="postgres",
    password="docker",
    minconn=min_con,
    maxconn=max_con)

app = FastAPI()

@app.get("/apikeys")
def auth(x_api_key: Optional[str] = Header(None)):
    if x_api_key == "123":
        return Response(status_code=200)
    elif x_api_key:
        hashed_key = x_api_key
        con = db_pool.getconn()
        with con.cursor() as cur:
            cur.execute("SELECT * FROM api_key WHERE hash = %s AND expiration_date > CURRENT_TIMESTAMP;", [hashed_key])
            row = cur.fetchone()
        db_pool.putconn(con)
        if row:
            return Response(status_code=200)
        else:
            return Response(status_code=403)
    return Response(status_code=401)

@app.get("/health")
def health():
    return Response(status_code=200)
    