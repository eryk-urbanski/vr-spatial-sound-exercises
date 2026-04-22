"""create initial schema

Revision ID: 20260421_0001
Revises:
Create Date: 2026-04-21 20:05:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260421_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


session_status = sa.Enum("created", "active", "completed", name="sessionstatus", native_enum=False)
command_status = sa.Enum("pending", "superseded", name="commandstatus", native_enum=False)


def upgrade() -> None:
    op.create_table(
        "sessions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("status", session_status, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "session_commands",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("command_type", sa.String(length=100), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=True),
        sa.Column("status", command_status, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_session_commands_session_id", "session_commands", ["session_id"], unique=False)
    op.create_index("ix_session_commands_status", "session_commands", ["status"], unique=False)
    op.create_table(
        "session_results",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("result_type", sa.String(length=100), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_session_results_session_id", "session_results", ["session_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_session_results_session_id", table_name="session_results")
    op.drop_table("session_results")
    op.drop_index("ix_session_commands_status", table_name="session_commands")
    op.drop_index("ix_session_commands_session_id", table_name="session_commands")
    op.drop_table("session_commands")
    op.drop_table("sessions")
