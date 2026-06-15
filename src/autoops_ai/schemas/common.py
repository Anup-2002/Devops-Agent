from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    error: ErrorDetail


class TimestampedSchema(BaseModel):
    created_at: datetime
    updated_at: datetime
