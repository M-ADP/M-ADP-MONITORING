from fastapi import FastAPI, APIRouter


def register_routers(app: FastAPI) -> None:

    v1_router = APIRouter()


    app.include_router(v1_router)
