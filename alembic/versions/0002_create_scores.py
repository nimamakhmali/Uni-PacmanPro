"""create scores table

Revision ID: 0002
Revises: 0001
Create Date: 2025-09-23

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "scores",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("points", sa.Integer(), nullable=False),
        sa.Column("level", sa.Integer(), nullable=True),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_scores_user_id", "scores", ["user_id"], unique=False)
    op.create_index("ix_scores_level", "scores", ["level"], unique=False)
    op.create_index("ix_scores_created_at", "scores", ["created_at"], unique=False)
    # leaderboard composite index suggestion (points desc, created_at desc)
    op.create_index("ix_scores_points_created_at", "scores", ["points", "created_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_scores_points_created_at", table_name="scores")
    op.drop_index("ix_scores_created_at", table_name="scores")
    op.drop_index("ix_scores_level", table_name="scores")
    op.drop_index("ix_scores_user_id", table_name="scores")
    op.drop_table("scores")


