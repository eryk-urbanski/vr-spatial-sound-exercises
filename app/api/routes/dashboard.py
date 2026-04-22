from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.api.dependencies import get_db_session, get_existing_session
from app.models import CommandStatus, SessionCommand, SessionResult
from app.schemas import DashboardCommandCreate, DashboardResultsResponse, SessionCommandRead


router = APIRouter()


@router.post(
    "/sessions/{session_id}/commands",
    response_model=SessionCommandRead,
    status_code=status.HTTP_201_CREATED,
    summary="Submit the latest dashboard command for a session",
)
def create_dashboard_command(
    session_id: UUID,
    command_in: DashboardCommandCreate,
    db: Session = Depends(get_db_session),
) -> SessionCommand:
    session_obj = get_existing_session(db, str(session_id))

    db.execute(
        update(SessionCommand)
        .where(
            SessionCommand.session_id == session_obj.id,
            SessionCommand.status == CommandStatus.pending,
        )
        .values(status=CommandStatus.superseded)
    )

    command = SessionCommand(
        session_id=session_obj.id,
        command_type=command_in.command_type,
        payload=command_in.payload,
        status=CommandStatus.pending,
    )
    session_obj.updated_at = datetime.now(timezone.utc)
    db.add(command)
    db.commit()
    db.refresh(command)
    return command


@router.get(
    "/sessions/{session_id}/results",
    response_model=DashboardResultsResponse,
    summary="Fetch session results for dashboard presentation",
)
def get_dashboard_results(
    session_id: UUID,
    db: Session = Depends(get_db_session),
) -> DashboardResultsResponse:
    session_obj = get_existing_session(db, str(session_id))
    results = db.scalars(
        select(SessionResult)
        .where(SessionResult.session_id == session_obj.id)
        .order_by(SessionResult.created_at.asc(), SessionResult.id.asc())
    ).all()
    return DashboardResultsResponse(session=session_obj, results=results)
