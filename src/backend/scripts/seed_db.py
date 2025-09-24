from __future__ import annotations

import random
from datetime import timedelta

from passlib.hash import bcrypt

from src.backend.db import get_engine, get_session_maker
from src.backend.db.models import Base, User, Score


def seed() -> None:
    engine = get_engine(echo=True)
    Base.metadata.create_all(engine)
    Session = get_session_maker(engine)

    with Session.begin() as session:
        # Users
        users = []
        for i in range(1, 4):
            username = f"user{i}"
            display_name = f"User {i}"
            email = f"user{i}@example.com"
            password_hash = bcrypt.hash("password123")
            user = User(username=username, display_name=display_name, password_hash=password_hash)
            # email is optional; set for first two users
            if i <= 2:
                user.email = email
            session.add(user)
            users.append(user)

        session.flush()  # get user IDs

        # Scores
        for user in users:
            for level in (1, 2, 3):
                points = random.randint(100, 500)
                duration_ms = random.randint(30_000, 180_000)
                session.add(Score(user_id=user.id, level=level, points=points, duration_ms=duration_ms))

    print("Seed data inserted.")


if __name__ == "__main__":
    seed()


