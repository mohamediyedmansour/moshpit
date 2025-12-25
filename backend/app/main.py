from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.config import settings
from app.logging import setup_logging
from app.routes.health import router as health_router
from app.routes.upload import router as upload_router

import logging

setup_logging()
logger = logging.getLogger("moshpit")


class UploadSizeLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get("content-length")
        if content_length:
            size_mb = int(content_length) / (1024 * 1024)
            if size_mb > settings.MAX_UPLOAD_SIZE_MB:
                return JSONResponse(
                    status_code=413,
                    content={"detail": "File too large"},
                )
        return await call_next(request)


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    version="0.1.0",
)


# CORS (lock this down in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(UploadSizeLimitMiddleware)

# Routers
app.include_router(health_router)
app.include_router(upload_router)


@app.on_event("startup")
async def startup():
    logger.info("moshpit server starting")


@app.on_event("shutdown")
async def shutdown():
    logger.info("moshpit server shutting down")
