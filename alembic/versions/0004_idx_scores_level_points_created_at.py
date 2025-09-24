"""add composite index for per-level leaderboard

Revision ID: 0004
Revises: 0003
Create Date: 2025-09-23

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index(
        "ix_scores_level_points_created_at",
        "scores",
        ["level", sa.text("points DESC"), sa.text("created_at DESC")],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_scores_level_points_created_at", table_name="scores")


