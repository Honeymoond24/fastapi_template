from fastapi import FastAPI

from app.presentation.api import root_router


def init_routers(app: FastAPI):
    app.include_router(root_router)
