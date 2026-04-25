"""add phone column

Revision ID: 71a89110dfdc
Revises: 5c2ba819f847
Create Date: 2026-04-24 20:23:05.255927

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '71a89110dfdc'
down_revision: Union[str, Sequence[str], None] = '5c2ba819f847'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    with op.batch_alter_table('users') as batch_op:
        batch_op.add_column(sa.Column('phone', sa.String(), nullable=True))
        batch_op.create_unique_constraint('uq_users_phone', ['phone'])


def downgrade() -> None:
    with op.batch_alter_table('users') as batch_op:
        batch_op.drop_constraint('uq_users_phone', type_='unique')
        batch_op.drop_column('phone')