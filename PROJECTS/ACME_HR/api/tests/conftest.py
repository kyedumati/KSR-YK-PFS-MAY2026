import os
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse, urlunparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pytest
from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv(ROOT / ".env")
_migration = urlparse(os.environ["MIGRATION_DATABASE_URL"])
os.environ["DATABASE_URL"] = urlunparse(_migration._replace(path="/acme_hr_test"))
os.environ["JWT_SECRET"] = "test-secret-key-for-acmehr-api-tests"
os.environ["ACCESS_TOKEN_MINUTES"] = "60"

from app.db import Base, get_session_factory  # noqa: E402
import app.models  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    env = os.environ.copy()
    env["MIGRATION_DATABASE_URL"] = os.environ["DATABASE_URL"]
    subprocess.run(
        [str(ROOT / ".venv/bin/alembic"), "upgrade", "head"],
        cwd=ROOT,
        env=env,
        check=True,
    )
    yield


@pytest.fixture(autouse=True)
def clean_tables():
    yield
    session = get_session_factory()()
    try:
        session.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(text(f"TRUNCATE TABLE `{table.name}`"))
        session.execute(text("SET FOREIGN_KEY_CHECKS=1"))
        session.commit()
    finally:
        session.close()


@pytest.fixture
def client():
    from fastapi.testclient import TestClient

    with TestClient(app) as test_client:
        yield test_client
