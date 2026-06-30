import os
import redis.asyncio as redis
from fastapi import FastAPI

app = FastAPI()

r = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379, decode_responses=True)

@app.post("/hit/{key}")
async def hit(key: str):
    count = await r.incr(key)
    return {"key": key, "count": count}

@app.get("/count/{key}")
async def count(key: str):
    value = await r.get(key)
    return {"key": key, "count": int(value) if value else 0}

@app.get("/healthz")
async def healthz():
    pong = await r.ping()
    return {"status": "ok", "redis": "up" if pong else "down"}
