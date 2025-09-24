"""add FK cascades and enum-like checks

Revision ID: 0005
Revises: 0004
Create Date: 2025-09-23

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # scores.user_id -> users.id ON DELETE CASCADE
    with op.batch_alter_table("scores") as batch:
        batch.drop_constraint("scores_user_id_fkey", type_="foreignkey")
        batch.create_foreign_key(
            "scores_user_id_fkey",
            referent_table="users",
            local_cols=["user_id"],
            remote_cols=["id"],
            ondelete="CASCADE",
        )

    # game_sessions.status and mode enum-like CHECKs
    op.create_check_constraint(
        "ck_game_sessions_status",
        "game_sessions",
        "status in ('pending','active','finished')",
    )
    op.create_check_constraint(
        "ck_game_sessions_mode",
        "game_sessions",
        "mode in ('solo','multi')",
    )


def downgrade() -> None:
    op.drop_constraint("ck_game_sessions_mode", "game_sessions", type_="check")
    op.drop_constraint("ck_game_sessions_status", "game_sessions", type_="check")

    with op.batch_alter_table("scores") as batch:
        batch.drop_constraint("scores_user_id_fkey", type_="foreignkey")
        batch.create_foreign_key(
            "scores_user_id_fkey",
            referent_table="users",
            local_cols=["user_id"],
            remote_cols=["id"],
        )


