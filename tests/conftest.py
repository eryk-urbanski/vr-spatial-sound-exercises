from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.db.base import Base
from app.main import create_app
from app.models import Session, SessionStatus
from tests.constants import SEEDED_SESSION_ID


@pytest.fixture
def test_app(tmp_path: Path) -> Generator[FastAPI, None, None]:
    database_url = f"sqlite:///{(tmp_path / 'test.db').as_posix()}"
    settings = Settings(
        app_name="Test Backend",
        debug=False,
        api_prefix="/api",
        database_url=database_url,
    )
    app = create_app(settings)
    Base.metadata.create_all(bind=app.state.engine)

    with app.state.session_factory() as db:
        db.add(Session(id=str(SEEDED_SESSION_ID), status=SessionStatus.created))
        db.commit()

    yield app

    Base.metadata.drop_all(bind=app.state.engine)
    app.state.engine.dispose()


@pytest.fixture
def client(test_app: FastAPI) -> Generator[TestClient, None, None]:
    app = test_app
    with TestClient(app) as test_client:
        yield test_client
