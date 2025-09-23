from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse
from sqlalchemy import text

from src.backend.db import get_engine
from src.backend.cache import get_redis_client

app = FastAPI(title="Uni-PacmanPro API", version="0.1.0")


@app.get("/health")
async def health_check():
    # Check Postgres
    pg_ok = False
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        pg_ok = True
    except Exception:
        pg_ok = False

    # Check Redis
    redis_ok = False
    try:
        redis = get_redis_client()
        pong = await redis.ping()
        redis_ok = bool(pong)
        await redis.close()
    except Exception:
        redis_ok = False

    overall = pg_ok and redis_ok
    return JSONResponse({
        "status": "ok" if overall else "degraded",
        "postgres": pg_ok,
        "redis": redis_ok,
    })


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("connected")
    try:
        while True:
            message = await websocket.receive_text()
            await websocket.send_text(f"echo: {message}")
    except Exception:
        # Connection closed by client or network error
        pass

