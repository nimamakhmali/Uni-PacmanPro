from __future__ import annotations

from sqlalchemy import text

from src.backend.db import get_engine


def run() -> None:
    engine = get_engine(echo=True)
    with engine.connect() as conn:
        print("-- Global Top 10 --")
        res = conn.execute(text(
            """
            SELECT u.username, s.points, s.level, s.created_at
            FROM scores s
            JOIN users u ON u.id = s.user_id
            ORDER BY s.points DESC, s.created_at DESC
            LIMIT 10;
            """
        ))
        for row in res.fetchall():
            print(dict(row._mapping))

        print("\n-- Per-Level Top 10 (level=1) --")
        res = conn.execute(text(
            """
            SELECT u.username, s.points, s.level, s.created_at
            FROM scores s
            JOIN users u ON u.id = s.user_id
            WHERE s.level = :level
            ORDER BY s.points DESC, s.created_at DESC
            LIMIT 10;
            """
        ), {"level": 1})
        for row in res.fetchall():
            print(dict(row._mapping))

        print("\n-- EXPLAIN (per-level) --")
        explain = conn.execute(text(
            """
            EXPLAIN ANALYZE
            SELECT u.username, s.points, s.level, s.created_at
            FROM scores s
            JOIN users u ON u.id = s.user_id
            WHERE s.level = :level
            ORDER BY s.points DESC, s.created_at DESC
            LIMIT 10;
            """
        ), {"level": 1}).fetchall()
        print("\n".join(r[0] for r in explain))


if __name__ == "__main__":
    run()


