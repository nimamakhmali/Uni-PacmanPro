"""create users table

Revision ID: 0001
Revises: 
Create Date: 2025-09-23

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(length=32), nullable=False),
        sa.Column("display_name", sa.String(length=64), nullable=True),
        sa.Column("email", sa.String(length=128), nullable=True),
        sa.Column("password_hash", sa.String(length=256), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_users_id", "users", ["id"], unique=False)
    op.create_index("ix_users_username", "users", ["username"], unique=True)
    op.create_index("ix_users_email", "users", ["email"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")


