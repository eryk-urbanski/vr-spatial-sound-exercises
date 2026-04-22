from uuid import UUID

from app.core.config import get_settings
from app.db.base import Base
from app.db.session import build_session_factory, create_engine
from app.models import Session, SessionStatus


DEFAULT_SESSION_ID = UUID("00000000-0000-0000-0000-000000000001")


def main() -> None:
    settings = get_settings()
    engine = create_engine(settings.database_url)
    session_factory = build_session_factory(engine)

    Base.metadata.create_all(engine)

    with session_factory() as db:
        session = db.get(Session, str(DEFAULT_SESSION_ID))
        if session is None:
            db.add(Session(id=str(DEFAULT_SESSION_ID), status=SessionStatus.created))
            db.commit()

    engine.dispose()
    print(f"Seeded demo session: {DEFAULT_SESSION_ID}")


if __name__ == "__main__":
    main()
