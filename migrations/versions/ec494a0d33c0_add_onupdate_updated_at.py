"""add onupdate updated_at

Revision ID: 71eb0a005507
Revises: 71a89110dfdc
Create Date: 2026-04-25 17:04:24.160685

"""

from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = '71eb0a005507'
down_revision: Union[str, Sequence[str], None] = '71a89110dfdc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass