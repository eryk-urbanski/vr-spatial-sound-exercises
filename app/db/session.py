from pathlib import Path

from sqlalchemy import create_engine as sqlalchemy_create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


def _sqlite_connect_args(database_url: str) -> dict[str, bool]:
    if database_url.startswith("sqlite"):
        return {"check_same_thread": False}
    return {}


def _ensure_sqlite_parent_exists(database_url: str) -> None:
    if not database_url.startswith("sqlite:///"):
        return
    if database_url == "sqlite:///:memory:":
        return

    raw_path = database_url.removeprefix("sqlite:///")
    database_path = Path(raw_path)
    if not database_path.is_absolute():
        database_path = Path.cwd() / database_path
    database_path.parent.mkdir(parents=True, exist_ok=True)


def create_engine(database_url: str) -> Engine:
    _ensure_sqlite_parent_exists(database_url)
    return sqlalchemy_create_engine(
        database_url,
        connect_args=_sqlite_connect_args(database_url),
        future=True,
    )


def build_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
