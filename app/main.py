from fastapi import FastAPI

from app.api.v1 import router as api_router
from app.db import init_db
from app.settings import settings

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


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
