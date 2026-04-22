from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_db_session, get_existing_session
from app.models import CommandStatus, SessionCommand, SessionResult
from app.schemas import LatestCommandResponse, SessionResultRead, VRResultCreate


router = APIRouter()


@router.post(
    "/sessions/{session_id}/results",
    response_model=SessionResultRead,
    status_code=status.HTTP_201_CREATED,
    summary="Submit results from the VR layer",
)
def create_vr_result(
    session_id: UUID,
    result_in: VRResultCreate,
    db: Session = Depends(get_db_session),
) -> SessionResult:
    session_obj = get_existing_session(db, str(session_id))
    result = SessionResult(
        session_id=session_obj.id,
        result_type=result_in.result_type,
        payload=result_in.payload,
    )
    session_obj.updated_at = datetime.now(timezone.utc)
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


@router.get(
    "/sessions/{session_id}/commands/latest",
    response_model=LatestCommandResponse,
    summary="Poll the latest pending dashboard command for a session",
)
def get_latest_command(
    session_id: UUID,
    db: Session = Depends(get_db_session),
) -> LatestCommandResponse:
    session_obj = get_existing_session(db, str(session_id))
    command = db.scalars(
        select(SessionCommand)
        .where(
            SessionCommand.session_id == session_obj.id,
            SessionCommand.status == CommandStatus.pending,
        )
        .order_by(SessionCommand.created_at.desc(), SessionCommand.id.desc())
        .limit(1)
    ).first()
    return LatestCommandResponse(session_id=session_id, command=command)
