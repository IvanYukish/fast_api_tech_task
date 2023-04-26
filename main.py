import sys

import uvicorn
from fastapi import FastAPI
from loguru import logger

from app.config import settings
from app.core.middleware import AuthMiddleware
from app.v1.router import api_router


def get_application():
    _app = FastAPI()
    _app.include_router(api_router, prefix=settings.API_V1_STR)

    # configure loguru
    logger.configure(handlers=[{"sink": sys.stdout, "serialize": settings.JSON_LOGS}])
    return _app


app = get_application()
app.add_middleware(AuthMiddleware)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
