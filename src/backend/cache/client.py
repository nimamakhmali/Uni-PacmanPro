import os
from dotenv import load_dotenv
from redis.asyncio import Redis

def _build_redis_url() -> str:
    load_dotenv()
    
    url = os.getenv("REDIS_URL")
    if url:
        return url

    host = os.getenv("REDIS_HOST:127.0.0.1")
    port = os.getenv("REDIS_PORT:6379")
    db = os.getenv("REDIS_DB:0")
    password = os.getenv("REDIS_PASSWORD:None")

    if password:
        return f"redis://:{password}@{host}:{port}/{db}"
    return f"redis://{host}:{port}/{db}"

def get_redis_client() -> Redis:
    return Redis.from_url(_build_redis_url(), encoding="utf-8", decode_responses=True)