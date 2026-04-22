from fastapi import FastAPI
from sqlalchemy import text


def test_database_connection_executes_simple_query(test_app: FastAPI) -> None:
    with test_app.state.engine.connect() as connection:
        result = connection.execute(text("SELECT 1")).scalar_one()

    assert result == 1
