from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.session import CommandStatus, SessionStatus


class DashboardCommandCreate(BaseModel):
    command_type: str = Field(min_length=1, max_length=100)
    payload: dict[str, Any] | None = None


class VRResultCreate(BaseModel):
    result_type: str = Field(min_length=1, max_length=100)
    payload: dict[str, Any]


class SessionRead(BaseModel):
    id: UUID
    status: SessionStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SessionCommandRead(BaseModel):
    id: int
    session_id: UUID
    command_type: str
    payload: dict[str, Any] | None
    status: CommandStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LatestCommandResponse(BaseModel):
    session_id: UUID
    command: SessionCommandRead | None


class SessionResultRead(BaseModel):
    id: int
    session_id: UUID
    result_type: str
    payload: dict[str, Any]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DashboardResultsResponse(BaseModel):
    session: SessionRead
    results: list[SessionResultRead]
