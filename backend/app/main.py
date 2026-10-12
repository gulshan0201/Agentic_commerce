from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
# from app.routes.health import router as health_router
from app.routes.api import api_router
from app.utils.exceptions import global_exception_handler

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API for the Agentic Commerce platform"
)

app.add_exception_handler(
    Exception,
    global_exception_handler
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# app.include_router(health_router)
app.include_router(api_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "application": settings.app_name,
        "environment": settings.app_env,
        "version": settings.app_version,
        "status": "running"
    }