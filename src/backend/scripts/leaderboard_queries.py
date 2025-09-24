from __future__ import annotations

import argparse
from datetime import datetime, timedelta
from sqlalchemy import text

from src.backend.db import get_engine


def run(level: int | None, limit: int, since_days: int | None) -> None:
    engine = get_engine(echo=False)
    with engine.connect() as conn:
        print(f"-- Global Top {limit} --")
        time_filter = ""
        params: dict[str, object] = {}
        if since_days is not None:
            since = datetime.utcnow() - timedelta(days=since_days)
            time_filter = "WHERE s.created_at >= :since"
            params["since"] = since

        res = conn.execute(text(
            """
            SELECT u.username, s.points, s.level, s.created_at
            FROM scores s
            JOIN users u ON u.id = s.user_id
            {time_filter}
            ORDER BY s.points DESC, s.created_at DESC
            LIMIT :limit;
            """.replace("{time_filter}", time_filter)
        ), {**params, "limit": limit})
        for row in res.fetchall():
            print(dict(row._mapping))

        if level is not None:
            print(f"\n-- Per-Level Top {limit} (level={level}) --")
            time_filter = "AND s.created_at >= :since" if since_days is not None else ""
            res = conn.execute(text(
            """
            SELECT u.username, s.points, s.level, s.created_at
            FROM scores s
            JOIN users u ON u.id = s.user_id
            WHERE s.level = :level
            {time_filter}
            ORDER BY s.points DESC, s.created_at DESC
            LIMIT :limit;
            """.replace("{time_filter}", time_filter)
            ), {**params, "level": level, "limit": limit})
            for row in res.fetchall():
                print(dict(row._mapping))

        # Per-user best score (global)
        print("\n-- Per-User Best (global) --")
        res = conn.execute(text(
            """
            SELECT u.username, max(s.points) as best_points
            FROM scores s
            JOIN users u ON u.id = s.user_id
            GROUP BY u.username
            ORDER BY best_points DESC
            LIMIT :limit;
            """
        ), {"limit": limit})
        for row in res.fetchall():
            print(dict(row._mapping))

        if level is not None:
            print("\n-- EXPLAIN (per-level) --")
            time_filter = "AND s.created_at >= :since" if since_days is not None else ""
            explain = conn.execute(text(
                """
                EXPLAIN ANALYZE
                SELECT u.username, s.points, s.level, s.created_at
                FROM scores s
                JOIN users u ON u.id = s.user_id
                WHERE s.level = :level
                {time_filter}
                ORDER BY s.points DESC, s.created_at DESC
                LIMIT :limit;
                """.replace("{time_filter}", time_filter)
            ), {**params, "level": level, "limit": limit}).fetchall()
            print("\n".join(r[0] for r in explain))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Leaderboard queries demo")
    parser.add_argument("--level", type=int, default=None, help="Filter by level (optional)")
    parser.add_argument("--limit", type=int, default=10, help="Number of rows to return")
    parser.add_argument("--since-days", type=int, default=None, help="Only scores since N days ago")
    args = parser.parse_args()

    run(level=args.level, limit=args.limit, since_days=args.since_days)


