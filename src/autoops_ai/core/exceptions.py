from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AutoOpsException(Exception):
    def __init__(self, message: str, code: str = "AUTOOPS_ERROR", status_code: int = 400) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AutoOpsException)
    async def autoops_exception_handler(_: Request, exc: AutoOpsException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": exc.code, "message": exc.message}},
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(_: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"error": {"code": "INTERNAL_SERVER_ERROR", "message": str(exc)}},
        )
