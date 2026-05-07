from contextlib import asynccontextmanager
from time import perf_counter

from fastapi import FastAPI, Request

from app.api.v1 import router as api_router
from app.db import init_db
from app.security import decode_access_token
from app.services.kafka_producer import close_producer, send_event
from app.settings import settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    try:
        yield
    finally:
        close_producer()


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)


@app.middleware("http")
async def audit_middleware(request: Request, call_next):
    started = perf_counter()
    response = await call_next(request)
    elapsed_ms = int((perf_counter() - started) * 1000)
    user_id = None
    role = None
    auth_header = request.headers.get("authorization")
    if auth_header and auth_header.lower().startswith("bearer "):
        token = auth_header.split(" ", 1)[1].strip()
        try:
            payload = decode_access_token(token)
            user_id = payload.get("sub")
            role = payload.get("role")
        except ValueError:
            pass
    send_event(
        "api_request",
        {
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": elapsed_ms,
            "user_id": user_id,
            "role": role,
        },
    )
    return response


app.include_router(api_router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "debug": settings.debug
    }

@app.get("/info")
def info():
    return {
        "name": settings.app_name,
        "version": settings.api_version
    }

@app.get("/config/jwt")
def jwt_config():
    return {
        "algorithm": settings.jwt_algorithm,
        "secret_length": len(settings.jwt_secret)
    }
