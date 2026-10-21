"""allow general chat messages

Revision ID: 15636b3f3ef2
Revises: c5bae4bda701
Create Date: 2026-10-19 03:51:24.019891

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15636b3f3ef2'
down_revision: Union[str, Sequence[str], None] = 'b9d7298387ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    with op.batch_alter_table("chat_messages") as batch_op:
        batch_op.alter_column(
            "project_id",
            existing_type=sa.INTEGER(),
            nullable=True,
        )


def downgrade() -> None:
    """Downgrade schema."""

    with op.batch_alter_table("chat_messages") as batch_op:
        batch_op.alter_column(
            "project_id",
            existing_type=sa.INTEGER(),
            nullable=False,
        )
