import os
import redis.asyncio as redis
from fastapi import FastAPI

app = FastAPI()

# "redis" here is the *service name* from docker-compose.yml.
# Docker automatically lets containers find each other by service name.
r = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379, decode_responses=True)

@app.post("/hit/{key}")
async def hit(key: str):
    count = await r.incr(key)   # atomic increment in Redis itself
    return {"key": key, "count": count}

@app.get("/count/{key}")
async def count(key: str):
    value = await r.get(key)
    return {"key": key, "count": int(value) if value else 0}

@app.get("/healthz")
async def healthz():
    pong = await r.ping()  # actually contacts redis, not a fake "ok"
    return {"status": "ok", "redis": "up" if pong else "down"}
