from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.api.exception_handlers import register_exception_handlers
from src.api.routers import register_routers


def create_app():
    app = FastAPI()

    @app.get("/")
    async def health_check():
        return JSONResponse(status_code=200, content={"status": "ok"})

    # 예외 핸들러 등록
    register_exception_handlers(app)
    register_routers(app)

    return app
