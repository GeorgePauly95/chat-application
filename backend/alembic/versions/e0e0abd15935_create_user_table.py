"""Create User table

Revision ID: e0e0abd15935
Revises:
Create Date: 2025-12-04 16:32:36.308292

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e0e0abd15935"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.INTEGER, primary_key=True),
        sa.Column("name", sa.VARCHAR),
        sa.Column("createdAt", sa.TIMESTAMP),
        sa.Column("deletedAt", sa.TIMESTAMP),
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
