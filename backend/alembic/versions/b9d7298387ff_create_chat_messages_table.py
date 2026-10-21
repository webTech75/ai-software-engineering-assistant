"""create chat messages table

Revision ID: b9d7298387ff
Revises: c5bae4bda701
Create Date: 2026-10-21
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b9d7298387ff"
down_revision: Union[str, Sequence[str], None] = "c5bae4bda701"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create chat_messages table."""

    op.create_table(
        "chat_messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_chat_messages_id"),
        "chat_messages",
        ["id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_chat_messages_project_id"),
        "chat_messages",
        ["project_id"],
        unique=False,
    )


def downgrade() -> None:
    """Drop chat_messages table."""

    op.drop_index(
        op.f("ix_chat_messages_project_id"),
        table_name="chat_messages",
    )

    op.drop_index(
        op.f("ix_chat_messages_id"),
        table_name="chat_messages",
    )

    op.drop_table("chat_messages")