"""create game_sessions table

Revision ID: 0003
Revises: 0002
Create Date: 2025-09-23

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "game_sessions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("mode", sa.String(length=16), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("winner_user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
    )
    op.create_index("ix_game_sessions_started_at", "game_sessions", ["started_at"], unique=False)
    op.create_index("ix_game_sessions_status", "game_sessions", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_game_sessions_status", table_name="game_sessions")
    op.drop_index("ix_game_sessions_started_at", table_name="game_sessions")
    op.drop_table("game_sessions")


