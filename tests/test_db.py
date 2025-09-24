from __future__ import annotations

import os
import tempfile

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from src.backend.db.models import Base, User, Score


@pytest.fixture()
def session():
    # use a temporary SQLite database for unit tests
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        engine = create_engine(f"sqlite:///{path}", future=True)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine, future=True)
        with Session.begin() as s:
            yield s
    finally:
        if os.path.exists(path):
            os.remove(path)


def test_user_crud(session):
    user = User(username="alice", display_name="Alice", password_hash="x")
    session.add(user)
    session.flush()

    found = session.execute(select(User).where(User.username == "alice")).scalar_one()
    assert found.id == user.id


def test_leaderboard_query(session):
    u1 = User(username="u1", display_name="U1", password_hash="x")
    u2 = User(username="u2", display_name="U2", password_hash="x")
    session.add_all([u1, u2])
    session.flush()

    session.add_all([
        Score(user_id=u1.id, points=200, level=1),
        Score(user_id=u1.id, points=150, level=1),
        Score(user_id=u2.id, points=250, level=1),
    ])

    session.flush()

    top = session.execute(
        select(Score).where(Score.level == 1).order_by(Score.points.desc()).limit(1)
    ).scalar_one()

    assert top.points == 250

