from pathlib import Path

from app.core.config import get_settings
from app.main import create_app


def test_app_boots_with_env_database_url(monkeypatch, tmp_path: Path) -> None:
    database_url = f"sqlite:///{(tmp_path / 'env-test.db').as_posix()}"
    monkeypatch.setenv("DATABASE_URL", database_url)
    monkeypatch.setenv("APP_NAME", "Env Driven Backend")
    get_settings.cache_clear()

    app = create_app()

    assert app.state.settings.database_url == database_url
    assert app.state.settings.app_name == "Env Driven Backend"
    app.state.engine.dispose()
    get_settings.cache_clear()
